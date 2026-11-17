"""The density denominator: dwellings per area on every level (S1-07).

`dwelling_count` is the number of current addresses with a residential usage
code. It is counted per address, never per property: a cooperative with one
BFE and forty flats counts forty.

If the count for an area moves more than 2 % between two runs, density is
frozen for that area until a person has looked at why (v5.1 §3.2). A jump
that size is far more likely to be a data error than forty new homes.
"""

from __future__ import annotations

from typing import Any

import psycopg

# Usage codes that count as a dwelling. Placeholder set used by the synthetic
# data. The real list of BBR codes is a business decision and is fixed
# together with the BBR adapter (S1-04).
BOLIGKODER = frozenset({"120", "130", "140"})

FREEZE_THRESHOLD = 0.02

_COUNT = """
SELECT x.area_id, count(*) AS n
FROM zone_a.property p
CROSS JOIN LATERAL (
  VALUES (p.municipality_id), (p.zip_id), (p.neighbourhood_id), (p.street_id)
) AS x (area_id)
WHERE p.superseded_at IS NULL AND p.valid_to IS NULL
  AND p.attrs->>'anvendelse' = ANY(%s)
  AND x.area_id IS NOT NULL
GROUP BY x.area_id
"""


def recompute_dwelling_counts(conn: psycopg.Connection) -> list[dict[str, Any]]:
    """Recount dwellings for every area. Returns one entry per area that changed.

    Each entry: area_id, old, new, frozen. `frozen` is True when this run froze
    density for the area. The first count for an area (old == 0) never freezes.
    """
    counted = dict(conn.execute(_COUNT, (sorted(BOLIGKODER),)).fetchall())
    existing = conn.execute(
        "SELECT area_id, dwelling_count, density_frozen FROM zone_a.area ORDER BY area_id"
        " FOR UPDATE"
    ).fetchall()
    changes: list[dict[str, Any]] = []
    for area_id, old, already_frozen in existing:
        new = counted.get(area_id, 0)
        if new == old:
            continue
        freeze = old > 0 and abs(new - old) / old > FREEZE_THRESHOLD
        conn.execute(
            "UPDATE zone_a.area SET dwelling_count = %s, density_frozen = %s, updated_at = now()"
            " WHERE area_id = %s",
            (new, already_frozen or freeze, area_id),
        )
        changes.append({"area_id": area_id, "old": old, "new": new, "frozen": freeze})
    return changes


def unfreeze_density(conn: psycopg.Connection, area_id: str, *, actor: str, reason: str,
                     trace_id: str) -> None:
    """Release a frozen area after a person has checked the jump. Always audited."""
    if not reason.strip():
        raise ValueError("a reason is required to unfreeze density")
    updated = conn.execute(
        "UPDATE zone_a.area SET density_frozen = false, updated_at = now()"
        " WHERE area_id = %s AND density_frozen",
        (area_id,),
    ).rowcount
    if updated == 0:
        raise LookupError(f"{area_id} is not frozen")
    conn.execute(
        "INSERT INTO audit.audit_log (actor, action, target, zone, trace_id, detail)"
        " VALUES (%s, 'DENSITY_UNFROZEN', %s, 'A', %s, jsonb_build_object('reason', %s::text))",
        (actor, area_id, trace_id, reason),
    )
