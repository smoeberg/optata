# Danish nationwide data-source inventory — v0.2

**Status:** Research catalogue v0.2 — evidence-backed source assessment for review; not source approval  
**Verified:** 17 November 2026  
**Repository baseline:** `main` `1a095f58685761629b47a572f24c703fdb9813f7`  
**Research branch:** `research/issue-25-danish-data-inventory`  
**Related product specification:** Agent 2, Issue #26 (comment `6954507907`)  
**Independent review incorporated:** Agent 3, Issue #25 (comment `6959574205`)  
**Scope:** Nationwide Denmark, actual public/commercial source candidates, documented interfaces, field families, geographic/time coverage, identity joins, rights/access and product/BI fit.  
**Non-scope:** Database/API design, implementation, migrations, ingestion, source procurement/selection, taxonomy approval or changes to accepted product decisions.

> **Evidence labels used throughout**
> - **D — Documented:** current primary-source documentation states the fact, interface, field, licence or cadence.
> - **S — Schema/response inspected:** exact schema/OpenAPI/XSD/field list or response was directly inspectable from the linked primary source during this research.
> - **P — Product/source page only:** authoritative or provider page describes the source, but no machine-readable schema/response was inspected.
> - **L — Lead:** plausible source or provider identified; technical/legal terms not verified.
> - **U — Unknown:** no adequate evidence. Never interpret U as permission or absence.
>
> A source being national does not prove point-level completeness for every facility type or geography. “Publicly reachable” does not itself establish commercial reuse, caching or redistribution rights.

## 1. Executive findings

### 1.1 What v0.2 changes from v0.1

1. **Health is no longer a generic gap.** The Sundhedsvæsenets Organisationsregister (SOR) is a strong national organisation/address directory with SOR IDs, organisation hierarchy, addresses/geography, contact details, unit types and medical specialities. It is publicly accessible through daily CSV/XML files and SOR Browser; SOR2 provides history and SOR/SHAK mappings. Yderregisteret adds provider/practice address, speciality and provider type, daily updates and data from 1995, but its public page does not establish a general self-service commercial API. The legacy SOR CSV/XML products are being retired on 31 December 2026; the authority recommends SorEntity_Daily.csv instead. Rights for commercial redistribution of SOR need written confirmation.
2. **Childcare has a real national register, but not a proven complete live POI API.** Statistics Denmark's child-care institution register is continuously updated from municipal systems; published counts are annual and municipal. STIL's Dagtilbudsregister is still being phased in and is not yet fully complete. The older enrolment microdata documentation explicitly warns of coverage omissions.
3. **STIL education data rights are materially clearer than v0.1 said.** The official terms give a free, worldwide, non-exclusive and otherwise unrestricted right to copy, distribute, publish, combine and use commercially, with visible source attribution, retrieval time, no implication of STIL endorsement, and no alteration of raw STIL data. API registration is required; some restricted data need privileged login. Individual-level data are not exposed through the public API.
4. **GeoFA is a major facility source candidate, not a completeness guarantee.** GeoFA documents facility point/area datasets for active sport, culture, nature/recreation, sailing and other facility families; data can be downloaded as GeoJSON/CSV/Excel and related formats. The published GeoFA specification says CC BY 4.0. Data contribution is by participating authorities/partners, so national access to the database does not prove uniform local completeness.
5. **Public EV charging now has a concrete national access route.** Denmark's NAP is Dataudveksleren, operated by Vejdirektoratet. Since 14 April 2026, public charge-point operators must provide the prescribed data in DATEX II; static fields include location, connector count/type, opening hours and vehicle compatibility, and dynamic fields include current operational/availability status. The actual NAP dataset API, access terms, completeness and response schema were not inspected; the real-time national solution and NAP are related but not interchangeable without checking their individual interfaces.
6. **Public-transport accessibility is more than a source lead.** Rejseplanen API 2.0 documents location search/bounding-box, nearby stops, reachability, trip, interval trip, journey detail and GIS-route services. Commercial quotas/prices are published: 50,000 calls/month free for non-commercial use; commercial 100,000 calls/day costs EUR 5,000/year plus service fee, 200,000 calls/day EUR 8,500/year plus service fee. This can support transit journey/reachability queries, but does not itself establish a static national multimodal routing graph for repeatable all-mode accessibility BI.
7. **Housing-market data is available, but small-area precision is a paid product.** Public Statistics Denmark tables cover national/region/landscape/municipality-area price and sales series; postcodes and more detailed categories are available in paid Betalingsdatabanken products. The public source documents microdata back to 1992 through Danmarks Datavindue, not a public unrestricted transaction-level API. Boligsiden prohibits automated copying/storage/analysis without prior written agreement.
8. **Libraries, museums and culture have useful registers/statistics but uneven point coverage.** The Danish Digital Library OpenPlatform can return physical library address/opening hours, but registration/client access is limited to Danish libraries or their partners. SLKS publishes library statistics; museum and performing-arts statistics are annual and not a complete branch-level POI API. GeoFA can supplement with facility points. 
9. **No single source covers Agent 2's 30 categories or all BI requirements.** A national multi-source evidence model is required. Categories with insufficient nationwide point evidence must be visibly marked partial/unavailable, not filled with unverified search results.

### 1.2 Overall source-readiness

| Product data domain | Evidence status | Nationwide product conclusion |
|---|---|---|
| Address identity / official geography | D/S | Strong national foundation: DAR/Adressevælger + DAGI/Datafordeler; preserve separate identifier namespaces |
| Buildings / dwelling stock | D/S | BBR is national; entity/field-level terms and personal-data treatment must be resolved per field |
| Population / household / income / labour statistics | D/S | DST Statistikbanken API supports official table data; geography and disclosure depend on each table |
| Education institutions and education indicators | D/S | STIL Institutionsregister and Uddannelsesstatistik API; daily institution refresh, free commercial data rights subject to terms |
| Childcare facilities | D/P | DST institution register and STIL Dagtilbudsregister are real national sources, but no verified complete live location API |
| Health providers / hospitals | D/P | SOR and Yderregister provide a national basis; public reuse rights and exact service contracts need confirmation |
| Libraries / culture | D/P | SLKS/DBC/GeoFA sources exist; library OpenPlatform is partner-gated; statistics are not location inventory |
| Sports / outdoor leisure | D/P | GeoFA is a material national dataset family under CC BY 4.0; local completeness varies |
| Social care / elder services | D/P | Tilbudsportalen is legally mandated for specified social offers; SOR/municipal data and DST indicators add context; not all elderly-care facilities covered by one national POI source |
| Public EV charging | D/P | AFIR/DATEX II obligation + Danish NAP; actual query schema/access and operational coverage not yet inspected |
| Public transport | D/P | Rejseplanen API 2.0 supports trip/reachability; commercial usage is priced; exact WADL/XSD response fields not inspected |
| Housing market | D/S | Public DST series + paid small-area tables; transaction microdata controlled; no unrestricted small-area transaction feed established |
| Rent market | D/P | DST rent index national and quarterly from 2021; not neighbourhood-level rent observations |
| Routing / walk-cycle-drive accessibility | L/U | No licensed nationwide routing graph, full mode matrix and reproducible schedule/version evidence approved in this review |

## 2. Product requirement reconciliation — Agent 2 / Issue #26

Agent 2's Issue #26 defines the following candidate taxonomy (not approved by founder) and BI requirements. This section maps them to evidence rather than changing the product requirements.

### 2.1 Facility taxonomy (FAC-01…FAC-30)

| Requirement | Candidate primary sources | Evidence / nationwide status | Limitation and required next check |
|---|---|---|---|
| FAC-01 Daycare / childcare facilities | DST Institutionsregister for børnepasning; STIL Dagtilbudsregister; municipal open data | **D/P — partial** | DST register is continuously updated from municipal system suppliers; annual published counts. STIL register still under build-out and not fully comprehensive. Obtain a current extract and inspect site/address identifiers, private coverage and terms. |
| FAC-02 Kindergartens | Same as FAC-01 | **D/P — partial** | Same source coverage caveat; map type codes to Agent 2 definition and distinguish physical sites from legal units. |
| FAC-03 Primary/lower-secondary schools | STIL Institutionsregister; Uddannelsesstatistik API | **D/S — strong for registered schools** | Institution register gives institution number, name, address, postcode, municipality, region, type and status fields in extract docs; verify multiple campuses and inactive/historical records. |
| FAC-04 Upper-secondary/vocational education | STIL Institutionsregister; Uddannelsesstatistik API | **D/S — strong for registered institutions** | Institution types and education statistics are available; institution vs campus distinction remains. |
| FAC-05 Higher/adult education | STIL Institutionsregister; Uddannelsesstatistik API | **D/S — strong for registered institutions** | Adult-learning provider and branch completeness must be checked against the chosen type codes. |
| FAC-06 Sports halls/indoor sports centres | GeoFA active-sport facility layers; municipal GIS/open data | **D/P — partial** | GeoFA includes active-sport and facility point/area types; inspect current live layer/type-code coverage and local contributor completeness. |
| FAC-07 Fitness/training centres | CVR production units; GeoFA where contributed; licensed POI provider | **D/L — insufficient authoritative POI evidence** | CVR identifies business/production units, not whether the site is a public gym or currently open. Obtain commercial provider sample and signed rights terms or build independent verification. |
| FAC-08 Swimming pools/aquatic facilities | GeoFA; municipal facility lists; CVR as secondary | **D/P — partial** | GeoFA may capture outdoor/active sport and water recreation; no complete national pool inventory verified. Inspect specific facility codes and municipalities. |
| FAC-09 Outdoor sports grounds/clubs/courts | GeoFA active-sport layers; municipal data; CVR for registered organisations | **D/P — partial** | GeoFA has relevant point/area types; coverage depends on local reporting. A club organisation is not the same as its physical facility. |
| FAC-10 Playgrounds/public play facilities | GeoFA; municipal open data; OSM | **D/P — partial** | GeoFA has a defined playground type; municipal datasets can add records. OSM is ODbL and not a complete authoritative source. Legepladsen.dk describes its own merge of OSM, GeoFA and selected municipal CC BY datasets; that is evidence of source fragmentation, not a licence to reuse the aggregator's database. |
| FAC-11 Grocery stores/supermarkets | CVR production units; commercial POI provider; OSM supplement | **D/L — insufficient authoritative POI evidence** | CVR industry/address may seed candidates but does not prove retail format, open status or branch completeness. Provider rights and coverage must be contracted. |
| FAC-12 Specialty retail/local shops | CVR production units; commercial POI provider; OSM supplement | **D/L — insufficient authoritative POI evidence** | Broad category mapping from industry codes is imperfect; no public authoritative point inventory verified. |
| FAC-13 Shopping centres/retail destinations | CVR, GeoFA where relevant, commercial POI provider | **L — gap** | Need explicit definition (centre polygon vs anchor business vs destination). No national authoritative source or rights-verified commercial feed confirmed. |
| FAC-14 Restaurants/cafés/everyday food venues | CVR production units; commercial POI provider; OSM supplement | **D/L — insufficient authoritative POI evidence** | CVR does not reliably identify public-facing restaurant premises or opening status. OSM completeness varies and ODbL review required. |
| FAC-15 Postal/parcel/collection points | PostNord/DAO/GLS/Bring operator locator data; commercial POI provider | **L — gap** | No current national open API, consolidated endpoint, field schema, licence or update contract verified. Each carrier's locator needs separate commercial permission. |
| FAC-16 General practitioners/medical clinics | SOR; Yderregisteret | **D/P — strong candidate for registered providers** | SOR contains organisation/address, unit type and speciality; Yderregister has practice address, speciality and provider type. Confirm which units are active public clinics, duplicate organisation levels and reuse terms. |
| FAC-17 Dental clinics | SOR; Yderregisteret; CVR secondary | **D/P — strong candidate for registered providers** | Yderregister explicitly includes dentists; SOR includes unit/speciality data. Confirm exact dental service categories, practice/site identity and public reuse rights. |
| FAC-18 Hospitals | SOR; regional health-authority lists; DST hospital statistics | **D/P — strong candidate for hospital organisations/sites** | SOR includes hospital-level health institutions and organisational units; one hospital may have multiple campuses/addresses. Need approved inclusion rules and field-level schema sample. |
| FAC-19 Pharmacies | SOR; Danish Medicines Agency pharmacy register/list (source lead) | **D/L — partial** | SOR may represent pharmacies as healthcare organisations; official pharmacy-specific register endpoint, current site fields and commercial terms not verified. |
| FAC-20 Elderly care homes/nursing facilities | SOR municipal units; municipal care lists; DST senior-service statistics | **D/P — partial** | SOR municipal units include examples such as care homes; DST mainly offers municipal-level service indicators. No verified single national, public branch-level register of all public/private nursing homes. |
| FAC-21 Public libraries | SLKS library register/statistics; DBC OpenPlatform; GeoFA/municipal data | **D/P — partial** | DBC API supports library address/opening hours but client registration is only via a Danish library/partner. SLKS/DST statistics are not an open national branch-level POI API. |
| FAC-22 Museums/galleries | SLKS museum lists; DST museum statistics; GeoFA culture; CVR | **D/P — partial** | SLKS list covers state-subsidised/state-owned museums but sites/branches may differ. DST uses CVR and museum reports; not a general current branch-location API. |
| FAC-23 Theatres/cinemas/performance venues | GeoFA culture types; DST cinema and theatre statistics; Scenit/Tereba (source lead) | **D/P — partial** | DST cinema statistics cover commercial cinemas and theatre stats rely on annual submissions; the data pages are activity statistics, not guaranteed location extracts. GeoFA types include theatre and cinema. |
| FAC-24 Cultural/community centres | GeoFA culture types (e.g. assembly/community halls); municipal open data | **D/P — partial** | GeoFA specifies forsamlingshus and foreningshus types; coverage depends on reporting authority. No complete national current point coverage measured. |
| FAC-25 Visitor attractions/major experience venues | GeoFA culture/nature; SLKS museum lists; commercial POI | **D/P — partial** | GeoFA includes amusement facilities and cultural/nature attractions; scope of “major” needs definition. No common nationwide completeness measure. |
| FAC-26 Public parks/green spaces | GeoFA nature/recreation layers; GeoDanmark/municipal GIS | **D/P — partial** | Polygon vs point representation; open-to-public status and access rights need verification. No uniform national park boundary register with visitor-access semantics confirmed. |
| FAC-27 Nature areas/beaches/public waterfront access | GeoFA nature/recreation/sailing; Danmarks Miljøportal; OSM supplement | **D/P — partial** | GeoFA includes outdoor facilities, trails, bathing and coastal amenities; nature/protection layers are not synonymous with public access. Layer-by-layer rights and access semantics required. |
| FAC-28 Bus stops/bus terminals | Rejseplanen API 2.0; Dataudveksleren / transport data | **D/P — strong candidate for transit stops** | Rejseplanen documents bounding-box stop search, nearby stops and location data; commercial use is paid. Inspect current WADL/XSD, operator coverage and caching terms. |
| FAC-29 Train/metro/light-rail stations | Rejseplanen API 2.0; transport authority data | **D/P — strong candidate** | Rejseplanen location and journey services cover stations/lines; confirm current stop ID, coordinates, mode/product fields from live schema. |
| FAC-30 Mobility hubs/public EV charging locations | Dataudveksleren NAP / DATEX II; real-time charge-point solution; operator APIs | **D/P — regulatory national data path, actual completeness unverified** | Required static and dynamic fields are documented. Must inspect NAP dataset, provider feeds, coverage, timestamps, API access and reuse conditions; do not equate operator compliance obligation with proven full feed completeness. |

**Category status meaning:** “strong candidate” means a real national register/API with relevant entity types exists; it does not mean every location is verified or complete. “Partial” means a national source family exists but coverage/site semantics vary. “Gap” means no rights-verified nationwide point inventory has been established.

### 2.2 Agent 2 BI requirements (BI-01…BI-21)

| Requirement | Data source(s) | Current feasibility | Caveat / evidence needed |
|---|---|---|---|
| BI-01 Facility count | FAC inventory above; source IDs; verification evidence | **Partial** | Count only distinct, verified, active places; several FAC categories lack authoritative nationwide POI data. |
| BI-02 Facility density per population | FAC inventory + DST population denominator | **Partial** | Must use same geographic support and aligned reference dates; suppression applies. |
| BI-03 Facility density per area | FAC inventory + licensed official/Optata boundary | **Partial** | Requires valid geometry/version and complete facility coverage; density is not quality. |
| BI-04 Category mix | FAC inventory + approved taxonomy | **Conditional** | Taxonomy and one-primary-category counting rules remain founder decisions. |
| BI-05 Population density | DST population + DAGI/approved boundary geometry | **Strong at table-supported levels** | Cannot downscale municipality/region indicators to neighbourhood or street. |
| BI-06 Population/household trend | DST time series + stable geography definitions | **Strong at supported table levels** | Table-specific periods, revisions, suppression and breaks must be preserved. |
| BI-07 Age/household structure | DST table/API | **Strong at supported table levels** | Denominator, universe and suppression differ by table; no universal threshold. |
| BI-08 Income level/distribution | DST table/API | **Partial to strong at supported levels** | Check whether personal vs household income, nominal/real basis, reference period and geography align. |
| BI-09 Employment/unemployment | DST table/API | **Partial to strong at supported levels** | Preserve age universe and labour-force definition; geographic availability varies. |
| BI-10 Education profile | DST + Uddannelsesstatistik API | **Partial to strong** | Public STIL data are aggregated/disclosure-controlled; API schema supports area/topic/subtopic/key figures/detailing/filters. Restricted data need special privilege. |
| BI-11 Housing mix | BBR entities + DST | **Strong for registered housing stock, subject to field rights** | BBR free basic data CC BY 4.0; not all fields necessarily unrestricted. Need field-level classification and privacy review. |
| BI-12 Housing age/size profile | BBR Bygning/Enhed and DST | **Strong for registered fields, subject to terms** | Preserve missing/unknown and register-quality caveats; do not assume every attribute is complete. |
| BI-13 Price level | DST EJ tables; paid DST EJS tables; transaction data | **Partial** | Public tables generally region/area/municipality level; postcode tables are paid. Transaction-level detail via controlled access, not unrestricted public API. |
| BI-14 Housing turnover | DST transaction counts + BBR stock | **Partial** | Align property category, period, geography and stock denominator. Small-area turnover unavailable until rights/fields acquired. |
| BI-15 Area comparison | All comparable sources | **Conditional** | Only same metric, definition, time and geographic support; no ranking across unlike geographies. |
| BI-16 Trend analysis | Historical DST, BBR, SOR2 where appropriate, other source histories | **Partial** | Each source has its own history; current snapshot feeds do not imply historical completeness. Record revisions and source changes. |
| BI-17 Distance catchment | Facility coordinates + geometry | **Partial** | Straight-line distance can be calculated only with valid coordinates; it is not travel time. Category coverage still partial. |
| BI-18 Travel-time accessibility | Rejseplanen API 2.0 for public transport; licensed road/walk/cycle routing network still needed | **Partial for transit queries; unavailable as full multimodal BI** | Rejseplanen reachability/trip services are live/time-specific; no verified static all-mode graph and replayable network version. |
| BI-19 Geographic overlays | DAGI, GeoFA, Plandata, licensed environmental layers | **Partial to strong by layer** | Layer-specific licence, geometry version, topology and point-vs-polygon semantics. |
| BI-20 Service gap analysis | FAC + DST demand/population indicators + accessibility | **Partial** | Only where both supply and denominator have sufficient geography/coverage; descriptive gap indicator, not causal proof. |
| BI-21 Composite profile/index | Underlying BI-01…20 | **Not source-provided; not approved** | Agent 2 says not default; requires founder approval, weights, normalization, missing-data and sensitivity method. |

### 2.3 Seven-section profile mapping

| Agent 2 profile section | Source basis | Current evidence |
|---|---|---|
| A — Overview/map | DAR/DAGI, GeoFA, verified FAC, DST headline indicators | Core geography is strong; facilities partial; boundary and POI rights vary by layer. |
| B — Facilities/services | FAC-01…30 | Coverage matrix §2.1; no blanket all-category completeness. |
| C — Population/households | DST Statistikbanken | Official data available at table-specific geographic levels and periods. |
| D — Income/socioeconomic | DST Statistikbanken | Indicator/table-specific; disclosure, denominator and geographic restrictions apply. |
| E — Education/employment | DST + STIL/Uddannelsesstatistik | National official statistics and institution directory; API registration, source attribution and disclosure rules. |
| F — Housing stock/market | BBR + DST EJ series + paid DST EJS + rent index | Stock data stronger than fine-grained transaction/market data; paid and restricted layers clearly separated. |
| G — Data quality/source coverage/update | Source-specific freshness, licence, resolution, retrieval timestamps | Requires explicit evidence/coverage status per metric and per category. |

## 3. Central source records — verified detail

### 3.1 DAR / Adressevælger and DAGI — address and geography

**Owner:** Klimadatastyrelsen / responsible register authorities; municipal address authorities maintain DAR addresses.  
**Distribution:** Datafordeleren; Adressevælger is the current documented address autocomplete/search route.  
**Interfaces:** Adressevælger search and ID lookup; Datafordeler DAR GraphQL, file download and WFS. Datafordeler GraphQL endpoint family: `https://graphql.datafordeler.dk/DAR/{version}`; schema at `.../DAR/{version}/schema`. DAGI has corresponding register services.  
**Fields / identifiers:** DAR address ID, house-number ID, address designation, status, building relation and bitemporal registration/effect fields (e.g. `id_lokalId`, `adressebetegnelse`, `bygning`, `registreringFra`, `registreringTil`, `virkningFra`, `virkningTil`). Preserve distinct identifiers for address, access point, property, cadastral parcel and official geography.  
**Geography/time:** Nationwide address register; daily/new changes may appear next day in Adressevælger; bitemporal data is available from register services.  
**Access/rights:** Adressevælger token; Datafordeler account/IT system and API key/OAuth. DAR-specific rights are set by Klimadatastyrelsen; do not infer unrestricted commercial bulk reuse without checking current register terms. Datafordeler's general free basic data terms refer to CC BY 4.0, but register-specific terms take precedence.  
**Verification:** D — exact service families documented; S — sample DAR GraphQL fields documented in the earlier v0.1 research, but current live response/schema was not fetched during this v0.2 pass.  
**Next check:** obtain current schema snapshots and verify field-level rights and replacement API's current usage policy.  
Sources: [Adressevælger overview](https://confluence.kds.dk/pages/viewpage.action?pageId=234782998); [phonetic search](https://confluence.kds.dk/pages/viewpage.action?pageId=244318431); [ID lookup](https://confluence.kds.dk/pages/viewpage.action?pageId=246743156); [DAR GraphQL terms/schema](https://datafordeler.dk/dataoversigt/danmarks-adresseregister-dar/dar-graphql-skema/); [Datafordeler general terms](https://datafordeler.dk/vejledning/brugervilkaar/).

### 3.2 BBR — buildings and dwelling stock

**Owner/distributor:** National BBR register, distributed by Datafordeleren.  
**Interfaces:** BBR GraphQL v3 `https://graphql.datafordeler.dk/BBR/v3`; schema `https://graphql.datafordeler.dk/BBR/v3/schema`; WFS entities; pre-generated JSON/CSV file downloads.  
**Documented entities:** `Bygning`, `Enhed`, `Etage`, `Opgang`, `Grund`, `TekniskAnlæg`, property relationship entities and case entities.  
**Sample documented fields:** Bygning `byg007Bygningsnummer`, `byg021BygningensAnvendelse`, `byg024AntalLejlighederMedKøkken`, `byg025AntalLejlighederUdenKøkken`, `byg026Opførelsesår`, `byg027OmTilbygningsår`. Exact current Enhed schema needs reinspection before mapping.  
**Geography/time:** National register; property/building/unit identities; bitemporal register model.  
**Access:** Datafordeler user + IT system and API key/OAuth.  
**Rights:** Datafordeler's BBR terms explicitly state CC BY 4.0 applies to **free basic data**. The same service warns that BBR may include person-identifiable property information and puts compliance responsibility on the recipient. This is not blanket permission for every field/entity, customer export or public address-level disclosure.  
**Verification:** D/S — endpoint, entity families and sample field names in official documentation; exact complete schema and current sample response not downloaded in this pass.  
**Next check:** produce entity/field-to-classification/terms matrix; distinguish public area aggregates from address-level facts; legal/privacy review before exposing individual property data.  
Sources: [BBR GraphQL](https://datafordeler.dk/dataoversigt/bygnings-og-boligregistret-bbr/bbr-graphql/); [BBR user terms](https://datafordeler.dk/vejledning/brugervilkaar/bygnings-og-boligregistret-bbr/); [Bygning object catalogue](https://grunddatamodel.datafordeler.dk/objekttypekatalog/Bygninger%20og%20boliger/Bygning.html); [Enhed object catalogue](https://grunddatamodel.datafordeler.dk/objekttypekatalog/Bygninger%20og%20boliger/Enhed.html).

### 3.3 Danmarks Statistik — official BI indicators

**Owner/publisher:** Danmarks Statistik.  
**API:** `https://api.statbank.dk`; `POST /v1/subjects`, `/v1/tables`, `/v1/tableinfo`, `/v1/data`. The table metadata response defines each table's dimensions, values, unit and notes; there is no universal indicator schema.  
**Geography/time:** Each table defines its own geography and reference period. Do not downscale region/municipality data to postcode/neighbourhood. Updates are table-specific.  
**Rights:** Statistics Denmark states Statistikbanken data can be reused commercially and non-commercially under CC BY 4.0 with attribution; verify selected table's notes and confidentiality status.  
**Disclosure:** Suppression is table/statistic-specific. Agent 3 correctly flags that there is no universal k-threshold; primary and secondary suppression and reconstruction risks must be considered across joined tables, filters, exports and repeated queries.  
**Verification:** D/S — API routes and table metadata/data structure documented; no individual live data response for each proposed indicator fetched in this pass.  
**Sources:** [API documentation](https://www.dst.dk/da/Statistik/hjaelp-til-statistikbanken/api); [English reuse statement](https://www.dst.dk/en/Statistik/hjaelp-til-statistikbanken/api); [confidentiality and disclosure](https://snyf.dst.dk/Site/Dst/SingleFiles/GetArchiveFile.aspx?ext=%7B2%7D&fi=formid&fo=datafortrolighed--pdf).

### 3.4 STIL — Institutionsregister and Uddannelsesstatistik API

**Owner:** Styrelsen for IT og Læring (STIL), under Børne- og Undervisningsministeriet.  
**Institution directory interfaces:** Institutionsregister data extract (CSV/XLSX); connected system-to-system REST `InstRegRestService`; legacy SOAP services `DataServiceXML` and `PubData` (PubData is legacy and not maintained). Production data updates daily. The service requires connection/subscription.  
**Extract fields documented:** institution number, main institution, name, address, postcode, postcode district, road code, municipality, region, latitude/longitude, contact fields, entity/institution types, education level, ministry, CVR/P-number, owner code, administrative municipality, active code, update date, creation month and closure date.  
**Statistics API:** `POST https://api.uddannelsesstatistik.dk/Api/v1/skema` and `POST /Api/v1/statistik`; OpenAPI v1 also documents `GET /Metadata/v1/DCAT-AP-DK`. The statistics request includes `område`, `emne`, `underemne`, `nøgletal[]`, `detaljering[]`, filters, page and page size; schema response supports JSON/text output depending endpoint. Requires API key/Bearer registration.  
**Access:** Uddannelsesstatistik API registration is free. Restricted datasets require special MitID Erhverv/Unilogin privileges. Public API does not expose personally identifiable individual data; data is disclosure-controlled.  
**Rights:** Official STIL terms provide a free, worldwide, non-exclusive, otherwise unrestricted right to copy, distribute, publish, combine and use commercially/non-commercially. Raw STIL data must not be changed; it may be input to further processing. Attribution wording and retrieval timestamp are mandatory; do not imply STIL endorsement. STIL may adjust API bandwidth/fair-use and can suspend keys; it does not guarantee permanent availability.  
**Cadence:** Institutionsregister production data daily. Uddannelsesstatistik datasets are published to portal and API together; each topic has its own calendar.  
**Verification:** D/S — current official API OpenAPI and REST service documentation indexed; institution field list and terms directly documented. A full current institution response and all API response examples were not downloaded in this pass.  
**Sources:** [Institutionsregister web services](https://viden.stil.dk/spaces/OFFINSTREG/pages/113410159/Institutionsregistrets+webservices); [institution extract](https://institutionsregisteret.stil.dk/dataudtraek); [Uddannelsesstatistik API](https://uddannelsesstatistik.dk/api/); [OpenAPI v1](https://api.uddannelsesstatistik.dk/api-docs/index.html); [API FAQ](https://uddannelsesstatistik.dk/api/faq/); [official terms](https://api.uddannelsesstatistik.dk/Terms); [disclosure rules](https://uddannelsesstatistik.dk/api/data-og-diskretionering/).

### 3.5 Childcare — DST Institutionsregister for børnepasning and STIL Dagtilbudsregister

**Owner/data providers:** DST's register is built from municipal childcare systems and data suppliers; STIL maintains the Dagtilbudsregister under the Ministry of Children and Education.  
**Actual data:** DST publishes annual institution/unit counts by municipality, offer type and ownership. Register updates are continuous from municipal system suppliers and are validated with providers/municipalities. The documentation says monthly data are received for children aged 0–18; some age-6+ data arrive annually.  
**Coverage caveats:** DST documentation notes the older enrolment register misses a small number of municipalities that do not deliver individual data and institutions (especially independent/non-profit institutions) outside municipal payment systems; SFO coverage also has limits. STIL's Dagtilbudsregister is still being phased in and is not yet fully comprehensive/quality assured.  
**Endpoint/schema:** No current public point-level REST/GraphQL API or full national extract schema for the child-care institution directory was verified. The public DST StatBank API gives aggregate statistical tables; it is not the raw institution location register.  
**Rights:** DST published statistics are reusable under its normal attribution terms; terms for raw register/individual microdata are separate and controlled. STIL API terms apply to data actually distributed through its API, but confirm the specific Dagtilbudsregister feed and extract terms before treating it as covered.  
**Verification:** D/P — official register description and collection cadence; exact national location extract not inspected.  
**Sources:** [DST institutions and units for childcare](https://www.dst.dk/da/Statistik/dokumentation/statistikdokumentation/institutioner-og-enheder-for-boernepasning); [statistical processing and collection](https://www.dst.dk/da/Statistik/dokumentation/statistikdokumentation/institutioner-og-enheder-for-boernepasning/statistisk-behandling); [STIL web services](https://viden.stil.dk/spaces/OFFINSTREG/pages/113410159/Institutionsregistrets+webservices); [UVM background on data limitations](https://www.uvm.dk/-/media/filer/uvm/udd/dagtilbud/viden-og-udvikling/kvalitetsundersoegelse/230201forarbejde-til-kvalitetsundersgelse--leverance-7-del-1--overordende-valg-vedrrende-kvalitetsun.pdf).

### 3.6 Health — SOR and Yderregisteret

**Owner:** Sundhedsdatastyrelsen owns/maintains national SOR register; regions, municipalities and organisations maintain different levels of their own units.  
**SOR contents:** SOR code, EAN/location number, hierarchy (institution owner → health institution → organisational unit), name, address/geography, contact details, unit type, medical speciality and SHAK mapping. Includes health organisations in Greenland and Faroe Islands as well as Denmark; the product scope must filter to Denmark.  
**Interfaces and files:** Public SOR Browser; public file distribution at `https://sor-filer.sundhedsdata.dk`; daily CSV/XML; expanded SOR2 CSV set with history and SOR/SHAK mappings; full/delta data via NSP SKRS; SOR lookup service via NSP. SOR Browser export limited to around 1,000 rows.  
**Current transition:** Sundhedsdatastyrelsen says Sor.csv and SOR XML v2 stop on 31 December 2026 and recommends `SorEntity_daily.csv`. The full SOR2 set includes `SorEntity_Daily.csv`, `Sor_Complete.zip`, `GeoLocations`, `LocationsCodes`, `SORClassifications`, `SHAKSORMap` and EDI mappings. SorEntity_Daily includes active units, future closures and future units; complete SOREntity includes history.  
**Yderregister:** Updated daily; contains provider practice address, speciality and provider type (GP, specialist, dentist, physiotherapist, psychologist etc.). Historical coverage begins 1995 with specified quarterly gaps. The public description directs researchers to Forskerservice for research extracts; exact public commercial download/API terms are not established.  
**Access:** SOR files do not require username/password; NSP service is system-to-system. Contact SOR team before production use. Yderregister research extracts via Forskerservice.  
**Rights/privacy:** SOR page says data are publicly accessible but include personal data for sole proprietorships and are subject to data-protection rules. No explicit commercial licence/redistribution grant was found in inspected SOR docs. Public access is not enough to approve commercial storage/display.  
**Verification:** D/P — source structure, access channels, cadence and file family documented; current SOR2 CSV/XSD field-by-field schema and a downloaded live response not inspected. Yderregister field list not inspected because linked XLS document was not readable in the source inspection.  
**Sources:** [About SOR](https://sundhedsdatastyrelsen.dk/data-og-registre/nationale-sundhedsregistre/sundhedsvaesenets-organisationsregister/om-sor); [use/access to SOR data](https://sundhedsdatastyrelsen.dk/data-og-registre/nationale-sundhedsregistre/sundhedsvaesenets-organisationsregister/brug-sor-data); [SOR transition notice](https://sundhedsdatastyrelsen.dk/data-og-registre/nationale-sundhedsregistre/sundhedsvaesenets-organisationsregister/aktuelt-om-sor/sor-nyhed_110226); [Yderregisteret](https://sundhedsdatastyrelsen.dk/data-og-registre/nationale-sundhedsregistre/yderregisteret).

### 3.7 Social care / elder services — Tilbudsportalen, SOR and DST

**Owner:** Social- og Boligstyrelsen has professional responsibility for Tilbudsportalen; Erhvervsstyrelsen runs its technical platform.  
**Coverage:** Nationwide mandatory reporting for foster families and specified offers for people with disabilities or social problems; supervisory authorities approve data before publication. This is not a full inventory of all nursing homes, home-care services or elderly-care facilities.  
**Interface/fields:** Portal search is confirmed; no public bulk/API schema, exact endpoint, machine-readable download, field dictionary, commercial licence or refresh SLA was verified.  
**Complementary evidence:** SOR has municipal units including care homes and rehabilitation centres. DST publishes municipality-level senior-service indicators based on EOJ systems (monthly or annual deliveries) and shelter statistics based on mandatory reports from covered section 110 shelters. These are service/activity indicators, not a complete POI directory.  
**Rights:** Unknown for systematic commercial bulk reuse of Tilbudsportalen; ask Social- og Boligstyrelsen/Erhvervsstyrelsen for terms and machine access. SOR rights also require written confirmation. DST aggregate statistics have their own published reuse terms.  
**Verification:** D/P — portal purpose, mandatory reporting and authority roles documented; no API response/schema.  
**Sources:** [Tilbudsportalen](https://www.sbst.dk/tvaergaende-omrader/tilbudsportalen); [SOR municipal units](https://sundhedsdatastyrelsen.dk/data-og-registre/nationale-sundhedsregistre/sundhedsvaesenets-organisationsregister/sor-kommuner); [DST senior services](https://www.dst.dk/da/Statistik/emner/sociale-forhold/social-stoette/sociale-ydelser-til-aeldre); [DST shelters](https://www.dst.dk/en/Statistik/emner/sociale-forhold/social-stoette/herberger-og-forsorgshjem).

### 3.8 GeoFA — sport, culture, nature and recreation facilities

**Owner/governance:** GeoDanmark collaboration; GeoFA documentation is maintained with KL/Klimadatastyrelsen and data contributions from municipalities/participating authorities.  
**Actual interface and formats:** GeoFA tools support WMS/WFS/WFS-T and REST/SQL API according to the official service documentation; download workflows support Excel, GeoJSON, CSV and other GIS formats. The official specification is the technical source for dataset metadata, geometry and individual field definitions. Exact live endpoint URL, current layer list and actual feature response were not inspected in this pass.  
**Fields/types:** GeoFA contains facility point/area datasets. The published specification v1.6.1 documents facility families including nature/nature facilities, accommodation, active sport, culture and sailing; it defines point/area geometry and type codes. Examples include playground (1031), public bonfire site (1022), assembly hall (5011), museum (5021), theatre (5031), amusement facility (5041), cinema (5051), association house (5061) and historic sites (5082).  
**Rights:** Official GeoFA specification says GeoFA data may be freely used under CC BY 4.0. Photo assets may carry separate attribution/copyright metadata.  
**Coverage/freshness:** Nationally accessible collection but authority/municipality contribution varies; no nationwide category completeness or common update frequency verified. Each dataset/layer must be inspected for source owner, update timestamp, status, geometry and quality.  
**Verification:** D/S — specification and rights page read; exact current live schema/response not fetched.  
**Sources:** [GeoFA overview](https://www.geodanmark.dk/home/vejledninger/geofa/); [download guide](https://www.geodanmark.dk/home/vejledninger/geofa/hent-geofa/); [technical specification](https://geodanmark.dk/wp-content/uploads/2023/02/SPEC-GeoFA-specifikation-1.6.1.pdf); [GeoFA rights and spec page](https://confluence.sdfi.dk/pages/viewpage.action?pageId=191398874).

### 3.9 Libraries and culture — SLKS, DBC, DST and GeoFA

**Libraries:** Slots- og Kulturstyrelsen publishes public and research library statistics based on data collected from municipal library systems and research libraries. DBC/Danish Digital Library OpenPlatform can expose physical library address and opening hours. API base `https://openplatform.dbc.dk`; client registration required, and client IDs are only issued to a Danish library or partner via a library. The docs do not establish unrestricted public access or a commercial licence for Optata.  
**Museums:** SLKS publishes lists of state-subsidised/state-owned museums, but some museums have several branches/visitor sites. DST museum statistics use SLKS-supported museum populations, CVR/DST business registers and museum submissions; annual activity data are not a national real-time branch directory.  
**Theatres/cinemas:** DST cinema statistics are annual and based on commercial cinema ticket systems (over 99% of sold tickets according to its quality page); theatre/scenic arts statistics rely on SLKS support information and voluntary submissions from producers. GeoFA has museum/theatre/amusement/cinema facility type codes.  
**Culture/attractions:** GeoFA plus SLKS lists and local data are the strongest public starting point. The national museum collection portal is not itself a branch-location dataset.  
**Rights/access:** DBC access is library-partner restricted; terms for commercial reuse and retention not confirmed. DST/SLKS statistics have published statistical reuse rules; individual source layers/branch lists need separate terms. GeoFA data CC BY 4.0.  
**Verification:** D/P — official pages and API access rules inspected; no DBC location response or complete SLKS branch dataset downloaded.  
**Sources:** [SLKS library statistics](https://slks.dk/omraader/kulturinstitutioner/biblioteker/biblioteksstatistik); [DBC OpenPlatform](https://danskernesdigitalebibliotek.github.io/OpenPlatform/); [SLKS museums](https://slks.dk/omraader/kulturinstitutioner/museer/om-statsanerkendte-og-statslige-museer/); [DST museums](https://www.dst.dk/da/Statistik/emner/kultur-og-fritid/museer-og-zoologiske-haver/museer); [DST cinema statistics](https://www.dst.dk/da/Statistik/dokumentation/statistikdokumentation/biografer-og-film); [DST theatre/scenic arts](https://www.dst.dk/da/Statistik/emner/kultur-og-fritid/film-og-teater/teater-og-scenekunst); [SLKS web services](https://slks.dk/omraader/kulturarv/databaserne/til-udviklere/webservices).

### 3.10 CVR — registered businesses and production units

**Owner:** Erhvervsstyrelsen. **Distribution:** Datafordeleren and other authorized distributors.  
**Interface:** Datafordeler CVR GraphQL, file downloads and WFS; authenticated with API key/OAuth. CVRPerson is restricted; do not request or use it for this product.  
**Fields:** Company and production-unit identities, names, legal form/status, addresses, industry codes and temporal information are relevant field families; exact current field names must be verified against the current CVR schema before use.  
**Geography:** Nationwide legal entities and production units. Not all production units are consumer-facing premises; registered industry code is not proof of a current open facility.  
**Rights:** CVR terms and personal-data restrictions must be checked per entity. No blanket public commercial redistribution conclusion in this report.  
**Verification:** D/P — source and service families documented; exact current CVR entity schema/response not inspected in this v0.2 pass.  
**Sources:** [CVR access conditions](https://datafordeler.dk/vejledning/brugeradgang/anmodning-om-adgang/det-centrale-virksomhedsregister-cvr/); [Datafordeler overview](https://datafordeler.dk/dataoversigt/).

### 3.11 Plandata — plans and development context

**Owner:** Plan- og Landdistriktsstyrelsen for its own layers; municipalities own/submit municipal planning.  
**Interfaces:** Public WFS for vector geometries/attributes, WMS/WMTS for map rendering; REST submission service is a separate write channel and not relevant to Optata's read-only research.  
**Fields:** Plan identifiers, plan types/status, geometry, publication/adoption/cancellation and modification dates; actual fields vary by layer. WFS docs describe use of `datoopdt` / `oprettet` for deltas, with publication/effective date semantics needing care.  
**Coverage:** National platform; municipal layer completeness and plan types vary.  
**Rights:** CC BY 4.0 for municipal planning layers and Plan- og Landdistriktsstyrelsen-owned layers; other authority layers shown in the platform may have different terms.  
**Verification:** D/P — service types, layer families and licence statements documented; current layer response not fetched.  
**Sources:** [Plandata web services](https://www.plandata.dk/webservices/introduktion-til-webservices); [WFS/delta guide](https://www.plandata.dk/webservices/introduktion-til-webservices/wfs).

### 3.12 DMI and environment / nature

**DMI:** DMI Open Data documents OGC API Features, EDR and STAC interfaces for observations, ocean, lightning, climate, radar and forecast. Each collection has distinct spatial/time coverage and update frequency. Use live for current conditions/forecasts; historical profile indicators require a stable extract and source timestamp. Open data terms/attribution must be checked for selected collection.  
**Danmarks Miljøportal / GEUS:** WMS/WFS/REST services exist across environment, groundwater, nature and geology, but owners, layer fields, rights and cadence vary by layer. WMS is visualization, not a feature-level fact source.  
**Verification:** D/P — service families identified, exact per-layer endpoint/response and reuse terms not comprehensively inspected.  
**Sources:** [DMI API docs](https://www.dmi.dk/friedata/dokumentation/apis); [DMI terms/docs](https://www.dmi.dk/friedata/dokumentation-paa-engelsk); [Danmarks Miljøportal](https://danmarksmiljoeportal.dk/); [GEUS data and maps](https://www.geus.dk/produkter-ydelser-og-faciliteter/data-og-kort).

### 3.13 Rejseplanen API 2.0 — public transport and transit reachability

**Owner/operator:** Rejseplanen with public transport authorities/operators.  
**Interface:** RESTful API 2.0. Official docs enumerate Address Lookup, Location Data, Location Details, nearby stops (within 1,000 m), location search by filters/name/bounding box, reachability, Trip Search, Interval Trip Search, Journey Detail, GIS Route by Context, departure/arrival boards and real-time journey data. Each service links a WADL; XSD is also documented.  
**Fields / response:** Service descriptions establish the data returned at a conceptual level (locations, trip proposals, stop times, durations, changes, route geometry/instructions, real-time data). Exact current response field names and XSD were not inspected in this pass.  
**Coverage:** National journey planner domain for stops/routes/services; exact operator/route completeness and date-specific timetable scope should be confirmed from Data Information and Timetable Information services. Timetable pools have ID, creation date/time, type and validity for station pools.  
**Access and price:** Current API 2.0 docs (updated 1 Oct 2026) say API 1.0 is closed. Non-commercial use: 50,000 calls/month free; >50,000 calls considered commercial. Commercial tiers: 100,000 calls/day EUR 5,000/year + small service fee; 200,000 calls/day EUR 8,500/year + small service fee. Provider acting on behalf of a customer must have the customer request access.  
**Rights/caching:** Exact commercial display, cache/retention and derived accessibility rights must be confirmed in the API agreement. Pricing does not itself prove broad reuse rights.  
**BI suitability:** Useful for transit route and reachability queries at a specific departure time and stop/coordinate. It is not evidence of a static national all-mode routing graph or a reproducible drive/walk/cycle travel-time matrix.  
**Verification:** D/P — current API 2.0 functions and pricing directly documented; WADL/XSD response schemas not fetched.  
**Sources:** [API 2.0 overview and pricing](https://labs.rejseplan.dk/hc/da/articles/21554723926557-Om-API-2-0); [English API 2.0 service list](https://labs.rejseplan.dk/hc/en-us/articles/21554723926557-Om-API-2-0).

### 3.14 EV charging — AFIR, Dataudveksleren NAP and national real-time data

**Regulatory authority:** Færdselsstyrelsen; national access point is Dataudveksleren operated by Vejdirektoratet. Klimadatastyrelsen participates in a separate national real-time charging-data solution. Charge point operators are the data providers.  
**Interface/standard:** Since 14 April 2026, operators must make the prescribed public charge-point data available in DATEX II (minimum CEN/TS 16157-10:2022) on the Danish NAP. OCPI is a voluntary operator/partner integration and does not replace the DATEX II NAP requirement. The Dataudveksleren is the national access point for traffic/mobility datasets.  
**Documented fields:** static location, number/type of connectors, opening hours and vehicle compatibility; dynamic operational/availability status. AFIR also requires pricing information for ad-hoc charging (specific rules and data fields should be checked in current delegated acts and NAP schema).  
**Coverage/cadence:** Legal obligation is national, but no completeness report, operator-by-operator ingestion status or NAP field response was inspected. Dynamic updates should not be assumed instantaneous without source timestamps.  
**Access/rights:** Dataudveksleren lists datasets and often allows access; specific dataset access/terms govern use. AFIR requires operators to make data available, but it does not automatically establish that every Optata use, retention or redistribution is permitted under all applicable terms. No subscription price for NAP access was found in inspected material.  
**Commercial evidence:** Elmer and Lynoplad describe their own collection from NAP and operator endpoints and publish their own refresh methods, but no third-party licence allowing Optata to reuse their aggregated datasets was verified. Do not scrape their websites or reuse their compiled database without agreement.  
**Verification:** D/P — statutory data categories, DATEX II deadline and NAP identity documented; actual live NAP API response, dataset coverage and commercial terms not inspected.  
**Sources:** [Færdselsstyrelsen AFIR data requirements](https://www.fstyr.dk/erhverv/afir/afir-krav-til-ladepunkter); [DATEX II/NAP notice](https://www.fstyr.dk/nyheder/2025/dec/afir-operatoerer-skal-sikre-data-tilgaengeliggoerelse-i-det-europaeiske-format-datex-ii-fra-den-14-april-2026); [Dataudveksleren](https://du-portal-ui.dataudveksler.app.vd.dk/data/171/overview); [real-time charge-point solution notice](https://www.fstyr.dk/nyheder/2025/dec/afir-operatoerer-skal-sikre-data-tilgaengeliggoerelse-i-det-europaeiske-format-datex-ii-fra-den-14-april-2026).

### 3.15 Housing market, sales and rent — DST, Datafordeler, OIS and commercial sources

**DST sales data:** Public StatBank tables include monthly, quarterly and annual price/sales indicators. Public geographic levels vary: tables include regions, landscapes, municipalities/area groupings; postcode-level detail is available in paid products. Public tables include EJ131, EJ56, EJ121, EJEN77, EJEN88, EJ67, LABY22 and EJ99. Public series include price indices back to 1992 for selected tables/categories.  
**Paid DST detail:** EJS10/EJS20 municipality tables and EJS30/EJS40 postcode tables, quarterly/annual, are listed in Betalingsdatabanken. The product page quotes DKK 7,554 excluding VAT per table for 12 months (current listed price at time of research; confirm at purchase). Historical EJS table ranges shown on the page end at 2020; newer public tables cover later periods. Custom statistics are available from DST Consulting under separate quote.  
**Microdata:** DST documents access to property-sales registers through Danmarks Datavindue; underlying data go back to 1992. This is controlled access, not a public unrestricted API.  
**Source chain:** DST says its base data come from Datafordeleren, specifically Ejerfortegnelsen (sale price and trade date) and Ejendomsvurderingen (property valuations). EJF is a distinct ownership register and has confidential entities requiring authority-approved access; do not assume public EJF GraphQL contains all sale details.  
**OIS:** DST's availability documentation points to OIS for detailed individual property information; current endpoint, API terms, rate limits, caching and commercial reuse were not verified.  
**Rent:** DST rent index is national, quarterly, for rented dwellings and cooperative dwellings, with coverage from 2021; it is not a postcode/neighbourhood listing of individual asking rents.  
**Commercial source:** Boligsiden explicitly prohibits third parties from automatically/systematically collecting, copying, storing or analysing its data; use requires prior written agreement. No scraping. Commercial access may be discussed directly with Boligsiden.  
**Verification:** D/S — DST table IDs, geography, historical span, paid product price and data source chain documented; individual transaction API response not inspected.  
**Sources:** [DST housing sales](https://www.dst.dk/da/Statistik/emner/oekonomi/ejendomme/ejendomssalg); [availability and paid tables](https://www.dst.dk/da/Statistik/dokumentation/statistikdokumentation/ejendomssalg/tilgaengelighed); [paid product and price](https://www.dst.dk/da/TilSalg/produkter/erhvervsliv-og-handel/ejendomssalg); [rent index methodology](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/rent-indices-for-housing/statistical-presentation); [EJF access](https://datafordeler.dk/dataoversigt/ejerfortegnelsen-ejf/ejerfortegnelsen-fildownload/); [Boligsiden data policy](https://www.boligsiden.dk/information/datapolitik).

## 4. Geographic and temporal resolution matrix

| Source | Nationwide? | Finest documented product resolution in this pass | Time/history |
|---|---|---|---|
| DAR / Adressevælger | Yes | Address / house number | Daily change feed semantics; bitemporal fields in register |
| DAGI | Yes | Official administrative geography (municipality, region, postcode, parish etc., layer-specific) | Effective/version dates; service-specific update |
| BBR | Yes | Building / unit / property relationships | Bitemporal register fields; field/entity history varies |
| DST general tables | Yes | Table-specific: national, region, municipality and other levels where table dimension exists | Table-specific period and update |
| STIL Institutionsregister | Yes for registered institutions | Institution record with address/postcode/municipality/region and coordinates in extract | Daily production updates; active/closure/history options vary by extract |
| STIL Uddannelsesstatistik | Yes for published education indicators | Area/detailing dimensions defined per data cube; no personal data | Subject-specific publication calendar |
| DST childcare register | Yes, with caveats | Published annual counts by municipality/type/ownership; institution register raw address schema not verified | Continuous register updates; monthly/annual source delivery; annual publication |
| SOR | Denmark plus Greenland/Faroe Islands | Organisation/unit/address/location; some units at department/clinic level | Daily updates; SOR2 historical entities and mappings |
| Yderregister | Yes for covered providers | Provider/practice address | Daily current updates; quarterly history from 1995 with gaps |
| Tilbudsportalen | Nationwide for legally specified offer types | Offer/foster-family record (exact point precision not verified) | Updates/reporting cadence not documented in reviewed page |
| GeoFA | National collection | Point and polygon facility geometry, layer/type-specific | Dataset-specific update; national completeness not established |
| CVR | Yes | Legal entity / production unit address | Register temporal data; exact feed cadence not verified |
| Plandata | Yes | Plan polygon / planning layer | Live published state; modification/effective dates differ |
| DMI | Denmark + relevant seas | Collection-specific grid/station/forecast | Collection-specific cadence and history |
| Rejseplanen | National journey planner network | Stop/location and route/journey | Timetable pool validity; real-time updates; query departure-time dependent |
| Dataudveksleren NAP EV | Intended national operator coverage | Charging location / connector / status | Static and dynamic; exact refresh and completeness per feed unknown |
| DST property sales | Yes | Public tables mostly region/municipality/landscape; paid tables to postcode | Public series from 1992 in selected tables; quarterly/monthly/annual; controlled microdata |
| DST rent index | Yes | National | Quarterly from 2021 |
| Boligsiden | National market portal | Listing/property detail on website | Listing changes; third-party automated reuse prohibited without agreement |

**Hard rule:** area profile calculations must carry the source's actual geographic level. No neighbourhood, street or small-area values may be inferred by allocating municipal or regional totals without an independently approved methodology and clear estimation label.

## 5. Live query, synchronization and evidence retention — source-independent findings

This is a source-use assessment, not an API or database design.

| Data use | Direct live source access | Local synchronized copy likely needed? | Why |
|---|---|---|---|
| Address search | Adressevælger | Optional approved reference cache | Interactive resolution; next-day update semantics |
| Address/property joins | DAR/BBR | Yes for repeated nationwide joins/history | Query fan-out and reproducibility; field-level rights first |
| DST indicators | Statistikbanken / STIL API | Selected indicator snapshots recommended | Profiles, comparisons and time series need stable period/revision tracking |
| Childcare institutions | DST/STIL extract if granted | Likely yes | Nationwide inventory and dedup require snapshot comparison |
| Health locations | SOR2 files; Yderregister access | Yes, if commercial rights confirmed | National directory and daily change/history |
| Social offers | Tilbudsportalen | Unknown pending API/export rights | Need a machine-readable feed and legal terms |
| GeoFA facilities | GeoFA download/services | Yes for area counts and history | Layer snapshots, geometry and update comparison |
| Libraries | DBC API/SLKS | Depends on partner agreement and rights | API is partner-gated; national branch snapshots useful |
| Rejseplanen | Live reachability/trip calls | Static stop/timetable data only under contract | Dynamic travel queries; costs and caching terms |
| EV charging | NAP / operator DATEX II | Static snapshot + dynamic freshness may be needed | Facility discovery plus current status; exact API/rights unknown |
| Property sales | DST public tables / paid Betalingsdatabank | Yes for repeatable trend series | Periodic releases and paid postcode detail; controlled microdata separately |
| Commercial POI feeds | Provider API/contract | Contract-dependent | Cache, derived data, history and export rights must be explicit |

### 5.1 What Mistral may access

Mistral web search is suitable for discovering public documentation and source pages. It is not a completeness guarantee and does not provide reliable authenticated structured access to all source registers.

For data products, Mistral should only receive bounded, authorized, structured results from Optata-controlled tools/connectors. Optata must keep source credentials server-side and enforce source terms, purpose, tenant access, geographic bounds, pagination, rate and output limits independently of model instructions. Model-generated text is not evidence. Preserve source record ID/URL, exact value/claim, source timestamp, retrieval timestamp, licence, geographic resolution and coverage state. Search candidates must not be counted as verified facilities until independent verification is complete.

Mistral documentation identifies web search, function calling and connectors, but product/API lifecycle is evolving; re-check the current supported Mistral API and connector terms before a later integration decision. No Mistral credentials or connector was created in this task.

Sources: [Mistral agent tools](https://docs.mistral.ai/studio/agents/agent-tools); [function calling](https://docs.mistral.ai/studio/agents/agent-tools/function-calling); [HTTP connectors](https://docs.mistral.ai/studio/connectors/http-connectors); [connectors overview](https://docs.mistral.ai/studio/connectors/overview).

## 6. Licence, access and commercial-risk matrix

| Source | Access / price evidence | Commercial use / storage / redistribution | Current risk |
|---|---|---|---|
| DAR / DAGI | Token/account/API key/OAuth; no universal price confirmed | Register-specific rights; check terms per data product and version | **High until written terms and current endpoint checked** |
| BBR | Datafordeler API key/OAuth; free basic data available | CC BY 4.0 for free basic data only; other fields/entities and personal data require separate classification/privacy review | **High** |
| DST StatBank | Public API; standard public tables | CC BY 4.0 attribution; table-level disclosure and source notes apply | **Low–medium** |
| DST paid housing tables | Paid Betalingsdatabank; page lists DKK 7,554 ex VAT/table/12 months | Purchase terms apply; confirm commercial customer redistribution and derived/export rights before purchase | **Medium–high** |
| STIL/Uddannelsesstatistik | Free API registration/API key; restricted data need privileged account | Free worldwide commercial/noncommercial use, copy/distribute/publish/combine; raw data not to be altered; attribution and retrieval time mandatory; terms may change | **Low–medium** (monitor terms and fair use) |
| STIL Institutionsregister connected service | Requires connection/subscription; daily production update | Confirm exact service/extract falls under Uddannelsesstatistik terms; no assumption until STIL confirms | **Medium** |
| SOR | Public daily files without login; NSP system-to-system options | Public access confirmed; explicit commercial licence not found; includes sole-proprietor personal data; ask owner before commercial reuse | **High** |
| Yderregister | Research extracts via Forskerservice; current general API not verified | Research access is not commercial reuse permission | **High** |
| Tilbudsportalen | Public portal search; API/export not verified | Commercial bulk/cache rights unknown | **High** |
| GeoFA | Download and service access | GeoFA specification states CC BY 4.0; photo metadata may have separate copyright | **Low–medium** (field/source owner and coverage checks remain) |
| DBC OpenPlatform | Client ID/secret; only library or partner may register | No general Optata entitlement or commercial redistribution right established | **High until library partner agreement** |
| SLKS/DST cultural statistics | Public statistical pages/API | Public aggregate statistics follow applicable DST reuse terms; raw lists/branch records need source-specific terms | **Medium** |
| CVR | Datafordeler account/API key/OAuth; CVRPerson restricted | Register/entity-specific terms; person data restricted; not every production unit is a public facility | **High** |
| Plandata | Public WFS/WMS/WMTS | CC BY 4.0 for municipal and Plan- og Landdistriktsstyrelsen-owned layers; other layers vary | **Medium** |
| DMI | Open-data API | Open-data terms/attribution per selected collection | **Low–medium** |
| Danmarks Miljøportal / GEUS | Service-specific access | Per-layer owner/licence; no universal reuse right | **High until layer terms verified** |
| Rejseplanen API 2.0 | Non-commercial free up to 50k/month; commercial EUR 5k/year at 100k/day or EUR 8.5k/year at 200k/day + service fee | Contract must confirm caching, display, derived travel times and customer redistribution | **High pending contract** |
| EV NAP / operators | NAP dataset access; no price found | AFIR requires data publication, but exact NAP and operator terms for Optata storage/redistribution/derived values still need confirmation | **Medium–high** |
| OSM / Overpass | Public Overpass instances; no SLA | ODbL 1.0; attribution, database share-alike and derivative/collective database analysis; tile-service policy separate | **High** |
| Boligsiden | Public website; commercial data access by written agreement | Automated collection/copy/storage/analysis expressly prohibited without prior written agreement | **High; no scraping** |
| Other commercial POI vendors | Contract/API pricing not inspected | No recommendation until coverage, source rights, caching, retention, derived use, redistribution, deletion, SLA and exit rights are documented | **High / not assessed** |

**Agent 3 corrections incorporated**
- STIL terms are not unknown: the official licence grant described above is explicit, subject to the exact dataset being covered and raw data remaining unchanged.
- BBR CC BY 4.0 is limited to free basic data, not a blanket grant for every field.
- DST disclosure is table/statistic-specific and query-composition-sensitive; no universal k-threshold.
- OSM legal treatment distinguishes collective databases, derivative databases and produced works; table separation alone does not resolve share-alike.
- Mistral tools must be server-authorized, bounded, logged and protected against untrusted arguments/SSRF; model output is never evidence.

## 7. Commercial provider leads — no recommendation or rights assumption

| Provider/source lead | Potential value | What is not verified | Status |
|---|---|---|---|
| Boligsiden | Housing listing/sales context and market data | Written commercial data agreement, API/schema, caching/export rights, price and derived-data rights | **Do not use without written agreement** |
| Commercial POI aggregators (e.g. HERE, TomTom, Google Maps Platform, Foursquare/other specialist POI suppliers) | Retail, food, health, service and attraction point inventory | Denmark category completeness, source provenance, permitted permanent storage, derived analytics, customer display/export, price and exit rights | **Leads only; no recommendation** |
| Charging aggregators (e.g. Eco-Movement and other AFIR/OCPI aggregators) | Consolidated operator coverage, status and pricing | Direct contract, rights to retain/redistribute normalized records, data freshness/SLA, source attribution and pricing | **Leads only; no recommendation** |
| Retail/business data resellers | Enriched CVR/P-number, chain, location and operational status | Whether derived fields can be used in a commercial profile, refresh, branch completeness and redistribution | **Leads only; no recommendation** |
| OSM-based providers | POI coverage and managed extracts | Whether service terms alter ODbL duties; data lineage and derivative database scope | **Not a workaround for ODbL; legal review required** |

No commercial vendor is selected or recommended by v0.2. A provider can only move from “lead” to “candidate” after a written rights schedule, sample extract/schema, Danish coverage evidence, category mapping, refresh/SLA, price, retention/cache/export terms, derived-data rights, deletion/correction obligations and exit/export rights have been reviewed.

## 8. Priority gaps and next investigations

### Priority 0 — needed before any product claim or procurement

1. **SOR rights and transition:** ask Sundhedsdatastyrelsen for written commercial-use, cache, historical retention and redistribution terms; validate SorEntity_Daily/SOR2 schema and migration path before 31 December 2026. Verify the Yderregister commercial access route and exact fields.
2. **NAP EV feed:** register/access Dataudveksleren dataset; fetch current DATEX II feed/sample; record field dictionary, operator coverage, provider IDs, update timestamps, licence, download/API method, retention and dynamic status cadence.
3. **GeoFA live schema:** retrieve current downloadable dataset catalog and current feature examples for every relevant active-sport/culture/nature type; map type codes to FAC-06/08/09/10/23/24/25/26/27; measure per-municipality gaps and source update dates.
4. **Childcare raw locations:** request current DST institution register/metadata and STIL Dagtilbudsregister extract, schema, active/inactive history, private/self-owned coverage, address granularity and exact rights. Compare institution totals with official municipal/provider counts.
5. **Rejseplanen contract:** obtain current API 2.0 WADL/XSD and sample payloads for location.boundingbox, location.nearbystops, reachability, trip and gisroute; obtain signed terms for commercial caching, derived travel times and customer display.
6. **Housing postcode data:** verify current DST Betalingsdatabank EJS30/EJS40 availability and updated years (the product page's listed historical spans end in 2020); obtain current price and customer redistribution rights. Verify OIS access/terms if property-level sale detail is considered.
7. **DST BI table selection:** for every BI-05…BI-16 indicator, inspect exact StatBank tableinfo, geography dimension, periods, suppression and update date. Avoid assuming that table existence implies postcode/neighbourhood coverage.

### Priority 1 — close remaining category gaps

8. **Pharmacies:** confirm Danish Medicines Agency's official pharmacy list/register endpoint, fields (site ID, address, type, active dates), cadence and commercial use; reconcile to SOR.
9. **Elder-care / nursing homes:** obtain current municipal care-home list metadata or national register proposal; test whether SOR organisation types cover actual locations; distinguish nursing homes, assisted living, home care and day centres.
10. **Libraries:** ask SLKS/DBC for a national branch extract and permitted commercial access; determine whether DBC OpenPlatform client can be issued through an approved library partner and what data may be retained.
11. **Museums/culture:** request SLKS current museum + branch/visitor-site directory; verify Scenit/Tereba terms and whether a current theatre venue export exists; map GeoFA culture features.
12. **Sports facilities:** get GeoFA current type-code tables and data coverage by municipality; ask KL/municipal contributors for known gaps; separate organisation records from facility points.
13. **Retail/food/parcel points:** compare CVR production units against a commercial POI sample; verify physical public-facing site status and rights. Request carrier locators for parcel points.
14. **Hospitals/GP/dentists:** reconcile SOR and Yderregister with regional provider lists; establish unique site-vs-organisation definitions and whether inactive/future units can be distinguished.
15. **Travel time:** evaluate licensed routing graph options for walking/cycling/driving; document geographic coverage, graph update cadence, traffic assumptions, accessibility and commercial rights. Do not use Rejseplanen transit reachability as a substitute for all modes.
16. **Rent data:** identify whether any licensed commercial rent/asking-rent source permits long-term area history; DST national quarterly index alone does not meet postcode-level rent trend requirements.

## 9. Evidence limitations and exact verification statement

### Directly verified in primary documentation on 17 November 2026
- SOR's data contents, hierarchy, daily updates, public file access, SOR2 historical files and 31 December 2026 retirement notice for older SOR CSV/XML files.
- Yderregister's practice address, speciality, provider type, daily update and historical coverage description.
- DST childcare register purpose, geographic output (municipality), continuous updates, source suppliers and documented coverage caveats.
- STIL Institutionsregister REST service availability, daily production update, extract path and field list; STIL Uddannelsesstatistik API endpoints, OpenAPI request shape, free registration and terms for commercial reuse.
- GeoFA specification's dataset families, geometry model, selected facility type codes and CC BY 4.0 statement.
- Tilbudsportalen national scope, legally mandated reporting for specified offers and authority roles.
- DBC OpenPlatform physical-library address/opening-hours function and library/partner client registration restriction.
- Rejseplanen API 2.0 service catalogue, reachability/trip capabilities and published usage tiers/prices.
- AFIR DATEX II requirement effective 14 April 2026, static/dynamic charge-point field families and Dataudveksleren as Danish NAP.
- DST property-sales table geography, paid postcode tables, price shown for Betalingsdatabank access, data history back to 1992 through Danmarks Datavindue and source chain to EJF/Ejendomsvurderingen.
- Boligsiden's prohibition on automated/systematic data collection without prior written agreement.
- Agent 2's FAC-01…30 taxonomy and BI-01…21 requirements as written in Issue #26 comment 6954507907.
- Agent 3's STIL, BBR, DST suppression, OSM and Mistral review corrections in Issue #25 comment 6959574205.

### Not verified against a live machine response or complete schema in this pass
- No authenticated Datafordeler DAR/BBR/CVR GraphQL query or full live schema download was executed.
- No full SOR2 CSV file, Yderregister spreadsheet, STIL current extract, DST full table response or childcare register file was downloaded and parsed.
- No GeoFA live WFS/REST feature response or nationwide category completeness statistics were fetched.
- No Rejseplanen WADL/XSD response payload was inspected.
- No Dataudveksleren DATEX II charge-point feed was fetched; operator coverage and real-time cadence remain unknown.
- No current Tilbudsportalen API/export endpoint or commercial reuse terms were verified.
- No commercial POI, charging aggregator or housing vendor contract/sample was obtained.
- No source access request, paid data purchase or legal opinion was commissioned.

### Interpretive conclusions (not source facts)
- “Strong candidate” is an assessment of source relevance, not a statement of complete facility coverage.
- Suggested live/sync use is an operational assessment, not a database design.
- Category coverage is not a guarantee of exact site counts; taxonomy and place identity rules remain open.
- No source is approved for production by this document.

## 10. Decisions / confirmations still required from founder

1. Approve/revise/reject Agent 2's 30-category taxonomy and place-counting rules.
2. Confirm whether each category must have authoritative national source coverage to be included in public counts, or whether licensed verified supplementary data may qualify.
3. Approve whether Optata may procure commercial POI data, including recurring costs and data retention/export requirements.
4. Decide whether OSM ODbL-derived facilities are acceptable in the commercial product after specialist legal review.
5. Confirm whether postcode-level housing market data is a required paid dependency and approve a DST budget if so.
6. Confirm required travel modes and whether transit reachability alone is useful as a separate metric.
7. Approve source-specific freshness targets and whether historical closed/inactive locations appear in trends.
8. Approve legal/privacy review of SOR sole-proprietor data and BBR field-level classification before place/property exposure.
9. Confirm whether all 30 categories are required at launch or whether product should explicitly display category coverage gaps while remaining nationwide.
10. Approve any composite index only after separate methodology and sensitivity proposal; BI-21 is not source-provided.

## 11. Handoff

**Agent 2 / Issue #26:** Reconcile the FAC and BI mapping in §2 with the profile and entitlement proposal. Product claims must respect partial/unsupported categories and geographic levels. In particular, BI-18 is only partially supported for transit and does not yet have a verified all-mode routing graph; BI-13/14 need paid postcode or controlled transaction data for smaller geographies.

**Agent 3:** Review SOR rights and personal data, STIL licence interpretation and dataset scope, GeoFA source/field licensing, Rejseplanen price/contract rights, NAP/AFIR reuse terms, DST paid table terms and OSM database obligations. Verify the exact transition of SOR file products before 31 December 2026.

**Status:** v0.2 is a reviewable research update, not final source approval. No database schema, API contract, implementation, migration, provider procurement or product decision is proposed or changed.
