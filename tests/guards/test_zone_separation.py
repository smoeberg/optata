"""Guard: zone separation is enforced by database roles (invariant 4, ADR-004).

DRAFT written by an AI assistant. Guard tests are a red field: a human owner
must review this file before it counts as a guard (projektgrundlag §7.1).
"""

import psycopg
import pytest


def _roles_that_can_read(conn, schema, table):
    rows = conn.execute(
        "SELECT rolname FROM pg_roles"
        " WHERE NOT rolsuper AND rolname !~ '^pg_'"
        "   AND has_schema_privilege(rolname, %s, 'USAGE')"
        "   AND has_table_privilege(rolname, %s, 'SELECT')"
        " ORDER BY rolname",
        (schema, f"{schema}.{table}"),
    ).fetchall()
    return [r[0] for r in rows]


def test_vault_only_disclosure(conn):
    """Only disclosure_service may read contact data."""
    assert _roles_that_can_read(conn, "vault", "identity_contact") == ["disclosure_service"]


@pytest.mark.parametrize("role", ["app_role", "public_reader", "ingest_role"])
def test_other_roles_are_denied_the_vault(conn, role):
    conn.execute(f"SET LOCAL ROLE {role}")
    with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
        conn.execute("SELECT full_name FROM vault.identity_contact LIMIT 1")


def test_disclosure_service_can_read_the_vault(conn):
    conn.execute("SET LOCAL ROLE disclosure_service")
    assert conn.execute("SELECT count(*) FROM vault.identity_contact").fetchone()[0] > 0


@pytest.mark.parametrize("table", ["identity", "orders", "order_event"])
def test_anonymous_cannot_reach_zone_b(conn, table):
    """public_reader serves anonymous traffic and must not be able to join to zone B."""
    conn.execute("SET LOCAL ROLE public_reader")
    with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
        conn.execute(f"SELECT 1 FROM zone_a.property p JOIN zone_b.{table} x ON true LIMIT 1")


def test_anonymous_can_read_zone_a(conn):
    conn.execute("SET LOCAL ROLE public_reader")
    assert conn.execute("SELECT count(*) FROM zone_a.property").fetchone()[0] > 0


def test_no_role_can_write_the_vault(conn):
    """The write path is not defined yet (S3). Until then nobody but the owner may write."""
    rows = conn.execute(
        "SELECT rolname FROM pg_roles WHERE NOT rolsuper AND rolname !~ '^pg_'"
        " AND has_table_privilege(rolname, 'vault.identity_contact', 'INSERT, UPDATE, DELETE')"
    ).fetchall()
    assert rows == []


def test_buyer_sees_only_own_orders(conn, dataset):
    """Row level security: app_role sees the orders of the identity in the session context."""
    buyer = dataset["orders"][0]["buyer_id"]
    conn.execute("SET LOCAL ROLE app_role")
    conn.execute("SELECT set_config('app.identity_id', %s, true)", (buyer,))
    seen = conn.execute("SELECT DISTINCT buyer_id::text FROM zone_b.orders").fetchall()
    assert seen == [(buyer,)]
    events = conn.execute(
        "SELECT count(*) FROM zone_b.order_event e"
        " WHERE e.order_id NOT IN (SELECT order_id FROM zone_b.orders)"
    ).fetchone()[0]
    assert events == 0


def test_no_session_context_means_no_rows(conn):
    conn.execute("SET LOCAL ROLE app_role")
    for table in ("identity", "orders", "order_event"):
        assert conn.execute(f"SELECT count(*) FROM zone_b.{table}").fetchone()[0] == 0


def test_buyer_cannot_create_an_order_for_someone_else(conn, dataset):
    buyer, other = dataset["orders"][0], dataset["orders"][1]
    conn.execute("SET LOCAL ROLE app_role")
    conn.execute("SELECT set_config('app.identity_id', %s, true)", (buyer["buyer_id"],))
    with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
        conn.execute(
            "INSERT INTO zone_b.orders (order_id, buyer_id, household_key, scope, area_id,"
            " criteria, level, status, created_at, last_signal_at)"
            " VALUES (gen_random_uuid(), %s, 'hk-x', 'AREA', %s, '{}', 'QUALIFIED', 'ACTIVE',"
            " now(), now())",
            (other["buyer_id"], other["area_id"]),
        )
