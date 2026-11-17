"""Bitemporal upsert of property versions (S1-06, ADR-002, invariant 2).

Every property version carries two time axes:

    valid_from / valid_to         when it was true in the world
    recorded_at / superseded_at   when it was our current knowledge

Nothing is ever rewritten. When a new version arrives, the row that held our
knowledge is marked superseded and new rows are inserted:

    change at a later date    supersede the open version, insert a closed copy
                              of it (valid_to = the change date) and the new
                              open version
    correction, same date     supersede the open version, insert the corrected one
    identical content         nothing happens, nothing is emitted

The database enforces the same rule with a trigger: the only update allowed
on zone_a.property is setting superseded_at once.

The clock is passed in. This module never reads the time itself, so runs are
reproducible.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from core.events import validate_event

_NAMESPACE = uuid.UUID("5b0f1f6e-7b55-4c0b-8f0e-70726f706572")

CONTENT_FIELDS = (
    "bfe", "municipality_id", "zip_id", "neighbourhood_id", "street_id", "attrs",
    "owner_kind", "owner_cvr", "quality_flags", "lon", "lat",
)
_JSON_FIELDS = {"attrs", "quality_flags"}


class OutOfOrderVersion(ValueError):
    """A version arrived that starts before the version we already hold as current."""


@dataclass(frozen=True)
class PropertyVersion:
    address_id: str
    bfe: str
    municipality_id: str
    zip_id: str
    valid_from: date
    attrs: dict[str, Any]
    neighbourhood_id: str | None = None
    street_id: str | None = None
    owner_kind: str | None = None
    owner_cvr: str | None = None
    quality_flags: dict[str, str] = field(default_factory=dict)
    lon: float | None = None
    lat: float | None = None

    def content(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in CONTENT_FIELDS}


def _hash(content: dict[str, Any]) -> str:
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


_COLUMNS = ("address_id", *CONTENT_FIELDS, "valid_from", "valid_to", "recorded_at")
_INSERT = (
    f"INSERT INTO zone_a.property ({', '.join(_COLUMNS)}, synthetic_seed) "
    f"VALUES ({', '.join(['%s'] * (len(_COLUMNS) + 1))})"
)


def _insert(conn: psycopg.Connection, address_id: str, content: dict[str, Any],
            valid_from: date, valid_to: date | None, recorded_at: datetime,
            synthetic_seed: int | None) -> None:
    values = [Jsonb(content[name]) if name in _JSON_FIELDS else content[name]
              for name in CONTENT_FIELDS]
    conn.execute(_INSERT, (address_id, *values, valid_from, valid_to, recorded_at,
                           synthetic_seed))


def upsert_property(conn: psycopg.Connection, version: PropertyVersion, *,
                    recorded_at: datetime, trace_id: str,
                    synthetic_seed: int | None = None) -> dict[str, Any] | None:
    """Apply one property version.

    Returns the `property.changed` event that was written, or None when the
    version is identical to what we already hold. Call inside a transaction.
    Raises OutOfOrderVersion when the version starts before the current one.
    """
    new_content = version.content()
    new_hash = _hash(new_content)

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            f"SELECT version_id, valid_from, synthetic_seed, {', '.join(CONTENT_FIELDS)}"
            " FROM zone_a.property"
            " WHERE address_id = %s AND superseded_at IS NULL AND valid_to IS NULL"
            " FOR UPDATE",
            (version.address_id,),
        )
        current = cur.fetchone()

    if current is None:
        change, fields, old_hash = "CREATED", list(CONTENT_FIELDS), None
        _insert(conn, version.address_id, new_content, version.valid_from, None, recorded_at,
                synthetic_seed)
    else:
        old_content = {name: current[name] for name in CONTENT_FIELDS}
        old_hash = _hash(old_content)
        if old_hash == new_hash:
            return None
        if version.valid_from < current["valid_from"]:
            raise OutOfOrderVersion(
                f"{version.address_id}: version from {version.valid_from} is older than the "
                f"current version from {current['valid_from']}"
            )
        fields = [name for name in CONTENT_FIELDS if old_content[name] != new_content[name]]
        seed = synthetic_seed if synthetic_seed is not None else current["synthetic_seed"]
        conn.execute(
            "UPDATE zone_a.property SET superseded_at = %s WHERE version_id = %s",
            (recorded_at, current["version_id"]),
        )
        if version.valid_from > current["valid_from"]:
            change = "CHANGED"
            _insert(conn, version.address_id, old_content, current["valid_from"],
                    version.valid_from, recorded_at, current["synthetic_seed"])
        else:
            change = "CORRECTED"
        _insert(conn, version.address_id, new_content, version.valid_from, None, recorded_at,
                seed)

    stamp = recorded_at.isoformat()
    event = {
        "event_id": str(uuid.uuid5(
            _NAMESPACE, f"{version.address_id}:{new_hash}:{version.valid_from}:{change}:{stamp}"
        )),
        "type": "property.changed",
        "schema_version": "1.0.0",
        "occurred_at": stamp,
        "recorded_at": stamp,
        "actor": {"kind": "SYSTEM", "pseudonym": None, "org_id": None},
        "zone": "A",
        "aggregate": {"kind": "PROPERTY", "id": version.address_id},
        "trace_id": trace_id,
        "causation_id": None,
        "payload": {
            "address_id": version.address_id,
            "change": change,
            "fields": fields,
            "valid_from": version.valid_from.isoformat(),
            "old_hash": old_hash,
            "new_hash": new_hash,
        },
    }
    validate_event(event)
    conn.execute(
        "INSERT INTO zone_a.property_event (event_id, address_id, type, schema_version, payload,"
        " actor, trace_id, occurred_at, recorded_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (event["event_id"], version.address_id, event["type"], event["schema_version"],
         Jsonb(event["payload"]), Jsonb(event["actor"]), trace_id, recorded_at, recorded_at),
    )
    return event


def property_as_of(conn: psycopg.Connection, address_id: str, *, valid_on: date,
                   known_at: datetime | None = None) -> dict[str, Any] | None:
    """The version that was true on `valid_on`, as we knew it at `known_at`.

    `known_at=None` means our knowledge today.
    """
    if known_at is None:
        knowledge = "superseded_at IS NULL"
        params: tuple[Any, ...] = (address_id, valid_on, valid_on)
    else:
        knowledge = "recorded_at <= %s AND (superseded_at IS NULL OR superseded_at > %s)"
        params = (address_id, valid_on, valid_on, known_at, known_at)
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT * FROM zone_a.property"
            " WHERE address_id = %s AND valid_from <= %s AND (valid_to IS NULL OR valid_to > %s)"
            f" AND {knowledge}"
            " ORDER BY recorded_at DESC, version_id DESC LIMIT 1",
            params,
        )
        return cur.fetchone()
