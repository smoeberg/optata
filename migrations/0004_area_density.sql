-- 0004_area_density
--
-- DRAFT. Written by an AI assistant. Migrations are a red field: a human owner
-- must review this file before anything relies on it (projektgrundlag §7.1).
--
-- Density per area on all four area levels. Internal figure: it holds raw
-- counts, including counts below 5, so it lives in zone B and is granted to
-- no application role. The public, k-anonymous version belongs to zone C and
-- is not built here.
--
-- Counting rules (v5.1 §4.2 and §4.3):
--   * Buyers are counted, not orders: distinct household_key.
--   * An AREA order counts in every area it overlaps: the area itself, the
--     areas it lies inside, and the areas inside it. A buyer looking in a
--     whole postal area is demand on every street in it.
--   * An ADDRESS order counts in the postal area and municipality of the
--     address. It never counts on street or neighbourhood level, so an owner
--     cannot work out that someone wants the house next door.
--   * Only ACTIVE orders count. `verified_buyers` further requires VERIFIED.
--
-- Refreshed after ingestion and when orders change. Never computed in a
-- request path.

CREATE MATERIALIZED VIEW zone_b.area_density AS
WITH RECURSIVE lineage (area_id, ancestor_id) AS (
  SELECT area_id, area_id FROM zone_a.area
  UNION ALL
  SELECT l.area_id, a.parent_id
  FROM lineage l
  JOIN zone_a.area a ON a.area_id = l.ancestor_id
  WHERE a.parent_id IS NOT NULL
),
overlap AS (
  -- the order's area, and every area it lies inside
  SELECT o.household_key, o.level, l.ancestor_id AS area_id
  FROM zone_b.orders o
  JOIN lineage l ON l.area_id = o.area_id
  WHERE o.scope = 'AREA' AND o.status = 'ACTIVE'
  UNION
  -- every area inside the order's area
  SELECT o.household_key, o.level, l.area_id
  FROM zone_b.orders o
  JOIN lineage l ON l.ancestor_id = o.area_id
  WHERE o.scope = 'AREA' AND o.status = 'ACTIVE'
  UNION
  SELECT o.household_key, o.level, x.area_id
  FROM zone_b.orders o
  JOIN zone_a.property p
    ON p.address_id = o.address_id AND p.superseded_at IS NULL AND p.valid_to IS NULL
  CROSS JOIN LATERAL (VALUES (p.zip_id), (p.municipality_id)) AS x (area_id)
  WHERE o.scope = 'ADDRESS' AND o.status = 'ACTIVE'
),
counted AS (
  SELECT area_id,
         count(DISTINCT household_key) FILTER (WHERE level = 'VERIFIED') AS verified_buyers,
         count(DISTINCT household_key) AS active_buyers
  FROM overlap
  GROUP BY area_id
)
SELECT a.area_id,
       a.level,
       a.dwelling_count,
       a.density_frozen,
       coalesce(c.verified_buyers, 0) AS verified_buyers,
       coalesce(c.active_buyers, 0)   AS active_buyers,
       CASE
         WHEN a.density_frozen OR a.dwelling_count = 0 THEN NULL
         ELSE round(1000.0 * coalesce(c.verified_buyers, 0) / a.dwelling_count, 1)
       END AS verified_per_1000
FROM zone_a.area a
LEFT JOIN counted c USING (area_id);

CREATE UNIQUE INDEX area_density_pk ON zone_b.area_density (area_id);

REVOKE ALL ON zone_b.area_density FROM PUBLIC, public_reader, app_role, disclosure_service,
  ingest_role;
