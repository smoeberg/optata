# Danish nationwide data-source inventory — Area Intelligence

**Status:** Research catalogue v0.1 — evidence-backed starting inventory, not a provider decision  
**Checked:** 17 November 2026  
**Repository baseline inspected:** `main` — `1a095f58685761629b47a572f24c703fdb9813f7`  
**Scope:** Nationwide Denmark; actual data-source/API capability, geography, access, rights, freshness and Mistral access pattern.  
**Non-scope:** Database schema, migrations, production ingestion, adapter implementation, final facility taxonomy, vendor selection or changes to accepted product/architecture decisions.

> **Important reading rule:** “Nationwide source” means the source is a national register/service or national statistical product. It does not mean every category has complete, current, point-level coverage in every Danish locality. “Unknown” means the primary source documentation or sample response inspected here did not establish the claim. No legal conclusion is made from a dataset landing page.

## 1. Executive summary

### 1.1 What is actually available

| Domain | Strongest identified source | Verified interface / evidence | Nationwide assessment | Recommended access pattern |
|---|---|---|---|---|
| Address identity | Klimadatastyrelsen / DAR via Adressevælger and Datafordeler | Adressevælger phonetic search and ID lookup; DAR GraphQL, file download and WFS; sample DAR GraphQL fields below | National authoritative address register | Live for user-entered address resolution; synchronize reference/relationship data if bulk joins or reproducible history are needed |
| Administrative geography | DAGI via Datafordeler / Dataforsyningen | Datafordeler GraphQL and WFS; Dataforsyningen geodata services | National authoritative geography; each geography type has its own identifiers/validity | Synchronize boundaries and versions; live lookup for individual identifiers |
| Buildings / dwellings | BBR via Datafordeler | BBR GraphQL v3, WFS and file download; entity schema is public | National register; coverage is register-defined, not a facility POI inventory | Synchronize for area counts, history and large-scale analysis; live lookup for individual properties |
| Population / households / income / employment / education statistics | Danmarks Statistik, Statistikbanken | `/v1/subjects`, `/v1/tables`, `/v1/tableinfo`, `/v1/data` | National statistical tables; geographic levels vary table by table | Query live for small, selected table slices; cache/synchronize selected indicators for repeated profiles and revision tracking |
| Schools / education institutions | STIL Institutionsregister | Nationwide CSV/XLSX extracts; institution types, address, postcode, municipality, region, coordinates, institution no., active code, CVR/P-no. | Strong evidence of national coverage for registered education institutions; not all informal learning/care settings | Bulk snapshot / scheduled refresh; web service access requires connection and is updated daily |
| Planning / land use | Plandata.dk | WFS/WMS/WMTS; WFS exposes plan geometries and attributes | National platform for municipal plans and state planning layers; coverage depends on plan layer and municipal reporting | Live spatial query for bounded areas; synchronize selected layers and deltas for repeated analysis |
| Environment / nature | Danmarks Miljøportal; GEUS; Datafordeler geodata | DMP web services include WMS/WFS and domain services; GEUS APIs/WFS; Datafordeler terrain/geodata | National platforms, but layer-specific coverage and update cycle must be inspected | Spatial layer sync for profiles; live WMS for visualization, not as a fact store |
| Weather / climate | DMI Open Data | REST OGC Features / EDR and STAC services for observations, ocean, lightning, climate, radar and forecast | National observation/model coverage; spatial and temporal resolution varies by collection | Live for current conditions/forecasts; synchronize historical or repeated area indicators |
| Businesses / retail / service firms | CVR via Datafordeler / Erhvervsstyrelsen | CVR GraphQL and downloads; non-person entities publicly available, CVRPerson restricted | National register of registered businesses; not a complete inventory of public-facing premises or open shops | Bulk/delta sync of relevant entities and production units; live lookup for a known CVR |
| Public transport | Rejseplanen API 2.0 (candidate) | Official API 2.0 documented as API-key access; detailed endpoint/field sample not inspected in this pass | Intended national public-transport journey data; coverage and licence must be confirmed against current API agreement | Live for journey/departure queries; synchronize static stops/routes only if agreement and feed terms permit |
| General facility discovery | OpenStreetMap (supplementary, community data) | Overpass read-only query service; OSM data under ODbL | Broad geographic reach, but completeness/accuracy vary by category and locality | Bulk extracts/diffs or a contracted provider for systematic coverage; public Overpass only for low-volume research, not production dependency |

### 1.2 Main finding about the 30 facilities

No single authoritative Danish public API was identified that supplies all 30 facility/service categories with national, point-level coverage, common identifiers, uniform opening/status fields and one licence.

The strongest current pattern is a **multi-source inventory**:
- authoritative registers for addresses, buildings, education institutions and businesses;
- selected national agency / municipal layers for specific services and infrastructure;
- OSM and/or licensed POI providers as discovery supplements, never silently treated as official truth;
- source-specific evidence and independent verification for status and counts.

The 30 rows in §6 are a **working coverage checklist** built from the six category families in the approved product direction. They are not an approved taxonomy. Final category boundaries and inclusion rules remain a founder decision.

### 1.3 Important current-date finding

The Dataforsyningen GSearch documentation says GSearch closes at the end of October 2026. As of this inventory date (17 November 2026), it must not be assumed to remain a production option. Klimadatastyrelsen's new Adressevælger is documented as its replacement for address autocomplete/search. Its token requirement, once-daily data refresh and no-current-rate-limit statement are documented; usage governance is expected to evolve. See §3.1.

## 2. Source inventory — actual interfaces and fields

### 2.1 DAR / Adressevælger — authoritative address identity

**Owner:** Klimadatastyrelsen is the data/model authority for DAR; municipal address authorities create and maintain addresses in DAR.  
**Distributor:** Datafordeleren and Klimadatastyrelsen's Adressevælger.  
**Role:** Primary authoritative address identity; not a property or cadastral identity.

**Documented interfaces**
- Adressevælger phonetic search and ID lookup:
  - Search for addresses / access addresses / named roads: documented at [Adressevælger — phonetic search](https://confluence.kds.dk/pages/viewpage.action?pageId=244318431).
  - ID lookup patterns: `https://adressevaelger.dk/husnumre/{id}?token=...` and `https://adressevaelger.dk/adresser/{id}?token=...` ([ID lookup documentation](https://confluence.kds.dk/pages/viewpage.action?pageId=246743156)).
  - Search response includes a result `id`, result `type` and display/title; examples also show road name, postcode, postcode district and number of house numbers.
  - Phonetic search returns the address/access-address designation and ID; additional fields require an ID lookup or a Datafordeler query.
- Datafordeler DAR GraphQL:
  - Endpoint pattern: `https://graphql.datafordeler.dk/DAR/{version}`; schema: `https://graphql.datafordeler.dk/DAR/{version}/schema`.
  - Example entity: `DAR_Adresse`; example fields inspected in official transition documentation: `adressebetegnelse`, `bygning`, `id_lokalId`, `registreringFra`, `registreringTil`, `status`, `virkningFra`, `virkningTil`; connection pagination exposes `pageInfo.endCursor` and `pageInfo.hasNextPage`.
  - Other documented entities include Adresse, Adressepunkt, Husnummer, NavngivenVej, NavngivenVejKommunedel, NavngivenVejPostnummer, NavngivenVejSupplerendeBynavn, Postnummer and SupplerendeBynavn.
- Datafordeler file download and WFS are also listed for DAR; file download supports JSON/CSV, WFS exposes register entities as GML/GeoJSON.

**Geographic / temporal coverage:** National authoritative register. DAR uses bitemporal validity/registration fields. Adressevælger states that new/changed addresses and house numbers are searchable the day after the DAR change. This is not a promise of instantaneous consistency.

**Access / price / rights**
- Adressevælger: mandatory `token`; current FAQ says no rate limit is introduced at present and data updates daily. No commercial price is stated on the inspected docs. Confirm token issuance, terms and operational limits with Klimadatastyrelsen before production.
- Datafordeler GraphQL and file downloads: API key or OAuth; create a user and IT system in Datafordeler Administration. Datafordeler documents register-specific terms. DAR page states Klimadatastyrelsen holds IP rights and determines terms of use. No price was stated in the pages inspected.
- Do not infer unrestricted bulk retention/redistribution solely from search being publicly reachable.

**Recommendation:** Live address autocomplete/resolve via Adressevælger; use the resulting authoritative DAR identifier to join other registers. For national reference, historical reproducibility or large area analysis, use approved Datafordeler bulk/delta facilities rather than issuing one live call per address.

**Critical migration note:** Do not build on legacy DAWA/GSearch paths without confirming retirement. GSearch docs state end-of-October-2026 closure; use the current Adressevælger docs and validate the live production contract.

Evidence:
- [Adressevælger overview and refresh](https://confluence.kds.dk/pages/viewpage.action?pageId=234782998)
- [Adressevælger FAQ](https://confluence.kds.dk/display/ADV/FAQ)
- [Phonetic search](https://confluence.kds.dk/pages/viewpage.action?pageId=244318431)
- [ID lookup](https://confluence.kds.dk/pages/viewpage.action?pageId=246743156)
- [DAR GraphQL schema and rights](https://datafordeler.dk/dataoversigt/danmarks-adresseregister-dar/dar-graphql-skema/)
- [DAR entities / services](https://datafordeler.dk/dataoversigt/)

### 2.2 DAGI / official geographies and Dataforsyningen

**Owner:** Klimadatastyrelsen / relevant register authorities.  
**Distributor:** Datafordeleren and Dataforsyningen.  
**Role:** Official geography, administrative areas and geospatial reference. It does not supply Optata-defined neighbourhood boundaries.

**Documented interfaces**
- Datafordeler GraphQL registry endpoint pattern: `https://graphql.datafordeler.dk/DAGI/{version}`; general GraphQL schema and entity pattern is documented for DAR/BBR/DAGI.
- Datafordeler WFS/WMS and file download are listed for relevant geographic registers.
- Dataforsyningen provides WMS/WFS and other geodata services. The older GSearch API endpoint was `https://api.dataforsyningen.dk/rest/gsearch/v2.0/{resource}`, but its own documentation says closure end October 2026; do not use as a new dependency.
- Dataforsyningen's GSearch docs show its former resources included address, house number, parcel, municipality, postcode, region, parish and place name. This is evidence of former resource coverage, not evidence that the service remains available now.

**Fields / spatial facts actually documented:** JSON responses include an authoritative `id`, `visningstekst`, and object geometry as GeoJSON in EPSG:25832; address/house-number results also expose `geometri` and `vejpunkt_geometri`. Those fields refer to the retired GSearch response documentation and must be revalidated against the replacement service before implementation.

**Coverage / cadence:** National authoritative geography. Historical GSearch docs stated daily refresh for address/house number/parcel and weekly for administrative geographies; those cadence values must not be carried over to a replacement API without confirmation.

**Rights / price:** Datafordeler and Dataforsyningen each publish service/data-specific terms. No single universal licence or commercial price can be inferred for every layer. Check metadata and terms per dataset/layer.

**Recommendation:** Synchronize official boundary geometries and their effective/version dates for repeatable area aggregation; use live API for individual lookups. Preserve separate identifiers/namespaces for municipality, postcode, urban area, parish and other official geographies. Optata-defined areas require a separately approved methodology.

Evidence:
- [Datafordeler GraphQL register list](https://confluence.kds.dk/pages/viewpage.action?pageId=193921171)
- [Datafordeler access and service types](https://datafordeler.dk/vejledning/)
- [Dataforsyningen API reference / GSearch retirement notice](https://docs.dataforsyningen.dk/)
- [Datafordeler data overview](https://datafordeler.dk/dataoversigt/)

### 2.3 BBR — buildings, units and housing stock

**Owner / register authority:** BBR is the national building and dwelling register; Datafordeler distributes it. The Datafordeler overview identifies Vurderingsstyrelsen as register authority on the BBR GraphQL service page.  
**Distributor:** Datafordeleren.  
**Role:** Building/property facts and housing stock, not a complete list of public facilities.

**Documented interfaces**
- BBR GraphQL v3:
  - Endpoint: `https://graphql.datafordeler.dk/BBR/v3`.
  - Schema: `https://graphql.datafordeler.dk/BBR/v3/schema`.
  - Access: API key, OAuth Shared Secret or OAuth certificate.
  - Entity families: `BBRSag`, `Bygning`, `BygningEjendomsrelation`, `Ejendomsrelation`, `Enhed`, `EnhedEjendomsrelation`, `Etage`, `FordelingAfFordelingsareal`, `Fordelingsareal`, `Grund`, `GrundJordstykke`, `Opgang`, `Sagsniveau`, `TekniskAnlæg`.
- BBR file download: pre-generated entity downloads in JSON/CSV.
- BBR WFS entities: GeoJSON/GML; register tables/entities are exposed as layers.

**Fields verified in official object documentation**
- `Bygning`: `byg007Bygningsnummer`, `byg021BygningensAnvendelse`, `byg024AntalLejlighederMedKøkken`, `byg025AntalLejlighederUdenKøkken`, `byg026Opførelsesår`, `byg027OmTilbygningsår`, `byg029DatoForMidlertidigOpførtBygning`, `byg030Vandforsyning`.
- The `Enhed` object is a physically separate functional unit in a building, e.g. dwelling or commercial premises. Exact current field list must be read from the versioned GraphQL schema/object catalogue before mapping fields.

**Temporal / geography:** Bitemporal register; GraphQL supports cursor pagination and registration/effect time. National register; query filters may include municipality code as demonstrated in official transition material. Coverage/quality reflects legal registration obligations and municipal register quality; do not treat every real-world building attribute as equally complete.

**Rights / access:** API key/OAuth; Datafordeler terms apply. Data may contain person-identifiable property information; Datafordeler explicitly places legal compliance responsibility on the recipient. No universal service price stated in inspected docs. Review the BBR terms and data classification before use.

**Recommendation:** Synchronize selected entities for national housing-stock and area aggregation; live GraphQL for a known property/identifier. Keep BBR facts distinct from DAR address identity and MAT cadastral identity.

Evidence:
- [BBR GraphQL service and entities](https://datafordeler.dk/dataoversigt/bygnings-og-boligregistret-bbr/bbr-graphql/)
- [BBR GraphQL v3 endpoint and entity documentation](https://confluence.kds.dk/pages/viewpage.action?desktop=true&macroName=display-metadata&pageId=219513710)
- [BBR object catalogue — Bygning and fields](https://grunddatamodel.datafordeler.dk/objekttypekatalog/Bygninger%20og%20boliger/Bygning.html)
- [BBR object catalogue — Enhed](https://grunddatamodel.datafordeler.dk/objekttypekatalog/Bygninger%20og%20boliger/Enhed.html)
- [Datafordeler access methods](https://datafordeler.dk/vejledning/)

### 2.4 Danmarks Statistik — population, households, income, labour and education indicators

**Owner / publisher:** Danmarks Statistik.  
**Distributor:** Statistikbanken API and bulk download.  
**Role:** Authoritative official statistical indicators; geography is table-specific.

**Actual API endpoints**
- Base: `https://api.statbank.dk`.
- `POST /v1/subjects` — subject hierarchy.
- `POST /v1/tables` — table catalogue.
- `POST /v1/tableinfo` — table metadata, variables and value codes; e.g. `{"table":"folk1c"}`.
- `POST /v1/data` — selected table values; requires table, format and selected variable codes/values.
- Responses for metadata can be JSON or XML; data supports CSV, JSON-stat, PX, DSTML, XLSX, HTML and streaming formats including BULK and SDMX.

**Fields / definitions:** API metadata provides table title, units, variables, value codes and notes. Data rows are observations with selected dimensions (e.g. area, sex, age, time) and values. The exact field/dimension set is table-specific and must be inspected through `tableinfo` for each selected indicator; there is no single universal population/income schema.

**Geography:** The API can return national and subnational data where a table includes that geography. The official docs explicitly show that omitting the area variable returns national data; a sample includes area codes for whole Denmark and selected municipalities. This does **not** establish postcode, parish, neighbourhood or street availability for every indicator.

**Cadence / limits:** Table updates differ; `tables` can filter on tables updated within the last N days. Ordinary (non-bulk) output currently has a documented cap of 1,000,000 cells; streaming formats avoid that cap. Read table metadata and update catalogue rather than assuming a common monthly/yearly cadence.

**Rights / price:** Danmarks Statistik states Statistikbanken and DST website statistical data may be used commercially and non-commercially with source attribution, corresponding to CC BY 4.0. A separate StatHost product has pricing; it is not needed for normal API use.

**Recommendation:** Discover tables/metadata programmatically, then curate a versioned indicator list. Query selected current observations live when response size is small; cache/synchronize profile indicators and metadata to support repeatable profiles, change tracking and reproducibility. Keep source reference period separate from retrieval time. Never downscale a municipality statistic to a neighbourhood.

Evidence:
- [Statistikbanken API official documentation](https://www.dst.dk/da/Statistik/hjaelp-til-statistikbanken/api)
- [English licence statement](https://www.dst.dk/en/Statistik/hjaelp-til-statistikbanken/api)

### 2.5 STIL Institutionsregister — education institutions

**Owner / responsible authority:** Ministry of Children and Education; register maintained through STIL, with institution/municipality/region submissions.  
**Distributor:** Institutionsregister website and STIL web services.  
**Role:** Strong nationwide directory for registered education institutions; not a general childcare/children's-services register.

**Actual extract and fields inspected**
- Current extract page offered CSV and Excel; at inspection it displayed 4,970 institutions, with filters for current/historical records and active/inactive status.
- Available columns include: institution number, main institution, institution name, address, postcode, postcode district, road code, municipality, region, latitude, longitude, institution manager, email, website, phone, entity type, institution type, education level, ministry, CVR number, P-number, owner code, administrative municipality, active code, update date, creation month and closure date.
- Institution types include primary schools, private schools, special schools, boarding schools, upper secondary, vocational, higher education, universities, adult education and other listed education providers.

**Cadence / access:** The data-extract facility can download current or historical records. The STIL web-service documentation says production data updates once daily and that system-to-system users must be connected/subscribed. Exact web-service endpoints and authentication contract were not inspected in this pass; do not invent them. The extract page shows a current nationwide dataset but is not evidence of a stable public REST API.

**Rights / price:** No explicit commercial licence, price or retention/redistribution terms were found on the inspected extract page. Obtain written terms for commercial display, caching and redistribution before ingestion. Web-service access requires onboarding/connection.

**Recommendation:** Use scheduled CSV extract or approved web service for the education-institution inventory. Record institution number, P-number and active/closure status; do not assume the register covers all nurseries, informal tutoring, sports clubs or cultural institutions.

Evidence:
- [Institutionsregister data extract and fields](https://institutionsregisteret.stil.dk/dataudtraek)
- [Register overview / responsible authority](https://institutionsregistret.stil.dk/)
- [STIL web-service access and daily update](https://viden.stil.dk/spaces/OFFINSTREG/pages/113410159/Institutionsregistrets+webservices)

### 2.6 CVR — businesses and production units

**Owner / register authority:** Erhvervsstyrelsen.  
**Distributor:** Datafordeleren (official), plus commercial resellers.  
**Role:** Legal business identity, branch and production-unit reference; not a reliable proof that a storefront is open to the public or currently operating at a specific address.

**Actual interface**
- Datafordeler CVR GraphQL entity service: endpoint pattern `https://graphql.datafordeler.dk/CVR/{version}`; API key/OAuth; public entities are exposed except restricted `CVRPerson`.
- CVR file downloads are listed through Datafordeler.
- CVR register documentation states only `CVRPerson` requires a separate access request with MitID Erhverv/OAuth. Other CVR entities are not access restricted.
- The CVR data model and current version/schema must be inspected per entity before field mapping. The API supports entity-based GraphQL; no single generic REST endpoint for all CVR is established by the sources inspected.

**Fields:** Company and production-unit identifiers, names, legal/operating status, addresses, industry codes and temporal/history attributes are plausible target fields, but exact GraphQL field names and allowed entity fields must be checked in the current schema before implementation. Do not copy field names from a commercial reseller as if they were the official schema.

**Coverage / cadence:** National register of registered legal entities and production units. Does not include every informal place/service and does not independently validate premises open to consumers. Exact change-feed/file cadence is service/entity-specific and was not confirmed in this pass.

**Rights / price:** Official Datafordeler terms and personal-data rules apply; CVRPerson restricted. Commercial reseller prices are provider-specific and not a substitute for source rights. No official API price was established in this pass.

**Recommendation:** Use CVR for identity, industry classification and candidate business premises; join production units to DAR address identity. Verify that a specific premises exists and is active before treating it as a facility. Avoid person/owner data unless separately approved.

Evidence:
- [Datafordeler CVR access conditions](https://datafordeler.dk/vejledning/brugeradgang/anmodning-om-adgang/det-centrale-virksomhedsregister-cvr/)
- [Datafordeler CVR / register overview](https://datafordeler.dk/dataoversigt/)

### 2.7 Plandata.dk — planning and zoning

**Owner / authority:** Plan- og Landdistriktsstyrelsen for its own layers; municipalities are data owners for municipal planning submitted to Plandata.  
**Distributor:** Plandata.dk web services.  
**Interfaces:** WFS (GML vector features and attributes), WMS (rendered map), WMTS (tiles); a separate REST API exists for plan submission by approved system-to-system users. The public WFS is the relevant read interface, not the submission API.
- WFS layers include local plans, municipal plan frameworks/guidelines, rural-zone permissions, heating, wastewater and zoning layers; statuses include proposal, adopted and cancelled variants.
- Official documentation says services read directly from Plandata's database and display current published data.
- Delta extraction can use `datoopdt` or `oprettet`, but publication/effective dates can lag internal updates; robust sync needs both plan publication/effective-date and modification-date logic.

**Geography / cadence:** National platform; data is municipality-reported. Layer coverage and completeness vary by plan type and local submission. Live services reflect current published state; no single universal update schedule is documented.

**Rights / price:** CC BY 4.0 applies to municipal planning layers and Plan- og Landdistriktsstyrelsen-owned layers. Other authority layers shown in the map may have different terms; inspect per-layer metadata. No service price stated.

**Recommendation:** Use live WFS with area/polygon filters for ad hoc planning queries; synchronize selected layers and changes for repeatable profile/market analysis. Store layer name, status, publication/effective dates and source municipality.

Evidence:
- [Plandata web services and licence terms](https://www.plandata.dk/webservices/introduktion-til-webservices)
- [Plandata WFS layers and delta guidance](https://www.plandata.dk/webservices/introduktion-til-webservices/wfs)

### 2.8 Environment, nature and geology

**Owners / distributors:** Danmarks Miljøportal (cross-authority environmental portal); GEUS for geological datasets; relevant environmental agencies and municipalities for individual source layers.
**Interfaces verified at high level:** Danmarks Miljøportal documents WMS/WFS plus REST/SOAP and domain-specific system-to-system services. GEUS offers data/maps APIs and WFS services for boreholes, groundwater and subsurface data. Exact per-layer endpoints, feature schemas, licences and refresh schedules were not sampled here.
**Coverage:** National portals, but layer coverage and update cycles are layer-specific. Environmental contamination, protected nature, water, geology, air and noise should be inventoried as distinct datasets.
**Rights / price:** No universal licence or price; inspect each layer's metadata and source owner. A map portal can aggregate data under different licences.
**Recommendation:** Use WMS for visualization only. For facts, counts or spatial analysis, use WFS/REST/download of the actual feature layer, preserve source-layer metadata, and synchronize when repeatability is required.

Evidence:
- [Danmarks Miljøportal API overview](https://danmarksmiljoeportal.dk/)
- [GEUS data and maps](https://www.geus.dk/produkter-ydelser-og-faciliteter/data-og-kort)

### 2.9 DMI — weather, climate and ocean

**Owner / publisher:** Danish Meteorological Institute (DMI).  
**Interfaces verified:** REST OGC API Features for meteorological observations, oceanographic observations, lightning and climate; STAC for radar and forecast files; EDR for subset forecast data. Documentation lists observation, ocean, lightning, climate, radar and forecast collections.
**Coverage:** National / Danish domain and relevant surrounding seas, with each collection's spatial/time coverage specified separately. Historical observations and forecasts are different products.
**Cadence:** Collection-specific. Use API collection metadata and product release notes; do not assume one universal interval.
**Rights / price:** DMI describes open data as free/open access; review current terms of use and attribution for the selected dataset.
**Recommendation:** Query live for current weather/forecast context; synchronize selected climate/historical observations if profiles or comparisons need stable, repeatable values. Weather is contextual, not a substitute for facility or socioeconomic evidence.

Evidence:
- [DMI APIs](https://www.dmi.dk/friedata/dokumentation/apis)
- [DMI API basics and standards](https://www.dmi.dk/friedata/dokumentation/basics)
- [DMI English open-data documentation / terms](https://www.dmi.dk/friedata/dokumentation-paa-engelsk)

### 2.10 Rejseplanen — public transport

**Owner / operator:** Rejseplanen / public transport authorities and operators.  
**Interface candidate:** Official Rejseplanen API 2.0 is documented as an API-key service. Exact current endpoints, response fields, feed licence, caching rights, quotas, price and national operator coverage were not verified against the current primary API documentation in this pass.
**Recommendation:** Candidate for live journey planning, departures and access-time calculation. Do not ingest or publish static stop/route data until the current API agreement/feed terms and permitted caching are confirmed. For repeatable access metrics, a licensed static feed and explicit routing methodology are required.

Evidence lead:
- [Rejseplanen API 2.0 overview](https://www.rejseplanen.dk/)

### 2.11 OpenStreetMap — supplementary POI discovery

**Owner / publisher:** OpenStreetMap Foundation and contributor community; not a Danish public authority.  
**Interface:** Overpass read-only API, e.g. `https://overpass-api.de/api/interpreter`; query language filters OSM objects by tags and area/geometry. National extracts and replication diffs are alternatives for systematic use.
**Fields:** OSM objects expose element type/id, tags and geometry; category-specific tags are community-defined and inconsistent. Do not treat OSM tags as a stable government taxonomy or a complete source of opening status.
**Coverage:** Broad national reach, but completeness varies significantly by category and locality. It is a discovery/supplementary layer, not authoritative evidence of all facilities.
**Rights:** OSM data is ODbL 1.0; attribution required and share-alike/database obligations can apply to derivative databases. OSM map tiles have separate usage conditions and are not an unrestricted commercial tile API. Legal review is required before combining or redistributing OSM-derived databases with differently licensed data.
**Operational limits:** Public Overpass instances are community resources, may be overloaded and have their own usage policies. The main global instance publishes a rough low-volume usage expectation; it is not a production SLA. For substantial/high-frequency use, use regional extracts/diffs, self-hosting or a contracted provider.
**Recommendation:** Use as candidate discovery and gap-finding. Never let a public Overpass endpoint be the sole production dependency for nationwide coverage.

Evidence:
- [OSM Foundation licence FAQ](https://osmfoundation.org/wiki/Licence/Licence_and_Legal_FAQ)
- [OSM copyright / licence](https://www.openstreetmap.org/copyright)
- [Overpass API instances and usage notes](https://wiki.openstreetmap.org/wiki/Overpass_API)
- [OSM Foundation API policy](https://operations.osmfoundation.org/policies/api/)

## 3. Address, property and geography joins

The following identity distinctions are mandatory:
- **DAR address ID** — address identity.
- **DAR house-number ID** — access/placement identity for the house number.
- **BFE / EBR identity** — property/real-estate identity and property relationships.
- **MAT identity** — cadastral parcel identity.
- **DAGI geography IDs** — official administrative/geographic units.
- **CVR number / P-number** — legal entity / production-unit identity.
- **STIL institution number** — education institution identity.
- **OSM element ID** — source-local community map object identity only.

A business may have multiple production units and premises. A BFE can relate to multiple addresses. A facility may be located at an address without being identical to a business or property. No one identifier should be overloaded as the universal facility key.

## 4. Nationwide geography coverage matrix

| Geography / resolution | DAR | DAGI / Dataforsyningen | BBR | Danmarks Statistik | STIL | Plandata |
|---|---|---|---|---|---|---|
| National / Denmark | Address register national | National official layers | National register | Many national totals | Nationwide extract | National platform |
| Region | Address linked to geography | Official region identity/geometry | Can filter/join through geography | Available in selected tables | Region column/filter | Region may be derived spatially |
| Municipality | Address/house number can be related | Official municipality identity/geometry | Municipality-based filtering in examples | Common in many tables; table-specific | Municipality column/filter | Municipality-owned planning layers |
| Postcode | DAR has postcode relationships | Official postcode geography | Join via address/geography | Only where table includes postcode | Postcode field | Not a universal planning dimension |
| Urban area | Not a DAR core unit | Official geography where supplied | Spatial join needed | Table-specific; not guaranteed | Not a standard universal field | Spatial overlay |
| Parish | Not a DAR core unit | Official geography where supplied | Spatial join needed | Table-specific | Not standard | Spatial overlay |
| Street / house | Authoritative street, house number and address IDs | Geometry/reference services | Building/unit relations may connect via identifiers | Rarely a published statistical resolution | Institution address | Plan polygon overlay |
| Optata area / district / neighbourhood | No native concept | No native concept | Spatial overlay after approved boundary | No assumption of matching statistical level | Spatial overlay | Spatial overlay |

**Conclusion:** National coverage is strong for core addresses, buildings and official geography. Fine-grained statistical coverage is indicator-specific. Optata-defined areas are not an authoritative national register and require an explicitly versioned boundary/membership method. A nationwide profile can be generated only where each metric's actual geography supports the requested area.

## 5. Live query versus synchronization

| Data need | Live query | Synchronize / bulk | Reason |
|---|---|---|---|
| User address autocomplete | Yes — Adressevælger | Optional address reference snapshot | Low-latency user input; address updates next day according to docs |
| Address-to-BBR/MAT/property joins | Targeted GraphQL lookup | Yes for broad joins/history | Many joins and historical reproducibility |
| Official area boundaries | Limited single-ID lookup | Yes | Spatial aggregation requires stable geometry/version |
| BBR dwelling/building counts | Targeted property lookup | Yes | Repeated nationwide/area aggregation is not efficient as per-user live fan-out |
| Selected DST indicators | Yes for small queries | Yes for curated profile set | Metadata and table revision must be tracked; API has ordinary response cell cap |
| STIL education institutions | Possible via approved web service | Prefer CSV/full extract + daily refresh | Nationwide list and historical/inactive rows are bulk-oriented |
| CVR / production units | Yes for a known CVR | Yes for discovery/area aggregation | National candidate discovery needs local index; restricted person entity excluded |
| Plandata WFS | Yes for bounded spatial query | Yes for selected layers/deltas | Current service supports spatial filters; repeatable aggregation needs snapshots |
| Environmental layers | WMS for map display; WFS/REST for facts | Yes for area analytics | Layer-specific update, rights and geometry |
| DMI current weather/forecast | Yes | Historical subset if needed | Current forecast is inherently time-sensitive |
| Rejseplanen journeys/departures | Yes | Static data only if licensed | User-specific departure time is dynamic |
| OSM POIs | Low-volume Overpass for research | Regional extracts/diffs or provider | Public instances not a reliable nationwide production backend |

### 5.1 Recommended controlled source-adapter boundary

Conceptual only; not a proposed code contract or database schema.

Mistral should not receive credentials or arbitrary network access. It should call a small, allowlisted set of Optata-controlled read tools. Each tool should:
1. accept a bounded query (area ID, radius/polygon, category, time window, page/cursor);
2. validate permitted source, geographic scope, rate and result size;
3. call either a source API or Optata's synchronized read model;
4. return structured facts plus source/provider, source record ID/URL, source update time if supplied, Optata retrieval time, licence/allowed-use tag, geographic resolution, coverage status and any warnings;
5. return explicit `unknown`, `not_covered`, `stale` or `no_data` rather than inventing a value;
6. retain evidence references so the discovery agent can propose candidates while independent verification/audit can inspect the primary source.

The model may summarize and compare tool results; it must not invent missing fields, classify an absence as zero, or publish an unverified candidate.

## 6. Thirty facility-category coverage checklist

The product baseline approves six category families, not the final 30 individual categories. The list below is a working audit decomposition only, to make source gaps visible. It is **not** a founder-approved taxonomy or an instruction to implement all rows exactly as named.

Legend: **Strong** = an identified national register/dataset directly supports a material part of the category; **Supplement** = OSM/CVR/municipal or another secondary source can discover candidates but is not authoritative/comprehensive; **Gap** = no reliable nationwide point-level source verified in this pass.

| # | Working category candidate | Primary source candidate | Supplement / fallback | Coverage assessment and caveat |
|---:|---|---|---|---|
| 1 | Daycare / nurseries | Municipal institution data; STIL only where institution is in scope | OSM, municipal open data | **Gap** — no national complete facility API verified |
| 2 | Primary / compulsory schools | STIL Institutionsregister | OSM; municipal school lists | **Strong** — national institution extract; validate school sites vs administrative units |
| 3 | Secondary / vocational schools | STIL Institutionsregister | OSM | **Strong** — registered institution types and locations |
| 4 | Universities / higher education | STIL Institutionsregister | OSM; institution websites | **Strong** — national institution register; campuses may be multiple locations |
| 5 | Libraries | Municipal/library authority datasets | OSM | **Supplement** — no nationwide live point register validated |
| 6 | Sports halls / indoor sports facilities | Municipal datasets; possible GeoFA layers | OSM | **Supplement** — municipal variation; no complete national API confirmed |
| 7 | Sports clubs / associations | CVR only for registered entities; association sources | OSM; municipal directories | **Gap** — CVR does not equal active physical facility |
| 8 | Swimming pools / aquatic centres | Municipal datasets | OSM | **Supplement** — no national authoritative point inventory confirmed |
| 9 | Fitness centres / gyms | CVR production units | OSM; commercial POI | **Supplement** — business register not proof of public access/open status |
| 10 | Playgrounds | Municipal GIS / GeoFA candidates | OSM | **Supplement** — no nationwide authoritative completeness established |
| 11 | Parks / public green spaces | GeoDanmark / municipal GIS | OSM | **Supplement** — geometry coverage likely stronger than access/amenity detail |
| 12 | Grocery stores / supermarkets | CVR production units | OSM; licensed retail POI | **Supplement** — chain store location and active/open status require validation |
| 13 | Shopping centres / malls | Municipal/owner data | OSM; commercial POI | **Gap** — no national authoritative register verified |
| 14 | Specialist retail / local shops | CVR production units | OSM; licensed POI | **Supplement** — CVR industry/address does not prove customer-facing premises |
| 15 | Restaurants / cafés | CVR production units | OSM; licensed POI | **Supplement** — no verified national government POI API with current opening status |
| 16 | Museums / galleries | Agency for Culture / museum statistics and institution data | OSM | **Supplement** — national institutional information may not give all branch locations |
| 17 | Theatres / cinemas / performance venues | Municipal/cultural institution lists | OSM; licensed POI | **Supplement** — no single authoritative point register confirmed |
| 18 | Concert / event venues | Municipal and venue operator datasets | OSM; licensed POI | **Gap** — event venue vs temporary event requires category rule |
| 19 | Community centres / civic halls | Municipal datasets | OSM | **Gap** — fragmented local ownership and definitions |
| 20 | Churches / religious buildings | Church/municipal/GeoDanmark layers | OSM | **Supplement** — buildings may be mapped, but active public use and denomination need source |
| 21 | Hospitals | Regional health authority / Sundhedsdatastyrelsen datasets | OSM | **Gap pending validation** — national authoritative facility endpoint/schema not inspected |
| 22 | GP / medical practices | Sundhedsdatastyrelsen / regional provider data | CVR; OSM | **Gap pending validation** — provider lists may expose provider IDs but public facility rights/fields need confirmation |
| 23 | Dentists / dental clinics | CVR production units | OSM; licensed POI | **Supplement** — no verified nationwide authoritative clinic-location API |
| 24 | Pharmacies | Danish Medicines Agency pharmacy register/list | CVR; OSM | **Candidate strong, not yet verified** — exact official endpoint, fields, licence and refresh need follow-up |
| 25 | Elder-care homes / care centres | Municipal/regional care data | CVR; OSM | **Gap** — municipal fragmentation and public/private definitions |
| 26 | Social support / shelters | National Board of Social Services / Tilbudsportalen | Municipal datasets | **Candidate strong, not yet verified** — facility types, public visibility and API rights need follow-up |
| 27 | Veterinary clinics | CVR production units | OSM; licensed POI | **Supplement** — no verified national facility register inspected |
| 28 | Public transport stops / stations | Rejseplanen API/feed | OSM | **Candidate strong, not yet verified** — API 2.0 exact endpoint/feed rights need current inspection |
| 29 | EV charging / mobility hubs | Commercial operator APIs (e.g. charge-point operators) | OSM; AFIR/national datasets candidate | **Gap** — fragmented operators, uptime and connector data need agreements |
| 30 | Nature / outdoor recreation sites (beaches, trails, shelters, access points) | Danmarks Miljøportal, GeoDanmark, agency/municipal GIS | OSM | **Supplement** — multiple layer owners; access status and public right-of-way need evidence |

### 6.1 Category conclusions

- **Best evidenced today:** education institutions (STIL), address/geography (DAR/DAGI), building stock (BBR), statistics (DST), planning (Plandata).
- **Business-derived candidate coverage:** CVR can seed candidate locations for registered businesses, but its legal/production-unit records are not a complete or verified public-facing POI registry.
- **Likely multi-source categories:** culture, retail, restaurants, sports, parks and nature.
- **Most material unresolved gaps:** childcare, health providers/hospitals, elder/social care, pharmacy point register, transport stops/feed terms, EV charging and a consistent national POI source.
- A national API's existence is not evidence of full point-level category coverage. Every candidate facility still needs address/coordinates, operational status, provenance and licence checks.

## 7. Access, licensing, price and operational risk register

| Source | Access / auth observed | Licence / commercial use | Price | Freshness / limits | Risk |
|---|---|---|---|---|---|
| Adressevælger | Mandatory token; docs currently say no rate limit; no current user management in FAQ | DAR-specific terms; not assumed unrestricted | No public price found | Daily update; changes searchable next day | **Medium** — confirm production terms/token and future access changes |
| Datafordeler (DAR/DAGI/BBR/CVR) | Account + IT system; API key/OAuth; some protected entities require approval | Register-specific; BBR has personal-data warning; DAR rights set by KDS | No universal price stated | GraphQL pagination, files, WFS; per-register | **High** — per-entity rights, personal data and operational access |
| Dataforsyningen | Service-specific API key / terms | Layer-specific | No universal price found | GSearch closure; other service status per docs | **High** — legacy API transition and layer-specific rights |
| Danmarks Statistik | Public API; POST JSON | CC BY 4.0 with attribution | API data free; StatHost is separate priced offering | 1m-cell non-bulk cap; bulk/streaming alternative; table cadence varies | **Low–medium** — geographic level and suppression are table-specific |
| STIL | CSV/XLSX download; web service requires connection | Commercial caching/redistribution terms not established | No public price found | Web service production updates daily; extract includes current/historical selection | **Medium–high** — need terms and stable machine interface |
| CVR | Datafordeler API key/OAuth; CVRPerson access-controlled | Register terms and personal data rules | Official service price not established | Entity/feed cadence not verified | **High** — legal identity/person data and premises mismatch |
| Plandata | Public WFS/WMS/WMTS; REST submission is separate | CC BY 4.0 for municipal plans and authority-owned layers; other layers vary | No service price stated | Live published database; delta needs effective/publication dates plus update date | **Medium** — layer-level licence and temporal semantics |
| Danmarks Miljøportal / GEUS | WMS/WFS/REST/SOAP depending on service | Layer-specific | Not established | Per-layer cadence | **High** — mixed source owners and terms |
| DMI | Public open-data REST/OGC/STAC/EDR | Open data; verify selected terms/attribution | Free/open per DMI docs | Per collection | **Low–medium** — collection schema/freshness and forecast semantics |
| Rejseplanen | API key / partner access | Current commercial display/cache/route terms not inspected | Unknown / agreement-dependent | API and feed-specific | **High** — access, price, caching and static feed rights |
| OSM / Overpass | Public read-only API; public instances | ODbL 1.0; attribution and share-alike/database analysis | OSM data free; provider/hosting may cost | Public instance usage policies; no SLA | **High** — share-alike implications, uneven completeness and availability |
| Commercial POI providers | Usually API key / contract | Must negotiate commercial display, storage, caching, derived use and redistribution | Quote/subscription unknown | SLA and refresh contract-dependent | **High** — lock-in, cost, retention and data portability |

**Legal gate:** no provider or dataset is approved for production solely by this catalogue. Legal review must cover source owner, distributor, rights to commercial display, caching, retention, derived data, redistribution, attribution, database rights, purpose limitation, personal data, deletion/correction obligations and termination/exit.

## 8. What Mistral can search directly versus what Optata must expose/synchronize

Mistral's capabilities are tool-dependent. The model itself does not automatically have direct authenticated access to Danish register APIs.

### 8.1 Direct web search

Mistral documents built-in `web_search` and `web_search_premium` tools for its Agents and Conversations APIs. These search public websites and return source references/citations. They are useful for:
- discovering official documentation and public announcements;
- checking a public webpage for a candidate facility;
- locating public source pages and evidence URLs;
- supplementary discovery where the source is web-indexed.

They are **not** a guaranteed structured interface to Datafordeler GraphQL, Statistics Denmark POST endpoints, authenticated STIL services or licensed POI databases. Search results may omit records, expose stale snippets or lack a complete geographic/category query. They cannot be used as proof of exhaustive national coverage.

### 8.2 Direct API tools via connector / function calling / MCP

Mistral documents:
- custom function calling for APIs and services;
- MCP connectors for external services;
- HTTP connectors that import an OpenAPI 3.0/3.1/3.2 document and expose supported operations as tools.

Therefore:
- A source with a supported OpenAPI spec and approved authentication can potentially be exposed as a connector after security review.
- GraphQL services such as Datafordeler do not become safe or supported merely because the URL is known; a controlled Optata wrapper/MCP tool is the better boundary.
- Credentials should be held server-side by Optata, not placed in model prompts.
- The model should receive bounded, typed tool outputs and source references, not unrestricted database access.

### 8.3 What requires synchronization or a controlled Optata read layer

| Requirement | Why direct Mistral web search is insufficient | Recommended path |
|---|---|---|
| National address / geography reference joins | Needs exact IDs, full coverage, consistent joins and temporal version | Approved source adapter and synchronized reference/geography data; live Adressevælger for user search |
| BBR/property-to-address joins | Authenticated GraphQL, large data and historical joins | Server-side Datafordeler adapter; synchronize required entities and history |
| Complete national statistics profile | Must enumerate tables, variables, geography and revisions; search snippets are not complete datasets | DST metadata discovery + selected table API calls; cache/sync approved indicators |
| All 30 facility categories | No one complete public web index; need dedup, coordinates, status, licence and source evidence | Multi-source adapters plus controlled candidate registry; synchronize bulk feeds where permitted |
| CVR candidate search at area scale | Requires high-volume structured query, branch/P-unit joins and dedup | Official CVR adapter / approved bulk-delta source; live lookup for known CVR |
| Facility freshness and closures | Web search cannot reliably distinguish stale listing, closure and missing result | Scheduled source refresh + independent evidence/verification workflow |
| Travel-time/catchment metrics | Requires deterministic routing graph, licensed network data and reproducible parameters | Approved routing engine/data feed; return methodology/version |
| Audit/replay and citations | Need immutable source snapshots or retained evidence and retrieval metadata | Controlled evidence capture with source URL/record ID, retrieved_at, source_updated_at and licence |

### 8.4 Recommended Mistral tool surface (conceptual only)

Keep the agent tool surface small and read-only:
- `search_area_sources(area_id, category, as_of)`
- `get_facility_candidates(area_id, category, limit, cursor)`
- `get_source_record(source_id, record_id)`
- `get_area_statistics(area_id, indicator_codes, period)`
- `resolve_address(query)`
- `get_coverage_status(area_id, categories, indicators)`

These names are illustrative only, not an API contract. Each tool must return data plus provenance, geographic resolution, freshness, rights tag and coverage status. Mistral may propose new candidates; it must not directly publish them. Discovery, independent verification and audit remain separate logical roles.

Mistral evidence:
- [Mistral Websearch](https://docs.mistral.ai/studio/agents/agent-tools/websearch)
- [Mistral Agents tool types](https://docs.mistral.ai/studio/agents/agent-tools)
- [Mistral function calling](https://docs.mistral.ai/studio/agents/agent-tools/function-calling)
- [Mistral HTTP connectors / OpenAPI support](https://docs.mistral.ai/studio/connectors/http-connectors)
- [Mistral connectors and MCP](https://docs.mistral.ai/studio/agents/learn/agent/connectors)

## 9. Unknowns requiring primary-source follow-up

These items are explicitly **not verified** and must not be presented as established facts:
1. Current exact Rejseplanen API 2.0 endpoint paths, response fields, geographic coverage, API quotas, price and cache/redistribution rights.
2. Official national point-level facility sources for hospitals, GP clinics, pharmacies, shelters, care homes, childcare, libraries, sports facilities and EV charging; including current endpoint/schema, licensing and refresh.
3. Exact current STIL REST endpoint/operation schema and commercial data-extract rights.
4. Exact current Datafordeler GraphQL schemas and entity field lists for every entity used (DAR, DAGI, BBR, CVR, MAT, EBR, GEODKV); this catalogue samples key fields but is not a full schema dump.
5. Per-table DST geographic levels and current update dates for the selected population, household, income, employment, education and housing indicators.
6. Exact licence/terms and price for each Danmarks Miljøportal/GEUS layer and for municipal open-data feeds.
7. Current Adressevælger production token/usage terms and any future account/rate-limit changes.
8. Commercial POI provider comparison and quotes (coverage, category mapping, duplicate rates, update cadence, SLA, retention, derived-data rights, exit/export).
9. The founder-approved final 30-category taxonomy and the precise meaning of “facility” for branches, campuses, temporary venues, home-based businesses, private-only services and inactive premises.
10. Whether route/travel-time catchments are part of the initial profile and which routing data rights apply.

## 10. Decisions required before design or integration

1. Approve the 30-category taxonomy and category inclusion/exclusion rules (the list in §6 is a research checklist only).
2. Confirm the authoritative address/geography source strategy (Adressevælger + Datafordeler/DAGI) and terms.
3. Decide which facility categories require authoritative coverage and which may use verified supplementary POI data.
4. Decide if OSM ODbL obligations are acceptable for the intended commercial product and how OSM-derived data may be combined with other datasets.
5. Approve commercial POI provider procurement criteria and budget, if government/open data cannot satisfy completeness.
6. Approve source-specific freshness targets and status/verification requirements.
7. Select exact DST indicator tables only after geographic resolution and suppression rules are inspected.
8. Obtain written commercial-use, caching and redistribution terms for STIL, Rejseplanen and municipal/agency layers where not explicit.
9. Approve the Mistral tool boundary and human approval requirements for discovery/verification/audit.
10. Only after the above evidence and decisions: begin separate API/database contract and adapter design Issues.

## 11. Research method and limitations

- Read repository coordination, product and architecture direction at the baseline commit listed above.
- Read primary documentation from Datafordeler/Klimadatastyrelsen, Dataforsyningen, Danmarks Statistik, STIL, Plandata, DMI, Mistral and OpenStreetMap Foundation where linked.
- Inspected official sample API paths and example fields for DAR GraphQL, BBR GraphQL, Statistikbanken and STIL extracts. Did not execute authenticated API calls, register for credentials, download nationwide source files, run API load tests, or inspect paid-provider responses.
- No tests were run; this is a research task.
- Web research checked 17 November 2026. Documentation and provider terms can change; re-check at procurement and integration.
- Where exact endpoint, schema, licence, price, update cadence or coverage was not confirmed from primary source material, the report says so explicitly.

## 12. Handoff to Agent 2 and Agent 3

**Agent 2 / Issue #26:** Use this inventory to map source-supported fields to the product/profile requirements. In particular, distinguish what can be shown as authoritative facts (DAR, BBR, STIL, DST) from supplementary POI discovery and from categories with no verified national source. Do not promise all 30 categories as complete before coverage and licensing decisions.

**Agent 3:** Independently reconcile source rights, personal-data handling (especially BBR/CVR), OSM ODbL compatibility, DST geographic disclosure, Mistral tool security, source provenance and the evidence gaps listed in §9. Challenge any assumption of complete nationwide POI coverage.

**Status:** This is an evidence-backed v0.1 inventory proposal, not final source approval. No code, database schema, migration, API contract or accepted decision was changed.
