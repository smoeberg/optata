# OPTATA — (a) Matching · (b) Notifikation & samtykke · (c) Leverance & faktura

De tre sidste kernemekanismer. De er skrevet som kode, regler og acceptkriterier — ikke beskrivelser.

---

# DEL A — Matching, tæthed og dedup i praksis

## A1. To match-typer (må ikke blandes sammen)

| Type | Fra → til | Formål | Udløser |
|---|---|---|---|
| **M1 Adresse-match** | Ordre (scope=ADDRESS) → ejer | Fremkald udbud (A2) | Kun VERIFIED → notifikation |
| **M2 Område-match** | Ordre (scope=AREA) → ejendomme/mæglere | Lead-liste, indsigt | Løbende, ingen ejer-kontakt |

**Regel:** M2 må **aldrig** udløse kontakt til en ejer. Det er kun M1, og kun på den konkrete adresse. Ellers bliver det massehenvendelser — juridisk og troværdighedsmæssigt fatalt.

## A2. Hard filters (før scoring)

```python
def hard_filter(order, prop) -> bool:
    if order.scope == "ADDRESS":
        return order.address_id == prop.address_id
    if not st_within(prop.geom, area(order.area_id).geom): return False
    if prop.attrs["anvendelse"] not in BOLIGKODER: return False
    if order.criteria.get("type") and prop.attrs["type"] != order.criteria["type"]:
        return False
    if prop.attrs["areal"] < order.criteria.get("areal_min", 0): return False
    if prop.attrs["vaerelser"] < order.criteria.get("rooms_min", 0): return False
    return True
```

Budget filtreres **ikke** hårdt fra — en ejer skal kunne se interesse, selvom budgettet ligger under vurderingen. Det er information, ikke støj.

## A3. Score (0–100, forklarbar)

| Signal | Vægt | Beregning |
|---|---|---|
| Budget-dækning | 30 | `min(1, budget_max / reference_pris)` — reference = VUR, suppleret med tinglyste overdragelser i området |
| Størrelses-fit | 20 | Gauss omkring ønsket areal, σ = 20 % |
| Type-fit | 15 | Eksakt match = 1, beslægtet = 0,5 |
| Horisont | 15 | 0–3M=1,0 · 3–6M=0,8 · 6–12M=0,5 · 12M+=0,2 |
| Verifikation | 15 | VERIFIED=1,0 · QUALIFIED=0,4 · CURIOS=0 |
| Friskhed | 5 | Decay over 90 dage siden `last_signal_at` |

```python
score = round(100 * sum(w * s for w, s in signals))
reason_codes = [code for code, s in signals if s >= 0.8]
# fx ["BUDGET_DAEKKER", "STOERRELSE_FIT", "VERIFICERET", "HORISONT_3_6M"]
```

**Krav:** `reason_codes` er **påkrævet** i API-svaret. En mægler og en ejer skal kunne se *hvorfor* — ellers er scoren et gæt, og produktet mister troværdighed.

**Tærskler:** M1 notifikation ved score ≥ 60 **og** level=VERIFIED. M2 lead-liste viser alle VERIFIED, sorteret efter score.

## A4. Tæthed (KPI'en hele forretningen hviler på)

```sql
CREATE MATERIALIZED VIEW area_density AS
SELECT a.area_id,
       a.dwelling_count,
       count(o.*) FILTER (WHERE o.level='VERIFIED' AND o.status='ACTIVE') AS verified,
       round(1000.0 * count(o.*) FILTER (WHERE o.level='VERIFIED' AND o.status='ACTIVE')
             / nullif(a.dwelling_count,0), 1) AS per_1000
FROM area a LEFT JOIN orders o ON o.area_id = a.area_id
GROUP BY 1,2;
```

**Nævneren er kritisk:** `dwelling_count` = aktive DAR-adresser med BBR-boliganvendelse. FX-01 (40 andelsenheder) skal tælle 40. Alarm ved `dwelling_count_delta > 2 %` — ellers bliver P2-porten målt på et forkert tal.

**Refresh:** efter ingestion + ved `order.verified/expired/withdrawn`. Aldrig realtime-beregnet i request-path.

## A5. Dedup i praksis (tre lag)

| Lag | Nøgle | Håndhævelse |
|---|---|---|
| Person | `identity.pseudonym` (MitID) | Broker-sub unik |
| Husstand | `household_key` = købers nuværende DAR-adresse | Delvis unik index + co-buyer |
| Scope | (husstand, scope, adresse/område) | Unik index på aktive |

```sql
CREATE UNIQUE INDEX order_one_per_household_scope
  ON orders (household_key, scope, coalesce(address_id, area_id))
  WHERE status IN ('ACTIVE','PAUSED','MATCHED','IN_DIALOG','AGREED');
```

**Co-buyer:** samboende tilføjes på samme ordre (`order_party`-tabel), ikke som ny ordre. Ved `identity.linked` (e-mail → MitID) merges ordren **in-place** med `causation_id` — aldrig slet+genskab, det ville bryde historikken.

## A6. Kørsel og idempotens

- **Event-drevet:** `order.verified`, `property.changed`, `owner.ownership_verified` → match for berørt adresse/område.
- **Batch:** natligt pr. område (fuld genberegning, billig fordi geo-partitioneret).
- **Idempotensnøgle:** `(order_id, address_id, criteria_hash, property_version)`. Uændret input → ingen ny notifikation.

## A7. Acceptkriterier

```
GIVEN ordre scope=AREA              THEN ingen owner.notified nogensinde
GIVEN ordre CURIOS på adresse       THEN intet match til ejer, kun intern liste
GIVEN FX-01 (40 enheder)            THEN dwelling_count=40, per_1000 korrekt
GIVEN FX-03 samboende               THEN 409 ved ny ordre, co-buyer tilbydes
GIVEN uændret criteria + property   THEN ingen duplikeret notifikation
GIVEN score beregnet                THEN reason_codes non-empty i API-svar
GIVEN attest udløbet                THEN match fjernes fra lead-liste før 06:00
```

---

# DEL B — Notifikation og samtykke

## B1. Kanaler og hvornår

| Kanal | Brug | Krav |
|---|---|---|
| **E-mail** | Primær (køber-status, ejer-interesse) | Verificeret adresse, afmeld-link |
| **Brev / digital post** | Ejer uden e-mail i kontaktregister | Saglig, afgrænset, afmelding via URL+kode |
| **In-app** | Aktive brugere | Ingen persondata i push-tekst |
| SMS | **Ikke i år 1** | For indgribende, dyrt, svært at afmelde pænt |

## B2. Ejer-notifikation: reglerne der gør den lovlig og værdifuld

```python
def may_notify_owner(address_id, order) -> Decision:
    require(order.level == "VERIFIED" and verification_valid(order))
    require(order.scope == "ADDRESS" and order.address_id == address_id)
    require(match_score >= 60)
    require(not suppressed(address_id))                 # afmelding vinder altid
    require(legal_basis_ref(address_id) is not None)    # jurist-godkendt grundlag
    require(frequency_ok(address_id))                   # loft, se B3
    require(quiet_hours_ok())                           # 08–20 lokal tid
    return ALLOW
```

**Aggregering er et krav, ikke en nice-to-have:** flere interesser på samme adresse samles til **én** notifikation: *"Der er 3 verificerede købere til din adresse."* Det sænker støj, hæver oplevet værdi og reducerer afmeldinger.

## B3. Frekvensloft og suppression

| Regel | Værdi |
|---|---|
| Maks. notifikation pr. adresse | 1 pr. 14 dage |
| Maks. pr. ejer på tværs af adresser | 2 pr. måned |
| Ny interesse inden for loft | Kø → med i næste samlede notifikation |
| Afmelding | **Permanent på adressen**, ikke kun tråden |
| Afvisning af konkret køber | Suppression på (adresse, pseudonym) |
| Hard bounce / klage | Øjeblikkelig suppression + review |

## B4. Skabelon-krav (ingen persondata i transit)

```
Emne: Verificeret købsinteresse på [vejnavn husnr]

Der er registreret 1 verificeret købsinteresse på din bolig.
Køberen er identificeret og har dokumenteret købeevne.

Du kan se interessen anonymt og vælge om du vil åbne en dialog.
Ingen kontaktoplysninger udveksles, før I begge accepterer.

[ Se interessen ]   [ Afmeld fremtidige henvendelser på denne adresse ]

Optata ApS · CVR · adresse · hvorfor du modtager denne henvendelse
```

**Forbudt i skabelonen:** købernavn, præcist budget, telefon, e-mail, dokumentvedhæftning, formuleringspres ("skynd dig", "sidste chance").

## B5. Samtykke-ledger (append-only)

```jsonc
// consent.granted / consent.revoked
{
  "subject_pseudonym": "E-2B91",
  "purpose": "OWNER_INTEREST_NOTIFICATION" | "DIALOG" | "IDENTITY_REVEAL"
           | "BANK_ATTESTATION_PROCESSING" | "B2B_AGGREGATION",
  "scope": { "address_id": "…" } | { "thread_id": "…" },
  "legal_basis_ref": "LEGAL-2026-004",     // juristens dokument-id
  "text_version": "v1.2",                  // hvad brugeren faktisk så
  "channel": "EMAIL", "granted_at": "…", "revoked_at": null
}
```

**Regler:** samtykke er **formåls- og scope-bundet**. Reveal kræver separat samtykke fra begge parter. Tilbagekaldelse propagere øjeblikkeligt til suppression og aborterer åbne tråde. `text_version` gemmes, så I kan bevise hvad der blev accepteret.

## B6. Levering og drift

- **Outbox** → worker → provider (EU). Idempotens på `notification_id`.
- **Retry:** 3 forsøg, eksponentiel backoff. Hard bounce → suppression.
- **Metrics:** `owner_notified_total`, `dialog_opened_total` (= A2-rate), `unsubscribe_rate`, `bounce_rate`, `frequency_capped_total`.
- **Alarm:** `unsubscribe_rate > 5 %` pr. område → produktet er for støjende; skru loft ned, ikke op.

## B7. Acceptkriterier

```
GIVEN afmeldt adresse        THEN ingen notifikation, uanset nye ordrer
GIVEN 3 nye interesser samme adresse inden 14 dage
                             THEN 1 samlet notifikation, ikke 3
GIVEN QUALIFIED (ikke VERIFIED) THEN ingen notifikation
GIVEN kl. 22                 THEN kø til næste dag 08:00
GIVEN samtykke tilbagekaldt  THEN tråd ABORTED + suppression aktiv
GIVEN skabelon-render        THEN ingen zone B-felter (CI-gate 5)
```

---

# DEL C — Leverance og faktura (den første krone, md. 4)

## C1. Tilstandsmaskine

```
ORDERED → SCOPED → GENERATING → IN_REVIEW → APPROVED
   → DELIVERED → ACCEPTED → INVOICED → PAID
                    └→ REVISION (1 inkluderet) → IN_REVIEW
   └→ CANCELLED (før GENERATING, uden faktura)
```

**Guards:** `DELIVERED` kræver `profile.review_state=APPROVED`. `INVOICED` kræver `DELIVERED`. Ingen faktura før leverance — det er både god skik og lavere debitorrisiko.

## C2. Scope-kontrakt (beskytter konsulentmarginen)

Analysen er et **produkt**, ikke en åben konsulentopgave. Fast scope i ordren:

| Felt | Eksempel |
|---|---|
| Område | ZIP-2300, defineret geometri |
| Lag | Fakta, Bevægelse, Hverdag, Efterspørgsel |
| Dybde | Antal claims, planlagte byggesager, institutionsdækning |
| Format | PDF + web-link, versioneret |
| Revisioner | **1 inkluderet**, herefter 4.500 kr./time |
| Leveringstid | 10 hverdage fra SCOPED |
| Datakilde-ansvar | Kilde+dato på hver påstand; ingen prognoser |

**Uden dette æder scope creep de 53 % dækningsbidrag.** Skriv det i ordren, ikke i en mail.

## C3. Leverance-pakken

```
analysis_{area_id}_v{version}/
├─ rapport.pdf            # vandmærket, versioneret, kildehenvisninger
├─ faktaark.csv           # zone A + C (k≥5), ingen persondata
├─ claims.json            # proveniens: source_id, dato, status, confidence
├─ metode.md              # kilder, friskhed, model_version, forbehold
└─ leverance_kvittering   # accept-tidsstempel, audit-ref
```

**Vandmærke + modtager-id** på PDF: kan spores ved lækage. Ingen zone B-data nogensinde i en leverance.

## C4. Faktura (danske krav, ikke generisk)

| Felt | Krav |
|---|---|
| Sælger | Optata ApS, CVR, adresse, bank/IBAN |
| Køber | Virksomhedsnavn, CVR |
| **EAN-nummer** | **Påkrævet** for kommune/region/pension visse steder — 13 cifre |
| Fakturanr. | Sekventielt, uafbrudt (bogføringskrav) |
| Dato + leveringsdato | Begge |
| Ydelse | "Områdeanalyse, ZIP-2300, v1" |
| Beløb | 85.000 kr. + **moms 25 % = 21.250** → **106.250 kr.** |
| Betalingsbetingelser | **Netto 30** (forhandling: netto 14 mod 2 % rabat) |
| Reference | Indkøbsordre/rekvirent — ellers afvises fakturaen af systemet |

**Vigtigt:** manglende EAN eller indkøbsreference er den hyppigste årsag til, at B2B-fakturaer til det offentlige og store selskaber ikke betales til tiden. Indsaml det i `SCOPED`, ikke ved fakturering.

## C5. Debitor og working capital (den post der manglede i planen)

```python
cash_forecast = ebitda_forecast \
  - receivables_delta(days_sales_outstanding=45) \
  - vat_payable_timing(quarterly) \
  + payables_delta(suppliers=30)
```

| Metric | Alarm |
|---|---|
| `dso_days` (debitorløbetid) | > 45 |
| `invoice_overdue_amount` | > 150.000 kr. |
| `vat_due_next_quarter` | Likviditet < vat + 1 måneds drift |
| `invoice_rejected_total{reason}` | EAN/reference mangler |

**Rykkerflow:** dag 31 venlig påmindelse → dag 45 rykker + gebyr 100 kr. → dag 60 inkasso-varsel. Automatiseret, men med manuel pause på strategiske kunder.

## C6. API

| Metode | Endpoint | Guard |
|---|---|---|
| POST | `/analyses` | Erhverv-auth, scope påkrævet |
| POST | `/analyses/{id}/scope` | EAN + reference + revisionsvilkår accepteret |
| POST | `/analyses/{id}/deliver` | `APPROVED` ellers 409 `PROFILE_NOT_APPROVED` |
| POST | `/analyses/{id}/accept` | Modtager-kvittering, audit |
| POST | `/analyses/{id}/invoice` | `DELIVERED`, idempotent, sekventielt nr. |
| POST | `/analyses/{id}/revision` | ≤1 gratis, ellers timepris accepteret |
| POST | `/webhooks/payment` | Signatur, idempotent, `PAID` |

## C7. Acceptkriterier

```
GIVEN profil PENDING           THEN deliver → 409 PROFILE_NOT_APPROVED
GIVEN scope uden EAN/reference THEN invoice blokeret (offentlig kunde)
GIVEN leveret + accepteret     THEN faktura 85.000 + 21.250 moms = 106.250
GIVEN gentaget invoice-kald    THEN samme fakturanr. (idempotent)
GIVEN 2. revision              THEN kræver accept af timepris
GIVEN leverance-payload        THEN ingen zone B-felter (CI-gate 5)
GIVEN faktura forfalden dag 45 THEN rykker + DSO-alarm
```

---

## Hvad de tre dele lukker

- **(a)** gør tæthed og match til **målbare, forklarbare størrelser** — og forhindrer at område-ordrer bliver til massehenvendelser.
- **(b)** gør ejer-kontakt til en **lovlig, dæmpet, samtykke-styret kanal** med frekvensloft og aggregering. Det er A2-motoren og GDPR-forsvaret i ét.
- **(c)** gør md. 4-indtægten **fakturerbar og betalbar** — med EAN, reference, scope-kontrakt og debitorstyring, som er den konkrete forskel på EBITDA og cash.

*Næste skridt kan være (a) ejerskabsverifikation i detaljer (EJF-match, andelsforening, selskab, dødsbo/fallback), (b) betalings- og abonnementsmodellen (eksklusivitet, binding, fornyelse, opsigelse, dunning), eller (c) sikkerheds- og trusselsmodel (STRIDE på vault, relay og reveal).*