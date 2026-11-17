# Optata — Arkitektur

**Version:** 1.1 · **Status:** Gældende · **Ejer:** DK-reviewer
**Læses før al kode.** Afvigelse kræver ADR + DK-godkendelse.

---

## 1. Formål og afgrænsning

Optata er et **ordrebogssystem med event-historik** oven på et offentligt
ejendomsregister. Det er ikke en boligportal, ikke et mæglersystem og ikke
en annonceplatform.

Systemet gør verificeret boligefterspørgsel synlig, anonym og handlingsbar:
købere registrerer ønsker, ejere og professionelle reagerer på dem, og
kontakt udveksles kun ved gensidig enighed.

Ordrebogen matches mod **begge sider**: skjult efterspørgsel hos ejere
(M1/M2) og **offentligt udbud via licenserede feeds (M3)**. Udbuddet er
en trigger — ordrebogen er aktivet.

**Tre zoner, tolv moduler, tretten invarianter.** Alt andet er implementation.

---

## 2. Datazoner

| Zone | Indhold | Dev-adgang | Eksport | Beskyttelse |
|------|---------|-----------|---------|-------------|
| **A** | BBR, DAR, EBR, Matrikel, VUR, plan, CVR, DST, claims, rapporter | ✅ Tilladt | ✅ Tilladt | Licens + kildehenvisning |
| **B** | Identitet, ordrer, verifikationsbeviser, ejerskab, tråde, samtykke | ❌ Aldrig | ❌ Aldrig | EU-prod, RLS, kryptering, audit |
| **C** | Aggregeret efterspørgsel, tæthed, gap-analyse | ✅ Syntetisk | ✅ Licenseret | k≥5, afrunding, suppression |

**Regler:**
- Zone C bygges kun via kontrollerede aggregationsjobs fra B.
- Front-end læser kun `PublicProfile` + A/C. Ingen query må joine til vault.
- Udvikling og staging bruger **syntetiske data** (deterministisk generator,
  vandmærket `_synthetic:true`). Aldrig prod-dumps.
- Al produktion hostes i EU. Adgang til prod er break-glass med audit.

---

## 3. Nøgler

| Nøgle | Hvad | Bruges til |
|-------|------|-----------|
| **DAR adresse-id** | Boligen/enheden | Alt efterspørgsel knyttes hertil |
| **BFE** | Ejendomsobjekt på tværs af registre | Samling af BBR/matrikel/EJF/VUR |
| **Matrikel-id** | Jordstykket | Geometri, grund, planforhold |
| **area_id** | Postnummer eller bydel | Tæthed, abonnement, eksklusivitet |
| **street_id** | Vejen | Gade-scope (M3-match uden adresse-id) |
| **municipality_id** | Kommunen | Kommune-scope (M3-match uden adresse-id) |
| **pseudonym** | Personen (K-7F3A / E-2B91) | Al visning, al kommunikation |

**BFE → adresse-id er 1:mange.** Andelsforeninger og udlejningsejendomme
er kernemodellen, ikke specialtilfælde. `dwelling_count` (nævneren i
tætheden) = aktive DAR-adresser med BBR-boliganvendelse.

**CPR lagres aldrig.** Kun broker-pseudonym + afledte attester.

---

## 4. Moduler

| Modul | Ansvar | Cases |
|-------|--------|-------|
| `registry` | Kilde-adapters, bitemporal store, PostGIS, tæthed | C1,C2,C4,C7 |
| `reports` | Cachede zone A-profiler, PDF/web | C1,C4,C7 |
| `agent` | Claim-ekstraktion, proveniens, review-kø | C7 |
| `orderbook` | Ordrer, events, dedup, integritet | C1,C2,C9 |
| `identity` | MitID/OIDC, pseudonym, vault, step-up, ejerskab | C2,C3,C6,C8 |
| `verification` | Attest, review, udløb, nedgradering | C8,C9 |
| `disclosure` | PublicProfile, attester, **eneste vault-indgang** | C3,C4,C5,C6 |
| `relay` | Tråde, beskeder, redaction, rate limit | C3,C5,C6 |
| `consent` | Grants, afmelding, retention, audit | C3,C5,C9 |
| `billing` | Abonnement, eksklusivitet, engangsgebyr, faktura | C4,C5,C6,C7 |
| `insights` | Zone C-aggregater, k-anonymitet, gap | C6,C7 |
| `listings` | Feed-adapters, licenshåndhævelse, bitemporal udbudsmodel, status-propagering, geokodning | C10 |

**Arkitekturstil:** Modulær monolit (`apps/api`) + workers
(`ingestion`, `agent_runner`, `matching`, `expiry`, `retention`).
Ingen microservices i år 1. `core/*` må ikke importere `apps/*`.
Moduler kommunikerer via domæne-events eller eksplicitte interfaces.

**Stack:** Python/FastAPI · PostgreSQL+PostGIS · Next.js · Redis+kø ·
EU-objektlager · EU-LLM-endpoint · Terraform · OIDC via MitID-broker.

---

## 5. De tretten invarianter

Disse må aldrig brydes. Hver har en guard-test i `tests/guards/`.

1. **BFE → adresse-id er 1:mange.** Ingen upsert må aggregere enheder væk.
2. **Al registerdata er bitemporal.** `valid_from/valid_to` + `recorded_at`.
   Historik overskrives aldrig.
3. **`order_event` er append-only.** `REVOKE UPDATE, DELETE`.
   Skemaændringer upcastes ved læsning, aldrig i store.
4. **Kun `disclosure` må læse vault.** Håndhæves med DB-rolle, ikke app-logik.
5. **Kun VERIFIED med gyldig attest udløser ejer-kontakt.** Og kun på
   den konkrete adresse (M1) — aldrig fra område-ordrer (M2).
6. **Ejerskabsverifikation kræves før visning af interesse.**
   Ejerskifte tilbagekalder automatisk.
7. **Reveal kræver seks guards i én transaktion:** pakke accepteret ∧
   betaling captured ∧ begge samtykker ∧ frisk step-up (≤5 min) ∧
   gyldig attest ∧ gyldigt ejerskab.
8. **Zone C: k≥5 + afrunding til 5 + komplementær suppression.**
   Max 3 dimensioner. Mindste geo = postnummer. Ingen daglige deltas.
9. **Én aktiv ordre pr. husstand+scope.** Samboende = co-buyer på samme ordre.
10. **Sletning er to-lags.** Zone B slettes hårdt; pseudonym event-historik,
    audit og bogføring bevares. Tombstone må ikke kunne mappes til en person.
11. **Ingen listing importeres uden aktiv `license_ref`.**
    Ingen scraping af portaler eller mæglersites — kun licenserede feeds.
12. **M3 kontakter KØBEREN, aldrig ejeren.** Kun VERIFIED køber må
    kontakte mægler. Mægler skal CVR-matche udbuddets agent_org.
13. **Salgspakken tilbydes KUN i M1** (privat ejer uden mægler).
    Aldrig i M3 — mægleren er allerede formidler.

---

## 6. Tilstandsmaskiner

```
ORDER:  CURIOS → QUALIFIED → VERIFIED → MATCHED → IN_DIALOG → AGREED → FULFILLED
            └──────────┴──────────┴─────────→ WITHDRAWN | EXPIRED | ERASED

DEAL:   DIALOG_OPEN → PRICE_AGREED → PACKAGE_OFFERED → PACKAGE_ACCEPTED
            → IDENTITY_REVEALED → FULFILLMENT → COMPLETED | ABORTED

IDENT:  EMAIL → MITID_PRIVATE → (+ ownership_verified pr. adresse)
        MITID_ERHVERV for organisationer (CVR-bundet)

ACCESS: ANONYMOUS → EMAIL_SESSION → AUTHENTICATED → STEP_UP

M3:     LISTING_MATCHED → AGENT_INVITED → IN_DIALOG → AGREED → FULFILLED_BY_AGENT
SCOPE:  MUNICIPALITY ⊃ AREA ⊃ STREET ⊃ ADDRESS
LISTING: ACTIVE → UNDER_OFFER → SOLD | WITHDRAWN | STALE
```

**Progressiv identitet:** anonym browsing → e-mail-ordre → MitID →
bankattest → step-up. MitID på tragtens top ville halvere tætheden.

---

## 7. Sikkerhedsmodel

- **Identitet:** MitID via broker (OIDC). Ingen CPR. Step-up ved følsomme kald.
- **Autorisation:** RBAC + område-scope, håndhævet i RLS.
- **Anonymitet:** Gensidig pseudonymisering. Attest-felter, aldrig dokumenter.
  Budgetintervaller, aldrig præcise beløb.
- **Relay:** Deterministisk redaction (regex → NER → EXIF/OCR → adfærd),
  LLM kun som supplement. Sikkerheden må aldrig afhænge af en model alene.
- **Audit:** Append-only, 5 år, uforanderlig. Skrives **før** data returneres.
- **Trusselsmodel:** `docs/security/stride.md` (vault, relay, reveal).

**P1-alarmer:** vault-adgang uden for disclosure · zone B-felt i public
payload · reveal gennemført uden guards · prod-data i dev.

---

## 8. Drift

| Job | Tid | Ved fejl |
|-----|-----|----------|
| Ingestion (DAR/EBR/EJF/BBR) | 02:00 | Karantæne-rapport; frys tæthed hvis dwelling_count ændres >2 % |
| Expiry (attest/ordre/abonnement) | 03:00 | **Frys mægler-lead-lister** — sælg ikke stale leads |
| Retention/sletning | 04:00 | P2 — et system der ikke sletter, bryder sit løfte |
| Matching | Natligt + event | Genkør pr. område |
| Listing-feeds | Hver 30. min | `feed-failed`; efter 24 t uden opdatering → STALE-markering |
| Listing-reconciliation | Natligt 02:30 | ACTIVE uden feed-træf → STALE, **ikke SOLD** |
| Agent-profil | Ved change-event | Review-kø må ikke tømmes automatisk |
| Backup + restore-test | Dagligt / månedligt | Restore-test er en gate |

**SLO'er:** anonym rapport 99,5 % / p95 <400 ms · relay 99,9 % / p95 <1,5 s ·
reveal 99,9 % korrekt guard-afvisning (fejl her er en hændelse, ikke en bug).

Runbooks: `docs/runbooks/`.

---

## 9. Leverancemodel

Udvikling leveres af et ukrainsk seniorteam med AI-kodegenerering.
Danske stiftere ejer kravspecifikation, kontrakter og kundekontakt.
DK-reviewer godkender al finansiel, juridisk og sikkerhedskritisk logik.

**Kontrakten er specifikationen. Koden er output. CI er dommeren.**

| Felt | AI-generering |
|------|--------------|
| UI, CRUD, DTO'er, API-klienter, adapters | ✅ Tilladt |
| Migrations | ⚠️ Assist + altid DK-review |
| Redaction, reveal-guards, vault-adgang | ❌ Menneske |
| Refusion, tinglysning, fortrydelse | ❌ Menneske + rigtige sager |
| RLS, zoner, samtykke, retention, sletning | ❌ Menneske + jurist |

**CI-gates 1–12** blokerer merge. Ingen overrides. Guards tilføjes i samme
PR som domænekoden — aldrig bagefter.

Se `docs/delivery/REQ-UA-001.md` og `docs/security/dk-review-checklist.md`.

---

## 10. Beslutninger og åbne punkter

Alle større beslutninger dokumenteres som ADR i `docs/architecture/adr/`.

**Accepteret:** ADR-001…012, 014, 015, 016, 017, 018.

**Åbne:**
- **ADR-013** — data engineer fra md. 2 (afgør første indtægt i md. 4)
- **ADR-008** — juridisk formidlingsvurdering af match+relay+reveal
  (jurist uge 6, spørgsmål L1–L3)
- **L32–L37** — juridisk afklaring af udbudsmatch (M3), blokerer S6
  (spørgsmål i `docs/compliance/legal-questions-week6.md`)

**Kalendertid, ikke kodetid — bestilles uge 1:**
Datafordeler-adgang · MitID-broker · medielicens.

---

## 11. Hvor sandheden bor

| Artefakt | Er specifikation for |
|----------|---------------------|
| `contracts/openapi.yaml` | API'ets form og fejl |
| `contracts/events/*.json` | Historikkens form |
| `contracts/feeds/agent-feed.v1.json` | Udbudsfeedets form |
| `tests/guards/*.py` | Sikkerhed og invarianter |
| `design/foundations/tokens.css` | Visuelt udtryk |
| `apps/web/i18n/da.json` | Al brugervendt tekst |
| `docs/compliance/retention.md` | Frister og sletning |

Kode, der afviger fra disse, er forkert — ikke omvendt.
