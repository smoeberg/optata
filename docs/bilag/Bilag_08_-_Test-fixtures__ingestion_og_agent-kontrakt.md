# OPTATA — (a) Test-fixtures & acceptkriterier · (b) Ingestion-adapters · (c) Agent-kontrakt

Alle tre dele leveres. De er skrevet som **kontrakter**, ikke beskrivelser — dvs. de kan lægges direkte i repo som tests, adapters og prompt-spec.

---

# DEL A — Fixtures og acceptkriterier pr. sprint

## A0. Fælles fixtures (genbruges i alle sprints)

```yaml
FX-01 andelsforening:
  bfe: "BFE-1001"
  address_ids: 40 stk (etage/dør)
  owner_kind: ANDELSFORENING
  # 1:mange må aldrig kollapsere til én bolig

FX-02 udlejningsejendom:
  bfe: "BFE-2002", 12 enheder, owner_kind: COMPANY (CVR)

FX-03 samboende medkøbere:
  identity A og B, samme household_key (DAR-adresse)
  # dedup: én aktiv ordre, co-buyer tilladt

FX-04 udløbet attest:
  expires_at: i går, status: VALID (skal auto-nedgraderes)

FX-05 besked med kontaktinfo:
  tekst: "ring 2045 6677", billede med EXIF GPS + navneskilt

FX-06 mægler andet postnummer:
  subscription: ZIP-2300, query: ZIP-2400

FX-07 lille zone C-celle:
  3 verificerede ordrer i samme budget_band

FX-08 sletteanmodning med aktiv ordre:
  identity erased_at sat, order_event bevaret
```

## A1. Acceptkriterier (Gherkin-stil, kørbare)

**S1 — Registry + rapport + anonym ordre**
```
GIVEN anonym besøgende
WHEN GET /properties/{FX-01.address_id[7]}
THEN 200, attrs + valuation + plan, quality_flags vist
AND ingen felter fra zone B i payload

GIVEN FX-01 (40 enheder)
WHEN tæthed beregnes for ZIP-2300
THEN dwelling_count = 40 (ikke 1)

GIVEN anonym bruger opretter ordre med e-mail
WHEN POST /orders
THEN 201, level=CURIOS, pseudonym tildelt
AND order_event(type=CREATED) append-only

GIVEN samme e-mail opretter ordre på samme adresse igen
WHEN POST /orders
THEN 409 ORDER_ALREADY_ACTIVE (unik index)
```

**S2 — Agent + review + faktura**
```
GIVEN claim uden source_id
WHEN insert
THEN DB constraint afviser

GIVEN area_profile.review_state=PENDING
WHEN POST /analyses/{id}/deliver
THEN 409 PROFILE_NOT_APPROVED

GIVEN profil genereret
WHEN læses
THEN hver påstand har source_id + dato + status
AND model_version gemt
```

**S3 — MitID + attest + udløb**
```
GIVEN CURIOS-ordre med e-mail
WHEN MitID-login gennemføres
THEN identity_link oprettes, ordren opgraderes in-place
AND ingen dublet-ordre

GIVEN FX-04 (udløbet)
WHEN natligt expiry-job kører
THEN verification.status=EXPIRED, order.level=QUALIFIED
AND ordren fjernes fra mægler-lead-liste
AND order_event(VERIFICATION_EXPIRED)

GIVEN FX-03 samboende
WHEN begge opretter ordre på samme adresse
THEN én aktiv ordre + co-buyer (ikke to)
```

**S4 — Ejerskabsmatch + notifikation + ejerside**
```
GIVEN MitID-bruger uden EJF-match på adressen
WHEN GET /owner/interest/{address_id}
THEN 403 OWNERSHIP_NOT_VERIFIED

GIVEN FX-02 selskabsejet
WHEN MitID Erhverv med korrekt CVR
THEN ownership_verified via COMPANY_ROLE

GIVEN ejer afmelder
WHEN POST /owner/unsubscribe
THEN ingen fremtidige owner.notified på adressen
AND eksisterende tråde aborteres

GIVEN ejerside udløbet (12 uger)
WHEN dashboard tilgås
THEN 402 SUBSCRIPTION_EXPIRED
```

**S5 — Relay + reveal**
```
GIVEN FX-05
WHEN message sendes
THEN ikke leveret, message.redacted logget
AND EXIF strippet, afsender forklaret

GIVEN kun køber har givet samtykke
WHEN POST /reveal
THEN 409 MISSING_CONSENT, ingen vault-læsning i audit

GIVEN alle 6 guards opfyldt
WHEN POST /reveal
THEN 200, RevealGrant oprettet, audit(zone=B)
AND gentaget kald er idempotent

GIVEN FX-06 mægler
WHEN lead-liste på andet postnummer
THEN tom liste (RLS), ikke 200 med data

GIVEN FX-07
WHEN zone C-eksport
THEN cellen udeladt (k<5)

GIVEN FX-08 sletning
WHEN erase udføres
THEN identity+evidence slettet, order_event bevaret pseudonymt
```

**Definition of Done pr. sprint:** alle ovenstående tests grønne · audit-log dækker zone B-kald · ingen prod-persondata i dev · menneskelig review af finansiel/juridisk logik.

---

# DEL B — Ingestion-adapters (BBR, DAR, EBR, EJF, VUR)

## B1. Fælles adapter-kontrakt

```python
class SourceAdapter(Protocol):
    source: str                      # 'BBR' | 'DAR' | ...
    def fetch(self, area_id, since: datetime) -> Iterator[RawRecord]: ...
    def normalize(self, raw) -> NormalizedRecord: ...
    def validate(self, rec) -> list[Issue]: ...
    def upsert(self, rec) -> ChangeEvent | None: ...   # bitemporal, idempotent
```

**Fælles regler:** checkpoint pr. kørsel · idempotensnøgle = (kilde, naturlig nøgle, version) · fejl → `quarantine`-tabel, aldrig stille drop · alle felter får `quality_flag` hvis usikre.

## B2. Feltmapping

| Kilde | Naturlig nøgle | Felter → Optata | Validering |
|---|---|---|---|
| **DAR** | `adresse_id` (UUID) | vej, husnr, etage, dør, postnr, status | Status=aktiv; UUID-format; postnr findes i `area` |
| **EBR** | `adresse_id`+`bfe` | koordinat, geometri | Point inden for `area.geom`; SRID 4326 |
| **BBR** | `bygning_id`+`enhed_id` | anvendelse, boligareal, værelser, opførelsesår, opvarmning, etager | areal>0 og <2000; værelser 1–20; anvendelse ∈ bolig-koder; år 1400–nu+5 |
| **EJF** | `bfe`+`ejer_id` | ejertype (privat/selskab/andelsforening), andelsforhold, CVR | owner_kind ∈ enum; CVR-modulus-11 hvis selskab |
| **VUR** | `bfe`/`adresse_id`+`dato` | vurdering, grundværdi, skattetal | amount>0; sanity: 0,1–50 mio.; flag `VUR_UNVERIFIED` |
| **Matrikel** | `matrikel_id`+`ejerlav` | areal, geometri | grundareal>0; geometri valid (ST_IsValid) |

## B3. Samlingslogik (den kritiske)

```
DAR.adresse_id  ──EBR──> BFE ──BBR──> bygning/enhed
                          │
                          ├──EJF──> owner_kind, CVR
                          └──VUR──> valuation
```

**Regler:**
1. **BFE → adresse_id er 1:mange.** Ingen upsert må aggregere enheder væk (FX-01).
2. `area_id` udledes af DAR-postnr, verificeres mod EBR-geometri. Konflikt → quarantine.
3. `dwelling_count` = antal aktive DAR-adresser med BBR-boliganvendelse i området. **Det er nævneren i tætheden** — fejl her ødelægger alle KPI'er.
4. Bitemporal upsert: luk `valid_to` på gammel version, indsæt ny med `recorded_at=now`. Emit `property.changed` → driver overvågningsproduktet.

## B4. Kørselsplan

| Kilde | Frekvens | Metode |
|---|---|---|
| DAR, EBR, EJF | Dagligt | Delta siden sidste checkpoint |
| BBR | Dagligt/ugentligt | Delta |
| VUR | Årligt + ved ændring | Fuld refresh pr. område |
| Matrikel | Ugentligt | Delta |
| Plan/byggesager | Ugentligt + manuel kuratering | Adapter pr. kommune + review-kø |

**KPI på datakvalitet:** dækningsgrad pr. register, quarantine-rate, andel felter med quality_flag. Dette eksponeres i B2B-dashboardet — det er et salgsargument.

---

# DEL C — Agentens claim-kontrakt

## C1. Output-schema (LLM må kun returnere dette)

```jsonc
{
  "claims": [{
    "subject": "Lokalplan 214, Amager",
    "predicate": "VEDTAGET",
    "value": { "boliger": 80, "type": "etagebolig", "hoejde_max": "5 etager" },
    "status": "VEDTAGET",          // VEDTAGET|FORESLAET|UNDER_BYGNING|STOPPET|RYGTE
    "effective_date": "2026-03-12",
    "source_id": "uuid",           // SKAL findes i source_document
    "quote": "…kort uddrag, max 200 tegn…",
    "confidence": 0.86
  }],
  "rejected": [{ "reason": "NO_SOURCE" | "NO_DATE" | "OPINION" | "DUPLICATE", "text": "…" }]
}
```

## C2. Prompt-kontrakt (system-regler)

```
Du udtrækker FAKTA om et område til en boligmarkedsanalyse.

MÅ:
- Udtrække påstande direkte understøttet af det medfølgende kildedokument.
- Angive source_id og effective_date for hver påstand.
- Klassificere status: VEDTAGET / FORESLAET / UNDER_BYGNING / STOPPET / RYGTE.
- Returnere kort citat (≤200 tegn) som dokumentation.

MÅ IKKE:
- Skrive fri tekst, vurderinger, prognoser eller anbefalinger.
- Udtrække påstande uden kilde eller dato → læg i "rejected".
- Bruge viden uden for de medfølgende dokumenter.
- Behandle personoplysninger (input er zone A only).

Output: kun JSON iht. schema. Ingen forklaring uden for JSON.
```

## C3. Afvisningsregler (deterministisk, efter LLM)

| Regel | Handling |
|---|---|
| `source_id` findes ikke i DB | REJECT `NO_SOURCE` |
| `effective_date` mangler/ugyldig | REJECT `NO_DATE` |
| `quote` > 200 tegn eller ikke fundet i kilden (fuzzy-match) | REJECT `QUOTE_MISMATCH` |
| `status=RYGTE` | Behold, men **må ikke** i "Bevægelse"-laget; kun i intern kø |
| Predicate ∈ opinionsliste ("attraktivt", "lovende", "bør") | REJECT `OPINION` |
| Duplet (subject+predicate+date+source) | Merge, højeste confidence |
| `confidence < 0.6` | Til manuel review, ikke auto-publish |

## C4. Publicerings-gate

```python
def publish(profile_id):
    require(all(c.review_state == 'APPROVED' for c in profile.claims))
    require(all(c.source_id and c.effective_date for c in profile.claims))
    require(profile.reviewed_by is not None)      # menneske, fase 1–2
    require(no_zone_B_fields(profile))
    profile.state = 'PUBLISHED'
    emit('profile.published', version=profile.version)
```

## C5. Friskhed og caching

- Profil caches pr. område; ny kørsel kun ved `property.changed`, ny `source_document` eller manuel trigger.
- Hver påstand viser **status + dato + kilde** i UI. Vedtaget ≠ rygtet.
- `model_version` + `prompt_version` gemmes → reproducerbarhed ved fejlretning.
- Omkostningskontrol: kun nye/ændrede dokumenter sendes til LLM; resten genbruges.

## C6. Agent-fixtures

```
FX-A1 artikel uden dato → rejected NO_DATE
FX-A2 "området er lovende" → rejected OPINION
FX-A3 lokalplan vedtaget, kilde+dato → claim VEDTAGET, publish-klar efter review
FX-A4 rygtesag fra debatindlæg → status RYGTE, ikke i Bevægelse-laget
FX-A5 citat ikke i kilden → QUOTE_MISMATCH
FX-A6 samme plan i to medier → merge, én claim
```

---

## Hvad dette giver

- **(a)** gør hvert sprint testbart og hvert guard bevisligt — AI-genereret kode kan verificeres mod det.
- **(b)** sikrer at datamodel og tæthed er korrekte fra dag 1 (BFE 1:mange, dwelling_count, bitemporalitet).
- **(c)** gør agenten til en **fakta-maskine med proveniens** i stedet for en tekstgenerator — det, en bank kan bruge.

*Næste naturlige skridt: (a) repo-struktur og CI-gates (hvad der må genereres vs. skal skrives i hånden), (b) API-kontrakter som OpenAPI-fil, eller (c) drifts- og observability-spec (datakvalitet, expiry-jobs, redaction-metrics).*