"""Read side of the registry: areas, current properties and the facts layer (S1-10, S1-11).

Everything here is zone A. The queries are written to run as `public_reader`,
which has no access to zone B, so a mistake here cannot leak personal data.
"""

from __future__ import annotations

from typing import Any

import psycopg
from psycopg.rows import dict_row

from core.registry.dwellings import BOLIGKODER

LEVELS = ("MUNICIPALITY", "ZIP", "NEIGHBOURHOOD", "STREET")

# Which property column points at an area of a given level. Fixed mapping:
# the column name is never taken from user input.
_MEMBERSHIP = {
    "MUNICIPALITY": "municipality_id",
    "ZIP": "zip_id",
    "NEIGHBOURHOOD": "neighbourhood_id",
    "STREET": "street_id",
}
_AREA = "area_id, level, parent_id, name, dwelling_count"
_CURRENT = "superseded_at IS NULL AND valid_to IS NULL"


def _rows(conn: psycopg.Connection, sql: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def search_areas(conn: psycopg.Connection, q: str | None = None, level: str | None = None,
                 limit: int = 20) -> list[dict[str, Any]]:
    """Areas whose name contains `q`, widest level first."""
    where, params = ["true"], []
    if q:
        escaped = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        where.append("name ILIKE %s")
        params.append(f"%{escaped}%")
    if level:
        where.append("level = %s")
        params.append(level)
    return _rows(
        conn,
        f"SELECT {_AREA} FROM zone_a.area WHERE {' AND '.join(where)}"
        " ORDER BY array_position(%s::text[], level), name, area_id LIMIT %s",
        (*params, list(LEVELS), limit),
    )


def get_area(conn: psycopg.Connection, area_id: str) -> dict[str, Any] | None:
    rows = _rows(
        conn, f"SELECT {_AREA}, density_frozen FROM zone_a.area WHERE area_id = %s", (area_id,)
    )
    return rows[0] if rows else None


def area_path(conn: psycopg.Connection, area_id: str) -> list[dict[str, Any]]:
    """Ancestors from the municipality down to the area itself."""
    return _rows(
        conn,
        "WITH RECURSIVE up AS ("
        f"  SELECT {_AREA}, 0 AS depth FROM zone_a.area WHERE area_id = %s"
        "  UNION ALL"
        "  SELECT a.area_id, a.level, a.parent_id, a.name, a.dwelling_count, up.depth + 1"
        "  FROM up JOIN zone_a.area a ON a.area_id = up.parent_id"
        f") SELECT {_AREA} FROM up ORDER BY depth DESC",
        (area_id,),
    )


def area_children(conn: psycopg.Connection, area_id: str, limit: int = 500
                  ) -> list[dict[str, Any]]:
    return _rows(
        conn,
        f"SELECT {_AREA} FROM zone_a.area WHERE parent_id = %s ORDER BY name, area_id LIMIT %s",
        (area_id, limit),
    )


def current_property(conn: psycopg.Connection, address_id: str) -> dict[str, Any] | None:
    """The version we currently hold as true. Owner CVR is deliberately not returned."""
    rows = _rows(
        conn,
        "SELECT address_id::text AS address_id, bfe, municipality_id, zip_id, neighbourhood_id,"
        " street_id, owner_kind, attrs, quality_flags, valid_from, recorded_at"
        f" FROM zone_a.property_public WHERE address_id = %s AND {_CURRENT}",
        (address_id,),
    )
    return rows[0] if rows else None


def area_facts(conn: psycopg.Connection, area: dict[str, Any]) -> dict[str, Any]:
    """The facts layer for one area: housing stock from the registers.

    Returns the layer plus `synthetic` and `data_as_of` for the profile's meta block.
    """
    column = _MEMBERSHIP[area["level"]]
    codes = sorted(BOLIGKODER)
    base = f"FROM zone_a.property_public WHERE {column} = %s AND {_CURRENT}"
    residential = f"{base} AND attrs->>'anvendelse' = ANY(%s)"
    area_id = area["area_id"]

    totals = _rows(
        conn,
        "SELECT count(*) FILTER (WHERE attrs->>'anvendelse' = ANY(%s)) AS dwellings,"
        " count(*) FILTER (WHERE NOT attrs->>'anvendelse' = ANY(%s)) AS other,"
        " coalesce(bool_or(synthetic_seed IS NOT NULL), false) AS synthetic,"
        f" max(recorded_at) AS data_as_of {base}",
        (codes, codes, area_id),
    )[0]
    by_usage = _rows(
        conn,
        f"SELECT attrs->>'anvendelse' AS key, count(*) AS count {residential}"
        " GROUP BY 1 ORDER BY 1",
        (area_id, codes),
    )
    by_owner = _rows(
        conn,
        f"SELECT coalesce(owner_kind, 'UNKNOWN') AS key, count(*) AS count {residential}"
        " GROUP BY 1 ORDER BY 1",
        (area_id, codes),
    )
    spread = _rows(
        conn,
        "SELECT percentile_cont(ARRAY[0.25, 0.5, 0.75]) WITHIN GROUP"
        "   (ORDER BY (attrs->>'areal')::numeric) AS areal,"
        " min((attrs->>'opfoerelsesaar')::int) AS year_min,"
        " percentile_disc(0.5) WITHIN GROUP (ORDER BY (attrs->>'opfoerelsesaar')::int)"
        "   AS year_median,"
        f" max((attrs->>'opfoerelsesaar')::int) AS year_max {residential}",
        (area_id, codes),
    )[0]

    areal = spread["areal"]
    return {
        "fakta": {
            "dwelling_count": totals["dwellings"],
            "non_residential_count": totals["other"],
            "by_usage": by_usage,
            "by_owner_kind": by_owner,
            "areal": None if not areal or areal[0] is None else {
                "p25": float(areal[0]), "median": float(areal[1]), "p75": float(areal[2]),
            },
            "opfoerelsesaar": None if spread["year_min"] is None else {
                "min": spread["year_min"], "median": spread["year_median"],
                "max": spread["year_max"],
            },
        },
        "synthetic": totals["synthetic"],
        "data_as_of": totals["data_as_of"],
    }


def area_profile(conn: psycopg.Connection, area_id: str) -> dict[str, Any] | None:
    """The public area profile. Layers without data are None, never zero."""
    area = get_area(conn, area_id)
    if area is None:
        return None
    facts = area_facts(conn, area)
    frozen = area.pop("density_frozen")
    return {
        "area": area,
        "path": area_path(conn, area_id),
        "children": area_children(conn, area_id),
        "layers": {
            "fakta": facts["fakta"],
            "bevaegelse": [],
            "hverdag": None,
            "efterspoergsel": None,
        },
        "meta": {
            "layer_status": {
                "fakta": "OK" if facts["fakta"]["dwelling_count"] else "NO_DATA_YET",
                "bevaegelse": "NO_DATA_YET",
                "hverdag": "NO_DATA_YET",
                "efterspoergsel": "NO_DATA_YET",
            },
            "synthetic": facts["synthetic"],
            "data_as_of": facts["data_as_of"],
            "density_frozen": frozen,
        },
    }
