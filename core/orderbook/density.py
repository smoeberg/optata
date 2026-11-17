"""Density: verified buyers per 1,000 dwellings, on every area level (S1-09).

The figures are computed by the materialized view zone_b.area_density; the
counting rules are documented in migrations/0004_area_density.sql. This module
only refreshes and reads it.

These are raw internal counts, including counts below 5. They must not be
shown to anyone outside staff. The public, k-anonymous figures belong to
zone C (core/insights) and are a separate, later piece of work.
"""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row


def refresh_density(conn: psycopg.Connection) -> None:
    """Recompute density. Call after ingestion and when orders change, never per request."""
    conn.execute("REFRESH MATERIALIZED VIEW zone_b.area_density")


def density(conn: psycopg.Connection, area_id: str) -> dict[str, Any] | None:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM zone_b.area_density WHERE area_id = %s", (area_id,))
        return cur.fetchone()
