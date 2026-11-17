# Optata — Repository- og platformsaudit

**Dato:** 17. november 2026  
**Auditeret baseline:** `main` @ `7403750d626f19d58c86e09c783679ac0bc94993`  
**Produktbaseline:** Projektgrundlag v5.2 · Arkitektur v2.1  
**Metode:** Statisk gennemgang af repository-træ, produkt-/arkitekturdokumentation, ADR'er, sprintbacklogs, Python-domænekode, API, OpenAPI/event/feed-kontrakter, SQL-migrationer, tests og CI-workflow.  
**Afgrænsning:** Dette er en repository-audit, ikke en penetrationstest, juridisk vurdering, datakildevalidering eller fuld runtime-/loadtest. CI-status er kontrolleret separat.

## 1. Konklusion

**Optata har et reelt teknisk fundament, men er ikke klar til at begynde fuld produktudvikling på tværs af platformen.** Den rigtige beslutning er at fortsætte med en afgrænset S0/S1-hardening og derefter bygge den første vertikale produktstrøm. SaleMandate, OfferLedger, Campaign og MitID må ikke behandles som implementeringsklare moduler endnu.

Repositoryet er i praksis en **modulær monolit under etablering** med en fungerende offentlig register-/område-API, bitemporal ejendomshistorik, syntetisk datagenerator, ingestion-framework, eventvalidering, databasemigrationer og testgrundlag. Det er mere end et tomt skelet. Men mange af de moduler, der gør Optata til den beskrevne markedsplatform, eksisterer kun som mapper, dokumenter eller kontraktudkast.

### Samlet modenhedsvurdering

| Område | Vurdering | Begrundelse |
|---|---:|---|
| Produktretning v5.2 | 8/10 | Samlet retning og faser er tydelige; enkelte gamle beslutninger står stadig som aktive |
| Arkitektur og modulgrænser | 7/10 | God modulær monolit-retning; domænegrænser er endnu ikke omsat til alle konkrete kontrakter |
| S0/S1 teknisk fundament | 6/10 | Register, API, ingestion, fixtures og tests findes; migrations og sikkerhed er stadig markeret som udkast |
| Data- og hændelsesmodel | 5/10 | Bitemporal registermodel og append-only eventtabeller findes; ordredomænet er endnu ikke event-authoritative |
| Sikkerhed og privatliv | 4/10 | Zone/RLS-fundament er begyndt, men der er konkrete rettigheds- og håndhævelseshuller |
| Test/CI | 6/10 | CI kører lint, importgrænser og tests; flere kritiske gates er ikke bygget eller håndhævet |
| Produktfunktionalitet | 2/10 | Ingen brugerflade, MitID, ordreflow, mandat, budbog, kampagne eller partnerflow |
| Produktionsparathed | 2/10 | Ingen godkendte migrations, rigtige integrationer, drift/runbooks eller lukkede juridiske gates |

Tallene er kvalitative auditvurderinger, ikke målte SLA'er.

## 2. Hvad der faktisk findes

### Implementeret i første version

- FastAPI-app med `/health`, områdeopslag, områdeprofil og ejendomsopslag.
- PostgreSQL-adgang for public API gennem read-only `public_reader`.
- Zone A registermodel med DAR-/BFE-/område-relationer og bitemporal versionshistorik.
- Ingestion-runner med adapterprotokol, batch-checkpoints, idempotent behandling og quarantine.
- Syntetisk fixture-generator og loader.
- Density-materialized view med tælling på husstandsniveau og særskilt adgangsbegrænsning.
- Event envelope-validering mod JSON Schema og upcasting af `order.created`.
- OpenAPI-kontrakt for de eksisterende offentlige endpoints.
- Unit-, contract- og guard-tests.
- CI-workflow med Ruff, import-linter og pytest.

### Ikke implementeret som produktfunktioner

- MitID/OIDC-login og identitets-/sessionsikkerhed.
- Bankattest, verification-review, udløb og vault-write path.
- Køberens ordreoprettelse, ordreændringer og command/state-machine-lag.
- SaleMandate, mandatparter, ejer-/fuldmagtsverifikation og tilbagekaldelse.
- OfferLedger, bud/modbud, accept, racekontrol og fulfillment-handoff.
- Licenseret listing-import i drift.
- Campaign-samtykke, audience-beregning, levering og kill-switch.
- Participation license og partner-/mægler-RLS.
- Zone C anonymiseringspipeline og offentlig efterspørgselsvisning.
- Rapport-/analyseprodukt, agent/medieanalyse og frontend.
- Betaling, fakturering, produktionshosting, observability, incident management og driftsrunbooks.

Mappestrukturen `core/identity`, `core/verification`, `core/consent`, `core/disclosure`, `core/relay`, `core/billing`, `core/insights` m.fl. er ikke i sig selv implementering; flere indeholder alene `__init__.py`.

## 3. Kritiske fund — skal løses før produktionsdata eller nye transaktionsflows

### A-01 — Zone A giver bredere databaseadgang end produktkontrakten tilsiger

**Alvor: Høj**

Migration `0001_zones_and_roles.sql` giver `public_reader` og `app_role` SELECT på alle tabeller i zone A. `zone_a.property` indeholder bl.a. `owner_cvr`, men API'et filtrerer feltet fra i `core/registry/read.py`. Den nuværende API-test beviser kun, at HTTP-responsen ikke viser CVR — ikke at database-rollen ikke kan læse feltet.

**Konsekvens:** Sikkerhedsgrænsen afhænger af, at alle fremtidige forespørgsler husker at filtrere feltet. Det er svagere end arkitekturens princip om databasehåndhævelse.

**Anbefalet rettelse:** Giv ikke brede tabelrettigheder til roller, der kun skal bruge udvalgte felter. Brug eksplicit kolonne-grants eller en sikker read-model/view uden ejer-CVR. Tilføj tests, der forsøger direkte SELECT af følsomme felter som `public_reader` og `app_role`.

### A-02 — Ordrens tilstand er ikke event-authoritative

**Alvor: Høj**

`zone_b.orders` har en muterbar `status`-kolonne, og `app_role` har UPDATE-rettighed. `order_event` er append-only, men databasen kræver ikke, at en statusændring ledsages af en gyldig hændelse. Der er endnu ikke et domæne-command-lag, der autoriserer og udfører overgange.

**Konsekvens:** Den autoritative historik kan afvige fra den aktuelle ordrestatus. En applikationsfejl eller direkte SQL-opdatering kan flytte en ordre til en ugyldig tilstand uden korrekt hændelse/audit.

**Anbefalet rettelse:** Definér ordre-state machine og tilladte commands. Gør status til en projektion af eventloggen, eller håndhæv alle ændringer gennem en kontrolleret databasefunktion/transaction boundary. App-rollen må ikke kunne opdatere status direkte. Tilføj negative tests for ugyldige overgange, manglende event, replay og samtidige kommandoer.

### A-03 — Ordre-/scope-modellen er ikke afstemt med v5.2 og ADR-018

**Alvor: Høj**

Migrationen tillader kun `AREA` og `ADDRESS`, mens ADR-018 beskriver `MUNICIPALITY ⊃ AREA ⊃ STREET ⊃ ADDRESS` og stadig siger, at M1-ejerkontakt kræver eksakt adresse. Den sidste regel er i konflikt med v5.2's beslutning om ingen uopfordret ejerkontakt. Områdekoden bruger samtidig niveauerne `MUNICIPALITY`, `ZIP`, `NEIGHBOURHOOD`, `STREET`; produktbaseline og ADR skal have ét entydigt scope-vokabular.

Derudover kræver databasen `address_id` for ADDRESS, men forbyder ikke `address_id` på AREA. Den unikke indeksnøgle bruger `coalesce(address_id, area_id)`, så en AREA-ordre med en address_id kan få en anden dedup-nøgle end en tilsvarende AREA-ordre uden.

**Konsekvens:** Scope- og deduplogikken kan implementeres forskelligt i API, matching, database og produkt.

**Anbefalet rettelse:** Erstat ADR-018's M1-regel, fastlæg én kanonisk scope-enum og dens parent/child relationer, og indfør en check constraint: ADDRESS kræver address_id; øvrige scope-typer skal have den korrekte scope_id og må ikke bære address_id. Tilføj en entydig, transaktionel dedup-regel for husstand + scope + scope_id.

### A-04 — Historiske ADR'er er stadig potentielt normative og ADR-017 er dobbeltbrugt

**Alvor: Høj**

Der ligger både `ADR-017-m3-agent-channel-no-package.md` og `ADR-017-structure-c-supersession.md`. Den gamle ADR-017 har fortsat status “Accepteret” og indeholder M3 invitation, reveal, kontakt og lead-/abonnementsflow, selv om en note øverst siger, at invitation/lead-kanalen er forkastet. ADR-018 er fortsat “Accepteret” og indeholder M1-ejerkontakt. Dokumentationsindekset siger, at accepterede ADR'er er normative.

**Konsekvens:** En udvikler eller agent kan med rimelighed følge en gammel, accepteret beslutning, der strider mod v5.2.

**Anbefalet rettelse:** Giv ADR'er globalt unikke ID'er. Markér den gamle M3-ADR som Superseded/Retired med link til den nye beslutning. Revider ADR-018 og alle referencer til M1/ejerkontakt. Tilføj et ADR-register med ID, status, dato og superseding ADR.

### A-05 — MitID/identitetsgrænsen er ikke implementeret, og RLS-sessionen er kun et mønster

**Alvor: Høj før zone B-produktion**

RLS-politikkerne bruger `current_setting('app.identity_id')`. Det er et almindeligt mønster, men enhver session, der har databaseforbindelse som `app_role`, kan selv sætte en brugerdefineret GUC. Det giver ikke i sig selv en uforfalskelig identitetsgrænse mod SQL, der kører under samme rolle. Der findes endnu ingen MitID/OIDC-verifikation, tokenvalidering, session-binding eller sikker kontekstoverførsel i API'et.

**Konsekvens:** RLS må ikke beskrives som bevist brugeridentitetssikkerhed, før forbindelsesmodellen og trusselsmodellen er fastlagt.

**Anbefalet rettelse:** Design auth/session-grænsen før S3: valider issuer, audience, nonce, state, signatur, assurance og session binding; brug kortlivede forbindelser/transaktioner; vurder om identitetskontekst skal etableres via en betroet gateway/security-definer-funktion eller særskilte DB-roller. Test spoofing af GUC og connection pooling. Ingen zone B-rigtige persondata før review.

### A-06 — Migrationerne er eksplicit AI-udkast og ikke godkendt driftsgrundlag

**Alvor: Høj**

Alle fire SQL-migrationer markerer sig selv som DRAFT/AI-written og kræver menneskelig review. De opretter roller, schemas, RLS, privilegier, triggere og materialized views. Der er ingen dokumenteret uafhængig godkendelse, rollback-/restore-øvelse eller produktionsmigrationstest.

**Konsekvens:** Migrationerne er nyttige som udviklingsprototype, men må ikke bruges som sikkerhedsbevis eller produktionsschema.

**Anbefalet rettelse:** Gennemfør særskilt DB/security-review af hver migration. Tilføj least-privilege privilege matrix, test af rollemedlemskab/default privileges, migration fra tom DB og fra forrige version, backup/restore og destructive-change gate. Markér review med reviewer, commit, dato og scope.

## 4. Vigtige arkitektur- og datakvalitetsfund

### A-07 — Manglende referentiel integritet for ordre-adresse

`zone_b.orders.address_id` har ikke foreign key til `zone_a.property(address_id)`. Det er muligt at oprette en adresseordre med en ikke-eksisterende eller forældet adresse. Der mangler også en eksplicit regel for, hvordan ordre-scope håndteres ved adresse-/områdeændringer.

**Rettelse:** Indfør en stabil adresseidentitet/reference med FK eller en valideret domain reference, og test ukendt, lukket, flyttet og ændret adresse.

### A-08 — Event-kontrakterne dækker ikke endnu de nye kerneaggregater

Envelope og eventtyper er primært PROPERTY og ORDER. Der findes ingen autoritative kontrakter for `mandate.*`, `offer.*`, `consent.*`, `listing.*`, `campaign.*` eller `participation.*`. Event envelope tillader desuden kun et begrænset sæt aggregate kinds, hvor MANDATE, OFFER, LISTING og CAMPAIGN mangler.

**Rettelse:** Definér event-katalog, aggregate IDs, idempotency, causation, actor/scope, versionering, retention og outbox/inbox-strategi før de tilsvarende moduler bygges.

### A-09 — Eventvalidering er ikke det samme som event-persistens eller autorisation

`validate_event` kontrollerer schema og forbudte payload keys. Det sikrer ikke, at afsender må udføre handlingen, at eventen er den lovlige næste tilstand, at event_id er idempotent i alle write paths, eller at event og projektion committes atomisk.

**Rettelse:** Etabler én event append service/transaction boundary med autorisation, state transition, event persistence, projection update og audit i samme transaktion. Overvej transactional outbox til workers.

### A-10 — Ingestion runner mangler håndhævet single-writer/cursor-kontrakt

Runneren forudsætter, at adapteren leverer stigende cursor, men kontrollerer ikke selv monotonicitet. Der er heller ingen synlig lås pr. source, der forhindrer to samtidige runs i at læse samme checkpoint og skrive konkurrerende checkpoints.

**Konsekvens:** Parallelle ingestion-jobs kan behandle batches overlappende eller flytte checkpoint uforudsigeligt. En fejlformet adapter kan bryde den forudsatte rækkefølge.

**Rettelse:** Lås source/checkpoint transaktionelt (fx advisory lock eller row lock), valider cursor progression, og test to samtidige workers, retry, crash mid-batch og out-of-order input.

### A-11 — Registerets geografi-/BBR-koder er fortsat placeholder- og pilotlogik

`BOLIGKODER = {120,130,140}` er markeret som placeholder, og rigtige BBR-koder skal fastlægges med adapteren. Geografiske niveauer og parent-links mangler dokumenteret datakilde-/licensvalidering. Areal-/årsfelter castes fra JSON til numeric/int i SQL uden en synlig quarantine-/quality policy i read path.

**Rettelse:** Definér datadictionary, kilde-/licensmatrix, kodeversioner, geometri/områdehistorik, valideringsregler og håndtering af manglende/ugyldige værdier før rigtige data.

### A-12 — Zone C er ikke bygget; rå density er kun internt prototypegrundlag

Density-viewet er korrekt placeret i zone B og ikke læsbart for applikationsroller. Men k-anonymitet, suppression, differensangreb, tidsserie- og småcellekontrol er ikke implementeret. v5.2 siger korrekt, at k≥5 ikke er anonymiseringsgodkendelse.

**Rettelse:** Hold efterspørgselslaget skjult udadtil indtil Zone C-pipeline og privacy review er færdige. Design test for gentagne forespørgsler, differens, overlappende geografier og ændringer over tid.

## 5. API, drift og udvikleroplevelse

- API'et er bevidst kun read-only Zone A. Det er godt for første pilot, men der findes ingen command API, auth middleware, idempotency keys, rate limits, pagination-kontrakter eller partner scopes.
- Trace ID tilføjes, men der er endnu ikke struktureret audit-/observability-korrelation, metrics, tracing, alerting eller incident runbooks.
- `/properties/{address_id}` og områdeprofiler cachelagres offentligt i fem minutter. Det er acceptabelt for nuværende offentlige facts, men cache-policy skal genovervejes, når licensstatus, rettelser eller sletningskrav påvirker data.
- `docker-compose.yml` er kun lokal udviklingsdatabase; ingen deployment-/staging-/production-konfiguration eller secrets-management er dokumenteret.
- `pyproject.toml` bruger åbne minimumsversioner (`>=`) og repositoryet har ingen lockfil. Reproducerbarhed og supply-chain kontrol er derfor begrænset.
- CI kører på PR og push til main, og bruger Ruff, import-linter og pytest. Der er ikke SAST, secret scanning, dependency/license scanning, SBOM, type checking, migration drift/destructive checks eller E2E.
- `docs/ci-gates.md` angiver selv, at gates 6–8 og 12 ikke er bygget, gate 9 er delvis, og menneskelig review/branch protection ikke er håndhævet.
- Ingen aktuelle migrations- eller sikkerhedsreview-signaturer er registreret.

## 6. Dokumentationskonflikter, der skal ryddes op

1. v5.2-headeren siger fortsat “beslutningsbaseline til stiftergodkendelse”, og autoritetsnoten siger “når PR'en er godkendt”, selv om PR #7 nu er merged. Ret status til gældende/vedtaget baseline.
2. ADR-017 er dobbeltbrugt og den gamle M3-ADR fremstår accepteret.
3. ADR-018 fastholder M1-ejerkontakt og ældre scope-model.
4. Flere gamle bilag/designfiler indeholder stadig invitation/reveal, owner outreach, pris- og mandatantagelser. Designindekset advarer om nogle, men der bør være tydelige historiske banners i de enkelte dokumenter.
5. `docs/ci-gates.md` og v5.2 skal holdes synkroniseret, så “implemented” ikke forveksles med “reviewed/approved”.
6. V5.2 nævner S0/S1 status som delvist implementeret; det er en rimelig status, men hver backlogopgave bør linke til konkret kode, test og kendte begrænsninger.

## 7. Anbefalet udviklingsrækkefølge

### Sprint A — S0/S1 hardening (start her)

1. Luk A-01: least-privilege zone A grants.
2. Luk A-02: beslut event-authoritative order state og fjern direkte status-update.
3. Luk A-03/A-07: kanonisk scope- og adresseintegritet.
4. Luk A-04: ADR-register og oprydning af M3/M1-beslutninger.
5. Luk A-05: dokumenteret identitets-/DB-session threat model — før S3.
6. Luk A-06: menneskelig DB/security review af migrationerne.
7. Luk A-10: single-writer ingestion og cursor tests.
8. Opdater kontrakter og guards, så de matcher v5.2.

**Exit-kriterier:** Alle høje fund lukket eller accepteret med dokumenteret risiko; tests beviser negative cases; migrations er reviewed; ingen gamle normative modstridende beslutninger.

### Sprint B — Første vertikale pilot: Zone A register/områdeprofil

1. Vælg ét afgrænset geografisk pilotområde.
2. Afklar skriftlig datakilde- og licensret for DAR/BBR/geografi.
3. Implementér én rigtig adapter bag eksisterende ingestion-kontrakt.
4. Kvalitetsmålinger, quarantine-review og kildeproveniens.
5. Stabil områdeprofil med tydelig kilde-/dato-/syntetisk status.
6. Først derefter frontend/rapportleverance og brugertest.

**Exit-kriterier:** Datarettigheder dokumenteret, datakvalitet målt, replay/idempotency bevist, fejl håndteres, rapporter kan reproduceres.

### Sprint C — S3 identitet og ordre (kun testmiljø først)

1. MitID broker- og OIDC-kontrakt.
2. Identity/session threat model og sikker DB-kontekst.
3. Verification evidence lifecycle og reviewer workflow.
4. Order aggregate, commands, event store og projections.
5. Household/co-buyer, scope og dedup.
6. Expiry worker og negative guards.
7. LG-2/DPIA/retention-review før virkelige personer.

**Exit-kriterier:** Komplet testflow med syntetiske identiteter; spoofing/replay/expiry/parallelle requests testet; sikkerhedsreview signeret.

### Sprint D — S4/S5/S6 designkontrakter, ikke produktion

Når S3 fundamentet er solidt, kan mandat, bud og campaign specificeres yderligere. De skal ikke implementeres som rigtige transaktionsflows, før relevante juridiske gates er skriftligt lukket. Start med domain contracts og testmodeller; ingen rigtig ejer/køber/partner.

## 8. Hvad vi ikke bør gøre endnu

- Ikke starte mikroservices.
- Ikke bygge alle UI-skærme før den første vertikale data-/ordreflow er bevist.
- Ikke integrere rigtige købere, ejere eller mæglere.
- Ikke importere data uden licens- og behandlingsgrundlag.
- Ikke bygge Campaign-delivery eller public demand density.
- Ikke implementere DIRECT/AGENT_EXECUTED handel eller opkræve transaktionsrelaterede gebyrer.
- Ikke betragte en grøn CI-run som menneskelig sikkerheds- eller juridisk godkendelse.

## 9. CI-status ved audit

GitHub Actions-run for merge-commit `7403750d626f19d58c86e09c783679ac0bc94993` blev afsluttet med **success** den 17. november 2026. Det bekræfter, at det nuværende CI-workflow passerede på denne commit. Workflowet kører dog kun Ruff, import-linter og pytest; det dækker ikke de manglende gates beskrevet ovenfor. Der blev ikke fundet særskilte commit statuses i combined-status endpointet, men Actions-run er grøn.

## 10. Endelig anbefaling

**Optata er klar til kontrolleret, afgrænset udvikling — ikke til bred featureudvikling eller produktion.**

Den stærkeste vej er:
1. Hardening af S0/S1 og lukning af de konkrete sikkerheds-/modelkonflikter.
2. Et rigtigt, licenseret Zone A-pilotdatasæt i ét område.
3. En gennemtestet MitID + VERIFIED ordreflow i testmiljø.
4. Derefter mandat/bud/campaign, styret af juridiske gates.

Det bevarer den ambitiøse platformretning uden at bygge transaktions- og persondatafunktioner oven på et endnu uafklaret sikkerheds- og datagrundlag.
