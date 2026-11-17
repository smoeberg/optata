-- 0005_zone_a_least_privilege
--
-- A-01 / C-01: replace broad Zone A property-table reads with an explicit
-- public read model. This migration is a security-sensitive draft and
-- requires independent human DB/security review before production use.
--
-- public_reader needs the fields consumed by the public registry API, but
-- must not read owner_cvr or arbitrary future keys in attrs. app_role has no
-- current use case requiring direct Zone A property access.

CREATE VIEW zone_a.property_public
WITH (security_barrier = true)
AS
SELECT
  address_id,
  bfe,
  municipality_id,
  zip_id,
  neighbourhood_id,
  street_id,
  jsonb_strip_nulls(jsonb_build_object(
    'anvendelse', attrs -> 'anvendelse',
    'areal', attrs -> 'areal',
    'vaerelser', attrs -> 'vaerelser',
    'opfoerelsesaar', attrs -> 'opfoerelsesaar'
  )) AS attrs,
  owner_kind,
  quality_flags,
  valid_from,
  valid_to,
  recorded_at,
  synthetic_seed,
  superseded_at
FROM zone_a.property;

COMMENT ON VIEW zone_a.property_public IS
  'Allowlisted public registry read model. Never add owner_cvr or unreviewed attrs keys.';

-- Remove the table-level grants introduced by migration 0001. Ingest remains
-- separately privileged and retains its existing SELECT/INSERT/UPDATE grants.
REVOKE ALL PRIVILEGES ON TABLE zone_a.property
  FROM PUBLIC, public_reader, app_role;

-- Revoke any direct grants on the view before granting the single intended
-- consumer. This also makes the intended role matrix explicit.
REVOKE ALL PRIVILEGES ON TABLE zone_a.property_public
  FROM PUBLIC, app_role, disclosure_service, ingest_role;

GRANT SELECT ON TABLE zone_a.property_public TO public_reader;
