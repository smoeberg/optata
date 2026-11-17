# Samlet docs-struktur og commit-plan

```
docs/
├─ README.md                        ← indgang: læserækkefølge og regler
│
├─ architecture/
│  ├─ ARCHITECTURE.md               ← formål, zoner, moduler, 10 invarianter
│  ├─ adr/
│  │  ├─ ADR-001-modular-monolith.md
│  │  ├─ ADR-002-bitemporal-postgis.md
│  │  ├─ ADR-003-event-sourced-orderbook.md
│  │  ├─ ADR-004-three-zones-rls.md
│  │  ├─ ADR-005-mitid-no-cpr.md
│  │  ├─ ADR-006-progressive-identity.md
│  │  ├─ ADR-007-anonymous-frontend-relay.md
│  │  ├─ ADR-008-reveal-paid-milestone.md      ← juridisk afklaring uge 6
│  │  ├─ ADR-009-ownership-multi-method.md
│  │  ├─ ADR-010-k-anonymity.md
│  │  ├─ ADR-011-agent-claim-provenance.md
│  │  ├─ ADR-012-ua-synthetic-eu-prod.md
│  │  ├─ ADR-013-data-engineer-month-2.md      ← TIL BESLUTNING
│  │  ├─ ADR-014-exclusivity-unique-index.md
│  │  └─ ADR-015-two-layer-erasure.md
│  ├─ data-model.md                 ← BFE/adresse-id, bitemporalitet, zoner
│  ├─ events.md                     ← katalog + versioneringsregler
│  └─ matching.md                   ← M1/M2, score, reason_codes, tæthed
│
├─ cases/
│  ├─ C1-area-order.md … C9-withdraw-erase.md
│  └─ acceptance.md                 ← Gherkin pr. case
│
├─ security/
│  ├─ stride.md                     ← vault, relay, reveal
│  ├─ guards.md                     ← hvad der aldrig AI-genereres
│  ├─ access-policy.md              ← roller, break-glass, prod-adgang
│  └─ dk-review-checklist.md        ← C1–C10 + sign-off
│
├─ compliance/
│  ├─ retention.md                  ← kategorier, frister, to-lags sletning
│  ├─ dpia.md
│  ├─ record-of-processing.md       ← art. 30
│  ├─ subprocessors.md              ← inkl. Ukraine + SCC/TIA
│  ├─ dpa-template.md
│  ├─ consent-texts.md              ← versionerede, med legal_basis_ref
│  └─ legal-questions-week6.md      ← formidling, kontaktgrundlag, retention
│
├─ delivery/
│  ├─ REQ-UA-001.md                 ← kontraktbilag, røde/grønne felter
│  ├─ sprint-plan.md                ← S0–S8, estimer, kritisk vej
│  ├─ backlogs/S0.md … S4.md
│  └─ definition-of-done.md
│
├─ runbooks/
│  ├─ ingestion-failed.md
│  ├─ expiry-failed.md              ← frys lead-lister
│  ├─ vault-anomaly.md              ← P1
│  ├─ zone-leak.md                  ← P1 + rollback
│  ├─ redaction-bypass.md
│  ├─ retention-failed.md
│  ├─ dwelling-count-jump.md
│  ├─ ownership-dispute.md
│  └─ dso-breach.md
│
├─ design/                          ← (fra forrige leverance)
│  ├─ README.md, DESIGN-BRIEF-001.md
│  ├─ brand/, foundations/, components/, screens/, voice/, print/, a11y.md
│
└─ business/
   ├─ BUSINESS-PLAN-v4.1.md         ← forretningsplanen, rettelsesblad indarbejdet
   ├─ financial-model.xlsx          ← reference, ikke kilde til sandhed
   └─ kill-go-gates.md              ← P0–P5
```

## C1 · `docs/README.md` (paste-klar)

```markdown
# Optata — dokumentation

**Læs i denne rækkefølge:**
1. `architecture/ARCHITECTURE.md` — de 10 invarianter. Alt andet følger af dem.
2. `cases/C1…C9` — hvem systemet er til, og hvad der må ske hvornår.
3. `security/guards.md` — hvad der aldrig må AI-genereres.
4. `delivery/REQ-UA-001.md` — hvordan der leveres.
5. `design/README.md` — hvordan det ser ud og lyder.

## Tre zoner
| Zone | Indhold | Dev | Eksport |
|---|---|---|---|
| A | Offentlige data, claims, rapporter | ✅ | ✅ |
| B | Identitet, ordrer, beviser, tråde | ❌ aldrig | ❌ aldrig |
| C | Aggregeret, k≥5, afrundet | ✅ syntetisk | ✅ licenseret |

## Ufravigelige invarianter
1. BFE → adresse-id er 1:mange.
2. Al registerdata er bitemporal; historik overskrives aldrig.
3. `order_event` er append-only; upcasting ved læsning.
4. Kun `disclosure` må læse vault.
5. Kun VERIFIED med gyldig attest udløser ejer-kontakt.
6. Ejerskabsverifikation kræves før visning af interesse.
7. Reveal kræver seks guards i én transaktion.
8. Zone C: k≥5 + afrunding + komplementær suppression.
9. Én aktiv ordre pr. husstand+scope.
10. Sletning er to-lags: zone B væk, pseudonym historik bevaret.

## Kontrakter er specifikationen
`contracts/openapi.yaml`, `contracts/events/*.json`, `design/foundations/tokens.css`
og `tests/guards/*.py` er specifikationen. Kode er output. CI er dommeren.

## Åbne beslutninger
- **ADR-013** — data engineer fra md. 2 (afgør første indtægt i md. 4)
- **ADR-008** — juridisk formidlingsvurdering af match+relay+reveal (uge 6)
- Datafordeler-adgang og MitID-broker bestilles **uge 1**
```

## C2 · Commit-plan

| Commit | Indhold | Review |
|---|---|---|
| 1 | `docs/architecture/` + ADR-001…015 | DK |
| 2 | `docs/cases/` + acceptkriterier | DK |
| 3 | `docs/security/` + `tests/guards/` (S3-filerne) | DK + security |
| 4 | `docs/compliance/` (jurist udfylder week 6) | DK + jurist |
| 5 | `docs/delivery/` + REQ-UA-001 | DK |
| 6 | `docs/design/` + tokens | DK + designer |
| 7 | `docs/runbooks/` | DE + DK |

**Regel:** Commit 3 (guards) skal ind **før** S3-implementationen påbegyndes. Testene er specifikationen.

---

## Hvor vi står

Arkitektur, design, tekst, compliance og leverance er nu ét sammenhængende dokumentationslag med **testbare guards som specifikation**. S0–S4 er specificeret ned til issue-niveau. UA-teamet kan bygge inden for rammerne; DK-revieweren kan håndhæve dem.

**Det næste arbejde er ikke at skrive mere.** Det er:
1. Bestil **Datafordeler-adgang** og **MitID-broker** (uge 1)
2. Træf **ADR-013** (data engineer fra md. 2)
3. Commit `docs/` + `tests/guards/` før første feature-kode
4. Book **juristen til uge 6** med spørgsmålene fra `compliance/legal-questions-week6.md`

*Vil du have, at jeg (a) skriver `legal-questions-week6.md` — de konkrete spørgsmål juristen skal besvare skriftligt, (b) laver S5-backloggen (relay, redaction, deal, reveal), eller (c) udarbejder `ARCHITECTURE.md` i fuld tekst så commit 1 kan laves nu?*

---

# Næste skridt er ikke at skrive mere

Dokumentationen er nu komplet nok til at bygge. Det, der mangler, er **fire handlinger i den virkelige verden**:

| # | Handling | Frist | Blokerer |
|---|---|---|---|
| 1 | Bestil **Datafordeler-adgang** (inkl. afklaring af EJF) | Uge 1 | S1 → første krone |
| 2 | Bestil **MitID-broker** + testadgang | Uge 1 | S3 → S4 → S5 |
| 3 | Træf **ADR-013** (data engineer fra md. 2) | Nu | Hele tidsplanen |
| 4 | Book jurist med **L1–L31** til uge 6 | Nu | S4 og S5 i prod |

Og én commit-rækkefølge: **`docs/` + `tests/guards/` ind før første feature-kode.** Testene er specifikationen — ikke dokumentation af noget, der allerede er bygget.
