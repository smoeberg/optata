# OPTATA — (a) Ejerskabsverifikation · (b) Betaling & abonnement · (c) Trusselsmodel (STRIDE)

---

# DEL A — Ejerskabsverifikation (den guard der beskytter alt)

## A1. Vigtig korrektion: EJF er ikke frit tilgængelig

Planen siger "EJF-match". Det skal nuanceres, ellers bygges en guard på en adgang I ikke har:

| Kilde | Adgang | Brugbarhed |
|---|---|---|
| **EJF (Ejerfortegnelsen)** | Kræver aftale/berettigelse via Datafordeleren — ikke åben for alle | Bedst, men **adgang skal bekræftes i uge 1** |
| **Tingbogen (adkomst/skøde)** | Offentlig, kan slås op pr. ejendom | God fallback; **tinglysningsforsinkelse** giver huller |
| **MitID + dokumentation** | Brugermedvirkende | Universel fallback, manuel review |

**Konsekvens:** design `ownership_verification` med **flere metoder** og en eksplicit fallback-kø. Hvis EJF-adgang afvises, skal produktet stadig virke — blot med manuel behandling i starten.

## A2. Ejerskabstyper (det er her det bliver svært)

| Type | Hvem er "ejer" i registeret | Verifikationsmetode |
|---|---|---|
| **Parcelhus/ejerlejlighed, privat** | Fysisk person | EJF-match eller tinglyst adkomst + MitID |
| **Andelsbolig** | **Foreningen** ejer ejendommen; andelshaver har andel | **EJF dur ikke.** Andelsbevis + forening/administrator-attest |
| **Selskabsejet (CVR)** | Juridisk person | MitID Erhverv + CVR-match + tegningsret |
| **Udlejningsejendom** | Selskab/privat | Som ovenfor; kun ejeren ser efterspørgsel, ikke lejerne |
| **Dødsbo** | Boet | Skifteretsattest + kontaktadvokat |
| **Værge/fuldmagt** | Ejeren, repræsenteret | Fuldmagt + værgebeskikkelse, altid manuel |
| **Sameje (flere ejere)** | 2+ personer | Én verifikation pr. ejer; **alle skal samtykke til reveal** |

**Kritisk designbeslutning:** andelsboliger er ~en stor del af storbyens boligmasse. Uden andels-flowet er pilotområdet reelt halvt dækket. Byg det i S4, ikke som senere tilføjelse.

## A3. Match-algoritme med konfidens

```python
def verify_ownership(identity, address_id) -> Result:
    prop = registry.get(address_id)

    # 1. Direkte register-match (stærkest)
    if ejf_available():
        owners = ejf.owners(prop.bfe)
        if identity.provider == "MITID_ERHVERV" and identity.cvr in owners.cvr:
            return VERIFIED(method="EJF_CVR", confidence=HIGH, ttl=180d)
        if identity_matches_name(identity, owners.persons):   # transient, gemmes ikke
            return VERIFIED(method="EJF_PERSON", confidence=HIGH, ttl=180d)

    # 2. Tinglyst adkomst (offentlig fallback)
    deed = tingbogen.adkomst(prop.bfe)
    if deed and identity_matches(identity, deed):
        return VERIFIED(method="DEED", confidence=MEDIUM, ttl=90d)
        # NB: tinglysningsforbehold → ny ejer kan mangle i op til måneder

    # 3. Andelsbolig
    if prop.owner_kind == "ANDELSFORENING":
        return PENDING_MANUAL(reason="ANDELSBEVIS_REQUIRED",
                              required_docs=["andelsbevis", "administrator_attest"])

    # 4. Alt andet → manuel kø
    return PENDING_MANUAL(reason="NO_REGISTER_MATCH")
```

**Navnematch er transient:** navn fra MitID sammenlignes i hukommelsen mod register, **gemmes aldrig**, logges aldrig. Kun resultatet (`VERIFIED`, metode, tidspunkt) persisteres.

## A4. Manuel kø (fallback der ikke må blive en flaskehals)

| Sagstype | Krævet dokumentation | Behandlingstid | Hvem |
|---|---|---|---|
| Andelsbevis | Andelsbevis + administrator-attest | 1–2 hverdage | DK-stifter |
| Dødsbo | Skifteretsattest | 2–3 dage | DK + jurist |
| Fuldmagt | Fuldmagt + identitet på begge | 2–3 dage | DK + jurist |
| Sameje | Alle ejere verificeret separat | pr. ejer | DK |
| Register-mismatch | Skøde/ejendomsskattebillet | 1–2 dage | DK |

**Kapacitet:** ved 100 ejere i pilot og ~25 % fallback = 25 sager × 15 min ≈ **6 timer**. Overkommeligt. Ved 12 bydele bliver det ~75 timer/år — automatisér andels-flowet først (administrator-API eller standardiseret attest).

## A5. Datamodel og udløb

```sql
CREATE TABLE ownership_verification (
  id            uuid PRIMARY KEY,
  identity_id   uuid NOT NULL,
  address_id    text,  bfe text,
  method        text NOT NULL,   -- EJF_PERSON|EJF_CVR|DEED|ANDELS_ATTEST|MANUAL|POWER_OF_ATTORNEY
  confidence    text NOT NULL,   -- HIGH|MEDIUM|LOW
  share         numeric,         -- sameje: ejerandel
  status        text NOT NULL,   -- PENDING|VERIFIED|REJECTED|EXPIRED
  evidence_hash text,            -- dokument i vault, kort retention
  reviewed_by   text,
  verified_at   timestamptz,
  expires_at    timestamptz NOT NULL,   -- 90–180 dage
  UNIQUE (identity_id, coalesce(address_id, bfe))
);
```

**Genverifikation:** ved `property.changed` med ejerskifte → **automatisk tilbagekald** af eksisterende verifikation. Ellers kan en tidligere ejer blive ved med at se efterspørgsel på en bolig, de har solgt. Det er en alvorlig fejl — test den.

## A6. Acceptkriterier

```
GIVEN andelsbolig (FX-01)      THEN EJF-match må IKKE bruges; manuel kø oprettes
GIVEN MitID Erhverv m. korrekt CVR på selskabsejet (FX-02) THEN VERIFIED
GIVEN ejerskifte i registry    THEN eksisterende ownership → EXPIRED, adgang fjernet
GIVEN sameje med 2 ejere       THEN reveal kræver BEGGE verifikationer + samtykker
GIVEN uverificeret bruger      THEN 403 OWNERSHIP_NOT_VERIFIED, ingen interest-data
GIVEN navnematch udført        THEN intet navn i DB, logs eller events
GIVEN verifikation udløbet     THEN adgang blokeret, genverifikation tilbudt
```

---

# DEL B — Betaling, abonnement og eksklusivitet

## B1. Betalingsmetoder pr. produkt

| Produkt | Metode | Note |
|---|---|---|
| Ejerside 1.495 (engangs) | Kort/MobilePay | Øjeblikkelig adgang, fortrydelse håndteres |
| Salgspakke 10.000 (engangs) | Kort/bankoverførsel | **Ikke escrow** — kun gebyr, aldrig købesum |
| Mægler 2.900/6.900 (abonnement) | Betalingsservice/PBS eller kort-abonnement | Dansk B2B-standard, lav churn-friktion |
| Overvågning 4.500, Demand Pro 9.500 | Faktura netto 30 + EAN | Indkøbsreference påkrævet |
| Analyse 85.000 | Faktura netto 30 + EAN | Som DEL C i forrige afsnit |

**Provider:** EU-baseret (Nets/Paylike/Stripe EU). **Optata rører aldrig købesummen i en bolighandel** — det ville udløse betalingstjeneste- og hvidvaskkrav.

## B2. Fortrydelsesret (dansk forbrugerret — må ikke overses)

| Produkt | Regel | Implementering |
|---|---|---|
| **Ejerside 1.495** | 14 dages fortrydelse ved fjernsalg af tjenesteydelse | Udtrykkeligt samtykke til **øjeblikkelig levering** + bekræftelse af, at fortrydelsesretten derved kan bortfalde/forholdsmæssigt afkortes. Checkbox med tekstversion gemt. |
| **Salgspakke 10.000** | 14 dage, men ydelsen påbegyndes typisk straks | Samme mekanisme + forholdsmæssig betaling for allerede leveret arbejde |
| **B2B-abonnementer** | Ingen forbrugerfortrydelse | Bindingsperiode i kontrakt |

```jsonc
// consent.granted
{ "purpose":"IMMEDIATE_DELIVERY_WAIVER", "text_version":"v1.0",
  "scope":{"product":"OWNER_PASS"}, "granted_at":"…" }
```

**Uden dette er hver eneste ejerside-salg en potentiel klagesag.** Det er en lille checkbox med stor juridisk vægt.

## B3. Eksklusivitet — håndhævet i databasen

```sql
CREATE TABLE subscription (
  id          uuid PRIMARY KEY,
  org_id      uuid NOT NULL,           -- CVR-bundet via MitID Erhverv
  product     text NOT NULL,           -- AGENT_ZIP|AGENT_DISTRICT|MONITORING|DEMAND_PRO|OWNER_PASS
  scope_id    text NOT NULL,           -- ZIP-2300 | DIST-NOERREBRO | address_id
  period_start date NOT NULL,
  period_end   date NOT NULL,
  binding_months int NOT NULL,         -- 6 for AGENT_ZIP, 12 for DISTRICT
  status      text NOT NULL,           -- ACTIVE|PENDING_CANCEL|EXPIRED
  auto_renew  boolean DEFAULT true
);

-- Én aktiv mægler pr. postnummer — DB-garanti, ikke forretningslogik
CREATE UNIQUE INDEX exclusive_agent_per_zip
  ON subscription (scope_id)
  WHERE product IN ('AGENT_ZIP','AGENT_DISTRICT') AND status='ACTIVE';
```

**Overlap-regel:** bydel-abonnement (1–2 postnumre) blokerer postnummer-abonnement i samme område og omvendt. Løs med `scope_overlap`-check før insert + advisory lock, så to samtidige salg ikke begge lykkes.

## B4. Livscyklus

```
TRIAL/PENDING → ACTIVE → RENEWAL_DUE(d-30) → RENEWED
                    └→ CANCEL_NOTICE → PENDING_CANCEL → EXPIRED(ved periodeudløb)
                    └→ PAYMENT_FAILED → DUNNING → SUSPENDED → EXPIRED
```

| Hændelse | Handling |
|---|---|
| Opsigelse i binding | Registreres, adgang fortsætter til periodeudløb |
| Ved opsigelse | **Køberne følger postnummeret, ikke mægleren** (§9) — leads frigives til næste kunde |
| Fornyelse | Auto-renew med 30 dages varsel + prisændringsvarsel |
| Betaling fejlet | Dag 3 retry → dag 7 påmindelse → dag 14 suspenderet → dag 30 opsagt |

**Vigtigt:** ved `EXPIRED` skal RLS-cachen invalideres **øjeblikkeligt**, ellers ser en tidligere mægler stadig leads. Test det.

## B5. Dunning og churn-metrics

```
subscription_renewal_rate{product}      # mål ≥70% for AGENT_ZIP (6 mdr.)
subscription_churn_reason{reason}       # PRICE|NO_LEADS|NO_DEALS|SWITCHED
leads_per_subscription_per_month        # værdi-bevis: <5 → churn-risiko
payment_failed_total / dunning_recovery_rate
mrr_by_product / arr
```

**Proaktiv churn-forebyggelse:** hvis `leads_per_month < 5` i to måneder → automatisk kundesucces-opgave. Det er billigere end at gensælge.

## B6. Acceptkriterier

```
GIVEN to samtidige køb på ZIP-2300   THEN kun ét lykkes (unique index + lock)
GIVEN bydel-abonnement aktivt        THEN postnummer-køb i området afvises
GIVEN opsigelse i binding            THEN adgang til period_end, ingen refusion
GIVEN abonnement EXPIRED             THEN lead-liste tom inden for 60 sek (RLS-invalidering)
GIVEN ejerside-køb uden waiver       THEN levering blokeret (fortrydelsesret)
GIVEN betaling fejlet 3 gange        THEN SUSPENDED, ikke slettet (genaktivering mulig)
GIVEN refusion                       THEN kreditnota med eget sekventielt nr.
```

---

# DEL C — Trusselsmodel (STRIDE på de tre kritiske komponenter)

## C1. Aktiver og kronjuveler

| Aktiv | Værdi for angriber | Konsekvens ved brud |
|---|---|---|
| **IdentityVault** | Navn, kontakt, MitID-reference | GDPR-brud, P1, banksalg dør |
| **Verifikationsbeviser** | Bankdokumenter, beløb | Svindel, identitetstyveri |
| **Ordrebogen** | Hvem vil købe hvad, hvor | Konkurrent kan kopiere moaten |
| **Relay-tråde** | Prisforhandlinger | Tillidsbrud, lækage |
| **Reveal-mekanismen** | Kobling pseudonym↔identitet | **Det mest følsomme enkeltkald i systemet** |

## C2. STRIDE — Vault

| Trussel | Angreb | Mitigation | Test |
|---|---|---|---|
| **S**poofing | Udvikler udgiver sig for disclosure-service | mTLS/service-identity; DB-rolle kun for `disclosure_service` | `vault.accessed{service≠disclosure}` → P1 |
| **T**ampering | Ændre attestbeløb i DB | Append-only verification + evidence_hash; ændring = ny record | Hash-validering ved læsning |
| **R**epudiation | "Jeg udleverede ikke identiteten" | Uforanderlig audit, 5 år, grant-id | Audit kan ikke UPDATE/DELETE |
| **I**nfo disclosure | SQL-injection/over-fetching via API | RLS + `additionalProperties:false` + parameteriserede queries | CI-gate 5: zone B i public payload |
| **D**oS | Masseopslag på adresser | Rate limit pr. session/IP, caching af zone A | Load-test |
| **E**levation | Support-rolle får vault-adgang | Separate roller, ingen vault i support-UI | RBAC-test pr. rolle |

## C3. STRIDE — Relay

| Trussel | Angreb | Mitigation | Test |
|---|---|---|---|
| **S** | Skrive som modparten | Sender = auth-context pseudonym, aldrig fra payload | Forged-sender-test |
| **T** | Ændre beskeder/pris efter enighed | Beskeder append-only; `agreed_terms_hash` låses ved PRICE_AGREED | Manipulations-test |
| **R** | Benægte aftalt pris | Hash + tidsstempel + begge parters klik, audit | Reveal kræver matchende hash |
| **I** | **Lækage af kontaktinfo** (forretningskritisk) | Deterministisk redaction (regex→NER→EXIF/OCR→adfærd), LLM kun supplement | FX-05 + stavevarianter |
| **I** | Læse andres tråd | RLS på thread-deltagelse | Cross-thread-test |
| **D** | Spam/flooding | Rate limit, karantæne ved gentagne redaction-træff | Repeat-offender-test |
| **E** | Mægler åbner tråd som part | Mægler er aldrig `deal.party` | Agent-reveal → 403 |

**Særlig risiko — omgåelse via mønstre:** "ring til mig på to nul fire fem…". Regex fanger ikke alt. Mitigation: adfærdsanalyse + LLM-klassifikator som **andet** lag, samt at gøre pakken attraktiv nok til at omgåelse er unødvendig.

## C4. STRIDE — Reveal (det mest følsomme kald)

| Trussel | Angreb | Mitigation |
|---|---|---|
| **S** | Reveal kaldt med stjålet session | Kræver **frisk MitID step-up** (max 5 min gammelt), ikke bare login |
| **T** | Manipulere deal-state til PACKAGE_ACCEPTED | State-transitions kun via domæne-events; betaling verificeres server-side mod provider |
| **R** | Benægte samtykke | `consent.granted` med `text_version` + `consent_ref`, append-only |
| **I** | **Reveal uden modpartens samtykke** | Guard: begge samtykker i **samme transaktion** som vault-læsning |
| **I** | Reveal til tredjepart (mægler/partner) | Kun de to parter; partner får kun det nødvendige til fulfillment |
| **D** | Reveal-spam | Idempotency-Key; gentaget kald returnerer eksisterende grant |
| **E** | Intern medarbejder kalder reveal | Ingen admin-endpoint til reveal; kun bruger-flow med step-up |

**Race condition (skal testes eksplicit):** to samtidige reveal-kald må ikke producere to grants eller to audits. Brug `SELECT … FOR UPDATE` på deal-rækken + idempotensnøgle.

**Time-of-check/time-of-use:** attest kan udløbe mellem guard-check og vault-læsning. Løsning: alle checks og læsning i **én DB-transaktion** med lås.

## C5. Tværgående trusler

| Trussel | Mitigation |
|---|---|
| **Re-identifikation** af anonym køber (få ordrer i lille område) | Budget-**intervaller** ikke præcise beløb; k≥5 i zone C; ingen præcis adresse på køber |
| **Insider/UA-adgang** | Ingen prod-adgang, syntetiske data, break-glass med audit og tidsbegrænsning |
| **Supply chain (AI-genereret kode)** | Afhængigheds-/licensscan, SAST, lockfiles, CODEOWNERS på guards |
| **Prompt injection i agent** | Input er zone A-dokumenter; output valideres mod schema; ingen tool-kald til zone B |
| **Backup-lækage** | Krypterede backups, EU-only, restore-test, adgang ligesom prod |
| **Enumeration** af adresser/ordrer | Rate limit, ingen sekventielle ID'er i public API (UUID) |

## C6. Sikkerhedstests som CI-gates

```
tests/guards/
├─ test_vault_only_disclosure.py       # DB-rolle + audit
├─ test_reveal_all_six_guards.py       # hver guard afviser isoleret
├─ test_reveal_concurrent_idempotent.py# race → ét grant
├─ test_reveal_toc_tou_expiry.py       # udløb mellem check og brug
├─ test_redaction_corpus.py            # FX-05 + 50 varianter
├─ test_rls_agent_scope.py             # FX-06
├─ test_k_anonymity.py                 # FX-07
├─ test_no_zone_b_in_public.py         # schema + payload-scan
└─ test_erasure_preserves_events.py    # FX-08
```

**Regel:** ingen af disse må AI-genereres. De skrives af mennesker, køres på hver PR, og en rød test blokerer merge uden undtagelse.

---

## Hvad de tre dele lukker

- **(a)** gør ejerskabsverifikation **realistisk** (EJF-adgang er ikke givet, andelsboliger kræver eget flow) og forhindrer den alvorlige fejl, at tidligere ejere bevarer adgang.
- **(b)** gør eksklusivitet til en **DB-garanti**, håndterer dansk fortrydelsesret korrekt og sikrer at køberne følger postnummeret — ikke mægleren.
- **(c)** gør de mest følsomme kald (**vault, relay, reveal**) til testbare sikkerhedsegenskaber i stedet for antagelser.

*Næste skridt kan være (a) den samlede leveranceplan S1–S7 med estimer og afhængigheder (hvad UA-teamet bygger i hvilken rækkefølge), (b) data retention- og slettepolitik som konkret jurist-bilag, eller (c) API- og UI-kontrakten for Demand Pro (B2B-dashboard, eksport, k-anonymitet i praksis).*