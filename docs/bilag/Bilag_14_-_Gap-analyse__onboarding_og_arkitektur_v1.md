# OPTATA — (a) Gap-analyse · (b) Onboarding til 250 verificerede · (c) Arkitekturdokument v1

---

# DEL A — Gap-analysen: fra efterspørgsel til byggebeslutning

## A1. Hvad den er — og hvad den ikke er

| ✅ Den er | ❌ Den er ikke |
|---|---|
| Et **observeret mismatch** mellem verificeret efterspørgsel og eksisterende boligmasse | En prognose eller anbefaling |
| Underbygget med kilde, dato og tæthed | En vurdering af, hvad der "bør" bygges |
| Et beslutningsgrundlag med usikkerhed vist | En garanti for afsætning |

**Agent-reglen gælder også her:** enhver gap-påstand skal have datagrundlag og usikkerhed. Ingen "der bør bygges 80 boliger" — men "der er 62 verificerede købere til 4-værelses i båndet 4–4,5M, og udbuddet i området er 11 enheder med 3 handler/år".

## A2. Beregning

```python
def gap(area_id, boligtype, budget_band, horizon):
    # 1. Efterspørgsel (zone C, k>=5, afrundet)
    D = demand.verified(area_id, boligtype, budget_band, horizon)
    if D.suppressed: return INSUFFICIENT_DATA

    # 2. Eksisterende masse (zone A)
    S = registry.count(area_id, boligtype, areal_range=budget_band.to_areal(area_id))

    # 3. Realistisk tilgængeligt udbud (ikke hele massen)
    turnover = tingbogen.transfers_per_year(area_id, boligtype, years=3)
    available = S * turnover                      # årligt omsat masse

    # 4. Konkurrence fra aktivt udbud
    active = listings.active(area_id, boligtype, budget_band)   # hvis licenseret kilde
    net_demand = max(0, D - active)

    # 5. Gap-størrelse og dækning
    return {
      "verified_demand": D.value,
      "stock": S,
      "annual_turnover": round(available, 1),
      "coverage_ratio": round(available / D.value, 2),   # <1 = underdækket
      "absorption_months": months_to_absorb(D.value, available),
      "confidence": confidence(D, S, turnover),
      "caveats": caveats(area_id, boligtype, budget_band)
    }
```

## A3. De fire tal kunden faktisk beslutter på

| Tal | Betydning | Eksempel |
|---|---|---|
| **Verified demand** | Reelle, finansierede købere i segmentet | 62 |
| **Coverage ratio** | Årligt udbud ÷ efterspørgsel | 0,18 → kraftigt underdækket |
| **Absorption months** | Tid til at optage efterspørgslen ved nuværende udbud | 34 mdr. |
| **Confidence** | Datagrundlagets styrke | MEDIUM (VUR forsinket, k=5-grænse ramt) |

**Fortolkning til developer:** coverage 0,18 og absorption 34 mdr. betyder, at et projekt på 40–80 enheder i dette segment **ikke kan mættes af det eksisterende udbud**. Det er den indsigt, de betaler 85.000 kr. for — ikke en anbefaling.

## A4. Obligatoriske forbehold (skrives i leverancen)

```jsonc
"caveats": [
  { "code":"DEMAND_NOT_COMMITTED", "text":"Verificeret købeevne er ikke en købsforpligtelse." },
  { "code":"GEO_SUBSTITUTION", "text":"Købere kan acceptere tilstødende områder; gap er ikke låst til postnummeret." },
  { "code":"PRICE_ELASTICITY", "text":"Efterspørgsel er målt ved nuværende prisniveau; nybyggeri prissættes anderledes." },
  { "code":"VUR_LAG", "text":"Vurderinger er forsinkede; prisreference suppleret med tinglyste handler." },
  { "code":"K_SUPPRESSION", "text":"En eller flere celler er skjult (k<5); totaler er afrundet." },
  { "code":"TIME_WINDOW", "text":"Efterspørgsel er et øjebliksbillede med 3-måneders rullende vindue." }
]
```

**Uden forbeholdene er analysen en holdning** — præcis det, §4 i forretningsplanen forbyder. Med dem er den et dokument, en bank kan lægge i et kreditudvalg.

## A5. Visualisering (dashboard-fanen "Gap")

```
Segment: Villa · 140–180 m² · 4,0–4,5 mio. · horisont 3–6 mdr.

Efterspørgsel (verificeret)   ████████████████████  62
Årligt udbud i segmentet      ███                    11
Coverage ratio                0,18  ⚠ underdækket
Absorption                    34 mdr.
Datagrundlag                  MEDIUM · 2 celler skjult (k<5)

Kilder: BBR 16.11.26 · Tingbogen 14.11.26 · Ordrebog rullende 3 mdr.
```

## A6. Acceptkriterier

```
GIVEN celle suppressed        THEN gap returnerer INSUFFICIENT_DATA, ikke estimeret værdi
GIVEN coverage beregnet       THEN caveats non-empty og confidence vist
GIVEN leverance               THEN ingen anbefalings- eller prognosesprog (CI-tekstlint)
GIVEN 4 dimensioner           THEN afvist (k-anonymitet)
GIVEN gap eksporteret         THEN vandmærke + audit + metodereference
```

---

# DEL B — Onboarding: de første 250 verificerede købere

## B1. Den reelle flaskehals (regnet baglæns)

```
Mål:      250 VERIFIED i ét postnummer (10.000 boliger)
Ratio:    ~10 % af rå ordrer bliver verificeret   → 2.500 rå ordrer
Konv.:    8 % fra besøg til ordre                 → ~31.000 lokale besøg
```

31.000 besøg fra beboere i ét postnummer kan **ikke købes** for 12–32k/md. i marketing. Det skal **distribueres** — og verifikationsraten skal hæves.

## B2. To greb der ændrer matematikken

| Greb | Effekt |
|---|---|
| **Hæv verifikationsraten fra 10 % → 25 %** | Rå ordrer falder fra 2.500 → 1.000; besøg fra 31.000 → **12.500** |
| **Distributionspartnere i stedet for annoncer** | Besøg kommer via foreninger/mægler/bank, ikke via betalt trafik |

**Verifikationsraten hæves ved at gøre bank-forhåndsgodkendelsen til indgangsværdien:** *"Bliv forhåndsgodkendt og kom i ordrebogen — ejere ser dig først, når din købeevne er dokumenteret."* Køberen får noget for besværet, ikke bare et skema.

## B3. Kanaler (prioriteret efter reach pr. krone)

| # | Kanal | Hvorfor den virker | Estimat reach |
|---|---|---|---|
| 1 | **Andels- og grundejerforeninger** | Kendt venteliste-logik, eksisterende mailinglister, lokal legitimitet | 2.000–6.000 husstande |
| 2 | **Bank/realkredit-partner** | Forhåndsgodkendelse er allerede en proces; Optata bliver destinationen | 300–800 godkendte/år lokalt |
| 3 | **Lokal mægler (pilot, eksklusiv)** | Har køberkartotek i dag — kan konvertere til ordrebog | 200–500 |
| 4 | **Områderapport som SEO/indhold** | Gratis, offentlig data, lokal søgeintention ("hvad sker der i…") | 1.000–4.000/md. over tid |
| 5 | **Lejebolig-ventelister / boligforeninger** | Folk der venter, vil eje | 500–2.000 |
| 6 | Betalt lokal annoncering | Dyrest, sidst | Supplering |

**Aftale-model for foreninger:** gratis område- og adresseindsigt til bestyrelsen + medlemmerne får før-adgang til rapporten. Ingen betaling, ingen kommission — ren distribution.

## B4. Aktiveringsstigen (hvad brugeren oplever)

| Trin | Oplevelse | Friktion | Mål-konvertering |
|---|---|---|---|
| 1 | Ser områderapport (anonym) | Ingen | 100 % |
| 2 | "Følg området" — e-mail | Ét felt | 8–15 % |
| 3 | 4 spørgsmål → QUALIFIED | 60 sek. | 40 % af trin 2 |
| 4 | MitID | 30 sek. | 70 % af trin 3 |
| 5 | Bankbevis upload / anmod bank | 2–10 min. | **35–60 %** af trin 4 |
| 6 | VERIFIED + badge + "du er synlig for ejere" | Review 1 hverdag | — |

**Kritisk design:** trin 5 er der, hvor 65 % falder fra. Derfor:
- Tillad **"anmod min bank"** (V2/V3) som alternativ til upload.
- Vis **hvad køberen får**: "Ejere åbner dialog 3× oftere med verificerede købere" (mål det, brug det).
- **Gem fremdrift**: delvis udfyldt ordre bevares og kan færdiggøres senere.
- **Påmindelse** efter 48 t med ét klik tilbage til trin 5.

## B5. Verifikations-throughput (den menneskelige flaskehals)

| Volumen | Manuel review (10 min/stk) | Kapacitet |
|---|---|---|
| 250 verificerede | ~42 timer | Stiftere, ~1 uge spredt |
| + løbende fornyelser (90 dage) | ~14 timer/kvartal | Overkommeligt |
| 12 bydele (3.000) | ~500 timer/år | **Automatisering påkrævet (V2/V3)** |

**Regel:** V1 manuel er fin til pilot. **V2 (bank-reference-validering) skal være klar før bydel nr. 3** — ellers bliver review den flaskehals, der stopper skalering.

## B6. Kampagneplan for pilotområdet (12 uger)

| Uge | Handling | Mål |
|---|---|---|
| 1–2 | Områderapport live + SEO-basis | Indeksérbar, delbar |
| 2–4 | 5 foreninger kontaktet, 2 aftaler | 2.000 husstande nået |
| 3–5 | Landing + venteliste pr. adresse | P0: ≥8 % konvertering |
| 4–6 | Banksamtale om forhåndsgodkendelse som indgang | Pilot-aftale eller V1-upload |
| 6–8 | Mæglerpilot (eksklusivitet, ikke rabat) | 200 købere konverteret |
| 8–10 | Verifikationsflow live + påmindelser | ≥25 % verifikationsrate |
| 10–12 | Ejer-notifikation (juridisk ok) | A2: ≥15 % dialog |

## B7. KPI'er og kill-kriterier

```
density_verified_per_1000{area}       # P2: ≥15 ved md. 11, mål 25
verification_rate{channel}            # mål ≥25% samlet
time_to_verified_p50                  # mål <5 dage
step5_dropoff_rate                    # alarm hvis >70%
cost_per_verified_order{channel}      # sammenlign kanaler ærligt
partner_reach{partner}                # husstande nået
```

| Signal | Handling |
|---|---|
| Verifikationsrate <10 % efter 4 uger | Problem i **onboarding**, ikke markedsføring → forenkl trin 5, tilbyd bank-anmodning |
| P0 <8 % | Skift budskab/område, byg ikke videre |
| Én kanal giver >60 % af verificerede | Fordobl dér, drop de andre |
| step5-dropoff >70 % | Bankbevis er for besværligt → V2 fremskyndes |

---

# DEL C — Arkitekturdokument v1 (paste-klar til `/docs`)

## C1. Struktur

```
docs/
├─ ARCHITECTURE.md          # dette dokument
├─ adr/                     # beslutninger, én pr. fil
├─ contracts/               # OpenAPI + events + prompts (i /contracts)
├─ runbooks/                # drift pr. job og incident
├─ security/                # STRIDE, guards, adgangspolitik
├─ compliance/              # retention, DPIA, DPA, subprocessors
└─ cases/                   # C1–C9 flows og acceptkriterier
```

## C2. ARCHITECTURE.md (indhold)

**1. Formål og afgrænsning**
Optata er et **ordrebogssystem med event-historik** oven på et offentligt ejendomsregister — ikke en boligportal. Systemet gør verificeret efterspørgsel synlig, anonym og handlingsbar.

**2. Tre zoner (ufravigelig)**
| Zone | Indhold | Dev | Eksport |
|---|---|---|---|
| A | Offentlige data, claims, rapporter | ✅ | ✅ |
| B | Identitet, ordrer, beviser, tråde | ❌ aldrig | ❌ aldrig |
| C | Aggregeret, k≥5, afrundet | ✅ syntetisk | ✅ licenseret |

**3. Modulkort**
`registry · reports · agent · orderbook · identity · verification · disclosure · relay · consent · billing · insights` — modulær monolit + workers (`ingestion · agent_runner · matching · expiry · retention`).

**4. Invarianter (må aldrig brydes)**
1. BFE → adresse-id er **1:mange**.
2. Al registerdata er **bitemporal**; historik overskrives aldrig.
3. `order_event` er **append-only**; upcasting ved læsning.
4. **Kun `disclosure` må læse vault.**
5. Kun **VERIFIED med gyldig attest** udløser ejer-kontakt.
6. **Ejerskabsverifikation** kræves før visning af interesse.
7. **Reveal** kræver: pakke accepteret ∧ betaling ∧ 2 samtykker ∧ frisk step-up ∧ gyldig attest — i **én transaktion**.
8. Zone C: **k≥5 + afrunding + komplementær suppression**.
9. **Én aktiv ordre pr. husstand+scope**; co-buyers på samme ordre.
10. Sletning er **to-lags**: zone B væk, pseudonym event-historik bevaret.

**5. Nøgler**
DAR adresse-id (bolig) · BFE (ejendom) · matrikel-id (jord) · area_id (postnummer/bydel) · pseudonym (person).

**6. Sikkerhedsmodel**
MitID via broker (OIDC), progressiv identitet, step-up ved følsomme kald, RLS i DB, audit 5 år, ingen prod-persondata til dev, EU-hosting.

**7. Drift**
SLO'er, jobs (ingestion 02:00, expiry 03:00, retention 04:00), alarmer (vault-adgang uden for disclosure = P1; zone B i public payload = P1 + rollback).

**8. Leverancemodel**
UA-seniorteam + AI-kodegenerering; DK-reviewer ejer guards, migrations, finansiel/juridisk logik. Kontrakter først, kode bagefter.

## C3. ADR-register (beslutninger der skal dokumenteres)

| ADR | Beslutning | Status |
|---|---|---|
| 001 | Modulær monolit, ikke microservices | Accepteret |
| 002 | Postgres + PostGIS, bitemporal via ranges | Accepteret |
| 003 | Event-sourcet ordrebog, append-only | Accepteret |
| 004 | Tre datazoner + RLS | Accepteret |
| 005 | MitID via broker, **ingen CPR lagret** | Accepteret |
| 006 | Progressiv identitet (anonym → e-mail → MitID → attest) | Accepteret |
| 007 | Anonym front-end + relay + gensidig reveal | Accepteret |
| 008 | Reveal som betalt milepæl, fast gebyr | Accepteret, **juridisk afklaring uge 6** |
| 009 | Ejerskab: EJF + Tingbogen + manuel fallback (andel) | Accepteret |
| 010 | k-anonymitet: k=5, afrunding, komplementær suppression | Accepteret |
| 011 | Agent: claim-pipeline med tvungen proveniens | Accepteret |
| 012 | UA-udvikling på syntetiske data, EU-prod | Accepteret |
| 013 | Data engineer fra md. 2 (ikke md. 4) | **Til beslutning** |
| 014 | Eksklusivitet håndhævet med unique index | Accepteret |
| 015 | To-lags sletning med tombstone | Accepteret |

## C4. Guard-indeks (det der aldrig AI-genereres)

```
tests/guards/
  vault_only_disclosure · reveal_all_six_guards · reveal_concurrent_idempotent
  reveal_toc_tou_expiry · redaction_corpus · rls_agent_scope · k_anonymity
  no_zone_b_in_public · erasure_preserves_events · ownership_revoked_on_transfer
  exclusive_agent_per_zip · order_one_per_household · claim_needs_source
```

## C5. Runbook-indeks

| Runbook | Trigger |
|---|---|
| `ingestion-failed` | Kilde-kørsel fejlet / quarantine-spike |
| `expiry-failed` | Udløbne VERIFIED i lead-lister → **frys lister** |
| `vault-anomaly` | Adgang uden for disclosure → P1 |
| `zone-leak` | Zone B i public payload → P1 + rollback |
| `redaction-bypass` | Rapporteret omgåelse |
| `retention-failed` | Slettejob fejlet → P2 |
| `dwelling-count-jump` | >2 % ændring → frys tætheds-KPI |
| `dso-breach` | Debitorer >45 dage |

## C6. Case-indeks

C1 område-ordre · C2 adresse-ordre · C3 ejer notificeret · C4 ejerside · C5 enighed→pakke→reveal · C6 mægler · C7 developer-analyse · C8 bankattest · C9 withdraw/expire/afmeld/slet.

## C7. Definition of Done (systemniveau)

Alle guards grønne · CI-gates 1–12 bestået · ADR skrevet ved større beslutning · runbook opdateret · audit dækker zone B · syntetiske fixtures reproducerbare · DK-review på CODEOWNERS-stier · ingen prod-persondata uden for EU-prod.

---

## Hvor vi står

Arkitekturen er nu **komplet på designniveau**: cases → flows → tilstande → events → moduler → data → guards → drift → compliance → leveranceplan. De tre åbne punkter er ikke arkitektur, men **beslutninger og adgang**:

1. **ADR-013:** data engineer fra md. 2 — afgør om første krone kommer i md. 4.
2. **Datafordeler + MitID-broker bestilles uge 1** — kalendertid, ikke kodetid.
3. **Jurist uge 6:** formidlingsvurdering af match+relay+reveal, og kontaktgrundlag.

*Vil du have, at jeg nu (a) skriver de faktiske ADR-filer (001–015) i fuld tekst, (b) laver sprint-backloggen for S0+S1 som konkrete issues med acceptkriterier, eller (c) udarbejder kravspecifikationen til UA-teamet (hvad de skal bygge, hvad de ikke må røre, og hvordan de leverer)?*