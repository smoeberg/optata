"""Load a generated dataset into a migrated database."""

from __future__ import annotations

import os
from typing import Any

import psycopg
from psycopg.types.json import Jsonb

ALLOWED_ENVIRONMENTS = {"dev", "test"}


def assert_safe_environment() -> None:
    """Synthetic data must never be loaded into staging or production."""
    env = os.environ.get("OPTATA_ENV", "")
    if env not in ALLOWED_ENVIRONMENTS:
        raise RuntimeError(
            f"refusing to load synthetic data: OPTATA_ENV is {env!r}, "
            f"expected one of {sorted(ALLOWED_ENVIRONMENTS)}"
        )


def load(conn: psycopg.Connection, data: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    """Insert `data` in one transaction. Returns the number of rows per table."""
    assert_safe_environment()
    with conn.transaction(), conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO zone_a.area (area_id, level, parent_id, name, dwelling_count,"
            " synthetic_seed) VALUES (%s, %s, %s, %s, %s, %s)",
            [(a["area_id"], a["level"], a["parent_id"], a["name"], a["dwelling_count"],
              a["_seed"]) for a in data["areas"]],
        )
        cur.executemany(
            "INSERT INTO zone_a.property (address_id, bfe, municipality_id, zip_id,"
            " neighbourhood_id, street_id, attrs, owner_kind, owner_cvr, lon, lat, valid_from,"
            " valid_to, recorded_at, synthetic_seed)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [(p["address_id"], p["bfe"], p["municipality_id"], p["zip_id"],
              p["neighbourhood_id"], p["street_id"], Jsonb(p["attrs"]), p["owner_kind"],
              p["owner_cvr"], p["lon"], p["lat"], p["valid_from"], p["valid_to"],
              p["recorded_at"], p["_seed"]) for p in data["properties"]],
        )
        cur.executemany(
            "INSERT INTO zone_b.identity (identity_id, provider, pseudonym, provider_sub,"
            " assurance, cvr, household_key, created_at, erased_at, synthetic_seed)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [(i["identity_id"], i["provider"], i["pseudonym"], i["provider_sub"],
              i["assurance"], i["cvr"], i["household_key"], i["created_at"], i["erased_at"],
              i["_seed"]) for i in data["identities"]],
        )
        cur.executemany(
            "INSERT INTO vault.identity_contact (identity_id, full_name, synthetic_seed)"
            " VALUES (%s, %s, %s)",
            [(c["identity_id"], c["full_name"], c["_seed"]) for c in data["identity_contacts"]],
        )
        cur.executemany(
            "INSERT INTO zone_b.orders (order_id, buyer_id, household_key, scope, area_id,"
            " address_id, criteria, level, status, created_at, last_signal_at, synthetic_seed)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [(o["order_id"], o["buyer_id"], o["household_key"], o["scope"], o["area_id"],
              o["address_id"], Jsonb(o["criteria"]), o["level"], o["status"], o["created_at"],
              o["last_signal_at"], o["_seed"]) for o in data["orders"]],
        )
        cur.executemany(
            "INSERT INTO zone_b.order_event (event_id, order_id, type, schema_version, payload,"
            " actor, trace_id, causation_id, occurred_at, recorded_at, synthetic_seed)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [(e["envelope"]["event_id"], e["order_id"], e["envelope"]["type"],
              e["envelope"]["schema_version"], Jsonb(e["envelope"]["payload"]),
              Jsonb(e["envelope"]["actor"]), e["envelope"]["trace_id"],
              e["envelope"]["causation_id"], e["envelope"]["occurred_at"],
              e["envelope"]["recorded_at"], e["_seed"]) for e in data["order_events"]],
        )
    return {name: len(rows) for name, rows in data.items()}
