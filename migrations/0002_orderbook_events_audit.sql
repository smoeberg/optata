-- 0002_orderbook_events_audit
--
-- DRAFT. Written by an AI assistant. Red field: a human owner must review this
-- file before anything relies on it (projektgrundlag §6.3 and §7.1).
--
-- Orders, the append-only order event log and the append-only audit log.

-- ---------------------------------------------------------------- orders

-- v5.1: every order is created after MitID login, so there are two levels.
CREATE TABLE zone_b.orders (
  order_id       uuid PRIMARY KEY,
  buyer_id       uuid NOT NULL REFERENCES zone_b.identity,
  household_key  text NOT NULL,
  scope          text NOT NULL CHECK (scope IN ('AREA', 'ADDRESS')),
  area_id        text NOT NULL REFERENCES zone_a.area,
  address_id     uuid,
  criteria       jsonb NOT NULL,
  level          text NOT NULL CHECK (level IN ('QUALIFIED', 'VERIFIED')),
  status         text NOT NULL CHECK (status IN
                   ('ACTIVE', 'PAUSED', 'MATCHED', 'IN_DIALOG', 'AGREED',
                    'WITHDRAWN', 'EXPIRED', 'ERASED')),
  created_at     timestamptz NOT NULL,
  last_signal_at timestamptz NOT NULL,
  synthetic_seed integer,
  CONSTRAINT address_scope_needs_address CHECK (scope <> 'ADDRESS' OR address_id IS NOT NULL)
);

-- Invariant 9: one active order per household and scope. Enforced here, not in
-- the application. Co-buyers join the same order instead of creating a new one.
CREATE UNIQUE INDEX order_one_per_household_scope
  ON zone_b.orders (household_key, scope, coalesce(address_id::text, area_id))
  WHERE status IN ('ACTIVE', 'PAUSED', 'MATCHED', 'IN_DIALOG', 'AGREED');

ALTER TABLE zone_b.orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_buyer_own ON zone_b.orders
  FOR ALL TO app_role
  USING (buyer_id = zone_b.current_identity())
  WITH CHECK (buyer_id = zone_b.current_identity());
GRANT SELECT, INSERT, UPDATE ON zone_b.orders TO app_role;

-- ---------------------------------------------------------------- append-only

CREATE FUNCTION audit.forbid_mutation() RETURNS trigger
  LANGUAGE plpgsql
  AS $$
BEGIN
  RAISE EXCEPTION '% on %.% is not allowed: the table is append-only',
    TG_OP, TG_TABLE_SCHEMA, TG_TABLE_NAME;
END
$$;

-- Invariant 3: order events are append-only. Schema changes are handled by
-- upcasting when events are read (core/events/upcast.py).
-- Payloads carry pseudonyms and reference ids only, never contact data.
CREATE TABLE zone_b.order_event (
  event_id       uuid PRIMARY KEY,
  seq            bigserial NOT NULL,
  order_id       uuid NOT NULL REFERENCES zone_b.orders,
  type           text NOT NULL,
  schema_version text NOT NULL,
  payload        jsonb NOT NULL,
  actor          jsonb NOT NULL,
  trace_id       text NOT NULL,
  causation_id   uuid,
  occurred_at    timestamptz NOT NULL,
  recorded_at    timestamptz NOT NULL DEFAULT now(),
  synthetic_seed integer
);
CREATE INDEX order_event_order_ix ON zone_b.order_event (order_id, occurred_at);

CREATE TRIGGER order_event_no_update_delete
  BEFORE UPDATE OR DELETE ON zone_b.order_event
  FOR EACH ROW EXECUTE FUNCTION audit.forbid_mutation();
CREATE TRIGGER order_event_no_truncate
  BEFORE TRUNCATE ON zone_b.order_event
  FOR EACH STATEMENT EXECUTE FUNCTION audit.forbid_mutation();

ALTER TABLE zone_b.order_event ENABLE ROW LEVEL SECURITY;
CREATE POLICY order_event_own ON zone_b.order_event
  FOR ALL TO app_role
  USING (order_id IN (SELECT order_id FROM zone_b.orders))
  WITH CHECK (order_id IN (SELECT order_id FROM zone_b.orders));
GRANT SELECT, INSERT ON zone_b.order_event TO app_role;
GRANT USAGE ON SEQUENCE zone_b.order_event_seq_seq TO app_role;

-- Audit of zone B and vault access. Kept 5 years. Insert only.
CREATE TABLE audit.audit_log (
  audit_id    bigserial PRIMARY KEY,
  actor       text NOT NULL,
  action      text NOT NULL,
  target      text NOT NULL,
  zone        text NOT NULL CHECK (zone IN ('A', 'B', 'C')),
  trace_id    text NOT NULL,
  detail      jsonb NOT NULL DEFAULT '{}',
  occurred_at timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER audit_log_no_update_delete
  BEFORE UPDATE OR DELETE ON audit.audit_log
  FOR EACH ROW EXECUTE FUNCTION audit.forbid_mutation();
CREATE TRIGGER audit_log_no_truncate
  BEFORE TRUNCATE ON audit.audit_log
  FOR EACH STATEMENT EXECUTE FUNCTION audit.forbid_mutation();

GRANT INSERT ON audit.audit_log TO app_role, disclosure_service;
GRANT USAGE ON SEQUENCE audit.audit_log_audit_id_seq TO app_role, disclosure_service;
