"""Guard: order events and the audit log are append-only (invariant 3, S0-04, S0-07).

DRAFT written by an AI assistant. Guard tests are a red field: a human owner
must review this file before it counts as a guard (projektgrundlag §7.1).
"""

import psycopg
import pytest

APPEND_ONLY = ["zone_b.order_event", "audit.audit_log"]


@pytest.mark.parametrize("statement", [
    "UPDATE zone_b.order_event SET type = 'tampered'",
    "DELETE FROM zone_b.order_event",
    "TRUNCATE zone_b.order_event",
    "UPDATE audit.audit_log SET actor = 'tampered'",
    "DELETE FROM audit.audit_log",
    "TRUNCATE audit.audit_log",
])
def test_app_role_cannot_mutate(conn, statement):
    conn.execute("SET LOCAL ROLE app_role")
    with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
        conn.execute(statement)


@pytest.mark.parametrize("table", APPEND_ONLY)
@pytest.mark.parametrize("operation", ["UPDATE {t} SET trace_id = 'x'", "DELETE FROM {t}",
                                        "TRUNCATE {t}"])
def test_even_the_owner_cannot_mutate(conn, table, operation):
    """The trigger stops a privileged role too, not only app_role."""
    conn.execute(
        "INSERT INTO audit.audit_log (actor, action, target, zone, trace_id)"
        " VALUES ('test', 'TEST', 'none', 'B', 'trace')"
    )
    with pytest.raises(psycopg.errors.RaiseException, match="append-only"), conn.transaction():
        conn.execute(operation.format(t=table))


def test_events_survive_attempts(conn):
    before = conn.execute("SELECT count(*) FROM zone_b.order_event").fetchone()[0]
    assert before > 0
    with pytest.raises(psycopg.errors.RaiseException), conn.transaction():
        conn.execute("DELETE FROM zone_b.order_event")
    after = conn.execute("SELECT count(*) FROM zone_b.order_event").fetchone()[0]
    assert after == before


def test_app_role_can_append_audit(conn):
    conn.execute("SET LOCAL ROLE app_role")
    conn.execute(
        "INSERT INTO audit.audit_log (actor, action, target, zone, trace_id)"
        " VALUES ('K-TEST', 'ORDER_VIEWED', 'order', 'B', 'trace-1')"
    )
