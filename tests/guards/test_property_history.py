"""Guard: register history is never overwritten (invariant 2, ADR-002).

DRAFT written by an AI assistant. Guard tests are a red field: a human owner
must review this file before it counts as a guard (projektgrundlag §7.1).
"""

import psycopg
import pytest


@pytest.fixture
def some_version(conn):
    return conn.execute("SELECT version_id FROM zone_a.property LIMIT 1").fetchone()[0]


@pytest.mark.parametrize("statement", [
    "UPDATE zone_a.property SET attrs = '{}' WHERE version_id = %s",
    "UPDATE zone_a.property SET valid_to = '2030-01-01' WHERE version_id = %s",
    "UPDATE zone_a.property SET recorded_at = now() WHERE version_id = %s",
    "UPDATE zone_a.property SET superseded_at = now(), owner_kind = 'COMPANY'"
    " WHERE version_id = %s",
    "DELETE FROM zone_a.property WHERE version_id = %s",
])
def test_existing_versions_cannot_be_rewritten(conn, some_version, statement):
    with pytest.raises(psycopg.errors.RaiseException, match="never overwritten"), \
            conn.transaction():
        conn.execute(statement, (some_version,))


def test_truncate_is_blocked(conn):
    with pytest.raises(psycopg.errors.RaiseException, match="never overwritten"), \
            conn.transaction():
        conn.execute("TRUNCATE zone_a.property")


def test_superseding_once_is_allowed_and_only_once(conn, some_version):
    conn.execute(
        "UPDATE zone_a.property SET superseded_at = now() WHERE version_id = %s", (some_version,)
    )
    with pytest.raises(psycopg.errors.RaiseException), conn.transaction():
        conn.execute(
            "UPDATE zone_a.property SET superseded_at = now() + interval '1 day'"
            " WHERE version_id = %s", (some_version,)
        )
    with pytest.raises(psycopg.errors.RaiseException), conn.transaction():
        conn.execute(
            "UPDATE zone_a.property SET superseded_at = NULL WHERE version_id = %s",
            (some_version,),
        )


def test_two_open_versions_for_one_address_are_impossible(conn):
    with pytest.raises(psycopg.errors.UniqueViolation), conn.transaction():
        conn.execute(
            "INSERT INTO zone_a.property (address_id, bfe, municipality_id, zip_id, attrs,"
            " valid_from, recorded_at)"
            " SELECT address_id, bfe, municipality_id, zip_id, attrs, valid_from, now()"
            " FROM zone_a.property LIMIT 1"
        )


@pytest.mark.parametrize("statement", [
    "UPDATE zone_a.property_event SET trace_id = 'x'",
    "DELETE FROM zone_a.property_event",
    "TRUNCATE zone_a.property_event",
])
def test_property_events_are_append_only(conn, statement):
    conn.execute(
        "INSERT INTO zone_a.property_event (event_id, address_id, type, schema_version, payload,"
        " actor, trace_id, occurred_at, recorded_at)"
        " VALUES (gen_random_uuid(), gen_random_uuid(), 'property.changed', '1.0.0', '{}', '{}',"
        " 't', now(), now())"
    )
    with pytest.raises(psycopg.errors.RaiseException, match="append-only"), conn.transaction():
        conn.execute(statement)


@pytest.mark.parametrize("role", ["public_reader", "app_role"])
@pytest.mark.parametrize("table", ["ingestion_checkpoint", "ingestion_quarantine"])
def test_ingestion_bookkeeping_is_internal(conn, role, table):
    conn.execute(f"SET LOCAL ROLE {role}")
    with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
        conn.execute(f"SELECT 1 FROM zone_a.{table} LIMIT 1")
