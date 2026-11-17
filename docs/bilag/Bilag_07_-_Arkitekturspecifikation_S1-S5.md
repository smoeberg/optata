# OPTATA — Arkitekturspecifikation S1–S5

Tre dele: **(A)** database + API for S1/S2, **(B)** relay- og reveal-protokol med guards, **(C)** skærm-for-skærm køber- og ejerflow. Alt er byggeklart og sporbart til cases.

---

# DEL A — Database og API (S1: registry/rapport/ordre · S2: agent/analyse)

## A1. Skema (PostgreSQL + PostGIS)

```sql
-- ═══ ZONE A: offentlige data (dev-tilgængelig) ═══

CREATE TABLE area (
  area_id        text PRIMARY KEY,           -- 'ZIP-2300' | 'DIST-NOERREBRO'
  area_type      text NOT NULL,              -- ZIP | DISTRICT
  name           text NOT NULL,
  geom           geometry(MultiPolygon,4326) NOT NULL,
  dwelling_count int  NOT NULL,              -- nævner i tæthed
  updated_at     timestamptz NOT NULL
);
CREATE INDEX area_geom_gix ON area USING gist(geom);

CREATE TABLE property (
  bfe            text NOT NULL,
  address_id     text NOT NULL,              -- DAR: boligen/enheden
  matrikel_id    text,
  geom           geometry(Point,4326) NOT NULL,
  area_id        text NOT NULL REFERENCES area,
  attrs          jsonb NOT NULL,             -- BBR: type, areal, værelser, år
  owner_kind     text,                       -- PRIVATE | COMPANY | ANDELSFORENING
  quality_flags  jsonb DEFAULT '{}',         -- felt-level usikkerhed
  valid_from     date NOT NULL,
  valid_to       date,                       -- NULL = gældende
  recorded_at    timestamptz NOT NULL,       -- transaction_time
  PRIMARY KEY (address_id, recorded_at)
);
CREATE INDEX prop_bfe_ix   ON property(bfe);          -- 1:mange BFE→adresser
CREATE INDEX prop_area_ix  ON property(area_id) WHERE valid_to IS NULL;
CREATE INDEX prop_geom_gix ON property USING gist(geom);

CREATE TABLE valuation (                      -- VUR: reference, ikke sandhed
  bfe text, address_id text, amount bigint, grundvaerdi bigint,
  valuation_date date, source text, recorded_at timestamptz,
  PRIMARY KEY (address_id, valuation_date)
);

CREATE TABLE source_document (                -- agentens kildegrundlag
  source_id     uuid PRIMARY KEY,
  kind          text NOT NULL,                -- MEDIA | PLAN | BUILDING | CVR | DST
  url           text, publisher text,
  published_at  date NOT NULL,
  retrieved_at  timestamptz NOT NULL,
  license_ref   text NOT NULL,                -- må ikke være NULL
  excerpt       text,                         -- kort uddrag, licenseret
  storage_key   text                          -- objektlager, EU
);

CREATE TABLE claim (
  claim_id      uuid PRIMARY KEY,
  area_id       text REFERENCES area,
  subject       text NOT NULL,                -- 'Lokalplan 214'
  predicate     text NOT NULL,                -- 'VEDTAGET'
  value         jsonb NOT NULL,
  status        text NOT NULL,                -- VEDTAGET|FORESLAET|UNDER_BYGNING|STOPPET|RYGTE
  effective_date date,
  source_id     uuid NOT NULL REFERENCES source_document,
  confidence    numeric(3,2) NOT NULL,
  model_version text NOT NULL,
  review_state  text NOT NULL DEFAULT 'PENDING', -- PENDING|APPROVED|REJECTED
  reviewed_by   text, reviewed_at timestamptz,
  CONSTRAINT claim_needs_source CHECK (source_id IS NOT NULL),
  CONSTRAINT claim_needs_date   CHECK (effective_date IS NOT NULL OR published_date_present())
);

CREATE TABLE area_profile (                   -- cached leverance
  profile_id    uuid PRIMARY KEY,
  area_id       text REFERENCES area,
  version       int NOT NULL,
  layers        jsonb NOT NULL,               -- fakta|bevaegelse|hverdag|efterspoergsel
  review_state  text NOT NULL,                -- PENDING|APPROVED
  generated_at  timestamptz NOT NULL,
  UNIQUE (area_id, version)
);

-- ═══ ZONE B: persondata (kun prod, RLS, audit) ═══

CREATE TABLE identity (
  identity_id     uuid PRIMARY KEY,
  provider        text NOT NULL,              -- EMAIL|MITID_PRIVATE|MITID_ERHVERV
  pseudonym       text UNIQUE NOT NULL,       -- 'K-7F3A' / 'E-2B91'
  provider_sub    text UNIQUE,                -- broker-pseudonym, ALDRIG CPR
  assurance       text NOT NULL,              -- LOW|SUBSTANTIAL|HIGH
  cvr             text,
  household_key   text,                       -- DAR adresse-id, dedup
  created_at      timestamptz NOT NULL,
  erased_at       timestamptz
);

CREATE TABLE identity_link (
  from_id uuid, to_id uuid, reason text, linked_at timestamptz,
  PRIMARY KEY (from_id, to_id)
);

CREATE TABLE orders (
  order_id        uuid PRIMARY KEY,
  buyer_id        uuid NOT NULL REFERENCES identity,
  area_id         text NOT NULL REFERENCES area,
  scope           text NOT NULL,              -- AREA|ADDRESS
  address_id      text,                       -- krævet hvis scope=ADDRESS
  criteria        jsonb NOT NULL,             -- type, areal, værelser, budget, horisont
  level           text NOT NULL,              -- CURIOS|QUALIFIED|VERIFIED
  status          text NOT NULL,              -- ACTIVE|PAUSED|MATCHED|IN_DIALOG|AGREED|WITHDRAWN|EXPIRED
  created_at      timestamptz NOT NULL,
  last_signal_at  timestamptz NOT NULL
);
-- §2.3: én aktiv ordre pr. husstand+scope
CREATE UNIQUE INDEX order_one_active
  ON orders (buyer_id, scope, coalesce(address_id, area_id))
  WHERE status IN ('ACTIVE','PAUSED','MATCHED','IN_DIALOG','AGREED');

CREATE TABLE order_event (                    -- append-only, moaten
  event_id    bigserial PRIMARY KEY,
  order_id    uuid NOT NULL,
  type        text NOT NULL,
  payload     jsonb NOT NULL,
  actor       text NOT NULL,
  occurred_at timestamptz NOT NULL
);
CREATE INDEX order_event_ix ON order_event(order_id, occurred_at);
REVOKE UPDATE, DELETE ON order_event FROM app_role;

CREATE TABLE verification (
  verification_id uuid PRIMARY KEY,
  order_id        uuid REFERENCES orders,
  method          text NOT NULL,              -- BANK_DOCUMENT|BANK_ATTESTATION|BANK_API|EQUITY
  issuer          text NOT NULL,
  approved_amount bigint NOT NULL,
  issued_at       date NOT NULL,
  expires_at      date NOT NULL,
  evidence_hash   text NOT NULL,
  evidence_key    text,                       -- krypteret vault, kort retention
  status          text NOT NULL,              -- PENDING|VALID|EXPIRED|REJECTED|REVOKED
  reviewed_by     text, reviewed_at timestamptz
);

CREATE TABLE ownership_verification (
  identity_id  uuid REFERENCES identity,
  address_id   text, bfe text,
  method       text NOT NULL,                 -- EJF_MATCH|MANUAL|COMPANY_ROLE
  verified_at  timestamptz NOT NULL,
  expires_at   timestamptz NOT NULL,
  PRIMARY KEY (identity_id, coalesce(address_id, bfe))
);

-- ═══ ZONE C: aggregeret (B2B-safe) ═══
CREATE MATERIALIZED VIEW area_demand AS
SELECT area_id, criteria->>'type' AS boligtype,
       width_bucket((criteria->>'budget_max')::bigint, 0, 20000000, 20) AS budget_band,
       count(*) AS verified_count
FROM orders
WHERE level='VERIFIED' AND status='ACTIVE'
GROUP BY 1,2,3
HAVING count(*) >= 5;                          -- k-anonymitet håndhævet i view
```

**RLS-politikker (zone B):**
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY buyer_own ON orders USING (buyer_id = current_identity());
CREATE POLICY agent_scope ON orders USING (
  level='VERIFIED' AND status='ACTIVE' AND area_id IN (
    SELECT scope_id FROM subscription
    WHERE org_id=current_org() AND product='AGENT_ZIP' AND status='ACTIVE'));
```

## A2. API (S1 + S2)

| Metode | Endpoint | Auth | Zone | Case |
|---|---|---|---|---|
| GET | `/areas?q=` | – | A | C1 |
| GET | `/areas/{id}/profile` | – | A | C1 |
| GET | `/properties/{address_id}` | – | A | C2 |
| POST | `/orders` | e-mail-session | B | C1/C2 |
| POST | `/orders/{id}/qualify` | MitID | B | C2 |
| POST | `/orders/{id}/verification` | MitID | B | C8 |
| GET | `/me/orders` | MitID | B | C2 |
| POST | `/orders/{id}/withdraw` | MitID | B | C9 |
| POST | `/analyses` | Erhverv | A+C | C7 |
| GET | `/analyses/{id}` | Erhverv | A+C | C7 |
| POST | `/internal/profiles/{id}/review` | staff | A | C7 |
| POST | `/internal/verifications/{id}/review` | staff | B | C8 |

**Kontrakter (uddrag):**
```jsonc
// POST /orders  (CURIOS, ingen MitID)
{ "scope":"ADDRESS", "address_id":"0a3f50a1-...", "area_id":"ZIP-2300",
  "criteria":{"type":"VILLA","areal_min":140,"rooms_min":4,
              "budget_max":4200000,"horizon":"3-6M"},
  "email":"..." }
→ 201 { "order_id":"...", "pseudonym":"K-7F3A", "level":"CURIOS",
        "next":"VERIFY_IDENTITY" }

// GET /properties/{address_id}  (zone A, ét opslag)
{ "address_id":"...", "bfe":"...", "attrs":{...}, "valuation":{...},
  "matrikel":{...}, "plan":[...], "area":{"id":"ZIP-2300","name":"Amager"},
  "quality_flags":{"areal":"BBR_UNVERIFIED"} }
```

**S2-regler i kode:** `POST /analyses` må ikke levere, før `area_profile.review_state='APPROVED'`. Claims uden kilde/dato afvises ved insert. Ingen LLM-kald med zone B-data.

---

# DEL B — Relay- og reveal-protokol

## B1. Sekvens (happy path)

```
Køber            Relay            Ejer            Disclosure      Partner
  │  msg (tekst)   │                │                 │             │
  ├───────────────>│ redaction      │                 │             │
  │                ├───────────────>│ (pseudonym K-7F3A)            │
  │                │<───────────────┤ svar            │             │
  │<───────────────┤                │                 │             │
  │  "enig 4,1 mio"│                │  "enig"         │             │
  ├───────────────>│<───────────────┤                 │             │
  │                │ deal.PRICE_AGREED                │             │
  │                ├─────────────────────────────────>│             │
  │                │        PACKAGE_OFFERED (10.000)  │             │
  │  accept+betal  │                │  accept+betal   │             │
  ├───────────────>│<───────────────┤                 │             │
  │                │ PACKAGE_ACCEPTED                 │             │
  │  samtykke+step-up               │  samtykke+step-up             │
  ├───────────────>│<───────────────┤                 │             │
  │                │ REVEAL REQUEST ─────────────────>│ guards ✓    │
  │<───────────────┼──────────────────────────────────┤ identiteter │
  │                │                │<────────────────┤             │
  │                │ FULFILLMENT_CASE ────────────────┼────────────>│
```

## B2. Guards (alle skal være sande i én transaktion)

```python
def reveal(thread_id, actor):
    d = deal(thread_id)
    require(d.state == 'PACKAGE_ACCEPTED')
    require(payment_status(d.package_id) == 'CAPTURED')
    require(consent(thread_id, 'BUYER') and consent(thread_id, 'OWNER'))
    require(auth_context().assurance == 'HIGH' and auth_context().step_up)
    require(verification_valid(d.order_id))          # ikke udløbet
    require(ownership_valid(thread.owner_id, thread.address_id))
    with audit(zone='B', action='IDENTITY_REVEALED'):
        grant = RevealGrant.create(...)              # irreversibel
        return vault.disclose(grant)                 # eneste indgang til vault
```

**Ingen anden kodevej må læse vault.** Håndhæves med DB-rolle: kun `disclosure_service` har SELECT på `identity_contact`.

## B3. Redaction-pipeline (deterministisk først)

| Lag | Regel | Handling |
|---|---|---|
| 1 | Regex: telefon (DK +45/8 cifre), e-mail, URL, CPR-mønster, kontonr. | Maskér + flag |
| 2 | NER (dansk model): personnavne, adresser, virksomheder | Maskér + flag |
| 3 | Billeder: EXIF/GPS strip, OCR-scan for kontaktinfo | Strip / afvis |
| 4 | Vedhæftninger: kun PDF/JPG/PNG, scan for kontaktinfo | Afvis ved træff |
| 5 | Adfærd: "ring til", tal skrevet med ord, gentagne forsøg | Rate limit → karantæne |
| 6 | LLM-klassifikator (supplement, EU-only) | Eskalér til review |

**Svar til afsender ved træff:** *"Beskeden indeholder kontaktinformation og blev ikke sendt. Kontakt udveksles automatisk, når I er enige og har accepteret pakken."*

## B4. Fejltilfælde (skal testes)

| Tilfælde | Forventet |
|---|---|
| Kun én part har givet samtykke | 409 `REVEAL_BLOCKED_MISSING_CONSENT` |
| Attest udløbet mellem enighed og reveal | 409 `VERIFICATION_EXPIRED` → deal tilbage til DIALOG |
| Betaling gennemført, men step-up mangler | 403 `STEP_UP_REQUIRED`, ingen vault-adgang |
| Ejer afmelder midt i dialog | Thread → `ABORTED`, køber informeres anonymt |
| Besked med telefon i billede-EXIF | Strip + OCR-træff → afvis, `message.redacted` |
| Reveal kaldt to gange | Idempotent: returnér eksisterende grant, ny audit-entry |
| Mægler forsøger reveal på egen lead | 403 — mægler er aldrig part i deal |

---

# DEL C — Skærm-for-skærm (køber og ejer)

## C1. Køberflow

**K1 · Landing** — *"Hvor vil du bo?"*
Søgefelt (område/postnummer) + 3 populære områderapporter. Ingen login, ingen cookie-wall ud over nødvendig. CTA: *"Se områdeprofil"*.

**K2 · Områderapport** (anonym, cached)
Fire faner: **Fakta** (boligmasse, ejerformer, priser) · **Bevægelse** (vedtaget/på vej/stoppet, kilde+dato synlig) · **Hverdag** (skoler, indkøb, transport) · **Efterspørgsel** (*"47 verificerede købere følger dette område"* — aggregeret, k≥5).
Sticky CTA: *"Følg området – få besked når noget matcher"*.

**K3 · Adresseopslag** (anonym)
BBR/VUR/matrikel/plan i ét kort. Kvalitetsflag hvor data er usikkert. CTA: *"Jeg er interesseret i denne bolig"*.

**K4 · Ordre, trin 1** (e-mail)
4 felter: boligtype, areal/værelser, budget, horisont. Magic link. Kvittering: *"Din ordre er registreret. Den er endnu ikke verificeret."*

**K5 · Opgradering** (MitID)
Forklaring: *"Verificerede købere bliver vist til ejere. Uverificerede gør ikke."* → MitID → 4 spørgsmål uddybet → status QUALIFIED.

**K6 · Bankbevis** (MitID)
Upload PDF eller "anmod min bank" (V2/V3). Viser krav: bank, dato, beløb, gyldighed. Status: *"Til gennemgang – typisk 1 hverdag"*.

**K7 · Min ordre** (MitID)
Status-badge VERIFIED + **udløbsdato** + antal match + "Opdater bevis" når <30 dage tilbage. Handlinger: pause,撤回, slet.

**K8 · Anonym dialog** (MitID)
Tråd med `E-2B91`. Banner: *"Begge parter er anonyme. Kontakt udveksles ved enighed."* Beskedfelt med inline-advarsel ved kontaktinfo. Knap: *"Vi er enige om pris"*.

**K9 · Enighed → pakke**
Opsummering (pris, vilkår, dato) → pakkeindhold og fast pris 10.000 → betaling → samtykke til afsløring → MitID step-up → **identitet udvekslet**. Derefter: partnerens sagsstatus.

## C2. Ejerflow

**E1 · Notifikation** (mail/brev, saglig)
*"Der er registreret verificeret købsinteresse på [adresse]. Du kan se den anonymt på Optata. Afmeld her."* Ingen køberdata i mailen.

**E2 · Verifikation** (MitID + EJF-match)
*"Bekræft at du ejer denne adresse."* MitID → match mod ejerfortegnelse. Fallback: selskab (MitID Erhverv) eller manuel dokumentation. **Ingen visning før match.**

**E3 · Anonymt bevis**
```
Køber K-7F3A · VERIFIED
Bankgodkendt op til 4.200.000 kr. (gyldig til 12.06.2026)
Horisont: 3–6 måneder · Villa, 140–180 m², 4+ værelser
[ Åbn anonym dialog ]  [ Afvis ]  [ Afmeld fremtidige ]
```

**E4 · Ejerside (1.495 kr., 12 uger)**
Dashboard: antal verificerede, budgetintervaller (aggregeret), horisont-fordeling, udvikling over tid. Alt anonymt. Nedtælling til udløb + forny.

**E5 · Dialog → enighed → pakke**
Identisk med K8/K9 — symmetrisk oplevelse, symmetrisk samtykke.

## C3. Fælles designregler

1. **Anonymt som default** — ingen skærm viser navn/kontakt før reveal.
2. **Attest, ikke dokument** — vis beløb+udsteder+gyldighed, aldrig PDF'en.
3. **Kilde og dato på enhver påstand** i rapporter.
4. **Udløb er synligt** for både køber (min ordre) og ejer (beviset).
5. **Afmeld er altid ét klik** og virker på adressen, ikke kun tråden.
6. **Ingen dark patterns** — afvis/withdraw er lige så synlige som accept.

---

## Prioriteret byggeorden

| Sprint | Leverance | Guard der skal testes |
|---|---|---|
| S1 | K1–K4 + registry + rapport | Anonym må aldrig se zone B |
| S2 | Agent + review + faktura | Ingen publicering uden APPROVED |
| S3 | K5–K7 + MitID + attest + udløb | Auto-nedgradering ved expires_at |
| S4 | E1–E4 + ejerskabsmatch | Ingen visning uden ownership_verified |
| S5 | K8/K9 + relay + reveal | Alle 6 guards i én transaktion |

*Vil du have, at jeg næste gang skriver (a) de konkrete test-fixtures og acceptkriterier pr. sprint, (b) ingestion-adapterne for BBR/DAR/EJF med feltmapping og valideringsregler, eller (c) agentens claim-schema og prompt-kontrakt med afvisningsregler?*