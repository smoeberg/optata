# OPTATA — Systemarkitektur bygget på cases og brugerflows

Vi lukker forretningen. Arkitekturen udledes nu **indefra**: fra konkrete brugeroplevelser → flows → tilstande → events → services → data. Ikke omvendt. Det er den eneste måde at undgå at bygge en platform, ingen kan bruge.

---

## 0. Metoden

```
Case (hvem, hvad, hvorfor)
  → Flow (skærm for skærm)
    → Tilstandsmaskine (hvad må ske hvornår)
      → Events (det, der gemmes og måles)
        → Services (det, der bygges)
          → Data (det, der skal findes)
```

**Regel:** intet bygges, som ikke kan spores til en case. Og hver case skal ende i et **målbart event** — ellers kan forretningen ikke styres.

---

## 1. Case-katalog (de ni cases, arkitekturen dækker)

| # | Case | Persona | Kerneflow | Forretningsbevis |
|---|---|---|---|---|
| **C1** | "Jeg vil bo i dette område" | Køber | Anonym → rapport → ordre | A1 |
| **C2** | "Jeg vil bo på denne adresse" | Køber | Adresseopslag → ordre → verifikation | A1, tæthed |
| **C3** | "Der er en køber til mit hus" | Ejer | Notifikation → anonymt bevis → dialog | A2 |
| **C4** | "Hvad er min bolig værd for andre?" | Ejer | Adresserapport → ejerside → interesse | A2, omsætning |
| **C5** | "Vi er enige — gør handlen færdig" | Køber+Ejer | Dialog → enighed → pakke → afsløring | Pakke-uptake |
| **C6** | "Giv mig købere i mit postnummer" | Mægler | Erhverv-login → anonyme leads → dialog | A4, recurring |
| **C7** | "Skal vi bygge 40 eller 80 boliger her?" | Developer | Bestil → agent-profil → leverance | A4, første krone |
| **C8** | "Bevis min købeevne" | Køber+Bank | Upload attest → review → VERIFIED | A3 |
| **C9** | "Jeg vil ikke mere" / "Bevis udløbet" | Alle | Withdraw / expire / afmeld / slet | Integritet, GDPR |

C9 er ikke en undtagelse — det er en **førsteklasses case**. Uden den bliver ordrebogen beskidt og GDPR ulovlig.

---

## 2. Cases som flows (skærm → tilstand → event)

### C1 — Køber, område (toppen af tragten)

| Trin | Skærm/oplevelse | Krav | Event |
|---|---|---|---|
| 1 | Landing: "Hvor vil du bo?" | **Ingen login** | `area.viewed` |
| 2 | Områderapport: boligmasse, priser, bevægelse, hverdag | Anonym, cached | `report.viewed` |
| 3 | "Følg dette område" → e-mail + magic link | Lav friktion | `order.created (CURIOS, scope=AREA)` |
| 4 | Kvittering + "Gør din ordre stærkere" | Opgraderings-CTA | `order.upgrade_prompted` |

**Arkitekturkrav:** rapporten skal være **statisk genereret + cached** (zone A). Ingen persondata i dette flow. Det er distributionsmotoren — den må aldrig kræve MitID.

### C2 — Køber, adresse (wedge)

| Trin | Oplevelse | Krav | Event |
|---|---|---|---|
| 1 | Adresseopslag: BBR, VUR, matrikel, plan, område | Zone A, ét opslag | `property.viewed` |
| 2 | "Jeg er interesseret i denne bolig" | E-mail-ordre | `order.created (scope=ADDRESS)` |
| 3 | 4 spørgsmål: budget, horisont, type, finansiering | MitID privat | `identity.verified`, `order.qualified` |
| 4 | Upload bankattest (C8) | Vault + review | `verification.submitted` |
| 5 | Status: **VERIFIED** + badge | Udløbsdato vist | `order.verified` |

**Arkitekturkrav:** ordre kan oprettes som CURIOS med e-mail og **opgraderes in-place** til MitID-identitet (`identity.linked`). Ellers får I dubletter og kan ikke måle funnel.

### C3 — Ejer, notificeret (A2-motoren)

| Trin | Oplevelse | Krav | Event |
|---|---|---|---|
| 1 | Saglig, afgrænset notifikation: "Der er registreret verificeret interesse på din adresse" | Juridisk grundlag + afmelding | `owner.notified` |
| 2 | Klik → **MitID + ejerskabsverifikation (EJF-match)** | Step-up | `owner.ownership_verified` |
| 3 | Anonymt bevis: pseudonym, bankgodkendt interval, horisont, type | **Ingen identitet** | `interest.viewed` |
| 4 | Valg: `[Åbn anonym dialog] [Afvis] [Afmeld]` | Samtykke registreres | `dialog.opened` / `interest.declined` / `owner.unsubscribed` |

**Arkitekturkrav (kritisk):** ejerskabsverifikation **før** visning. Uden den kan enhver se efterspørgslen på andres adresser — det er både et GDPR-brud og et troværdighedsbrud. Ejerskab matches mod EJF via MitID-identitet, med manuel fallback for selskabs-/andelsforhold.

### C4 — Ejer, inbound (ejersiden, 1.495 kr.)

| Trin | Oplevelse | Event |
|---|---|---|
| 1 | Adresserapport (gratis, zone A) | `report.viewed` |
| 2 | "Se dokumenteret interesse på din adresse" → MitID + ejerskab | `owner.ownership_verified` |
| 3 | Betaling 1.495 → 12 ugers adgang | `subscription.started (OWNER_PASS)` |
| 4 | Dashboard: antal verificerede, budgetintervaller, horisont — **anonymt** | `owner_dashboard.viewed` |
| 5 | Udløb efter 12 uger → forny eller stop | `subscription.expired` |

**Arkitekturkrav:** adgang er **tidsbegrænset og adresse-scopet**. Rettigheden ligger i `consent`/`billing`, håndhæves i query-laget (RLS), ikke i UI.

### C5 — Enighed → pakke → afsløring (kernen i transaktionen)

```
DIALOG_OPEN ──(relay, anonym)──> PRICE_AGREED
                                    │  begge markerer enighed
                                    ▼
                            PACKAGE_OFFERED (10.000 fast)
                                    │  accept + betaling
                                    ▼
                            PACKAGE_ACCEPTED
                                    │  gensidigt samtykke + MitID step-up
                                    ▼
                          IDENTITY_REVEALED (audit, irreversibel)
                                    │  advokatpartner aktiveres
                                    ▼
                            FULFILLMENT_IN_PROGRESS
                                    │  dokumenter, tinglysning, refusion
                                    ▼
                                COMPLETED
```

| Trin | Oplevelse | Event |
|---|---|---|
| 1 | Anonym chat, pseudonymer, redaction aktiv | `message.sent`, `message.redacted` |
| 2 | "Er I enige om pris og vilkår?" — begge klikker | `deal.price_agreed` |
| 3 | Pakke tilbydes med indhold og fast pris | `package.offered` |
| 4 | Accept + betaling | `package.accepted`, `payment.captured` |
| 5 | Samtykke til afsløring (begge) + step-up | `reveal.consent_given` ×2 |
| 6 | Identiteter udveksles, audit-ref | `identity.revealed` |
| 7 | Partner-sag oprettes, dokumenter flyder | `fulfillment.case_created` |

**Arkitekturkrav:** afsløring er en **service med én indgang og hårde guards** — ikke en knap i frontend. Guards: `PACKAGE_ACCEPTED` ∧ begge samtykker ∧ step-up ∧ gyldig verifikation. Alle fire skal være sande i samme transaktion.

### C6 — Mægler (recurring-motoren)

| Trin | Oplevelse | Krav | Event |
|---|---|---|---|
| 1 | MitID Erhverv → CVR + rolle | Erhvervsidentitet | `org.authenticated` |
| 2 | Abonnement på postnummer (eksklusivt) | Eksklusivitets-check | `subscription.started (AGENT_ZIP)` |
| 3 | Lead-liste: **anonyme** verificerede købere, budgetinterval, horisont, type | Ingen identitet, ingen eksport | `lead_list.viewed` |
| 4 | "Åbn dialog" → relay (samme som C5) | Samtykke fra køber | `dialog.opened` |
| 5 | Tæthed og historik i postnummeret | Zone C-aggregater | `area_insights.viewed` |

**Arkitekturkrav:** mægleren ser **kun** ordrer i sit postnummer, og **kun** pseudonym + attester. Ingen CSV-eksport af leads. Eksklusivitet håndhæves i DB (unique constraint på postnummer + aktiv periode), ikke i forretningslogik alene.

### C7 — Developer (første krone)

| Trin | Oplevelse | Event |
|---|---|---|
| 1 | Bestil områdeanalyse (85.000) | `analysis.ordered` |
| 2 | Agent genererer profil: fakta / bevægelse / hverdag / efterspørgsel | `claims.extracted`, `profile.generated` |
| 3 | **Menneskelig review-kø** — hver påstand har kilde + dato | `profile.reviewed` |
| 4 | Leverance (PDF/web) + faktura | `analysis.delivered`, `invoice.issued` |

**Arkitekturkrav:** ingen publicering uden review-flag. Claims uden `source_id`+dato afvises i kode. `model_version` gemmes → reproducerbarhed.

### C8 — Bankattest (kvalitetsmotoren)

```
CURIOS ──4 spørgsmål + MitID──> QUALIFIED ──attest──> [REVIEW] ──> VERIFIED
                                                          │            │
                                                          │      expires_at
                                                          ▼            ▼
                                                       REJECTED    QUALIFIED (auto)
```

| Metode | Flow | Arkitektur |
|---|---|---|
| V1 dokument | Upload PDF → hash → manuel review → attest | Vault (krypteret, kort retention), attest-felter eksponeres |
| V2 attest | Bank-reference valideres | Adapter pr. bank |
| V3 partner | Bank pusher med samtykke | Webhook + idempotens |

**Arkitekturkrav:** `expires_at` + natlig job der nedgraderer. Attesten (beløb, udsteder, dato, gyldighed) er det, front-end må vise — **aldrig dokumentet**.

### C9 — Withdraw / expire / afmeld / slet

| Trigger | Handling | Event |
|---|---|---|
| Køber trækker ordre | Status `WITHDRAWN`, bliver i historik | `order.withdrawn` |
| Attest udløber | VERIFIED → QUALIFIED, fjernes fra mægler-liste | `verification.expired` |
| Ejer afmelder | Stop al notifikation på adressen | `owner.unsubscribed` |
| Sletteanmodning | Identitet+bevis slettes; **pseudonym event-historik bevares** | `identity.erased` |
| Ordre inaktiv 90 dage | Auto-expire | `order.expired` |

**Arkitekturkrav:** to-lags sletning. Zone B (identitet, bevis) slettes hårdt. Event-log (pseudonym, aggregeret) bevares → ordrebogens historik og integritet overlever.

---

## 3. Konsoliderede tilstandsmaskiner

```
ORDER:    CURIOS → QUALIFIED → VERIFIED → MATCHED → IN_DIALOG → AGREED → FULFILLED
              └──────────────┴──────────┴─────────→ WITHDRAWN | EXPIRED

DEAL:     DIALOG_OPEN → PRICE_AGREED → PACKAGE_OFFERED → PACKAGE_ACCEPTED
              → IDENTITY_REVEALED → FULFILLMENT → COMPLETED | ABORTED

IDENTITY: EMAIL → MITID_PRIVATE → (MITID_ERHVERV for org)
          + ownership_verified (ejer, pr. adresse)

ACCESS:   ANONYMOUS → EMAIL_SESSION → AUTHENTICATED → STEP_UP
```

**Hårde guards (i domænekoden, ikke UI):**
1. `NOTIFIED` kræver `VERIFIED` ∧ gyldig attest.
2. `interest.viewed` kræver `ownership_verified` på adressen.
3. `IDENTITY_REVEALED` kræver pakke accepteret ∧ 2 samtykker ∧ step-up.
4. Mægler-query kræver aktivt abonnement ∧ postnummer-scope.
5. Zone C-eksport kræver k-anonymitet ≥ 5.

---

## 4. Event-katalog (det, forretningen måles på)

| Domæne | Events |
|---|---|
| Funnel | `area.viewed`, `report.viewed`, `order.created`, `order.qualified`, `order.verified` |
| Ejer | `owner.notified`, `owner.ownership_verified`, `interest.viewed`, `dialog.opened`, `interest.declined` |
| Deal | `deal.price_agreed`, `package.offered/accepted`, `identity.revealed`, `fulfillment.completed` |
| Integritet | `order.withdrawn/expired`, `verification.expired/rejected`, `identity.erased` |
| B2B | `subscription.started/expired`, `lead_list.viewed`, `analysis.ordered/delivered` |
| Sikkerhed | `message.redacted`, `reveal.consent_given`, `auth.step_up`, `vault.accessed` |

**Alle KPI'er er afledt heraf:** tæthed = aktive VERIFIED pr. område / boliger; ejerrespons = `dialog.opened` / `owner.notified`; pakke-uptake = `package.accepted` / `deal.price_agreed`; leakage = `message.redacted` / `message.sent`.

---

## 5. Services udledt af cases

| Modul | Cases | Ansvar |
|---|---|---|
| `registry` | C1,C2,C4,C7 | Kilde-adapters, bitemporal store, BFE/adresse-id, PostGIS |
| `reports` | C1,C4,C7 | Cachede zone A-profiler, PDF/web |
| `agent` | C7 | Claim-ekstraktion, proveniens, review-kø |
| `orderbook` | C1,C2,C9 | Ordrer, events, dedup, integritet |
| `identity` | C2,C3,C6,C8 | MitID/OIDC, pseudonym, vault, step-up, ejerskabsmatch |
| `verification` | C8,C9 | Attest, review, udløb, nedgradering |
| `disclosure` | C3,C4,C6 | PublicProfile, attester, reveal-protokol |
| `relay` | C3,C5,C6 | Tråde, beskeder, redaction, rate limit |
| `consent` | C3,C5,C9 | Grants, afmelding, retention, audit |
| `billing` | C4,C5,C6,C7 | Abonnement, eksklusivitet, engangsgebyr |
| `insights` | C6,C7 | Zone C-aggregater, k-anonymitet |

**Arkitekturstil:** modulær monolit + workers (ingestion, agent, matching, expiry). Ingen microservices i år 1.

---

## 6. Minimal datamodel udledt af flows

```
Property(bfe, address_id[], matrikel, geom, area_id, attrs, valid/transaction_time)
Area(area_id, type, geom, bolig_count)

Identity(identity_id, provider, pseudonym, assurance, cvr?, created_at)
IdentityLink(from, to, reason, at)
OwnershipVerification(identity_id, address_id/bfe, method, verified_at, expires_at)

Order(order_id, buyer_pseudonym, area_id, scope, criteria, level, status, timestamps)
OrderEvent(order_id, type, payload, actor, occurred_at)      -- append-only
Verification(order_id, method, issuer, amount, issued_at, expires_at, evidence_hash, status)

Thread(thread_id, order_id, address_id, state, buyer_pseudo, owner_pseudo)
Message(thread_id, sender_pseudo, body_redacted, flags[], created_at)
Deal(thread_id, state, agreed_price?, package_id)
RevealGrant(thread_id, buyer_consent, owner_consent, stepup_ref, revealed_at, audit_ref)

Subscription(org_id/identity_id, product, scope_id, period, exclusive, status)
Consent(subject, purpose, scope, granted_at, revoked_at)
AuditLog(actor, action, target, zone, occurred_at)
```

**Zoner:** `Property/Area/reports/claims` = A (dev-tilgængelig). `Identity/Verification/Thread/Message/RevealGrant` = B (kun prod, RLS, audit). `insights` = C (k-anonymitet).

---

## 7. Skærm-inventar (frontend, anonymt som default)

| Skærm | Auth | Zone |
|---|---|---|
| Landing / områdesøgning | Ingen | A |
| Områderapport | Ingen | A |
| Adresseopslag / adresserapport | Ingen | A |
| Ordre-formular (4 spørgsmål) | E-mail → MitID | A+B |
| Min ordre / status | MitID | B |
| Attest-upload | MitID | B |
| Ejer-notifikation (landing) | MitID + ejerskab | B |
| Ejer-dashboard (12 uger) | MitID + ejerskab + betaling | B |
| Anonym dialog (relay) | MitID | B |
| Enighed → pakke → afsløring | MitID step-up | B |
| Mægler lead-liste | MitID Erhverv + abonnement | B (pseudonym) |
| Developer bestilling / profil | Erhverv | A+C |

**Regel:** ingen skærm må kunne joine til vault. Front-end læser `PublicProfile` + zone A/C.

---

## 8. Walking skeleton — byg i case-rækkefølge

| Iteration | Cases | Leverance | Færdigt når |
|---|---|---|---|
| **S1** | C1 | Registry + rapport + landing + e-mail-ordre | Anonym kan følge område, ordre gemmes |
| **S2** | C7 | Agent + review + faktura | Første analyse kan leveres og betales |
| **S3** | C2,C8 | MitID + verifikation + udløb | Ordre kan blive VERIFIED med attest |
| **S4** | C3,C4 | Ejerskabsmatch + notifikation + ejerside | Ejer ser anonymt bevis, betaler 1.495 |
| **S5** | C5 | Relay + redaction + deal + reveal | Anonym dialog → enighed → afsløring, audit |
| **S6** | C6 | Erhverv + eksklusivitet + lead-liste | Mægler ser anonyme leads i eget postnummer |
| **S7** | C9 | Withdraw/expire/afmeld/slet | Ordrebogen kan renses, GDPR-flow virker |

**Bemærk:** C9 bygges sidst som *feature*, men **designes først** (dedup, pseudonym, retention). Ellers kan historikken ikke renses bagefter.

---

## 9. Test-cases som fixtures (det, AI-kodegenerering ikke må røre)

| Fixture | Hvorfor |
|---|---|
| Andelsbolig: BFE med 40 adresse-id'er | 1:mange må ikke bryde |
| Samboende medkøbere, samme DAR-adresse | Husstands-dedup |
| Selskabsejet ejendom (CVR) | Ejerskabsmatch via Erhverv |
| Attest udløbet i går | Auto-nedgradering, fjernes fra mægler-liste |
| Besked med telefonnummer i billede-EXIF | Redaction + strip |
| Reveal-forsøg uden den ene parts samtykke | Guard skal afvise |
| Mægler-query på andet postnummer | RLS skal afvise |
| Sletteanmodning med aktiv ordre | Zone B slettes, event-historik bevares |
| Zone C-celle med 3 ordrer | k-anonymitet blokerer eksport |

Disse skrives af mennesker og testes mod rigtige sager. Resten kan genereres.

---

## Konklusion

Arkitekturen er nu udledt af **ni cases**, ikke af en produktliste. Det giver tre ting:

1. **Hver service har en bruger** — intet bygges uden flow.
2. **Hver guard har en case** — anonymitet, ejerskab, afsløring og eksklusivitet er testbare.
3. **Hver KPI har et event** — tæthed, ejerrespons og pakke-uptake måles direkte fra kernen.

Den kritiske rækkefølge er **S1 → S2 → S3 → S4 → S5**: distribution → indtægt → kvalitet → ejerside → transaktion. Det matcher forretningen præcist.

*Vil du have, at jeg nu går ned i (a) S1+S2 som konkret API- og databasespec (endpoints, tabeller, indices), (b) relay- og reveal-protokollen som sekvensdiagram med guards og fejltilfælde, eller (c) skærm-for-skærm wireframe-beskrivelser af køber- og ejerflowet?*