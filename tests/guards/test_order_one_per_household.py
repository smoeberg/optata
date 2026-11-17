"""Guard: one active order per household and scope (invariant 9).

DRAFT written by an AI assistant. Guard tests are a red field: a human owner
must review this file before it counts as a guard (projektgrundlag §7.1).
"""

import psycopg
import pytest

INSERT = (
    "INSERT INTO zone_b.orders (order_id, buyer_id, household_key, scope, area_id, address_id,"
    " criteria, level, status, created_at, last_signal_at)"
    " VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, '{}', 'QUALIFIED', %s, now(), now())"
)


def _existing(dataset, scope):
    return next(o for o in dataset["orders"] if o["scope"] == scope)


@pytest.mark.parametrize("scope", ["AREA", "ADDRESS"])
def test_second_active_order_is_rejected(conn, dataset, scope):
    o = _existing(dataset, scope)
    with pytest.raises(psycopg.errors.UniqueViolation), conn.transaction():
        conn.execute(INSERT, (o["buyer_id"], o["household_key"], o["scope"], o["area_id"],
                              o["address_id"], "ACTIVE"))


def test_co_resident_cannot_open_a_second_order(conn, dataset):
    """FX-03: another identity in the same household hits the same index."""
    o = dataset["orders"][0]
    co_resident = dataset["identities"][-1]
    assert co_resident["household_key"] == o["household_key"]
    assert co_resident["identity_id"] != o["buyer_id"]
    with pytest.raises(psycopg.errors.UniqueViolation), conn.transaction():
        conn.execute(INSERT, (co_resident["identity_id"], o["household_key"], o["scope"],
                              o["area_id"], o["address_id"], "ACTIVE"))


def test_withdrawn_order_does_not_block_a_new_one(conn, dataset):
    o = _existing(dataset, "AREA")
    conn.execute(INSERT, (o["buyer_id"], o["household_key"], o["scope"], o["area_id"],
                          o["address_id"], "WITHDRAWN"))


def test_address_scope_requires_an_address(conn, dataset):
    o = _existing(dataset, "AREA")
    with pytest.raises(psycopg.errors.CheckViolation), conn.transaction():
        conn.execute(INSERT, (o["buyer_id"], "hk-new", "ADDRESS", o["area_id"], None, "ACTIVE"))
