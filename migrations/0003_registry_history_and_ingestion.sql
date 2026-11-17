-- 0003_registry_history_and_ingestion
--
-- DRAFT. Written by an AI assistant. Migrations are a red field: a human owner
-- must review this file before anything relies on it (projektgrundlag §7.1).
--
-- Makes zone_a.property fully bitemporal and adds the ingestion bookkeeping.
--
-- Two time axes (ADR-002):
--   valid_from / valid_to        when the version was true in the world
--   recorded_at / superseded_at  when we held it as our current knowledge
--
-- A change never rewrites a row. The row that held our knowledge is marked
-- superseded, and new rows are inserted. "What did we know in March about
-- June?" can therefore always be answered. See core/registry/bitemporal.py.

ALTER TABLE zone_a.property DROP CONSTRAINT property_pkey;
ALTER TABLE zone_a.property ADD COLUMN version_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY;
ALTER TABLE zone_a.property ADD COLUMN superseded_at timestamptz;
ALTER TABLE zone_a.property
  ADD CONSTRAINT property_valid_range CHECK (valid_to IS NULL OR valid_to > valid_from);
ALTER TABLE zone_a.property
  ADD CONSTRAINT property_superseded_after_recorded
  CHECK (superseded_at IS NULL OR superseded_at >= recorded_at);

-- At most one open version per address in our current knowledge.
CREATE UNIQUE INDEX property_one_current
  ON zone_a.property (address_id)
  WHERE superseded_at IS NULL AND valid_to IS NULL;
CREATE INDEX property_address_ix ON zone_a.property (address_id, recorded_at);

DROP INDEX zone_a.property_zip_ix;
DROP INDEX zone_a.property_street_ix;
CREATE INDEX property_zip_ix ON zone_a.property (zip_id)
  WHERE superseded_at IS NULL AND valid_to IS NULL;
CREATE INDEX property_street_ix ON zone_a.property (street_id)
  WHERE superseded_at IS NULL AND valid_to IS NULL;

-- Invariant 2: history is never overwritten. The only change allowed on an
-- existing row is setting superseded_at once. Nothing can be deleted.
CREATE FUNCTION zone_a.property_history_guard() RETURNS trigger
  LANGUAGE plpgsql
  AS $$
BEGIN
  -- Nested on purpose: OLD and NEW do not exist for DELETE and TRUNCATE.
  IF TG_OP = 'UPDATE' THEN
    IF OLD.superseded_at IS NULL
       AND NEW.superseded_at IS NOT NULL
       AND (to_jsonb(NEW) - 'superseded_at') = (to_jsonb(OLD) - 'superseded_at') THEN
      RETURN NEW;
    END IF;
  END IF;
  RAISE EXCEPTION '% on zone_a.property is not allowed: history is never overwritten', TG_OP;
END
$$;

CREATE TRIGGER property_history_row
  BEFORE UPDATE OR DELETE ON zone_a.property
  FOR EACH ROW EXECUTE FUNCTION zone_a.property_history_guard();
CREATE TRIGGER property_history_truncate
  BEFORE TRUNCATE ON zone_a.property
  FOR EACH STATEMENT EXECUTE FUNCTION zone_a.property_history_guard();

-- property.changed events. Append-only log; consumers keep their own offset
-- in `seq` and are idempotent on event_id (ADR-003). Zone A: no personal data.
CREATE TABLE zone_a.property_event (
  event_id       uuid PRIMARY KEY,
  seq            bigint GENERATED ALWAYS AS IDENTITY,
  address_id     uuid NOT NULL,
  type           text NOT NULL,
  schema_version text NOT NULL,
  payload        jsonb NOT NULL,
  actor          jsonb NOT NULL,
  trace_id       text NOT NULL,
  occurred_at    timestamptz NOT NULL,
  recorded_at    timestamptz NOT NULL
);
CREATE UNIQUE INDEX property_event_seq_ix ON zone_a.property_event (seq);
CREATE INDEX property_event_address_ix ON zone_a.property_event (address_id, seq);

CREATE TRIGGER property_event_no_update_delete
  BEFORE UPDATE OR DELETE ON zone_a.property_event
  FOR EACH ROW EXECUTE FUNCTION audit.forbid_mutation();
CREATE TRIGGER property_event_no_truncate
  BEFORE TRUNCATE ON zone_a.property_event
  FOR EACH STATEMENT EXECUTE FUNCTION audit.forbid_mutation();

GRANT SELECT ON zone_a.property_event TO public_reader, app_role;
GRANT SELECT, INSERT ON zone_a.property_event TO ingest_role;

-- ---------------------------------------------------------------- ingestion

-- One row per source: where the last committed batch ended.
CREATE TABLE zone_a.ingestion_checkpoint (
  source     text PRIMARY KEY,
  cursor     text NOT NULL,
  run_id     text NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- Records that failed validation. Nothing is ever dropped silently: a fetched
-- record is either applied, found unchanged, or lands here.
CREATE TABLE zone_a.ingestion_quarantine (
  quarantine_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source        text NOT NULL,
  natural_key   text NOT NULL,
  payload_hash  text NOT NULL,
  payload       jsonb NOT NULL,
  issues        jsonb NOT NULL,
  run_id        text NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  resolved_at   timestamptz,
  UNIQUE (source, natural_key, payload_hash)
);

GRANT SELECT, INSERT, UPDATE ON zone_a.ingestion_checkpoint TO ingest_role;
GRANT SELECT, INSERT, UPDATE ON zone_a.ingestion_quarantine TO ingest_role;
-- The bookkeeping tables are internal. Revoke what 0001 never granted but a
-- later blanket grant might: anonymous traffic has no business here.
REVOKE ALL ON zone_a.ingestion_checkpoint, zone_a.ingestion_quarantine FROM public_reader, app_role;

-- ---------------------------------------------------------------- denominator

-- Set when dwelling_count jumps more than 2 % between two runs. While set,
-- density is not reported for the area (v5.1 §3.2). Cleared by a person.
ALTER TABLE zone_a.area ADD COLUMN density_frozen boolean NOT NULL DEFAULT false;
