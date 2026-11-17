# OPTATA — (a) Repo & CI-gates · (b) OpenAPI-kontrakt · (c) Drift & observability

Tre dele. De er skrevet som **repo-indhold**, ikke beskrivelser: filstruktur, gates, kontrakt og driftsregler kan lægges direkte ind.

---

# DEL A — Repo-struktur og CI-gates

## A1. Monorepo (modulær monolit + workers)

```
optata/
├─ apps/
│  ├─ api/                    # FastAPI — tynd transport, ingen forretningslogik
│  └─ web/                    # Next.js — anonym som default
├─ core/                      # domænet — det eneste sted med regler
│  ├─ registry/               # bitemporal ejendomsmodel
│  ├─ orderbook/              # ordrer, events, dedup, integritet
│  ├─ identity/               # MitID/OIDC, pseudonym, vault, step-up
│  ├─ verification/           # attest, review, udløb
│  ├─ disclosure/             # PublicProfile, attester, REVEAL (eneste vault-indgang)
│  ├─ relay/                  # tråde, redaction, rate limit
│  ├─ consent/                # grants, afmelding, retention, audit
│  ├─ agent/                  # claim-ekstraktion, proveniens, review-kø
│  ├─ insights/               # zone C, k-anonymitet
│  └─ billing/                # abonnement, eksklusivitet, engangsgebyr
├─ workers/
│  ├─ ingestion/              # kilde-adapters + checkpoints
│  ├─ agent_runner/           # cachede profilkørsler
│  ├─ matching/               # score pr. område
│  └─ expiry/                 # attest/ordre/abonnement-udløb
├─ contracts/
│  ├─ openapi.yaml            # DEL B — single source of truth
│  ├─ events/*.json           # event-skemaer (append-only katalog)
│  └─ prompts/agent_v*.md     # prompt-kontrakter, versionerede
├─ tests/
│  ├─ fixtures/               # FX-01…FX-08, FX-A1…A6
│  ├─ guards/                 # MÅ IKKE AI-genereres
│  ├─ contract/               # API + events
│  └─ e2e/                    # case-flows C1…C9
├─ migrations/                # Alembic, fremad-only
├─ infra/                     # Terraform, EU-only
├─ docs/adr/                  # arkitekturbeslutninger (bus-factor)
└─ .github/CODEOWNERS
```

**Modulregel:** `core/*` må ikke importere fra `apps/*`. Moduler kommunikerer via **domæne-events** eller eksplicitte service-interfaces — aldrig direkte på tværs af tabeller.

## A2. Hvad AI må generere — og hvad mennesker skriver

| Område | AI-generering | Menneske (DK review) |
|---|---|---|
| UI-komponenter, layouts, kort | ✅ Fri | Let review |
| CRUD, DTO'er, API-klienter | ✅ Fri | Kontrakttest skal være grøn |
| Ingestion-adapters, feltmapping | ✅ Assist | Valideringsregler + BFE 1:mange |
| Tests (unit, contract) | ✅ Assist | Guards skrives først af menneske |
| Migrations | ⚠️ Assist | Altid review + rollback-plan |
| **Redaction-regler** | ❌ | Deterministisk lag skrives i hånden |
| **Reveal-guards + vault-adgang** | ❌ | Menneske, par-review |
| **Refusion, tinglysning, fortrydelse** | ❌ | Menneske + test mod rigtige sager |
| **RLS-policies, zone-adskillelse** | ❌ | Menneske + security-review |
| **Samtykke/retention/sletning** | ❌ | Menneske + jurist-godkendelse |

**CODEOWNERS:**
```
/core/disclosure/    @dk-reviewer @security
/core/relay/redaction/ @dk-reviewer
/core/consent/       @dk-reviewer @legal
/core/verification/  @dk-reviewer
/migrations/         @dk-reviewer @data-lead
/infra/              @security
/contracts/          @dk-reviewer @data-lead
/tests/guards/       @dk-reviewer
```

## A3. CI-gates (rækkefølge = stop ved første fejl)

| # | Gate | Blokerer merge hvis |
|---|---|---|
| 1 | **Contract-first** | Kode afviger fra `openapi.yaml` eller event-skema |
| 2 | **Lint + typecheck** | Fejl |
| 3 | **Unit + contract tests** | Nogen rød |
| 4 | **Guard tests** (`tests/guards/`) | Nogen rød — *ingen undtagelser* |
| 5 | **Zone-lækage-test** | Zone B-felt optræder i anonym/B2B-payload |
| 6 | **k-anonymitet-test** | Zone C-celle med <5 returneres |
| 7 | **SAST + secrets scan** | High/critical fund |
| 8 | **Afhængigheds- + licensscan** | Copyleft/ukendt licens eller kendt CVE |
| 9 | **Migration-test** | Ikke-idempotent, destruktiv uden plan, eller bryder bitemporalitet |
| 10 | **Syntetisk-data-check** | Prod-lignende persondata fundet i dev-fixtures |
| 11 | **Menneskelig review** | Ændring i CODEOWNERS-sti uden DK-godkendelse |
| 12 | **E2E case-flow** | C1–C9 ikke grønne for berørte flows |

**Ekstra regel:** ændring i `contracts/prompts/` kræver ny `prompt_version` + genkørsel af agent-fixtures (FX-A1…A6).

## A4. Miljø- og datapolitik

| Miljø | Data | Adgang |
|---|---|---|
| local/dev | **Kun syntetisk** (generator i `tests/fixtures/gen/`) | UA-team |
| staging | Syntetisk + zone A (offentlige) | UA + DK |
| prod | Zone A/B/C, EU-only | DK-drift, auditeret break-glass |

**Ingen prod-dump til dev. Nogensinde.** Syntetisk generator skal kunne producere FX-01…FX-08 deterministisk (seed), så tests er reproducerbare.

---

# DEL B — OpenAPI 3.1 (uddrag, kontrakt-first)

```yaml
openapi: 3.1.0
info: { title: Optata Core API, version: 0.4.0 }
servers: [{ url: https://api.optata.dk/v1 }]

security: [{ anonymous: [] }]

components:
  securitySchemes:
    anonymous: { type: http, scheme: none }
    emailSession: { type: apiKey, in: header, name: X-Session }
    mitid: { type: openIdConnect, openIdConnectUrl: https://broker.optata.dk/.well-known/openid-configuration }
    mitidStepUp: { type: apiKey, in: header, name: X-Step-Up-Ref }
    orgAuth: { type: openIdConnect, openIdConnectUrl: https://broker.optata.dk/erhverv/.well-known/openid-configuration }

  parameters:
    Idempotency: { name: Idempotency-Key, in: header, schema: { type: string }, required: true }

  schemas:
    Error:
      type: object
      required: [code, message]
      properties:
        code: { type: string, enum: [
          ORDER_ALREADY_ACTIVE, OWNERSHIP_NOT_VERIFIED, VERIFICATION_EXPIRED,
          MISSING_CONSENT, STEP_UP_REQUIRED, REVEAL_BLOCKED, PROFILE_NOT_APPROVED,
          SUBSCRIPTION_EXPIRED, MESSAGE_REDACTED, K_ANONYMITY_BLOCKED, RATE_LIMITED ] }
        message: { type: string }
        trace_id: { type: string }

    PublicProfile:            # det eneste front-end må vise om en person
      type: object
      required: [pseudonym, level]
      properties:
        pseudonym: { type: string, example: K-7F3A }
        level: { type: string, enum: [CURIOS, QUALIFIED, VERIFIED] }
        badges:
          type: array
          items: { type: string, enum: [MITID_VERIFIED, BANK_APPROVED, HORIZON_3_6M] }
        budget_band: { type: string, example: "4.0-4.5M" }   # interval, aldrig præcist beløb
        verification_expires_at: { type: string, format: date }
      additionalProperties: false      # ← forhindrer zone B-lækage ved fejl

    Order:
      type: object
      properties:
        order_id: { type: string, format: uuid }
        scope: { type: string, enum: [AREA, ADDRESS] }
        area_id: { type: string }
        address_id: { type: [string, "null"] }
        criteria: { type: object }
        level: { type: string, enum: [CURIOS, QUALIFIED, VERIFIED] }
        status: { type: string, enum: [ACTIVE, PAUSED, MATCHED, IN_DIALOG, AGREED, WITHDRAWN, EXPIRED] }

paths:
  /areas/{id}/profile:
    get:
      security: [{ anonymous: [] }]
      responses: { "200": { description: Zone A profil }, "404": { description: Ukendt område } }

  /properties/{address_id}:
    get:
      security: [{ anonymous: [] }]
      responses: { "200": { description: BBR+VUR+matrikel+plan, zone A } }

  /orders:
    post:
      security: [{ emailSession: [] }]
      parameters: [{ $ref: '#/components/parameters/Idempotency' }]
      requestBody:
        content: { application/json: { schema: { $ref: '#/components/schemas/Order' } } }
      responses:
        "201": { description: Oprettet som CURIOS }
        "409": { content: { application/json: { schema: { $ref: '#/components/schemas/Error' } } } }

  /orders/{id}/qualify:
    post:
      security: [{ mitid: [] }]
      responses: { "200": { description: QUALIFIED }, "403": { description: MitID kræves } }

  /orders/{id}/verification:
    post:
      security: [{ mitid: [] }]
      requestBody:
        content: { multipart/form-data: { schema: { type: object, properties: { document: { type: string, format: binary } } } } }
      responses: { "202": { description: Til manuel review } }

  /owner/interest/{address_id}:
    get:
      security: [{ mitid: [] }]
      responses:
        "200":
          content: { application/json: { schema: { type: array, items: { $ref: '#/components/schemas/PublicProfile' } } } }
        "403": { description: OWNERSHIP_NOT_VERIFIED }

  /threads/{id}/messages:
    post:
      security: [{ mitid: [] }]
      responses:
        "201": { description: Leveret (redacted) }
        "422": { description: MESSAGE_REDACTED }
        "429": { description: RATE_LIMITED }

  /deals/{id}/agree:
    post: { security: [{ mitid: [] }], responses: { "200": { description: PRICE_AGREED når begge har markeret } } }

  /deals/{id}/package:
    post: { security: [{ mitid: [] }], responses: { "202": { description: PACKAGE_OFFERED/ACCEPTED } } }

  /deals/{id}/reveal:
    post:
      security: [{ mitid: [], mitidStepUp: [] }]
      parameters: [{ $ref: '#/components/parameters/Idempotency' }]
      responses:
        "200": { description: Identiteter udvekslet, audit-ref returneres }
        "403": { description: STEP_UP_REQUIRED }
        "409": { description: MISSING_CONSENT | VERIFICATION_EXPIRED | REVEAL_BLOCKED }

  /agent/leads:
    get:
      security: [{ orgAuth: [] }]
      description: Kun VERIFIED i eget postnummer. Ingen eksport. Ingen identitet.
      responses:
        "200":
          content: { application/json: { schema: { type: array, items: { $ref: '#/components/schemas/PublicProfile' } } } }

  /insights/areas/{id}/demand:
    get:
      security: [{ orgAuth: [] }]
      responses: { "200": { description: Zone C, k>=5 }, "403": { description: K_ANONYMITY_BLOCKED } }

  /internal/profiles/{id}/review:
    post: { security: [{ orgAuth: [] }], responses: { "200": { description: APPROVED/REJECTED } } }

  /webhooks/bank-attestation:
    post: { description: V3 bank-partner, idempotent, signaturverificeret, responses: { "202": { description: Modtaget } } }
```

**Kontraktregler:** `PublicProfile.additionalProperties: false` er en **security-kontrol**, ikke kosmetik. Alle skrivende kald kræver `Idempotency-Key`. Fejl returnerer altid `code` + `trace_id`.

---

# DEL C — Drift, observability og runbooks

## C1. SLO'er

| Service | SLO | Måling |
|---|---|---|
| Anonym rapport/adresseopslag | 99,5 % / p95 < 400 ms | Cached zone A |
| Ordre-oprettelse | 99,5 % / p95 < 800 ms | Inkl. dedup-check |
| Relay-levering | 99,9 % / p95 < 1,5 s | Redaction inkl. |
| Reveal | 99,9 % korrekt guard-afvisning | **Fejl her er en hændelse, ikke en bug** |
| Ingestion | Daglig kørsel fuldført < 06:00 | Pr. kilde |
| Expiry-job | Fuldført dagligt < 03:00 | Ingen udløbne VERIFIED i lead-lister |

## C2. Metrics (det, forretningen og sikkerheden styres på)

**Datakvalitet**
```
registry_coverage_ratio{source,area}
registry_quarantine_rate{source}
registry_field_flagged_ratio{source,field}
dwelling_count_delta{area}          # alarm ved >2% hop
```

**Ordrebog & funnel**
```
orders_active{area,level}
density_verified_per_1000{area}     # = KPI P2
order_level_conversion{from,to}
verification_pending_age_hours
verification_expired_total
```

**Ejer & deal**
```
owner_notified_total / owner_dialog_opened_total   # = ejerrespons A2
deal_price_agreed_total / package_accepted_total   # = pakke-uptake
reveal_guard_denied_total{reason}
```

**Sikkerhed**
```
message_redacted_total{rule}        # leakage-indikator
redaction_repeat_offender_total
vault_access_total{service}         # skal KUN være disclosure
zone_b_field_in_public_payload_total  # skal være 0 → alarm ved >0
k_anonymity_blocked_total
```

## C3. Logging & audit

| Type | Indhold | Opbevaring |
|---|---|---|
| App-log | trace_id, ingen persondata, ingen CPR | 30 dage |
| **Audit (zone B)** | actor, action, target, zone, samtykke-ref, step-up-ref | 5 år, append-only, uforanderlig |
| Vault-adgang | hvem, hvorfor, grant-id | 5 år |
| Redaction-hændelser | regel, hash af besked (ikke indhold) | 90 dage |

**Alarm-regler:** `vault_access_total{service!="disclosure"} > 0` → **P1**. `zone_b_field_in_public_payload_total > 0` → **P1 + auto-rollback**.

## C4. Jobs og runbooks

| Job | Frekvens | Runbook ved fejl |
|---|---|---|
| Ingestion (DAR/EBR/EJF/BBR) | Dagligt 02:00 | Kør fra checkpoint; quarantine-rapport til data-lead; **stop tætheds-KPI hvis dwelling_count ændres >2 %** |
| Expiry (attest/ordre/abonnement) | Dagligt 03:00 | Hvis fejlet: **frys mægler-lead-lister** indtil kørt — sælg ikke stale leads |
| Matching | Natligt + event | Genkør pr. område; ingen realtime-krav |
| Agent-profil | Ved change-event | Kun nye dokumenter; review-kø må ikke tømmes automatisk |
| Retention/sletning | Dagligt 04:00 | Zone B slettes hårdt; event-historik bevares pseudonymt |
| Backup + restore-test | Dagligt / månedligt restore | Restore-test er en gate, ikke en øvelse |

**Incident-prioriteter**
- **P1:** vault-adgang uden for disclosure · zone B-lækage · reveal gennemført uden guards · prod-data i dev.
- **P2:** expiry fejlet · ingestion fejlet >24 t · redaction bypass rapporteret.
- **P3:** latency, cache-miss, enkelt quarantine-bunke.

## C5. Adgang og drift (UA + DK)

| Rolle | Prod-adgang |
|---|---|
| UA-udvikler | Ingen direkte. Deploy via CI. Logs uden persondata. |
| DK-drift | Break-glass med godkendelse + audit, tidsbegrænset |
| DK-reviewer | Kode + guards + migrations |
| Support (UA) | Kun pseudonymiserede sager via admin-UI, ingen vault |

**Bus-factor:** hver kritisk komponent har ≥2 ejere, runbook i repo, ADR for hver større beslutning. Backup-udvikler (evt. EU-baseret) med adgang til repo + infra fra dag 1.

## C6. Omkostningskontrol

```
llm_tokens_total{purpose}     # agent, redaction-supplement
llm_cost_estimate_dkk_daily
profile_cache_hit_ratio       # mål >85%
tile_cache_hit_ratio
```
Alarm hvis LLM-forbrug >2× budget eller cache-hit <70 % — det er de to poster, der kan løbe løbsk.

---

## Hvad de tre dele giver tilsammen

- **(a)** gør AI-kodegenerering *sikker*: kontrakten og guards er menneskeskrevne, koden er output, CI er dommeren.
- **(b)** gør anonymitet til en **kontrakt** (`additionalProperties: false`), ikke en hensigt — og gør reveal idempotent og guard-styret.
- **(c)** gør drift til en del af produktet: datakvalitet, udløb og vault-adgang er målbare, alarmerede og salgbare over for en bank.

*Næste skridt kan være (a) event-skema-kataloget (`contracts/events/*.json`) med versioneringsregler, (b) den syntetiske datagenerator så UA-teamet kan arbejde uden persondata fra dag 1, eller (c) admin-/review-UI'et til agent-claims og bankattester — den flaskehals I får først.*