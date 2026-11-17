# Optata — Arkitektur v2.1

**Status:** Målarkitektur · 17. november 2026  
**Autoritativt grundlag:** `docs/Optata - Projektgrundlag v5.2.md`  
**Ejer:** Stifter + teknisk reviewer  
**Regel:** Ændringer i invariants, zoner, moduler eller transaktionsflows kræver ADR og review. Juridiske release gates er beskrevet i v5.2 §10.

## 1. Formål og systemgrænse

Optata er en modulær markedsplatform, der forbinder registerdata, verificeret efterspørgsel, sælgermandater, strukturerede bud, udførende partnere og samtykkebaseret distribution.

Optata ejer platformens proces- og datalag. Det er ikke ensbetydende med, at Optata må udføre lovregulerede formidleropgaver. Systemet skal understøtte en juridisk godkendt rollefordeling uden at antage, at platformens tekniske kontrol giver en tilladelse.

## 2. Arkitekturprincipper

- Modulær monolit + workers. Ingen mikroservices før dokumenteret behov.
- Kontrakter først: OpenAPI, event schemas og DB-migrationer versionsstyres.
- PostgreSQL/PostGIS med zone-separation, DB-roller og RLS.
- Zone B er lukket som standard; kun eksplicitte service-roller får adgang.
- Alle følsomme handlinger kræver purpose, scope, actor og audit.
- Bitemporalitet bruges på registerfakta; forretningshændelser er append-only.
- Alle eksterne data har source, license, provenance, observed_at og valid-time.
- Feature flags kan slukke features, aldrig omgå guards.
- Syntetiske fixtures er deterministiske og tydeligt vandmærkede.

## 3. Zoner

| Zone | Indhold | Miljø | Hovedkontrol |
|---|---|---|---|
| A | Register, geometri, licenserede listings, claims, rapporter | Dev/test/prod efter kildevilkår | kilde-/licensspor, bitemporalitet, read scopes |
| B | MitID-identitet, ordrer, attester, ejerskabsbevis, samtykke, mandat, bud, kampagneinteraktion, audit | Kun kontrolleret EU-prod for rigtige data | RLS, kryptering, mindst privilegium, retention, audit |
| C | Aggregerede/afledte datasæt til B2B | Licenseret publicering | k-regler + suppression + differens-/re-identifikationskontrol |

k≥5 er ikke alene tilstrækkeligt til anonymisering. Zone C-publicering kræver dokumenteret vurdering af kombinationer, tidsserier, geografisk granularitet, differensangreb og eksterne hjælpedata.

## 4. Moduler og ejerskab

| Modul | Ansvar | Må ikke eje |
|---|---|---|
| registry | registerkilder, bitemporal ejendomsmodel | køber-/sælgeridentitet |
| reports | rapporter og områdeprofiler | rå zone B |
| agent | claims/medieanalyse med provenance | automatisk publicering uden review |
| orderbook | købsintention, status, scope, matching | identitetsvault |
| identity | MitID/OIDC, pseudonymer, sessions | CPR-lagring |
| verification | attestbehandling, reviewer, udløb | mandatbeslutninger |
| disclosure | eneste kontrollerede adgang til identitetsoplysninger | forretningsbeslutninger |
| consent | versioneret samtykke og tilbagekaldelse | skjult samtykkeafledning |
| billing | betaling for platformprodukter | escrow/købesum |
| insights | aggregering, metrics, k-anonymitetskontrol | re-identifikation |
| listings | licenserede udbud, status, attribution | scraping eller uautoriseret videredistribution |
| mandates | SaleMandate, parter, scope, executor, vilkår | antagelse om juridisk formidlingstilladelse |
| offers | OfferLedger, bud, modbud, accept og historik | fri chat eller uautoriseret aftaleindgåelse |
| campaigns | samtykkebaseret kampagnestyring og levering | ekstern kontakt eller målretning uden samtykke |
| relocation | koordinerer flytteforløb, mål, tidslinje, scenarier, afhængigheder og beslutningshistorik | SaleMandate, købsordre, OfferLedger, identitetsvault, finansieringsafgørelser eller juridiske aftaler |


**Grænser:** Et modul skriver kun egne tabeller. Andre moduler bruger kontrakter/domæneevents. Direkte tabeladgang på tværs er forbudt, undtagen eksplicitte read models med ejer og test.

## 5. Nøgler og relationer

- `address_id`: DAR-adresse.
- `bfe_id`: fast ejendom; relation til adresser er 1:mange.
- `matrikel_id`: matrikulær identitet.
- `area_id`, `street_id`, `municipality_id`: versionsbundne geografiske scopes.
- `identity_id`: intern personidentitet, aldrig CPR.
- `household_key`: dedup-nøgle med formålsbegrænset scope.
- `mandate_id`, `offer_id`, `listing_id`, `campaign_id`, `relocation_case_id`: UUID.
- RelocationCase holder typed references til andre modulers aggregates; den ejer eller skriver ikke deres data.
- `source_ref` + `license_ref`: proveniens og brugsret for eksterne data.

Alle relationer mellem personidentitet og ejendom/ordre skal være formålsbundne, RLS-beskyttede og auditerede.

## 6. Ufravigelige invarianter

### Data og adgang
1. BFE→adresse er 1:mange; en BFE må ikke forveksles med en boligadresse.
2. Registerfakta er bitemporale; historik overskrives aldrig.
3. Ordre-, mandat-, bud- og audit-hændelser er append-only; status er en projektion af hændelser.
4. Kun disclosure-service kan læse identitetsvault; support/admin har ingen bypass.
5. Zone B kan ikke læses af public_reader eller almindelige app-roller; DB/RLS håndhæver dette.
6. Alle følsomme handlinger auditeres før data returneres eller sideeffekt udføres.
7. Ingen CPR lagres i DB, logs, events, traces eller fixtures. Transient behandling kræver særskilt dokumenteret godkendelse.

### Efterspørgsel og verifikation
8. Kun VERIFIED med gyldig attest kan afgive bud eller indgå i VERIFIED-density.
9. Attestudløb, tilbagetrækning eller falsk/manglende bevis fjerner VERIFIED-rettigheder øjeblikkeligt.
10. Én aktiv ordre pr. husstand+scope; medkøbere knyttes til samme ordre.
11. Matching skal gemme modelversion, score og reason codes; matchresultat må ikke i sig selv udløse kontakt eller identitetsdeling.

### Mandat og bud
12. SaleMandate kræver identifikation og dokumenteret ret/fuldmagt for alle nødvendige parter; sameje kan ikke reduceres til én owner_identity.
13. Højst ét aktivt, konfliktende mandat pr. ejendom/adresse efter en eksplicit konfliktregel; DB-constraint og transaktion håndhæver dette.
14. Mandat har versionerede vilkår, scope, executor, start/slut, audit og øjeblikkelig suspendering/tilbagekaldelse efter gyldig anmodning.
15. Bud kræver aktivt mandat, VERIFIED-køber, gyldig attest og gyldig budfrist.
16. Bud er append-only. Ændringer/tilbagetrækninger/modbud er nye hændelser, aldrig overskrivning.
17. Accept er en platformshændelse og må ikke betegnes som endelig købsaftale, før den juridiske aftalemodel udtrykkeligt definerer det.
18. Ingen bud, køberidentitet eller kontaktdata eksporteres uden for Optatas rails undtagen via godkendt fulfillment og dataminimeret partneroverdragelse.
19. Mægler-/partneradgang er skæringsmængden af organisationens godkendte scope, aktiv participation license og det konkrete mandat/arbejdsopgave.

### Listings, Campaign og aggregering
20. Listing kræver gyldig license_ref og kildeattribution; ingen scraping.
21. Campaign kræver eget aktivt og licenseret udbud, godkendt indhold, aktivt formålsspecifikt samtykke og alle leveringsguards.
22. Samtykke er eksplicit, versioneret, formålsbundet og tilbagekaldeligt; tilbagekaldelse stopper fremtidig levering.
23. Mute, suppression, quiet hours og frekvenslofter kontrolleres i domænet og ved hver levering.
24. Audience-gulv og k-anonymitet kontrolleres efter samtykke-, mute-, suppression-, relevans- og frekvensfiltrering. Ingen rå modtagerliste eller pseudonymeksponering til annoncør.
25. Listing SOLD/WITHDRAWN/STALE eller licensudløb stopper relevante kampagner og match-notifikationer.
26. Zone C-publicering kræver k≥5 plus suppression og dokumenteret angrebs-/re-identifikationsvurdering.

## 7. Domæneflows

### 7.1 Order → VERIFIED
MitID login → ordre → QUALIFIED → attest upload/review → VERIFIED → udløb/fornyelse. Ingen e-mail-opgradering eller CURIOS.

### 7.2 SaleMandate
DRAFT → PARTIES_PENDING → REVIEW (hvis manuel kontrol) → ACTIVE → SUSPENDED / REVOKED / EXPIRED / COMPLETED.

Mandat aktiveres først, når alle nødvendige parter, ejerskabsbeviser, vilkår og executor-mode er valideret. Sameje repræsenteres som relationer, ikke en enkelt owner_identity-kolonne.

### 7.3 OfferLedger
SUBMITTED → ACKNOWLEDGED → COUNTERED (nyt offer) → ACCEPTED / DECLINED / WITHDRAWN / EXPIRED. Hver statusændring er event. Accept skal indeholde aktuel mandate version, offer version, tidsstempel og actor. Fulfillment startes separat.

### 7.4 Campaign
DRAFT → VALIDATING → REVIEW → APPROVED → SCHEDULED → DELIVERING → COMPLETED; sidegrene REJECTED, STOPPED, CANCELLED. Hver levering revaliderer licens, samtykke, mute, suppression, relevans, frekvens og quiet hours.

### 7.5 Listing
INGESTED → VALIDATED → ACTIVE → UNDER_OFFER → SOLD / WITHDRAWN / STALE / LICENSE_BLOCKED. STALE må aldrig automatisk fortolkes som SOLD.


### Koordineret flytning
27. RelocationCase er et koordinerende aggregate/workflow, ikke en handel, et mandat eller en købsaftale.
28. SaleMandate, købsordre/-interesse og OfferLedger forbliver separate aggregates med hver sin ejer, state machine, juridiske grundlag og audit.
29. RelocationCase må kun læse status gennem versionerede domænekontrakter/read models; direkte cross-module writes og direkte tabelkobling er forbudt.
30. Hvert spor kan startes, sættes på pause, afsluttes eller trækkes tilbage uafhængigt. En statusændring i et spor må ikke implicit aktivere, annullere eller ændre et andet.
31. Case-deltagere og husstandsrelationer skal verificeres og autoriseres. Hver deltager godkender egne handlinger; én persons samtykke kan ikke udvide en anden persons adgang eller mandat.
32. Samtykke er granular per formål, datakategori, modtager, spor og varighed. Linkning af salg og køb giver ikke automatisk ret til at dele identitet, økonomi, bud eller dokumenter på tværs.
33. Scenarier skal vise datakilde, observationstid, gyldighed, status (verificeret/estimat/muligt match/uafklaret), antagelser og usikkerhed. Match må ikke fremstilles som tilgængelig bolig eller garanteret handel.
34. Finansierings- og juridiske forudsætninger markeres som afklaringspunkter; Optata må ikke udlede eller love finansiel/juridisk gennemførlighed uden dokumenteret grundlag og relevant faglig vurdering.
35. Koordinering på tværs følger saga-principperne i C-06 og audit/outbox i C-07. Der findes ingen samlet transaktion, der atomisk gennemfører salg og køb.

## 8. To udførelsesveje

| | DIRECT | AGENT_EXECUTED |
|---|---|---|
| Mandat | Optata-platformen registrerer mandat | Samme |
| Budrails | Optata OfferLedger | Samme |
| Udførelse | Godkendt juridisk/closingpartner | Valgt mægler/udfører |
| Optatas rolle | Platform inden for juridisk godkendt scope | Platform + scoped koordinering |
| Kommercielt vederlag | Ikke fastlagt som endelig pris | Deltagelses-/abonnementsmodel er hypotese |

Begge veje er målarkitektur. Ingen prod-release uden LG-1, LG-5 og relevante betalings-/forbrugerretlige gates.

## 9. API- og eventprincipper

- OpenAPI og event schemas er source of truth; ændres før implementering.
- Alle commands er idempotente og har actor, purpose, scope, idempotency key og trace_id.
- Events har event_id, type, schema_version, occurred_at, recorded_at, actor, zone, aggregate, trace_id og payload.
- Fejl er stabile maskinlæsbare koder; ingen følsomme værdier i fejlbeskeder.
- Eksterne webhooks signeres, replay-beskyttes og valideres mod versioneret schema.

## 10. Juridiske gates

- LG-1: L1–L5 samlet rolle/formidling/ansvar.
- LG-2: L11–L16 persondata/retention/CPR/DPIA.
- LG-3: L26–L31 register-, medie-, tredjelands- og IP-rettigheder.
- LG-4: L32–L37 listings/feed.
- LG-5: L38–L42 mandat, bud, executor og partnerrolle.
- LG-6: L43–L48 Campaign, samtykke, profilering, P2B og retention.
- LG-7: L21–L25 betaling, AML og forbrugerret.

Åbne spørgsmål er release blockers, ikke implicitte godkendelser.

## 11. Implementeringsstatus pr. baseline

| Område | Status |
|---|---|
| S0 skelet, modulgrænser, syntetiske data, CI-baseline | Delvist implementeret; se S0-S1 backlog |
| S1 bitemporal register, testadapter, density, zone A API | Første version implementeret; rigtige adaptere/geometri/UI mangler |
| S2 analyse/agent | Ikke dokumenteret som færdig |
| MitID/ordre/attest/vault | Ikke implementeret |
| SaleMandate | Designmål, ikke implementeret |
| OfferLedger | Designmål, ikke implementeret |
| Campaign | Specifikation, ikke implementeret |
| Listing feed | Kontrakt/spec, ikke produktionsklar |
| Partner fulfillment | Ikke implementeret |
| RelocationCase | Foreslået tværgående proces; ikke implementeret |

## 12. Ændringsstyring

Ændringer af invarianter 12–26, mandat-/budstate, datazoner eller partnerroller kræver:
1. ADR med kontekst, valgmuligheder, beslutning, konsekvenser og status.
2. Opdatering af relevante kontrakter og sprint backlog.
3. Negative tests/guards.
4. Menneskelig review af sikkerhed og juridiske antagelser.

**Denne arkitektur er teknisk målarkitektur, ikke juridisk godkendelse.**


## 13. Tværgående kontrakter

Den fælles rolle- og autoritetsmodel er beskrevet i [Role & Authority Model v1.0](../security/ROLE-AUTHORITY-MODEL-v1.0.md) og ADR-020. Den præciserer invarianterne 4–6, 12, 19 og 27–32. Dokumentet er Proposed og må ikke fortolkes som implementeret adgangskontrol.

De konkrete, testbare krav til least privilege, identitets-/sessionsikkerhed, event-authoritative writes, saga-workflows, audit/outbox, Zone C-release, samtykke-tilbagekaldelse, projections og ingestion findes i:

- [Architecture Contracts v1.0](ARCHITECTURE-CONTRACTS-v1.0.md)

Kontraktdokumentet er **Proposed for technical review**. Det beskriver ønsket kontrolniveau, men betyder ikke, at kontrollerne er implementeret, reviewet eller godkendt til produktion. Auditfund A-01–A-12 forbliver åbne, indtil de konkrete acceptkriterier er opfyldt.
