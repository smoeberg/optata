import uuid
from dataclasses import replace
from datetime import UTC, date, datetime

import psycopg
import pytest

from core.orderbook import density, refresh_density
from core.registry import (
    BOLIGKODER,
    PropertyVersion,
    recompute_dwelling_counts,
    unfreeze_density,
    upsert_property,
)
from tools.fixtures.generate import FX01_BFE, ZIP_ID

NOW = datetime(2026, 9, 1, tzinfo=UTC)


def _expected(dataset):
    """Independent re-implementation of the counting rules, in plain Python."""
    parent = {a["area_id"]: a["parent_id"] for a in dataset["areas"]}
    level = {a["area_id"]: a["level"] for a in dataset["areas"]}
    address = {p["address_id"]: p for p in dataset["properties"]}

    def lineage(area_id):
        while area_id is not None:
            yield area_id
            area_id = parent[area_id]

    verified = {a: set() for a in parent}
    active = {a: set() for a in parent}
    for order in dataset["orders"]:
        if order["scope"] == "AREA":
            inside = set(lineage(order["area_id"]))
            hit = {a for a in parent if a in inside or order["area_id"] in set(lineage(a))}
        else:
            prop = address[order["address_id"]]
            hit = {prop["zip_id"], prop["municipality_id"]}
        for area_id in hit:
            active[area_id].add(order["household_key"])
            if order["level"] == "VERIFIED":
                verified[area_id].add(order["household_key"])
    return level, verified, active


def test_density_matches_an_independent_count_on_every_level(conn, dataset):
    level, verified, active = _expected(dataset)
    rows = conn.execute(
        "SELECT area_id, level, verified_buyers, active_buyers FROM zone_b.area_density"
    ).fetchall()
    assert len(rows) == len(level)
    for area_id, lvl, n_verified, n_active in rows:
        assert lvl == level[area_id]
        assert n_verified == len(verified[area_id]), area_id
        assert n_active == len(active[area_id]), area_id


def test_zip_density_is_verified_per_thousand_dwellings(conn):
    row = density(conn, ZIP_ID)
    assert row["dwelling_count"] == 300
    assert row["verified_buyers"] == 15
    assert float(row["verified_per_1000"]) == 50.0


def test_address_orders_never_count_on_street_or_neighbourhood(conn, dataset):
    """Otherwise an owner could work out that someone wants a neighbour's house."""
    area_buyers = {o["household_key"] for o in dataset["orders"] if o["scope"] == "AREA"}
    rows = conn.execute(
        "SELECT area_id, active_buyers FROM zone_b.area_density"
        " WHERE level IN ('STREET', 'NEIGHBOURHOOD')"
    ).fetchall()
    assert rows
    for _area_id, n_active in rows:
        assert n_active <= len(area_buyers)
    address_only = len({o["household_key"] for o in dataset["orders"]}) - len(area_buyers)
    assert address_only > 0
    assert density(conn, ZIP_ID)["active_buyers"] == len(area_buyers) + address_only


def test_a_buyer_with_three_overlapping_orders_counts_once(conn, dataset):
    """Buyers are counted, not orders: two streets and their neighbourhood, one household."""
    streets = [a for a in dataset["areas"] if a["level"] == "STREET"]
    neighbourhood = streets[0]["parent_id"]
    three = [s["area_id"] for s in streets if s["parent_id"] == neighbourhood][:2]
    three.append(neighbourhood)
    assert len(three) == 3
    before = density(conn, neighbourhood)["verified_buyers"]

    identity_id, household = str(uuid.uuid4()), "hk-three-streets"
    conn.execute(
        "INSERT INTO zone_b.identity (identity_id, provider, pseudonym, provider_sub, assurance,"
        " household_key, created_at) VALUES (%s, 'MITID_PRIVATE', 'K-THREE', 'sub-three',"
        " 'SUBSTANTIAL', %s, now())", (identity_id, household),
    )
    for street in three:
        conn.execute(
            "INSERT INTO zone_b.orders (order_id, buyer_id, household_key, scope, area_id,"
            " criteria, level, status, created_at, last_signal_at)"
            " VALUES (gen_random_uuid(), %s, %s, 'AREA', %s, '{}', 'VERIFIED', 'ACTIVE', now(),"
            " now())", (identity_id, household, street),
        )
    refresh_density(conn)

    assert density(conn, neighbourhood)["verified_buyers"] == before + 1
    assert density(conn, ZIP_ID)["verified_buyers"] == 16


def test_mixed_levels_in_one_household_count_once_as_active(conn, dataset):
    """One household, one VERIFIED and one QUALIFIED order in the same neighbourhood."""
    streets = [a for a in dataset["areas"] if a["level"] == "STREET"]
    neighbourhood = streets[0]["parent_id"]
    two = [s["area_id"] for s in streets if s["parent_id"] == neighbourhood][:2]
    before = density(conn, neighbourhood)

    identity_id, household = str(uuid.uuid4()), "hk-mixed"
    conn.execute(
        "INSERT INTO zone_b.identity (identity_id, provider, pseudonym, provider_sub, assurance,"
        " household_key, created_at) VALUES (%s, 'MITID_PRIVATE', 'K-MIXED', 'sub-mixed',"
        " 'SUBSTANTIAL', %s, now())", (identity_id, household),
    )
    for street, level in zip(two, ("VERIFIED", "QUALIFIED"), strict=True):
        conn.execute(
            "INSERT INTO zone_b.orders (order_id, buyer_id, household_key, scope, area_id,"
            " criteria, level, status, created_at, last_signal_at)"
            " VALUES (gen_random_uuid(), %s, %s, 'AREA', %s, '{}', %s, 'ACTIVE', now(), now())",
            (identity_id, household, street, level),
        )
    refresh_density(conn)

    after = density(conn, neighbourhood)
    assert after["active_buyers"] == before["active_buyers"] + 1
    assert after["verified_buyers"] == before["verified_buyers"] + 1


def test_withdrawn_orders_do_not_count(conn, dataset):
    verified = next(o for o in dataset["orders"] if o["level"] == "VERIFIED")
    conn.execute("UPDATE zone_b.orders SET status = 'WITHDRAWN' WHERE order_id = %s",
                 (verified["order_id"],))
    refresh_density(conn)
    assert density(conn, ZIP_ID)["verified_buyers"] == 14


@pytest.mark.parametrize("role", ["public_reader", "app_role", "ingest_role",
                                  "disclosure_service"])
def test_raw_density_is_not_readable_by_application_roles(conn, role):
    """Raw counts include cells below 5. Only the k-anonymous zone C version may be exposed."""
    conn.execute(f"SET LOCAL ROLE {role}")
    with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
        conn.execute("SELECT 1 FROM zone_b.area_density LIMIT 1")


# ---------------------------------------------------------------- denominator


def test_recount_agrees_with_the_generator(conn):
    assert recompute_dwelling_counts(conn) == []


def test_cooperative_counts_forty_on_every_level(conn, dataset):
    """FX-01: one BFE, forty dwellings. Counting BFE would give one."""
    units = [p for p in dataset["properties"] if p["bfe"] == FX01_BFE]
    street = units[0]["street_id"]
    in_street = conn.execute(
        "SELECT count(*) FROM zone_a.property WHERE street_id = %s AND bfe = %s",
        (street, FX01_BFE),
    ).fetchone()[0]
    assert in_street == 40
    assert density(conn, street)["dwelling_count"] >= 40


def _new_home(dataset, i, usage="120"):
    base = dataset["properties"][100]
    return PropertyVersion(
        address_id=str(uuid.uuid5(uuid.NAMESPACE_OID, f"density-{i}")), bfe=f"SYN-BFE-NEW-{i}",
        municipality_id=base["municipality_id"], zip_id=base["zip_id"],
        neighbourhood_id=base["neighbourhood_id"], street_id=base["street_id"],
        valid_from=date(2026, 8, 1), attrs={"anvendelse": usage, "areal": 100},
        owner_kind="PRIVATE",
    )


def test_small_change_updates_the_count_without_freezing(conn, dataset):
    upsert_property(conn, _new_home(dataset, 1), recorded_at=NOW, trace_id="t")
    changes = {c["area_id"]: c for c in recompute_dwelling_counts(conn)}
    assert changes[ZIP_ID] == {"area_id": ZIP_ID, "old": 300, "new": 301, "frozen": False}


def test_non_residential_units_are_not_counted(conn, dataset):
    assert "320" not in BOLIGKODER
    upsert_property(conn, _new_home(dataset, 1, usage="320"), recorded_at=NOW, trace_id="t")
    assert recompute_dwelling_counts(conn) == []


def test_jump_above_two_percent_freezes_density(conn, dataset):
    for i in range(10):
        upsert_property(conn, _new_home(dataset, i), recorded_at=NOW, trace_id="t")
    changes = {c["area_id"]: c for c in recompute_dwelling_counts(conn)}
    assert changes[ZIP_ID]["new"] == 310
    assert changes[ZIP_ID]["frozen"] is True

    refresh_density(conn)
    row = density(conn, ZIP_ID)
    assert row["density_frozen"] is True
    assert row["verified_per_1000"] is None, "a frozen area must not report density"


def test_frozen_stays_frozen_until_a_person_releases_it(conn, dataset):
    for i in range(10):
        upsert_property(conn, _new_home(dataset, i), recorded_at=NOW, trace_id="t")
    recompute_dwelling_counts(conn)
    upsert_property(conn, _new_home(dataset, 99), recorded_at=NOW, trace_id="t")
    changes = {c["area_id"]: c for c in recompute_dwelling_counts(conn)}
    assert changes[ZIP_ID]["frozen"] is False, "this run did not cause a new freeze"
    frozen = conn.execute(
        "SELECT density_frozen FROM zone_a.area WHERE area_id = %s", (ZIP_ID,)
    ).fetchone()[0]
    assert frozen is True

    with pytest.raises(ValueError):
        unfreeze_density(conn, ZIP_ID, actor="staff-1", reason=" ", trace_id="t")
    unfreeze_density(conn, ZIP_ID, actor="staff-1", reason="new block of flats, confirmed in BBR",
                     trace_id="t")
    refresh_density(conn)

    assert density(conn, ZIP_ID)["verified_per_1000"] is not None
    audit = conn.execute(
        "SELECT actor, detail->>'reason' FROM audit.audit_log WHERE action = 'DENSITY_UNFROZEN'"
    ).fetchone()
    assert audit == ("staff-1", "new block of flats, confirmed in BBR")
    with pytest.raises(LookupError):
        unfreeze_density(conn, ZIP_ID, actor="staff-1", reason="again", trace_id="t")


def test_removed_dwelling_lowers_the_count(conn, dataset):
    home = _new_home(dataset, 1)
    upsert_property(conn, home, recorded_at=NOW, trace_id="t")
    recompute_dwelling_counts(conn)
    converted = replace(home, valid_from=date(2026, 9, 1),
                        attrs={"anvendelse": "320", "areal": 100})
    upsert_property(conn, converted, recorded_at=datetime(2026, 9, 5, tzinfo=UTC), trace_id="t")
    changes = {c["area_id"]: c for c in recompute_dwelling_counts(conn)}
    assert (changes[ZIP_ID]["old"], changes[ZIP_ID]["new"]) == (301, 300)
