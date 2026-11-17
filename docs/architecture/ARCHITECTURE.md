# Optata — Arkitektur v2.0
Status: Gældende · Afstemt med projektgrundlag v5.1 · Ejer: DK-reviewer
Afvigelse kræver ADR + DK-godkendelse.

## 1. Formål
Optata er et efterspørgselsdrevet boligmarked. Vi ejer origination,
mandat, budproces og prisdannelse. Mæglere deltager i vores rails,
fordi efterspørgslen og mandaterne ligger her.

Fire lag: register (zone A) · ordrebog (verificeret efterspørgsel) ·
marked (mandat + bud) · distribution (analyse, rækkevidde, API).

## 2. v5.1 — gældende beslutninger
- MitID fra starten. Ingen e-mail-ordrer, intet CURIOS-niveau.
- Ingen uopfordret kontakt til ejere. Ejeren logger selv ind.
- Ejersiden er mandat-indgang med 12 måneders adgang.
- Al notifikation er frivilligt tilvalg (opt-in).
- Digital Post kun efter aftale med leverandør.
- M3-lite forkastet: køberen får aldrig mæglerens kontaktdata.

## 3. Datazoner
A: offentlige registre, claims, udbud (licens), rapporter — dev tilladt.
B: identitet, ordrer, attester, mandater, bud, kampagner, samtykke —
   kun EU-prod, RLS, kryptering, audit. Aldrig dev, aldrig eksport.
C: aggregeret, k>=5, afrundet, komplementær suppression — licenseret.

## 4. Nøgler
DAR adresse-id · BFE (1:mange til adresser) · matrikel-id ·
area_id · street_id · municipality_id (DAGI) · pseudonym.
CPR lagres aldrig.

## 5. Moduler (14)
registry · reports · agent · orderbook · identity · verification ·
disclosure · consent · billing · insights · listings ·
mandates · offers · campaigns

Modulær monolit + workers: ingestion, agent_runner, matching,
expiry, retention, feeds, campaign_delivery, reputation.
core/* må ikke importere apps/*. Kommunikation via domæne-events.

## 6. De 20 invarianter
1.  BFE → adresse-id er 1:mange.
2.  Al registerdata er bitemporal; historik overskrives aldrig.
3.  order_event, offer og audit er append-only; upcast ved læsning.
4.  Kun disclosure må læse vault.
5.  Kun VERIFIED med gyldig attest må kontakte ejer eller afgive bud.
6.  Ejerskabsverifikation kræves før visning af interesse;
    ejerskifte tilbagekalder automatisk.
7.  Reveal kræver accepteret bud ∧ gensidigt samtykke ∧ frisk step-up
    ∧ gyldig attest ∧ gyldigt ejerskab — i én transaktion.
    DIRECT tillige betaling; AGENT_EXECUTED tillige CVR-match.
8.  Zone C: k>=5, afrunding til 5, komplementær suppression,
    max 3 dimensioner, mindste geo = postnummer.
9.  Én aktiv ordre pr. husstand+scope; samboende = co-buyer.
10. Sletning er to-lags: zone B væk, pseudonym historik bevaret.
11. Ingen listing importeres uden aktiv license_ref. Ingen scraping.
12. M3 kontakter køberen, aldrig ejeren. Mægler skal CVR-matche
    udbuddets agent_org.
13. Salgspakken tilbydes kun i DIRECT (ejer uden mægler).
14. Mandat kræver MitID + ejerskabsbevis for ALLE ejere.
    Ét aktivt mandat pr. adresse. Tilbagekaldelse øjeblikkelig.
15. Bud kræver VERIFIED køber med gyldig attest. Append-only.
16. Intet bud, ingen accept, ingen identitetsudveksling uden for
    Optatas rails. Ingen eksport af ordrebog, bud eller kontakt.
17. Mægleradgang = (postnummer ∩ mandat hvor de er udfører).
18. Al mægler→køber-kommunikation går gennem Optatas inbox.
    Audience >=25 og k>=5 på alle celler.
19. Markedsføringssamtykke er eksplicit, formålsbundet, tilbagekaldeligt.
    Loft og mute håndhæves i domænet.
20. Kampagner kræver eget aktivt udbud med licens, struktureret
    indhold, attribution og scanning. Ingen eksterne kontaktveje.

## 7. Tilstandsmaskiner
ORDER:   ACTIVE → MATCHED → OFFER_SUBMITTED → ACCEPTED → FULFILLED
         └→ PAUSED | WITHDRAWN | EXPIRED | ERASED
MANDATE: DRAFT → ACTIVE → SUSPENDED | REVOKED | EXPIRED
OFFER:   SUBMITTED → ACKNOWLEDGED → COUNTERED → ACCEPTED | DECLINED | EXPIRED
LISTING: ACTIVE → UNDER_OFFER → SOLD | WITHDRAWN | STALE
CAMPAIGN:DRAFT → REVIEW → APPROVED → SENT → STOPPED | REJECTED
IDENT:   MITID_PRIVATE (+ ownership pr. adresse) | MITID_ERHVERV (CVR)
ACCESS:  AUTHENTICATED → STEP_UP  (ingen anonym identitet, ingen e-mail-ordre)

## 8. Markedets to veje
DIRECT:          mandat hos Optata · bud i Optata · advokatpartner
                 gennemfører · sælger betaler 10.000 kr. fast gebyr
AGENT_EXECUTED:  mandat hos Optata · bud i Optata · valgt mægler
                 udfører · Optata tjener deltagelsesabonnement
Default er DIRECT. Mægleren er sælgers tilvalg, ikke en port.

## 9. Sikkerhed
MitID via broker (OIDC), ingen CPR. Step-up <=5 min ved følsomme kald.
RLS i DB. Audit append-only 5 år, skrives før data returneres.
Indholdsscanning: deterministisk først, LLM som supplement.
P1: vault-adgang uden for disclosure · zone B i public payload ·
reveal uden guards · prod-data i dev · kampagne uden samtykke.

## 10. Drift
ingestion 02:00 · feeds hver 30 min · reconciliation 02:30 ·
expiry 03:00 (fejl → frys lead-lister) · retention 04:00 ·
campaign_delivery løbende med loft · reputation natligt.
STALE ≠ SOLD. dwelling_count-ændring >2 % → frys tætheds-KPI.

## 11. Leverancemodel
UA-seniorteam + AI-kodegenerering. DK-reviewer ejer guards,
migrations, finansiel/juridisk logik, RLS, samtykke, retention.
Kontrakten er specifikationen. Koden er output. CI er dommeren.
Guards tilføjes i samme PR. Branch protection håndhæves.

## 12. Hvor sandheden bor
contracts/openapi.yaml · contracts/events/*.json ·
contracts/feeds/agent-feed.v1.json · tests/guards/*.py ·
design/foundations/tokens.css · apps/web/i18n/da.json ·
docs/compliance/retention.md

## 13. Åbne punkter
ADR-013 (data engineer fra md. 2) · L38–L40 (mandat/bud/positionering)
· L43–L44 (kampagnesamtykke og profilering) · Datafordeler inkl. EJF
og DAGI · MitID-broker · Digital Post-aftale · mægler-feed-aftale.
