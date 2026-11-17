# OPTATA — (a) Leveranceplan S1–S7 · (b) Retention- & slettepolitik · (c) Demand Pro-kontrakt

---

# DEL A — Leveranceplan med estimer og afhængigheder

## A1. Team og kapacitet

| Rolle | Fra | Kapacitet | Opgave |
|---|---|---|---|
| Stifter A (DK) | md. 1 | ~50 % byg / 50 % salg | Spec, review-kø, kundekontakt |
| Stifter B (DK) | md. 1 | ~30 % byg / 70 % salg | Spec, attester, jura-styring |
| **Data engineer (UA senior)** | **md. 2** ← se A5 | 100 % | Registry, ingestion, PostGIS, tæthed |
| Fullstack (UA senior) | md. 3 | 100 % | Web, ordre-flow, relay, admin-UI |
| DK reviewer (fractional) | md. 3 | ~20 % | Guards, migrations, finansiel logik |
| Data/product (UA) | md. 20 | 100 % | Demand Pro, insights |

**Effektiv byggekapacitet år 1:** ~2,3 FTE + AI-løft. Estimer nedenfor er **persondage inkl. AI-assistance**, men **ekskl. review og tests af guards** (de lægges oveni som DK-tid).

## A2. Sprint-plan

| Sprint | Indhold | Estimat | Hvem | Kalender | Kritisk afhængighed |
|---|---|---|---|---|---|
| **S0** | Repo, IaC, EU-miljøer, zoner, syntetisk generator, CI-gates 1–12 | 12 pd | Data eng + DK | Uge 1–3 | Ingen — **start her** |
| **S1** | Registry (DAR/EBR/BBR/VUR), bitemporalitet, PostGIS, tæthed, rapport, landing, e-mail-ordre | 30 pd | Data eng 20 / FS 10 | Uge 3–8 | **Datafordeler-adgang** + S0 |
| **S2** | Agent (claim-pipeline), review-UI, profil-cache, leverance-PDF, faktura | 22 pd | FS 12 / DE 6 / DK 4 | Uge 6–10 | S1 (data), **medielicens** |
| **S3** | MitID/OIDC, pseudonym, vault, ordre-opgradering, attest-upload, review-UI, expiry-job | 26 pd | FS 16 / DE 4 / DK 6 | Uge 8–13 | **MitID-broker (bestil uge 1)** |
| **S4** | Ejerskabsverifikation (EJF/deed/andel), notifikation, samtykke-ledger, ejerside, betaling 1.495 | 28 pd | FS 18 / DE 6 / DK 4 | Uge 12–17 | S3 + **jurist kontaktgrundlag (uge 6)** |
| **S5** | Relay + redaction, deal-state, pakke-betaling, reveal + guards, audit | 30 pd | FS 18 / DK 12 | Uge 16–22 | S4 + **formidlingsafklaring** + advokatpartner |
| **S6** | MitID Erhverv, eksklusivitet (DB), lead-liste, abonnement/PBS, dunning | 20 pd | FS 14 / DK 6 | Uge 20–26 | S5 + P2-tæthed |
| **S7** | Withdraw/expire/afmeld/slet, retention-jobs, tombstone, GDPR-indsigt | 16 pd | FS 8 / DE 4 / DK 4 | Uge 24–30 | Designet i S0, bygges sidst |
| **S8** | Insights zone C, k-anonymitet, Demand Pro API + dashboard | 26 pd | Data/product + FS | md. 18–24 | 12 mdr. historik |

**Sum år 1:** ~184 persondage kerne + ~40 pd DK-review/guards ≈ **224 pd**. Med 2,3 FTE ≈ 250 arbejdsdage/år minus møder/salg → **planen er stram men mulig**, forudsat S0 og adgangene ikke skrider.

## A3. Kritisk vej (kalendertid, ikke kodetid)

```
Uge 1: Datafordeler-aftale ─┐
Uge 1: MitID-broker bestilt ─┼─→ S1 ─→ S2 ─→ første krone (md. 4)
Uge 1: Medielicens ─────────┘        │
Uge 6: Jurist (kontakt + formidling) ─┴─→ S3 ─→ S4 ─→ S5 ─→ S6
```

**De fire ting der kan vælte tidsplanen — ingen af dem er kode:**

| Blokerer | Konsekvens hvis sen | Modtræk |
|---|---|---|
| Datafordeler-adgang | S1 kan ikke starte | Bestil uge 1; byg mod **syntetisk + offentlige dumps** imens |
| MitID-broker (2–6 uger) | S3/S4/S5 skrider | Bestil uge 1; testmiljø først, prod senere |
| Jurist: kontaktgrundlag + formidling | S4/S5 må ikke lanceres | Uge 6 som hård port; byg kun bag feature-flag |
| EJF-adgang afvist | Andels/manuel kø bliver flaskehals | Fallback via Tingbogen + manuel kø fra dag 1 |

## A4. Rækkefølge-regler

1. **S0 før alt.** Uden zoner, syntetiske data og CI-gates kan UA-teamet ikke arbejde lovligt eller sikkert.
2. **Guards skrives før featuren.** `tests/guards/` oprettes i samme PR som domænekoden — aldrig bagefter.
3. **Feature-flags på alt juridisk ufærdigt.** Ejer-kontakt og reveal deployes mørke og tændes først efter jurist-godkendelse.
4. **S7 designes i S0, bygges sidst.** Retention kan ikke bolt-es på en færdig event-log.
5. **Ingen S6 før P2.** Mæglerproduktet må ikke sælges på en tæthed, der ikke er bevist.

## A5. Én beslutning der skal træffes nu

**Planen har en modsigelse:** 90-dages-planen kræver datamodel i uge 4–7, men omkostningsbasen ansætter data engineer i **md. 4 (≈ uge 13)**. Det kan ikke begge være sandt.

| Option | Konsekvens |
|---|---|
| **A — Ansat fra md. 2** (anbefalet) | +~60.000 kr. år 1. S1 holder, første krone md. 4 holder |
| B — Fractional data engineer uge 3–12, fast fra md. 4 | Samme pris ca., men onboarding to gange |
| C — Stifter bygger S1 selv | Første krone skrider til md. 6–7; A4-beviset forsinkes |

**Vælg A.** Det er den billigste måde at beskytte den eneste indtægt, der findes i år 1.

## A6. Buffer og definition of done

- **Buffer:** 20 % på hvert sprint (AI-kodegenerering giver variance i review, ikke i skrivning).
- **DoD:** alle guard-tests grønne · CI-gates 1–12 bestået · audit dækker zone B · ADR skrevet · runbook opdateret · DK-review gennemført på CODEOWNERS-stier.

---

# DEL B — Retention- og slettepolitik (jurist-bilag)

## B1. Kategorier, formål og frister

| # | Datakategori | Zone | Formål | Grundlag | Retention | Sletning |
|---|---|---|---|---|---|---|
| 1 | Offentlige ejendomsdata (BBR/DAR/VUR/matrikel) | A | Analyse, rapport | Legitim interesse / offentlig data | Så længe relevant + historik | Erstattes af ny version; ingen persondata |
| 2 | Claims + kildedokumenter | A | Områdeprofil | Licens + legitim interesse | Kildelicens styrer; claims 5 år | Uddrag slettes ved licensophør |
| 3 | Køberidentitet (pseudonym, MitID-sub) | B | Ordrebog, dedup | Samtykke / kontrakt | **Aktiv ordre + 12 mdr.** | Hård sletning + tombstone |
| 4 | Bankbevis-dokument (PDF) | B | Verifikation | Samtykke | **90 dage efter review** | Slettes; kun attest-felter bevares |
| 5 | Attest-felter (udsteder, interval, dato) | B | Kvalitet i ordrebog | Kontrakt | Til `expires_at` + 12 mdr. | Anonymiseres til aggregeret |
| 6 | Ejeridentitet + ejerskabsbevis | B | Adgangskontrol | Samtykke / kontrakt | Verifikation + 90 dage | Hård sletning |
| 7 | Ejerrespons (dialog/afvisning) | B | A2, matching | **Eget formål, eget samtykke** | 12 mdr. fra sidste aktivitet | Hård sletning |
| 8 | Relay-beskeder (redacted) | B | Forhandling | Samtykke | **6 mdr. efter tråd lukket** | Hård sletning |
| 9 | RevealGrant + samtykke | B | Bevise lovlig udveksling | Retlig forpligtelse | **5 år** | Uforanderlig audit |
| 10 | Event-log (pseudonymt) | B→C | Historik, integritet, KPI | Legitim interesse | **5 år** | Bevares ved sletning (tombstone) |
| 11 | Audit-log (vault/reveal) | B | Sikkerhed, compliance | Retlig forpligtelse | **5 år** | Uforanderlig |
| 12 | Faktura/bogføring | B | Bogføringslov | Retlig forpligtelse | **5 år fra regnskabsårets udløb** | Slettes ikke før frist |
| 13 | Aggregeret efterspørgsel (k≥5) | C | B2B-produkt | Legitim interesse, anonymiseret | Ubegrænset | Genberegnes ved sletning |

**Bemærk konflikten:** kategori 12 (bogføring) og 9 (audit) kan **ikke** slettes på brugeranmodning. Det skal stå i privatlivspolitikken — ellers lover I noget, I ikke kan holde.

## B2. Sletning i to lag (løser "fuld historik" vs. GDPR)

```python
def erase_identity(identity_id, reason):
    with transaction():
        vault.delete_documents(identity_id)          # kat. 4, 6
        identity.null_contact_fields(identity_id)    # kat. 3, 7
        identity.set_erased_at(identity_id)
        relay.delete_threads(identity_id)            # kat. 8
        orders.set_status(identity_id, 'ERASED')
        # BEVARES:
        #   order_event (pseudonym, ingen kontakt)     kat. 10
        #   audit + reveal grants                      kat. 9, 11
        #   bogføring                                  kat. 12
        emit('identity.erased', pseudonym=..., tombstone_ref=...)
    insights.refresh_all()                           # kat. 13 genberegnes
```

**Tombstone-garanti:** efter sletning findes pseudonymet stadig i events, men **ingen tabel i systemet kan mappe det til en person**. Det er definitionen på anonymiseret historik — og det er det, der gør moaten lovlig.

## B3. Automatiserede jobs

| Job | Frekvens | Handling |
|---|---|---|
| `retention.documents` | Dagligt 04:00 | Slet bankbevis-PDF >90 dage efter review |
| `retention.threads` | Dagligt | Slet beskeder 6 mdr. efter lukket tråd |
| `retention.identities` | Dagligt | Slet identitet 12 mdr. efter sidste aktive ordre |
| `retention.owner_response` | Dagligt | 12 mdr. inaktivitet |
| `verification.expiry` | Dagligt 03:00 | Nedgrader VERIFIED → QUALIFIED |
| `insights.refresh` | Efter sletning | Genberegn zone C, håndhæv k≥5 |
| `retention.report` | Månedligt | Rapport til DK: antal slettet, fejl, restancer |

**Alarm:** ethvert fejlet retention-job er **P2**. Et system der ikke sletter, er et system der bryder sit eget løfte.

## B4. Registreredes rettigheder

| Rettighed | Implementering | SLA |
|---|---|---|
| Indsigt | Selvbetjening: "Mine data" → eksport af zone B om egen identitet | Øjeblikkelig |
| Berigtigelse | Ordre-kriterier redigerbare; attest kræver ny review | 1 hverdag |
| Sletning | `POST /me/erase` → to-lags sletning, kvittering | 30 dage (lovkrav), typisk <1 dag |
| Tilbagekaldelse | Samtykke-ledger, propagere til suppression + abort tråde | Øjeblikkelig |
| Dataportabilitet | JSON-eksport af egne ordrer + attester | Øjeblikkelig |
| Indsigelse | Support-sag → DK-vurdering | 30 dage |

## B5. Underdatabehandlere (skal stå i DPA'en)

| Subprocessor | Land | Data | Overførselsgrundlag |
|---|---|---|---|
| MitID-broker | DK/EU | Identitet | EU, ingen tredjeland |
| Hosting (EU) | EU | Alle zoner | EU |
| LLM-udbyder | **EU-endpoint påkrævet** | Kun zone A | EU, ingen træning på data |
| Betalingsudbyder | EU | Betaling | EU |
| Medieovervågning | DK/EU | Kildelicens | EU |
| **UA-udviklingsteam** | **Ukraine** | **Kun syntetiske data** | SCC + TIA — men **ingen prod-persondata** |
| Advokatpartner | DK | Fulfillment-sag | Selvstændig dataansvarlig |

**Nøglepointe til banken:** *"Udvikling i Ukraine behandler ikke persondata. Produktion er EU-only. Adgang er auditeret og tidsbegrænset."* Det er den sætning, der gør due diligence mulig.

## B6. DPIA og dokumenter der skal findes før lancering

- [ ] DPIA (systematisk behandling af persondata + nye teknologier)
- [ ] Fortegnelse over behandlingsaktiviteter (art. 30)
- [ ] DPA-skabelon til B2B-kunder
- [ ] Subprocessor-liste + varsling ved ændring
- [ ] Privatlivspolitik med undtagelserne (bogføring/audit)
- [ ] Samtykketekster, versionerede (`text_version`)
- [ ] Juridisk grundlag pr. notifikationstype (`legal_basis_ref`)
- [ ] Beredskab for databrud (72-timers anmeldelse)

---

# DEL C — Demand Pro: API, dashboard og k-anonymitet i praksis

## C1. Hvad kunden køber — og ikke køber

| ✅ Inkluderet | ❌ Aldrig inkluderet |
|---|---|
| Aggregeret efterspørgsel pr. område/type/budgetbånd | Identitet, navn, kontakt |
| Tæthed og udvikling over tid | Enkeltordrer eller pseudonymer |
| Verifikationsgrad (andel med bankbevis) | Præcise budgetbeløb |
| Ejendomsdatamodel + historik (zone A) | Relay-tråde eller forhandlinger |
| Claims med kilde + dato | Dokumenter eller attester |
| Change-feed (byggesager, planer) | Data der kan re-identificere en person |

**Kontraktformulering:** *"Leverancen er aggregeret, anonymiseret efterspørgselsstatistik. Kunden må ikke forsøge re-identifikation. Overtrædelse ophæver adgang uden refusion."*

## C2. k-anonymitet — de tre angreb man faktisk skal forsvare mod

| Angreb | Eksempel | Mitigation |
|---|---|---|
| **Direkte lille celle** | 3 villa-købere i budgetbånd 4–4,5M i ZIP-2300 | Supprimér celle (k<5) |
| **Komplementær afsløring** | Total vises, alle andre celler vises → den skjulte kan udregnes | **Komplementær suppression**: skjul også nærmeste celle/total |
| **Differencing over tid** | Måned 1: 5 i bånd X. Måned 2: 6. Én person flyttede → kan kobles til hændelse | **Tids-aggregering**: vis kvartal eller rullende 3 mdr., ikke daglige deltas; afrund til nærmeste 5 |

```python
def publish_cell(rows, dims):
    if count(rows) < K:                       # K = 5
        return SUPPRESSED
    return round_to_nearest(count(rows), 5)   # afrunding mod differencing

def publish_table(cells):
    suppressed = [c for c in cells if c.value is SUPPRESSED]
    if len(suppressed) == 1 and table.has_total:
        suppress_nearest_sibling()            # komplementær
    if any(c.dims_is_unique_combination() for c in suppressed):
        collapse_dimension()                  # fx budgetbånd 20 → 8
    return cells
```

**Ekstra regler:**
- Ingen kombination af >3 dimensioner (område × type × budget × horisont = for tyndt).
- Mindste geografiske enhed = **postnummer**. Aldrig adresse, aldrig gade.
- Ingen eksport af rå rækker — kun aggregerede tabeller.

## C3. API

| Metode | Endpoint | Beskrivelse |
|---|---|---|
| GET | `/v1/demand/areas` | Områder kunden har licens til |
| GET | `/v1/demand/areas/{id}/summary` | Tæthed, verifikationsgrad, trend (kvartal) |
| GET | `/v1/demand/areas/{id}/matrix?type=&budget_band=&horizon=` | Aggregeret matrix, k≥5, afrundet |
| GET | `/v1/demand/areas/{id}/history?from=&to=` | Rullende 3-mdr. serier |
| GET | `/v1/properties/{address_id}` | Zone A: BBR, VUR, matrikel, plan |
| GET | `/v1/areas/{id}/changes?since=` | Change-feed: byggesager, planer, `property.changed` |
| GET | `/v1/areas/{id}/claims?status=VEDTAGET` | Claims med kilde + dato |
| POST | `/v1/exports` | Async job → signeret, vandmærket fil |
| GET | `/v1/exports/{id}` | Status + download-URL (kortlivet) |

**Kontrakt-eksempel:**
```jsonc
// GET /v1/demand/areas/ZIP-2300/matrix?type=VILLA&horizon=3-6M
{
  "area_id": "ZIP-2300",
  "period": "2026-Q4",
  "k_threshold": 5,
  "rounding": 5,
  "rows": [
    { "budget_band": "3.5-4.0M", "verified_count": 15, "share": 0.34 },
    { "budget_band": "4.0-4.5M", "verified_count": 25, "share": 0.56 },
    { "budget_band": "4.5-5.0M", "verified_count": null, "suppressed": true,
      "reason": "K_ANONYMITY" }
  ],
  "total": { "verified_count": 45, "note": "afrundet; komplementær suppression anvendt" },
  "meta": { "dwelling_count": 10412, "density_per_1000": 4.3,
            "verification_rate": 0.11, "data_freshness": "2026-11-16" }
}
```

## C4. Dashboard (fire faner)

| Fane | Indhold | Værdi for kunden |
|---|---|---|
| **Efterspørgsel** | Tæthed pr. område, matrix, verifikationsgrad, trend | "Hvor mange reelle købere er der?" |
| **Udbud & boligmasse** | BBR-fordeling, ejerformer, arealer, opførelsesår | "Hvad findes der i forvejen?" |
| **Bevægelse** | Vedtaget/på vej/stoppet med kilde + dato | "Hvad ændrer området?" |
| **Gap-analyse** | Efterspørgsel minus eksisterende boligmasse pr. type/budget | **"Skal vi bygge 40 eller 80 — og hvilken type?"** |

**Gap-analysen er salgsargumentet.** Den kombinerer zone A (hvad findes) med zone C (hvad efterspørges) — og det er præcis den beslutning, en developer betaler 85.000 kr. for at få belyst.

## C5. Licens, adgang og audit

```sql
CREATE TABLE b2b_license (
  org_id uuid, product text,             -- DEMAND_PRO
  area_ids text[],                       -- kun licenserede områder
  seats int, rate_limit_per_min int,
  export_allowed boolean DEFAULT true,
  valid_from date, valid_to date
);
```

| Kontrol | Håndhævelse |
|---|---|
| Område-scope | RLS + license-check i hvert kald |
| Rate limit | Pr. org, pr. endpoint; 429 med `Retry-After` |
| Eksport | Async, vandmærket med org-id + timestamp, signeret URL (15 min) |
| Audit | Hvert kald logges: org, endpoint, area, rows_returned, suppressed_count |
| Misbrug | Mønsterdetektion: mange små område-kald → forsøg på re-identifikation → alarm |

**Vandmærkning er ikke pynt:** hvis en kundes data dukker op hos en konkurrent, kan I bevise hvorfra.

## C6. Datakvalitet som del af leverancen

Eksponér altid i `meta`:
```jsonc
{ "coverage": { "BBR": 0.99, "VUR": 0.94, "EJF": 0.71 },
  "quality_flags": { "VUR": "FORSINKET_2024", "PLAN": "MANUELT_KURATERET" },
  "freshness": { "registry": "2026-11-16", "claims": "2026-11-14" },
  "methodology_url": "https://optata.dk/metode/v3" }
```

En bank stoler mere på data, der **indrømmer sin usikkerhed**, end på data der lader som om den er perfekt. Det er et salgsargument, ikke en svaghed.

## C7. Acceptkriterier

```
GIVEN celle med 3 ordrer        THEN suppressed=true, ingen værdi i payload
GIVEN én skjult celle + total   THEN komplementær suppression anvendt
GIVEN 4 dimensioner forespurgt  THEN 400 TOO_MANY_DIMENSIONS
GIVEN adresse-niveau forespurgt THEN 400 GEO_TOO_GRANULAR
GIVEN org uden licens på område THEN 403 + tom payload (RLS)
GIVEN eksport                   THEN vandmærke + audit + kortlivet URL
GIVEN to måneders kald          THEN værdier afrundet til 5, ingen daglige deltas
GIVEN sletning af køber         THEN zone C genberegnet, k≥5 stadig håndhævet
```

---

## Hvad de tre dele lukker

- **(a)** gør planen **eksekverbar**: estimer, kritisk vej, og den ene beslutning (data engineer fra md. 2) der afgør om første krone kommer i md. 4.
- **(b)** gør GDPR til **kode og frister** i stedet for en hensigt — og løser konflikten mellem "fuld historik" og sletteret med tombstones.
- **(c)** gør B2B-produktet **salgbart og sikkert**: k-anonymitet med de tre reelle angreb, gap-analyse som værdiløfte, og audit der beskytter moaten.

*Næste skridt kan være (a) gap-analysens beregningsmodel (hvordan efterspørgsel minus boligmasse bliver til en byggeanbefaling med forbehold), (b) onboarding- og aktiveringsflowet for de første 250 verificerede købere (den reelle flaskehals), eller (c) et samlet arkitekturdokument v1 der konsoliderer alle afsnit til repo'ets `/docs`.*