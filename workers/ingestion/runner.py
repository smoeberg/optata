"""Adapter framework for register ingestion (S1-01).

An adapter knows one source: how to fetch records after a cursor, how to turn
a raw record into a PropertyVersion, and which validation rules apply. The
runner owns everything the adapters share:

    checkpoint     each batch commits together with the cursor it reached, so
                   an interrupted run resumes after the last committed batch
    idempotency    applying a record twice changes nothing the second time
    quarantine     a record that fails is stored with its issues. Every fetched
                   record ends as changed, unchanged or quarantined; none is
                   dropped

Adapters must yield records in ascending cursor order and only records whose
cursor is greater than `since`.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from datetime import datetime
from itertools import batched
from typing import Any, Protocol

import psycopg
from psycopg.types.json import Jsonb

from core.registry import OutOfOrderVersion, PropertyVersion, upsert_property


@dataclass(frozen=True)
class RawRecord:
    natural_key: str
    cursor: str
    data: dict[str, Any]


@dataclass(frozen=True)
class Issue:
    field: str
    code: str
    message: str


class SourceAdapter(Protocol):
    source: str

    def fetch(self, since: str | None) -> Iterator[RawRecord]: ...

    def normalize(self, raw: RawRecord) -> PropertyVersion: ...

    def validate(self, version: PropertyVersion) -> list[Issue]: ...


@dataclass
class RunResult:
    source: str
    run_id: str
    fetched: int = 0
    changed: int = 0
    unchanged: int = 0
    quarantined: int = 0
    checkpoint: str | None = None


def _quarantine(conn: psycopg.Connection, source: str, raw: RawRecord, issues: list[Issue],
                run_id: str) -> None:
    payload = json.dumps(raw.data, sort_keys=True, default=str)
    conn.execute(
        "INSERT INTO zone_a.ingestion_quarantine (source, natural_key, payload_hash, payload,"
        " issues, run_id) VALUES (%s, %s, %s, %s, %s, %s)"
        " ON CONFLICT (source, natural_key, payload_hash) DO NOTHING",
        (source, raw.natural_key, hashlib.sha256(payload.encode()).hexdigest(),
         Jsonb(json.loads(payload)), Jsonb([asdict(i) for i in issues]), run_id),
    )


def run(conn: psycopg.Connection, adapter: SourceAdapter, *, recorded_at: datetime,
        run_id: str, batch_size: int = 500, synthetic_seed: int | None = None) -> RunResult:
    """Run one adapter from its checkpoint to the end of what the source offers."""
    row = conn.execute(
        "SELECT cursor FROM zone_a.ingestion_checkpoint WHERE source = %s", (adapter.source,)
    ).fetchone()
    result = RunResult(source=adapter.source, run_id=run_id, checkpoint=row[0] if row else None)

    for batch in batched(adapter.fetch(result.checkpoint), batch_size):
        counts = {"changed": 0, "unchanged": 0, "quarantined": 0}
        with conn.transaction():
            for raw in batch:
                try:
                    version = adapter.normalize(raw)
                    issues = adapter.validate(version)
                except Exception as exc:  # noqa: BLE001 - a bad record must not stop the run
                    issues = [Issue("*", "NORMALIZE_FAILED", f"{type(exc).__name__}: {exc}")]
                if not issues:
                    try:
                        with conn.transaction():
                            event = upsert_property(
                                conn, version, recorded_at=recorded_at,
                                trace_id=f"{adapter.source}:{run_id}",
                                synthetic_seed=synthetic_seed,
                            )
                        counts["changed" if event else "unchanged"] += 1
                        continue
                    except OutOfOrderVersion as exc:
                        issues = [Issue("valid_from", "OUT_OF_ORDER", str(exc))]
                _quarantine(conn, adapter.source, raw, issues, run_id)
                counts["quarantined"] += 1
            cursor = batch[-1].cursor
            conn.execute(
                "INSERT INTO zone_a.ingestion_checkpoint (source, cursor, run_id)"
                " VALUES (%s, %s, %s)"
                " ON CONFLICT (source) DO UPDATE SET cursor = excluded.cursor,"
                " run_id = excluded.run_id, updated_at = now()",
                (adapter.source, cursor, run_id),
            )
        # Only counted once the batch has committed.
        result.fetched += len(batch)
        result.changed += counts["changed"]
        result.unchanged += counts["unchanged"]
        result.quarantined += counts["quarantined"]
        result.checkpoint = cursor

    assert result.fetched == result.changed + result.unchanged + result.quarantined
    return result
