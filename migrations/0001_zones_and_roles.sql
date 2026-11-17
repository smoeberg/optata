-- 0001_zones_and_roles
--
-- DRAFT. Written by an AI assistant. Zone separation, roles and RLS are a red
-- field (projektgrundlag §6.3 and §7.1): a human owner must review this file
-- before anything relies on it.
--
-- Three zones enforced by the database, not by application code (ADR-004):
--   zone_a  public register data            readable by everyone
--   zone_b  identities, orders, events      app_role only, row level security
--   vault   contact data                    disclosure_service only
--   zone_c  aggregates, k >= 5              built by controlled jobs (later sprint)
--   audit   append-only log
--
-- Forward-only. Roles are cluster-wide, so they are created only if missing.

DO $$
DECLARE
  r text;
BEGIN
  FOREACH r IN ARRAY ARRAY['public_reader', 'app_role', 'disclosure_service', 'ingest_role']
  LOOP
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = r) THEN
      EXECUTE format('CREATE ROLE %I NOLOGIN', r);
    END IF;
  END LOOP;
END
$$;

CREATE SCHEMA zone_a;
CREATE SCHEMA zone_b;
CREATE SCHEMA vault;
CREATE SCHEMA zone_c;
CREATE SCHEMA audit;

REVOKE ALL ON SCHEMA zone_a, zone_b, vault, zone_c, audit FROM PUBLIC;

GRANT USAGE ON SCHEMA zone_a TO public_reader, app_role, ingest_role;
GRANT USAGE ON SCHEMA zone_c TO public_reader, app_role;
GRANT USAGE ON SCHEMA zone_b TO app_role, disclosure_service;
GRANT USAGE ON SCHEMA vault  TO disclosure_service;
GRANT USAGE ON SCHEMA audit  TO app_role, disclosure_service;

-- ---------------------------------------------------------------- zone A

-- Five levels in the owner view (v5.1 §4.3). The fifth level, the owner's own
-- house, is a row in zone_a.property.
CREATE TABLE zone_a.area (
  area_id        text PRIMARY KEY,
  level          text NOT NULL CHECK (level IN ('MUNICIPALITY', 'ZIP', 'NEIGHBOURHOOD', 'STREET')),
  parent_id      text REFERENCES zone_a.area,
  name           text NOT NULL,
  dwelling_count integer NOT NULL CHECK (dwelling_count >= 0),
  synthetic_seed integer,          -- NULL = real data. Never NULL outside production.
  updated_at     timestamptz NOT NULL DEFAULT now()
);

-- Bitemporal (ADR-002): valid_from/valid_to is when it was true in the world,
-- recorded_at is when we learned it. A change closes the old version and
-- inserts a new one. History is never overwritten.
-- BFE -> address_id is one-to-many: one row per dwelling, never per property.
CREATE TABLE zone_a.property (
  address_id       uuid NOT NULL,
  bfe              text NOT NULL,
  municipality_id  text NOT NULL REFERENCES zone_a.area,
  zip_id           text NOT NULL REFERENCES zone_a.area,
  neighbourhood_id text REFERENCES zone_a.area,
  street_id        text REFERENCES zone_a.area,
  attrs            jsonb NOT NULL,
  owner_kind       text CHECK (owner_kind IN ('PRIVATE', 'COMPANY', 'ANDELSFORENING')),
  owner_cvr        text,
  quality_flags    jsonb NOT NULL DEFAULT '{}',
  lon              double precision,
  lat              double precision,
  valid_from       date NOT NULL,
  valid_to         date,
  recorded_at      timestamptz NOT NULL,
  synthetic_seed   integer,
  PRIMARY KEY (address_id, recorded_at)
);
CREATE INDEX property_bfe_ix    ON zone_a.property (bfe);
CREATE INDEX property_zip_ix    ON zone_a.property (zip_id) WHERE valid_to IS NULL;
CREATE INDEX property_street_ix ON zone_a.property (street_id) WHERE valid_to IS NULL;

GRANT SELECT ON ALL TABLES IN SCHEMA zone_a TO public_reader, app_role;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA zone_a TO ingest_role;

-- ---------------------------------------------------------------- zone B

-- v5.1: login is MitID. There is no e-mail identity and no e-mail column.
-- provider_sub is the broker's pseudonymous subject, never a CPR number.
CREATE TABLE zone_b.identity (
  identity_id    uuid PRIMARY KEY,
  provider       text NOT NULL CHECK (provider IN ('MITID_PRIVATE', 'MITID_ERHVERV')),
  pseudonym      text NOT NULL UNIQUE,
  provider_sub   text NOT NULL UNIQUE,
  assurance      text NOT NULL CHECK (assurance IN ('SUBSTANTIAL', 'HIGH')),
  cvr            text,
  household_key  text,
  created_at     timestamptz NOT NULL,
  erased_at      timestamptz,
  synthetic_seed integer
);

-- Session context set by the API for every request:
--   SELECT set_config('app.identity_id', '<uuid>', true);
CREATE FUNCTION zone_b.current_identity() RETURNS uuid
  LANGUAGE sql STABLE
  AS $$ SELECT nullif(current_setting('app.identity_id', true), '')::uuid $$;

ALTER TABLE zone_b.identity ENABLE ROW LEVEL SECURITY;
CREATE POLICY identity_own ON zone_b.identity
  FOR ALL TO app_role
  USING (identity_id = zone_b.current_identity())
  WITH CHECK (identity_id = zone_b.current_identity());

GRANT SELECT, INSERT, UPDATE ON zone_b.identity TO app_role;
-- disclosure_service needs the pseudonym-to-identity mapping to perform a reveal.
CREATE POLICY identity_disclosure ON zone_b.identity
  FOR SELECT TO disclosure_service
  USING (true);
GRANT SELECT ON zone_b.identity TO disclosure_service;

-- ---------------------------------------------------------------- vault

-- Contact data. Only disclosure_service may read it (invariant 4).
-- The write path (at MitID login) is defined in S3 and is not granted here.
-- No CPR column: ADR-005 is reopened in v5.1 and waits for the digital
-- mailbox supplier's answer. If CPR is required it is added here and nowhere else.
CREATE TABLE vault.identity_contact (
  identity_id    uuid PRIMARY KEY REFERENCES zone_b.identity,
  full_name      text NOT NULL,
  synthetic_seed integer
);
GRANT SELECT ON vault.identity_contact TO disclosure_service;
