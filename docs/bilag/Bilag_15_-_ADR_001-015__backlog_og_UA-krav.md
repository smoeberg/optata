# OPTATA — (a) ADR 001–015 · (b) Sprint-backlog S0+S1 · (c) Kravspecifikation til UA-teamet

Tre artefakter, klar til repo og kontrakt.

---

# DEL A — Architecture Decision Records

**Fælles skabelon:** `Status · Kontekst · Beslutning · Konsekvenser · Alternativer fravalgt · Verifikation`

---

### ADR-001 — Modulær monolit, ikke microservices
**Status:** Accepteret
**Kontekst:** 2,3 FTE byggekapacitet i år 1. Seks indtægtsben skal deles om én kerne.
**Beslutning:** Én deploybar applikation (`apps/api`) med hårde modulgrænser i `core/*` + separate workers. Moduler kommunikerer via domæne-events eller eksplicitte interfaces — aldrig via tværgående tabeladgang. Stack: **Python/FastAPI** (geo/data/LLM-nærhed) + **Next.js** frontend.
**Konsekvenser:** Én deployment, én transaktion, lav driftsbyrde. Split af `agent_runner` og `ingestion` først ved målt behov (md. 18+). Modulgrænser håndhæves med import-lint i CI.
**Fravalgt:** Microservices (drift æder kapaciteten), serverless (kolde starts + geo-biblioteker).
**Verifikation:** CI-gate: `core/*` må ikke importere `apps/*`; ingen cross-module tabel-SELECT.

---

### ADR-002 — PostgreSQL + PostGIS, bitemporal via ranges
**Status:** Accepteret
**Kontekst:** Moaten er historikken. Overvågningsproduktet sælger *ændringer*. Banken skal kunne se, hvad vi vidste hvornår.
**Beslutning:** Postgres + PostGIS. Al registerdata har `valid_from/valid_to` (virkelighedstid) og `recorded_at` (systemtid). Upsert lukker gammel version og indsætter ny — **overskriver aldrig**.
**Konsekvenser:** Historik kan ikke genskabes af en konkurrent, der starter i dag. `property.changed` driver overvågning og agent-cache. Større datamængde; partitionering pr. område fra start.
**Fravalgt:** CRUD med audit-trigger (kan ikke rekonstruere gyldighedstid), separat tidsserie-DB (to sandheder).
**Verifikation:** Migration-test: ingen destruktiv UPDATE på `property`; fixture med 24 mdr. historik rekonstrueres korrekt.

---

### ADR-003 — Event-sourcet ordrebog, append-only
**Status:** Accepteret
**Kontekst:** Tæthed, ejerrespons, konvertering og historik er alle afledt af hændelser.
**Beslutning:** `order_event` er append-only. `REVOKE UPDATE, DELETE` for app-rolle. Transactional outbox → worker publisher. Orden garanteres pr. aggregate, ikke globalt. Konsumenter idempotente på `event_id`.
**Konsekvenser:** KPI'er beregnes fra events, ikke fra statusfelter. Skemaændringer kræver upcasting **ved læsning** — gamle events omskrives aldrig i store.
**Fravalgt:** Kafka i år 1 (unødvendig drift), status-CRUD ( mister historikken).
**Verifikation:** `test_event_append_only`, `test_upcast_1_0_to_1_1`, idempotens-test på konsument.

---

### ADR-004 — Tre datazoner + RLS
**Status:** Accepteret
**Kontekst:** UA-udvikling, banksalg og GDPR kræver hård adskillelse.
**Beslutning:** Zone A (offentlig, dev-tilgængelig) · Zone B (persondata, kun EU-prod, RLS + audit) · Zone C (aggregeret, k≥5, eksportérbar). Adskillelse håndhæves i **DB-roller og RLS**, ikke kun i applikationslogik.
**Konsekvenser:** Front-end kan ikke joine til vault. Zone C bygges kun via kontrollerede aggregationsjobs. Dev bruger syntetiske data.
**Fravalgt:** Én database med felt-level filtering (for skrøbeligt over for AI-genereret kode).
**Verifikation:** `test_no_zone_b_in_public`, `test_rls_agent_scope`, `vault.accessed{service≠disclosure}` → P1-alarm.

---

### ADR-005 — MitID via broker, ingen CPR lagret
**Status:** Accepteret
**Kontekst:** Identitet skal være stærk, men CPR i databasen gør os til et højrisiko-mål og skærper tredjelandskrav.
**Beslutning:** Godkendt broker (Criipto/Signicat) via OIDC. Gem **kun broker-pseudonym** + afledte attester. CPR og navn passerer transient i hukommelsen ved match og **logges/gemmes aldrig**. MitID Erhverv til B2B (CVR-bundet).
**Konsekvenser:** Dedup og én-person-én-ordre virker uden CPR. Broker-lock-in afbødes af OIDC-abstraktion og stabilt pseudonym. Navnematch ved ejerskab er transient.
**Fravalgt:** Direkte NSIS-implementation (for tung), CPR som nøgle (uacceptabel risiko).
**Verifikation:** `test_no_cpr_persisted`, log-scan i CI, schema-constraint.

---

### ADR-006 — Progressiv identitet
**Status:** Accepteret
**Kontekst:** P0 kræver ≥8 % konvertering. MitID på tragtens top halverer den.
**Beslutning:** Anonym browsing → e-mail/magic link (ordre CURIOS) → MitID (QUALIFIED) → bankattest (VERIFIED) → step-up (følsomme kald). Ordre opgraderes **in-place** via `identity.linked`.
**Konsekvenser:** To ordrebøger måles: rå (distribution) og verificeret (salgbar). Ingen dubletter ved opgradering. MitID-omkostning holdes nede.
**Fravalgt:** MitID på alt login (dræber tætheden).
**Verifikation:** `test_identity_merge_no_duplicate_order`, funnel-metrics pr. trin.

---

### ADR-007 — Anonym front-end + relay + gensidig reveal
**Status:** Accepteret
**Kontekst:** Markedsføringsret, partbeskyttelse og disintermediation.
**Beslutning:** Al front-end er gensidig anonym (pseudonym + attester). Al kommunikation via relay med deterministisk redaction. Identitet udveksles kun ved `IDENTITY_REVEALED`.
**Konsekvenser:** Ingen persondata udleveres til ejer eller mægler. Mæglerproduktet er **anonym dialog-adgang**, ikke en kontaktliste. Redaction bliver en sikkerhedskritisk komponent.
**Fravalgt:** Kontaktudlevering mod betaling (GDPR + formidlingsrisiko), åben chat uden redaction (lækage).
**Verifikation:** `test_redaction_corpus` (50+ varianter), `test_no_zone_b_in_public`, `test_agent_cannot_reveal`.

---

### ADR-008 — Reveal som betalt milepæl, fast gebyr
**Status:** Accepteret — **juridisk afklaring påkrævet uge 6**
**Kontekst:** Salgspakken skal monetisere matchet uden at blive formidling.
**Beslutning:** Fast gebyr 10.000 kr., **aldrig success fee**. Reveal kræver seks guards i **én transaktion**: pakke accepteret ∧ betaling captured ∧ begge samtykker ∧ frisk MitID step-up (≤5 min) ∧ gyldig attest ∧ gyldigt ejerskab. Kun `disclosure` læser vault.
**Konsekvenser:** Afsløring er den naturlige betalingsmilepæl. **Fast gebyr fritager ikke i sig selv for formidlingsvurdering** — match+relay+reveal vurderes samlet af jurist. Model A (advokatpartner som formel formidler) er udgangspunkt.
**Fravalgt:** %-salær (formidling), egen escrow (betalingstjenestelov + hvidvask).
**Verifikation:** `test_reveal_all_six_guards`, `test_reveal_concurrent_idempotent`, `test_reveal_toc_tou_expiry`.

---

### ADR-009 — Ejerskab: EJF + Tingbogen + manuel fallback
**Status:** Accepteret
**Kontekst:** EJF-adgang er ikke givet. Andelsboliger ejes af foreningen — EJF dur ikke.
**Beslutning:** Multi-metode: `EJF_PERSON`/`EJF_CVR` (hvis adgang) → `DEED` (tinglyst adkomst, offentlig) → `ANDELS_ATTEST`/`MANUAL`/`POWER_OF_ATTORNEY`. Konfidens + TTL (90–180 dage). **Ejerskifte i registry tilbagekalder automatisk** eksisterende verifikation.
**Konsekvenser:** Produktet virker selv hvis EJF afvises. Manuel kø er en planlagt kapacitet (~6 timer i pilot). Sameje kræver verifikation + samtykke fra **alle** ejere.
**Fravalgt:** EJF-only (blokerer andelsboliger og hele piloten).
**Verifikation:** `test_andels_not_ejf`, `test_ownership_revoked_on_transfer`, `test_sameje_all_consent`.

---

### ADR-010 — k-anonymitet: k=5, afrunding, komplementær suppression
**Status:** Accepteret
**Kontekst:** Zone C sælges til banker. Tre reelle angreb: lille celle, komplementær afsløring, differencing over tid.
**Beslutning:** k≥5 · afrunding til nærmeste 5 · komplementær suppression ved én skjult celle + total · max 3 dimensioner · mindste geo = postnummer · tidsvindue = kvartal eller rullende 3 mdr.
**Konsekvenser:** Nogle celler skjules — det er en feature, ikke en fejl. Gap-analysen returnerer `INSUFFICIENT_DATA` i stedet for estimater.
**Fravalgt:** k=3 (for tyndt i små områder), daglige deltas (differencing), præcise budgetbeløb.
**Verifikation:** `test_k_anonymity`, `test_complementary_suppression`, `test_too_many_dimensions`.

---

### ADR-011 — Agent: claim-pipeline med tvungen proveniens
**Status:** Accepteret
**Kontekst:** En analyse uden kilde er en holdning — en bank kan ikke bruge den.
**Beslutning:** LLM returnerer **kun** struktureret JSON iht. schema. Deterministisk validering bagefter: `source_id` skal findes, `effective_date` skal være gyldig, citat ≤200 tegn og fuzzy-matchet i kilden. Ingen publicering uden menneskelig `reviewed_by`. `model_version` + `prompt_version` gemmes.
**Konsekvenser:** Reproducerbarhed, friskhedsflag, RYGTE holdes ude af Bevægelse-laget. Cache pr. område holder LLM-omkostning nede.
**Fravalgt:** Fri tekstgenerering (hallucinationer), auto-publicering (troværdighedsrisiko).
**Verifikation:** `claim_needs_source` DB-constraint, FX-A1…A6, `test_publish_requires_approved`.

---

### ADR-012 — UA-udvikling på syntetiske data, EU-prod
**Status:** Accepteret
**Kontekst:** Ukraine er tredjeland. Banken kræver due-diligence-klarhed.
**Beslutning:** Produktion EU-only. Udvikling/staging: **kun syntetiske data** (deterministisk generator, vandmærket `_synthetic:true`). Ingen prod-dumps. SCC + TIA + subprocessorliste. Adgang til prod kun via break-glass med audit og tidsbegrænsning.
**Konsekvenser:** UA-teamet kan arbejde fra dag 1 uden persondata. CI-gate 10 blokerer prod-lignende data i fixtures. Salgsargument: *"Udvikling i Ukraine behandler ikke persondata."*
**Fravalgt:** Anonymiseret prod-kopi (re-identifikationsrisiko), prod-adgang til udviklere.
**Verifikation:** `test_no_prod_like_data`, ugyldige DK-telefonnumre, `example.invalid`-e-mails.

---

### ADR-013 — Data engineer fra måned 2
**Status:** **TIL BESLUTNING** — afgør første krone i md. 4
**Kontekst:** 90-dages-planen kræver datamodel i uge 4–7. Omkostningsbasen ansætter i md. 4 (≈uge 13). Begge kan ikke være sande.
**Beslutning (foreslået):** Ansat fra **md. 2**. Merudgift ~60.000 kr. i år 1.
**Konsekvenser:** S1 holder, første analyse leveres md. 4, A4-beviset kommer til tiden. Uden beslutningen skrider første indtægt til md. 6–7, og hele læringsplanen forsinkes.
**Alternativer:** Fractional uge 3–12 (dobbelt onboarding) · stifter bygger S1 (indtægt skrider).
**Verifikation:** Ansættelseskontrakt underskrevet inden uge 6; S1-milepæl nået uge 8.

---

### ADR-014 — Eksklusivitet håndhævet med unique index
**Status:** Accepteret
**Kontekst:** Samme køber til tre mæglere = alle tre churner.
**Beslutning:** `CREATE UNIQUE INDEX exclusive_agent_per_zip ON subscription(scope_id) WHERE product IN ('AGENT_ZIP','AGENT_DISTRICT') AND status='ACTIVE'`. Bydel/postnummer-overlap checks med advisory lock. Ved opsigelse: **køberne følger postnummeret, ikke mægleren**. RLS-cache invalideres øjeblikkeligt ved EXPIRED.
**Konsekvenser:** DB-garanti, ikke forretningslogik. To samtidige salg kan ikke begge lykkes.
**Fravalgt:** Applikations-level check (race condition).
**Verifikation:** `test_exclusive_agent_per_zip`, `test_concurrent_purchase`, `test_rls_invalidation_on_expire`.

---

### ADR-015 — To-lags sletning med tombstone
**Status:** Accepteret
**Kontekst:** "Fuld historik" (§2.3) vs. sletteret (GDPR). Bogføring og audit kan ikke slettes på anmodning.
**Beslutning:** Zone B slettes hårdt (identitet, beviser, tråde). Pseudonym event-historik + audit + bogføring bevares. `identity.erased` emitterer tombstone; zone C genberegnes. Undtagelserne står i privatlivspolitikken.
**Konsekvenser:** Moaten overlever sletning — ingen tabel kan mappe pseudonym til person. Retention-jobs er P2 ved fejl.
**Fravalgt:** Slet alt (moat + lovpligtig bogføring går tabt), behold alt (GDPR-brud).
**Verifikation:** `test_erasure_preserves_events`, `test_tombstone_unmappable`, månedlig retention-rapport.

---

# DEL B — Sprint-backlog S0 + S1

**Konventioner:** `S{n}-{nn}` · estimat i persondage · ejer = DE (data engineer UA) / FS (fullstack UA) / DK (stifter/reviewer) · alle issues kræver grønne CI-gates 1–12.

---

## S0 — Fundament (12 pd · uge 1–3)
**Mål:** UA-teamet kan arbejde lovligt, sikkert og reproducerbart. Ingen feature bygges før S0 er grøn.

| ID | Issue | Est. | Ejer | Afhænger af |
|---|---|---|---|---|
| S0-01 | Monorepo-skelet + modulgrænser + import-lint | 1,0 | DE | – |
| S0-02 | IaC: EU-miljøer (dev/staging/prod) + netværk/IAM | 2,0 | DE | – |
| S0-03 | CI-pipeline: gates 1–12 som kørbare jobs | 2,0 | DE+DK | 01 |
| S0-04 | Zone-model + DB-roller + RLS-baseline | 1,5 | DK | 02 |
| S0-05 | Syntetisk datagenerator v0 + vandmærke | 2,0 | DE | 04 |
| S0-06 | Kontrakt-skelet: OpenAPI + event-envelope + upcaster | 1,5 | DE | 01 |
| S0-07 | Append-only audit-log + trace_id-propagering | 1,0 | DK | 04 |
| S0-08 | Observability + P1-alarmer (vault, zone-lækage) | 0,5 | DE | 02 |
| S0-09 | CODEOWNERS + ADR-skabelon + runbook-skelet | 0,5 | DK | – |

**Acceptkriterier S0:**

```
S0-01  GIVEN import fra apps/* i core/*  THEN CI fejler
       GIVEN cross-module tabel-SELECT   THEN lint fejler

S0-02  GIVEN prod-miljø                  THEN region ∈ EU, ingen offentlig DB-adgang
       GIVEN dev-miljø                   THEN ingen forbindelse til prod-netværk

S0-03  GIVEN PR med guard-fejl           THEN merge blokeret, ingen override
       GIVEN alle 12 gates               THEN kørbare lokalt via `make ci`

S0-04  GIVEN app_role                    THEN UPDATE/DELETE på order_event afvist
       GIVEN disclosure_service          THEN eneste rolle med SELECT på identity_contact
       GIVEN anonym query                THEN kan ikke joine zone B

S0-05  GIVEN seed 42                     THEN identisk output ved genkørsel
       GIVEN alle poster                 THEN _synthetic=true, ugyldigt DK-nr, .invalid-mail
       GIVEN `make dev`                  THEN fuld database uden persondata

S0-06  GIVEN kode afviger fra OpenAPI    THEN CI-gate 1 fejler
       GIVEN gammel event-version        THEN upcastes ved læsning, store uændret

S0-07  GIVEN audit-entry                 THEN UPDATE/DELETE afvist på DB-niveau
       GIVEN kald på tværs af services   THEN samme trace_id

S0-08  GIVEN vault.accessed{service≠disclosure} THEN P1-alarm udløses i test
       GIVEN zone B-felt i public payload       THEN alarm + rollback-trigger

S0-09  GIVEN ændring i /core/disclosure  THEN DK-review påkrævet af CODEOWNERS
```

---

## S1 — Registry, tæthed, rapport, anonym ordre (30 pd · uge 3–8)
**Mål:** Anonym bruger kan se en område-/adresserapport og afgive en ordre. Tæthed kan måles korrekt.

| ID | Issue | Est. | Ejer | Afhænger af |
|---|---|---|---|---|
| S1-01 | Adapter-framework: checkpoint, idempotens, quarantine | 2,0 | DE | S0 |
| S1-02 | DAR-adapter + validering | 2,0 | DE | 01 |
| S1-03 | EBR-adapter + geokodning (SRID 4326) | 2,0 | DE | 02 |
| S1-04 | BBR-adapter + boligkoder + quality_flags | 3,0 | DE | 02 |
| S1-05 | VUR-adapter + sanity + `VUR_UNVERIFIED` | 1,5 | DE | 02 |
| S1-06 | Bitemporal upsert + `property.changed` | 3,0 | DE+DK | 02–05 |
| S1-07 | BFE↔adresse-id-samling + area-udledning + `dwelling_count` | 3,0 | DE+DK | 06 |
| S1-08 | PostGIS: area-geometri, indices, tile-cache | 2,0 | DE | 03,07 |
| S1-09 | `area_density` materialized view + refresh-triggers | 1,5 | DE | 07 |
| S1-10 | Zone A API: `/areas`, `/areas/{id}/profile`, `/properties/{id}` | 2,0 | FS | 07,08 |
| S1-11 | Områderapport: statisk render + cache (4 lag, efterspørgsel tom) | 2,0 | FS | 10 |
| S1-12 | Web: landing + adressesøgning + adressekort | 2,0 | FS | 10 |
| S1-13 | Ordre CURIOS: magic link + dedup-index + `order.created` | 2,5 | FS+DK | S0-04,06 |
| S1-14 | Fixtures FX-01/02/03 + guard-tests (density, dedup, zone) | 1,5 | DK | 07,09,13 |

**Acceptkriterier S1:**

```
S1-01  GIVEN genkørsel af samme kørsel   THEN ingen duplikater (idempotensnøgle)
       GIVEN valideringsfejl             THEN post i quarantine, aldrig stille drop
       GIVEN afbrudt kørsel              THEN genoptages fra checkpoint

S1-02  GIVEN adresse-id                  THEN UUID-format, postnr findes i area
       GIVEN inaktiv adresse             THEN ekskluderes fra dwelling_count

S1-03  GIVEN koordinat                   THEN ST_Within(area.geom) = true
       GIVEN konflikt postnr vs. geometri THEN quarantine + rapport

S1-04  GIVEN areal ≤0 eller >2000        THEN quarantine
       GIVEN ikke-bolig anvendelse       THEN ekskluderes fra dwelling_count
       GIVEN usikkert felt               THEN quality_flag sat, ikke skjult

S1-05  GIVEN vurdering uden for 0,1–50 mio. THEN flag + quarantine
       GIVEN VUR ældre end indeværende år   THEN flag VUR_UNVERIFIED vist i UI

S1-06  GIVEN ny version af samme post    THEN gammel valid_to lukkes, ny recorded_at
       GIVEN ændring                     THEN property.changed emitteres (outbox)
       GIVEN historik-forespørgsel       THEN tilstand på vilkårlig dato rekonstrueres

S1-07  GIVEN FX-01 (BFE med 40 enheder)  THEN 40 rækker, dwelling_count += 40
       GIVEN FX-02 (12 enheder, CVR)     THEN owner_kind=COMPANY, 12 adresser
       GIVEN dwelling_count ændring >2 % THEN alarm + frys tætheds-KPI

S1-08  GIVEN adresseopslag               THEN p95 <400 ms med cache
       GIVEN geo-query                   THEN GIST-index bruges (EXPLAIN verificeret)

S1-09  GIVEN 25 verificerede / 10.000    THEN per_1000 = 2,5
       GIVEN order.verified/expired      THEN view refreshes, ikke realtime-beregnet
       GIVEN dwelling_count = 0          THEN nullif beskytter mod division

S1-10  GIVEN anonym GET /properties/{id} THEN 200 med zone A, ingen zone B-felter
       GIVEN ukendt adresse              THEN 404, ingen enumeration-lækage

S1-11  GIVEN rapport                     THEN cached, kilde+dato på hver påstand
       GIVEN efterspørgselslag tomt      THEN viser "ingen data endnu", ikke 0 som fakta

S1-12  GIVEN landing                     THEN ingen login, ingen cookie-wall
       GIVEN adressesøgning              THEN autocomplete på DAR, ingen persondata

S1-13  GIVEN e-mail-ordre                THEN 201 CURIOS + pseudonym + order.created
       GIVEN samme husstand+scope igen   THEN 409 ORDER_ALREADY_ACTIVE
       GIVEN magic link udløbet          THEN ny link kan udstedes uden dublet

S1-14  GIVEN alle fixtures               THEN reproducerbare med seed
       GIVEN guard-tests                 THEN grønne før S1 må merges
```

**Definition of Done S1:** Alle guards grønne · zone-lækage-test bestået · `dwelling_count` verificeret mod FX-01/02 · ADR-002/003/004 opdateret · runbook `ingestion-failed` skrevet · DK-review på S1-06/07/13.

---

# DEL C — Kravspecifikation til UA-teamet

**Dokument:** `REQ-UA-001 · Leverance- og sikkerhedskrav`
**Status:** Vedlægges kontrakten som bilag. Underskrives før første commit.

---

## C1. Formål og rollefordeling

| Part | Ejer |
|---|---|
| **Optata (DK)** | Kravspecifikation, kontrakter, guards, kundekontakt, salg, juridisk grundlag, prod-drift |
| **UA-team** | Implementation inden for kontrakterne, tests, adapters, UI, workers |
| **DK-reviewer** | Godkendelse af al finansiel, juridisk og sikkerhedskritisk logik |

**Kerneprincip:** *Kontrakten er specifikationen. Koden er output. CI er dommeren.*

---

## C2. Hvad I bygger — og hvad I ikke må røre

| Område | Tilladelse |
|---|---|
| UI-komponenter, layouts, kort, autocomplete | ✅ Fri (AI-assisteret) |
| CRUD, DTO'er, API-klienter, integrationer | ✅ Fri inden for OpenAPI |
| Ingestion-adapters, feltmapping, transformation | ✅ Assist — valideringsregler specificeret af DK |
| Unit- og contract-tests | ✅ Assist — mod DK-skrevne guards |
| Migrations | ⚠️ Assist — **altid** DK-review + rollback-plan |
| **Redaction-regler** | ❌ Skrives af DK |
| **Reveal-guards + vault-adgang** | ❌ Skrives af DK |
| **Refusion, tinglysning, fortrydelsesfrist** | ❌ Skrives af DK, testes mod rigtige sager |
| **RLS-policies, zone-adskillelse, DB-roller** | ❌ Skrives af DK |
| **Samtykke, retention, sletning** | ❌ Skrives af DK + jurist |

**AI-kodegenerering er opmuntret** i de grønne felter og **forbudt** i de røde. Begrunnelse: AI er stærkest i UI og transformation, svagest præcis dér hvor pengene og ansvaret ligger.

---

## C3. Miljøer og data (ufravigeligt)

| Miljø | Data | Adgang |
|---|---|---|
| local / dev | **Kun syntetisk** (`make dev`, seed) | UA |
| staging | Syntetisk + zone A (offentlige) | UA + DK |
| **prod** | Zone A/B/C, **EU-only** | Kun DK-drift. UA: break-glass med godkendelse, tidsbegrænset, auditeret |

**Forbud:**
- Ingen prod-dump, prod-eksport eller prod-kopi til dev/staging — nogensinde.
- Ingen persondata i prompts til LLM uden for EU.
- Ingen persondata i logs, screenshots, tickets eller chat.
- Ingen rigtige CPR, navne, telefonnumre eller e-mails i fixtures. Generatoren emitterer **ugyldige** numre og `example.invalid`.

**Håndhævelse:** CI-gate 10 scanner fixtures. Overtrædelse = kontraktbrud, ikke en advarsel.

---

## C4. Leveranceproces

```
1. DK leverer: kontrakt (OpenAPI/event-schema) + guards + acceptkriterier
2. UA implementerer mod kontrakten (AI-assisteret hvor tilladt)
3. UA kører `make ci` lokalt — alle 12 gates grønne
4. PR oprettes med: issue-ID, ADR-reference, testbevis
5. CI kører gates 1–12
6. CODEOWNERS-sti → DK-review påkrævet
7. Merge → automatisk deploy til staging
8. Prod-deploy: kun DK, efter feature-flag-godkendelse
```

**Regler:**
- **Kontrakt først.** Ingen kode før `contracts/` er opdateret og godkendt.
- **Guards før feature.** `tests/guards/` oprettes i samme PR — aldrig bagefter.
- **Feature-flags** på alt juridisk ufærdigt (ejer-kontakt, reveal). Deployes mørkt.
- **Ingen direkte push til main.** Ingen force-push. Ingen bypass af CI.

---

## C5. Kvalitetskrav (Definition of Done pr. leverance)

- [ ] Alle CI-gates 1–12 grønne
- [ ] Guard-tests for berørt domæne grønne
- [ ] Contract-tests mod OpenAPI + event-skema grønne
- [ ] Ingen zone B-felter i public/B2B-payload (automatisk scan)
- [ ] Migrations idempotente + rollback-plan dokumenteret
- [ ] Audit dækker alle zone B-kald
- [ ] ADR opdateret ved større beslutning
- [ ] Runbook opdateret ved nyt job/fejltilstand
- [ ] DK-review gennemført på CODEOWNERS-stier
- [ ] Ingen nye afhængigheder med ukendt licens eller kendt CVE

---

## C6. Sikkerhed og adgang

| Krav | Detalje |
|---|---|
| Identitet | Navngivne konti, MFA, ingen delte logins |
| Kode | Signerede commits, branch protection, CODEOWNERS |
| Hemmeligheder | Aldrig i repo. Kun secret manager. Rotation ved personaleændring |
| Adgang | Mindste privilegium. Ingen prod-DB-adgang for udviklere |
| Enheder | Krypteret disk, låst skærm, ingen prod-data på lokale maskiner |
| Afhængigheder | Lockfiles, SAST, licensscan på hver PR |
| Hændelser | Rapportér sikkerhedsafvigelse til DK **inden 24 timer** |

---

## C7. Kommunikation og ritualer

| Ritual | Frekvens | Indhold |
|---|---|---|
| Async standup | Dagligt | Skriftligt: gjort / blokeret / næste |
| Sprint-planlægning | Hver 2. uge | Issues, estimer, afhængigheder |
| Kontrakt-review | Ved behov | DK + UA, før implementation |
| Demo | Hver 2. uge | Kørbare flows mod acceptkriterier |
| Retro | Månedligt | Hvad bremsede, hvad automatiseres |

**Sprog:** Kode, kommentarer, commits, ADR og docs på **engelsk**. Kundevendt tekst og UI på **dansk** (leveres af DK).
**Tidszone:** UA/DK = 1 times forskel. Kerne-overlap 10:00–16:00 CET.
**Eskalering:** Blokering >4 timer → DK-kontakt samme dag. Aldrig "vent og se".

---

## C8. Dokumentation og bus-factor

- **Bus-factor ≥ 2** pr. kritisk komponent: mindst to personer kan deploye og fejlfinde.
- Al viden i repo: ADR, runbooks, inline-kommentarer på ikke-indlysende regler.
- Ingen viden kun i hoveder, chat eller private noter.
- Backup-udvikler (evt. EU-baseret) med repo- og infra-adgang fra dag 1.
- Månedlig **restore-test** af backup — en gate, ikke en øvelse.

---

## C9. Juridiske og kommercielle vilkår

| Punkt | Krav |
|---|---|
| **IP** | Fuld overdragelse af al kode, dokumentation og afledte rettigheder til Optata ApS ved betaling |
| **Fortrolighed** | NDA dækkende forretningsmodel, data, kunder og arkitektur |
| **Genbrug** | Forbud mod genbrug af Optata-specifik kode, kontrakter eller data i andre projekter |
| **Databehandling** | Ingen persondata behandlet. SCC + TIA på plads som værn, ikke som arbejdsgrundlag |
| **Subprocessorer** | UA-teamet må ikke indsætte underleverandører uden skriftlig godkendelse |
| **Valuta** | Kontrakt i EUR/USD → 5–10 % FX-buffer i Optatas budget |
| **Opsigelse** | Løbende overdragelse: repo, docs, credentials, runbooks. Ingen lock-in |
| **Kontinuitet** | Ved afbrydelse (strøm, mobilisering, konflikt): backup-udvikler overtager inden 5 arbejdsdage |

---

## C10. Onboarding-checklist (uge 1)

- [ ] Kontrakt + NDA + IP-bilag underskrevet
- [ ] REQ-UA-001 læst og underskrevet
- [ ] Navngivne konti + MFA oprettet
- [ ] Repo-adgang, branch protection verificeret
- [ ] `make dev` kører lokalt med syntetiske data
- [ ] `make ci` kører og viser alle 12 gates
- [ ] Arkitektur-gennemgang: zoner, invarianter, guards (2 timer, DK)
- [ ] Gennemgang af forbudte felter (C2) med konkrete eksempler
- [ ] Eskaleringskanal + kontaktperson aftalt
- [ ] Første issue: S0-01 (repo-skelet)

---

## C11. Hvad succes ser ud som efter 8 uger

| Milepæl | Bevis |
|---|---|
| S0 grøn | UA kan arbejde uden persondata, CI blokerer fejl |
| S1 grøn | Adresseopslag returnerer alt, `dwelling_count` korrekt på FX-01 |
| Rapport live | Anonym bruger ser områdeprofil med kilde+dato |
| Ordre registreret | CURIOS-ordre med dedup, `order.created` i event-log |
| Ingen sikkerhedsafvigelser | 0 vault-adgang uden for disclosure, 0 zone-lækage |

---

## Afsluttende note

De tre artefakter hænger sammen: **ADR'erne** er beslutningerne, **backloggen** er rækkefølgen, **kravspecifikationen** er rammen UA-teamet leverer inden for. Ingen af dem kan stå alene.

Den eneste åbne beslutning er **ADR-013 (data engineer fra md. 2)**. Den afgør, om S1 kan starte i uge 3 — og dermed om den første krone kommer i måned 4.

*Næste skridt kan være (a) S2-backloggen (agent + review-UI + faktura) som konkrete issues, (b) kontrakt-filerne i fuld tekst (`openapi.yaml` + `events/*.json`), eller (c) DK-reviewerens checkliste — hvad der præcist skal gennemgås før merge i de røde felter.*