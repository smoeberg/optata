# Optata Area Intelligence v1.0

**Status:** Founder-approved product direction; detailed implementation design pending  
**Date:** 17 November 2026  
**Authority:** Subordinate to [Projectgrundlag v5.2](../Optata%20-%20Projektgrundlag%20v5.2.md) and [Architecture v2.1](../architecture/ARCHITECTURE.md). This document does not approve API/DB contracts or a data provider.

## 1. Purpose

Area Intelligence gives every supported geographic area a traceable profile of the facilities, services, population and socioeconomic characteristics available there. It is a distinct product capability connected to Property Discovery through shared geography.

- **Area Intelligence:** What is in this area, what services are available, and what characterizes the area?
- **Property Discovery:** What is this address/property, and what verified register facts and reports are available about it?

A user can move between an area profile and the properties/addresses located in or related to that area.

## 2. Geographic navigation and identity

The product navigation is:

**Region → Municipality → Area → City → District → Neighbourhood → Street → House/address**

This is not a strict administrative containment tree. Official geographies can overlap, use different definitions or change over time. Optata-defined areas can overlap official boundaries and one another.

### 2.1 Official geographies

Use official identifiers and geometries where available, including relevant types such as:
- Region
- Municipality
- Urban area
- Parish
- Postcode

The actual availability and statistical suitability of each geography must be verified per source/table.

### 2.2 Optata-defined geographies

Optata may define:
- Area
- District
- Neighbourhood

Each definition requires a documented boundary/membership method, geometry version, effective period, owner and change history. A neighbourhood must not be silently treated as an official statistical geography.

### 2.3 Streets and properties

Streets and addresses use authoritative address identity (e.g. DAR where licensed/available). Property identity (e.g. BFE) and cadastral identity are separate from address identity. A property may relate to multiple addresses; do not collapse these identities.

All geographic entities and relationships need stable namespaced identifiers, source references, geometry/geometry reference, validity and version history. Relations may be many-to-many and time-dependent.

## 3. Standard area profile

Every supported area should use the same profile structure, with explicit availability states where data does not exist:

1. Overview and boundary/map
2. Facility and service inventory
3. Population and household profile
4. Income and socioeconomic indicators
5. Education and employment indicators
6. Housing stock and housing-market indicators
7. Data quality, source coverage and update status

A profile must distinguish:
- Counts inside the selected area's boundary
- Counts within a distance or travel-time catchment from a selected point/address
- Facilities in intersecting/nearby areas

These are different measures and must not be mixed.

## 4. Facility and service inventory

The product direction is to map **30 primary facility/service categories** for each area. Users should be able to see a count per category, open a category to view the individual places on a map, and inspect a place profile.

The initial category families discussed are:
- Education and children
- Sport and leisure
- Shopping and retail
- Culture and experiences
- Health and care
- Nature, transport and infrastructure

The exact 30-category taxonomy, inclusion/exclusion rules, subcategories, canonical identity rules and source strategy remain to be specified and approved before implementation contracts are fixed. Illustrative examples from product discussions are not a final taxonomy.

Each facility record should support:
- Stable facility/place identity and possible duplicate/merge relationships
- Category and taxonomy version
- Name, address and coordinates/geospatial point
- Operational status and status evidence
- Source references and evidence snapshots/claims
- First-seen, observed-at and last-verified timestamps
- Verification/audit status and history
- Area memberships derived from versioned geometries
- Applicable source licence and permitted use

Counts must be reproducible from eligible facility records and a specific version of the area's geometry and taxonomy.

## 5. AI discovery, verification and audit

AI is used to discover candidates and maintain the registry, not to invent facts. Three logical roles are required:

### 5.1 Discovery

- Search permitted authoritative and supplementary sources.
- Find new facilities and possible changes, closures or relocations.
- Capture source URLs/identifiers, observation time and evidence.
- Propose candidate records or changes; do not publish directly.

### 5.2 Independent verification

- Independently check place identity, category, address/location and operational status.
- Consult source evidence directly rather than accepting the discovery agent's summary.
- Detect duplicates, mismatches and stale evidence.
- Record its own evidence and outcome.

### 5.3 Independent audit

- Review evidence quality, conflicts, category rules and geographic assignment.
- Check whether counts follow from approved records and boundaries.
- Escalate unresolved or high-impact conflicts for human review.
- Record a separate audit decision.

The verification and audit roles must not merely ask the same model to confirm the discovery agent's answer. Independence is an evidence/process requirement; it may later be implemented with separate agent instances, models or deterministic checks, as long as the controls are genuinely independent.

### 5.4 Publication states

Minimum conceptual states:

| State | Meaning | Included in public active count? |
|---|---|---|
| Verified | Supported by adequate evidence and passed required controls | Yes |
| Pending | Candidate awaiting sufficient verification | No |
| Disputed | Material source/evidence conflict | No |
| Inactive | Closure/inactivity supported by evidence | No; retain history |

Absence of a fresh confirmation is not proof of closure. Pending/disputed records must remain visible to authorized reviewers but excluded from public verified totals. High-impact or ambiguous changes require human review.

## 6. Evidence, provenance and freshness

Every published facility fact must be traceable to:
- Source/provider and source record or URL
- Source licence/terms and allowed purpose
- Observation/retrieval timestamp
- Evidence supporting the specific claim
- Verification and audit outcomes
- Validity/status period where known
- Change history and actor/agent role

Refresh cadence should be category- and source-specific. Do not repeatedly crawl everything on a fixed daily schedule if a source offers change feeds or a more appropriate update cadence. Respect rate limits, terms and source availability.

A source's last retrieval time is not necessarily the date the source data itself was updated. Store these separately.

## 7. Statistics and socioeconomic profile

Potential indicators include:
- Population and households
- Income and disposable income
- Income distribution
- Employment and socioeconomic status
- Education
- Housing type, tenure and housing stock

Danmarks Statistik/Statistikbanken is a candidate primary source for official statistical indicators. Exact tables, geographic levels, variables, definitions, release dates, revisions, disclosure rules and terms must be checked per indicator before integration.

Each statistic must retain:
- Source and table/indicator code
- Definition and population/universe
- Geographic type and stable geographic identifier
- Period/reference year
- Unit and calculation (e.g. mean, median, decile)
- Retrieval timestamp and source revision
- Disclosure/suppression state and usage rights

Only publish a statistic at a geographic level actually supported by the source. Do not copy municipality figures down to a city, neighbourhood, street or house and present them as local observed facts. Modelled estimates, if ever introduced, must be clearly labelled and accompanied by methodology and uncertainty. Apply source disclosure rules and avoid small-cell inference.

## 8. Data sources and providers

Candidate sources may include official Danish registers, statistical products, municipal open data/GIS, transport datasets and provider APIs such as BoligIQ or GrunddataAPI. No provider is selected by this specification.

Before integration, establish:
- API coverage and exact fields/identifiers
- Source-level provenance and freshness
- Licence, caching, retention, derived-data and redistribution rights
- Commercial display/use rights
- Rate limits, SLA, versioning and pricing
- Exit strategy and ability to replace the provider

Provider adapters must map into Optata-owned canonical contracts. Vendor response formats and vendor IDs must not become the domain model's sole identity system.

## 9. Architecture boundaries

Area Intelligence is a distinct Zone A capability for public/licensed geography, facilities and statistics, subject to classification of each data category. It should integrate with the registry and reports modules through explicit contracts.

Conceptual components:
- Area Registry and Geometry
- Facility Taxonomy and Facility Registry
- Source and Licence Registry
- Discovery/Verification/Audit workflow
- Area Aggregation Engine
- Socioeconomic/Statistics Adapter and Profile
- Area Profile and Facility Detail read APIs

Property Discovery reuses geographic identities and relations but remains a distinct product capability. Zone C exports and commercial aggregate products require separate aggregation, licensing and re-identification review.

## 10. Quality and release rules

- Synthetic fixtures are the default during development.
- No AI-generated or unverified facility is presented as a fact.
- No pending/disputed facility contributes to public counts.
- No statistic is shown below its supported geographic resolution.
- No data is ingested or redistributed without documented rights.
- Public release requires source coverage, quality, security, privacy and licence review.
- Every displayed count/profile must be reproducible and explainable from underlying approved records and source versions.

## 11. Open implementation decisions

1. Final taxonomy of 30 categories and inclusion/exclusion rules.
2. Canonical facility identity and deduplication rules.
3. Exact official geography datasets and Optata neighbourhood boundary methodology.
4. Data-source/provider selection and commercial licensing.
5. Refresh policy, confidence/evidence thresholds and human-review thresholds.
6. API, database and event contracts.
7. Whether/how travel-time catchments are calculated and licensed.
8. Statistical tables and the exact geographic resolution available per indicator.
9. Product UI, profile layout and ranking/sorting behavior.

These details require separate Issues and review. This document records the approved product direction; it does not state that Area Intelligence is implemented or production-ready.
