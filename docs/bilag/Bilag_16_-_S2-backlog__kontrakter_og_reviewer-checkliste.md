# OPTATA — (a) S2-backlog · (b) Kontraktfiler i fuld tekst · (c) DK-reviewerens checkliste

---

# DEL A — Sprint S2: Agent, review, leverance og faktura

**Omfang:** 22 persondage · uge 6–10 · **Afhængigheder:** S1 grøn (registry + zone A) · medielicens aktiv · jurist har godkendt kildebrug
**Mål:** Første områdeanalyse kan genereres, reviewes, leveres og faktureres. **Den første krone.**

## A1. Issues

| ID | Issue | Est. | Ejer | Afhænger af |
|---|---|---|---|---|
| S2-01 | `source_document`-register + licensfelt + dedup på URL/hash | 1,5 | DE | S1 |
| S2-02 | `claim`-tabel + DB-constraints (kilde, dato, status-enum) | 1,5 | DE+DK | 01 |
| S2-03 | Agent-runner: EU-LLM, struktureret output, cache pr. område | 3,0 | DE | 02 |
| S2-04 | **Deterministisk validator** (afvisningsregler, quote-match) | 2,0 | **DK** | 02 |
| S2-05 | Dedup/merge af claims på tværs af kilder | 1,0 | DE | 04 |
| S2-06 | Review-UI: kilde ↔ claim, citat-highlight, genveje | 3,0 | FS | 04 |
| S2-07 | **Publish-gate** + profilversionering + `reviewed_by` | 1,5 | **DK** | 06 |
| S2-08 | Leverance-render: PDF + web, vandmærke, claims.json, metode.md | 2,5 | FS | 07 |
| S2-09 | Analyse-ordre + **scope-kontrakt** (EAN, reference, revisioner) | 2,0 | FS+DK | S0 |
| S2-10 | Leverance + accept-kvittering (audit) | 1,0 | FS | 08,09 |
| S2-11 | Faktura: sekvensnr., moms, EAN-validering, idempotens, webhook | 2,0 | FS+DK | 10 |
| S2-12 | Guard-tests + fixtures FX-A1…A6 + zone-scan på leverance | 1,5 | **DK** | 04,07,08 |
| S2-13 | Metrics (LLM-forbrug, cache-hit) + runbook `agent-failed` | 0,5 | DE | 03 |

**Røde felter (S2-04, 07, 12) må ikke AI-genereres.** De ejer sandheden om, hvad der må publiceres og faktureres.

## A2. Acceptkriterier

```
S2-01  GIVEN dokument uden license_ref     THEN insert afvises
       GIVEN samme URL+hash igen           THEN dedup, ingen ny source_id
       GIVEN arkiv-materiale uden licens   THEN afvises (kun feeds/uddrag tilladt)

S2-02  GIVEN claim uden source_id          THEN DB-constraint afviser
       GIVEN claim uden effective_date     THEN afviser
       GIVEN status ∉ enum                 THEN afviser

S2-03  GIVEN LLM-svar uden for schema      THEN kasseres, logges, ingen claim oprettes
       GIVEN uændrede kilder               THEN cache-hit, ingen LLM-kald
       GIVEN prompt med zone B-felt        THEN kald blokeret (input-scanner)
       GIVEN kørsel                        THEN model_version + prompt_version gemt

S2-04  GIVEN source_id findes ikke i DB    THEN REJECT NO_SOURCE
       GIVEN citat ikke fuzzy-matchet i kilde THEN REJECT QUOTE_MISMATCH
       GIVEN predicate ∈ opinionsliste     THEN REJECT OPINION
       GIVEN status = RYGTE                THEN beholdes, men aldrig i Bevægelse-laget
       GIVEN confidence < 0,6              THEN til manuel kø, ikke auto-publish

S2-05  GIVEN samme plan i to medier        THEN merge til én claim, højeste confidence
       GIVEN merge                         THEN begge source_ids bevares som proveniens

S2-06  GIVEN reviewer åbner claim          THEN kilde vises med citat highlightet
       GIVEN mismatch                      THEN visuelt markeret, approve deaktiveret
       GIVEN genvej A/R/E                  THEN handling + næste claim på <20 sek.
       GIVEN reviewer                      THEN identitet gemmes i reviewed_by

S2-07  GIVEN én PENDING claim              THEN publish → 409 PROFILE_NOT_APPROVED
       GIVEN reviewed_by NULL              THEN publish afvises
       GIVEN publish                       THEN ny version, gammel bevares uændret

S2-08  GIVEN leverance                     THEN vandmærke med modtager-id + version
       GIVEN payload                       THEN ingen zone B-felter (automatisk scan)
       GIVEN claims.json                   THEN source_id, dato, status, confidence med
       GIVEN metode.md                     THEN kilder, friskhed, forbehold, model_version

S2-09  GIVEN offentlig kunde uden EAN      THEN scope kan ikke fuldføres
       GIVEN scope                         THEN revisionsvilkår (1 inkl.) accepteret eksplicit
       GIVEN 2. revision                   THEN kræver accept af timepris 4.500

S2-10  GIVEN deliver før APPROVED          THEN 409
       GIVEN accept                        THEN kvittering med tidsstempel + audit-ref

S2-11  GIVEN gentaget invoice-kald         THEN samme fakturanr. (idempotent)
       GIVEN faktura                       THEN 85.000 + 21.250 moms = 106.250
       GIVEN nummerserie                   THEN sekventiel, ingen huller
       GIVEN payment-webhook               THEN signaturverificeret, idempotent

S2-12  GIVEN FX-A1…A6                      THEN alle grønne før merge
       GIVEN zone-scan på PDF/JSON         THEN 0 persondatafelter

S2-13  GIVEN cache-hit < 70 %              THEN alarm
       GIVEN LLM-forbrug > 2× budget       THEN alarm + kørsel pauses
```

## A3. Definition of Done S2

Alle guards grønne · ingen publicering uden menneskelig review · leverance uden zone B · faktura idempotent og moms-korrekt · ADR-011 opdateret · runbook `agent-failed` skrevet · DK-review på S2-04/07/11/12.

**Forretningsmilepæl:** S2 grøn = **P1-porten kan nås** (≥2 betalte analyser inden md. 6).

---

# DEL B — Kontraktfiler

## B1. `contracts/openapi.yaml` (S1+S2 komplet)

```yaml
openapi: 3.1.0
info:
  title: Optata Core API
  version: 0.5.0
  description: >
    Kontrakt-først. Zone A er anonymt tilgængelig. Zone B kræver MitID.
    PublicProfile.additionalProperties=false er en sikkerhedskontrol.
servers:
  - url: https://api.optata.dk/v1

security: [{ anonymous: [] }]

tags:
  - name: public
  - name: orders
  - name: analyses
  - name: internal

components:
  securitySchemes:
    anonymous: { type: http, scheme: none }
    emailSession: { type: apiKey, in: header, name: X-Session }
    mitid:
      type: openIdConnect
      openIdConnectUrl: https://broker.optata.dk/.well-known/openid-configuration
    mitidStepUp: { type: apiKey, in: header, name: X-Step-Up-Ref }
    orgAuth:
      type: openIdConnect
      openIdConnectUrl: https://broker.optata.dk/erhverv/.well-known/openid-configuration
    staffAuth: { type: http, scheme: bearer, bearerFormat: JWT }

  parameters:
    Idempotency:
      name: Idempotency-Key
      in: header
      required: true
      schema: { type: string, maxLength: 64 }

  schemas:
    Error:
      type: object
      required: [code, message, trace_id]
      additionalProperties: false
      properties:
        code:
          type: string
          enum: [ORDER_ALREADY_ACTIVE, OWNERSHIP_NOT_VERIFIED, VERIFICATION_EXPIRED,
                 MISSING_CONSENT, STEP_UP_REQUIRED, REVEAL_BLOCKED, PROFILE_NOT_APPROVED,
                 SUBSCRIPTION_EXPIRED, MESSAGE_REDACTED, K_ANONYMITY_BLOCKED,
                 RATE_LIMITED, NO_SOURCE, NO_DATE, QUOTE_MISMATCH, OPINION,
                 EAN_REQUIRED, SCOPE_INCOMPLETE, REVISION_NOT_ACCEPTED, TOO_MANY_DIMENSIONS]
        message: { type: string }
        trace_id: { type: string }

    QualityFlags:
      type: object
      additionalProperties: { type: string }
      example: { areal: BBR_UNVERIFIED, vurdering: VUR_FORSINKET }

    Property:
      type: object
      required: [address_id, bfe, area_id, attrs]
      additionalProperties: false
      properties:
        address_id: { type: string, format: uuid }
        bfe: { type: string }
        matrikel_id: { type: [string, "null"] }
        area_id: { type: string }
        owner_kind: { type: string, enum: [PRIVATE, COMPANY, ANDELSFORENING] }
        attrs: { type: object }
        valuation: { type: [object, "null"] }
        plan: { type: array, items: { type: object } }
        quality_flags: { $ref: '#/components/schemas/QualityFlags' }
        valid_from: { type: string, format: date }
        recorded_at: { type: string, format: date-time }

    Claim:
      type: object
      required: [subject, predicate, value, status, effective_date, source_id, confidence]
      additionalProperties: false
      properties:
        claim_id: { type: string, format: uuid }
        subject: { type: string, maxLength: 200 }
        predicate: { type: string, maxLength: 100 }
        value: { type: object }
        status: { type: string, enum: [VEDTAGET, FORESLAET, UNDER_BYGNING, STOPPET, RYGTE] }
        effective_date: { type: string, format: date }
        source_id: { type: string, format: uuid }
        quote: { type: string, maxLength: 200 }
        confidence: { type: number, minimum: 0, maximum: 1 }
        review_state: { type: string, enum: [PENDING, APPROVED, REJECTED] }
        model_version: { type: string }
        prompt_version: { type: string }

    AreaProfile:
      type: object
      required: [area_id, version, layers, review_state]
      additionalProperties: false
      properties:
        profile_id: { type: string, format: uuid }
        area_id: { type: string }
        version: { type: integer }
        review_state: { type: string, enum: [PENDING, APPROVED, PUBLISHED] }
        reviewed_by: { type: [string, "null"] }
        layers:
          type: object
          properties:
            fakta: { type: object }
            bevaegelse: { type: array, items: { $ref: '#/components/schemas/Claim' } }
            hverdag: { type: object }
            efterspoergsel: { type: [object, "null"], description: "Zone C, k>=5 eller null" }
        meta:
          type: object
          properties:
            coverage: { type: object }
            freshness: { type: object }
            methodology_url: { type: string }

    Order:
      type: object
      required: [scope, area_id, criteria]
      additionalProperties: false
      properties:
        order_id: { type: string, format: uuid, readOnly: true }
        scope: { type: string, enum: [AREA, ADDRESS] }
        area_id: { type: string }
        address_id: { type: [string, "null"] }
        criteria:
          type: object
          properties:
            type: { type: string }
            areal_min: { type: integer }
            rooms_min: { type: integer }
            budget_max: { type: integer }
            horizon: { type: string, enum: ["0-3M", "3-6M", "6-12M", "12M+"] }
        level: { type: string, enum: [CURIOS, QUALIFIED, VERIFIED], readOnly: true }
        status: { type: string, readOnly: true,
                  enum: [ACTIVE, PAUSED, MATCHED, IN_DIALOG, AGREED, WITHDRAWN, EXPIRED, ERASED] }
        pseudonym: { type: string, readOnly: true }

    AnalysisScope:
      type: object
      required: [area_id, layers, buyer_reference, terms_accepted]
      additionalProperties: false
      properties:
        area_id: { type: string }
        layers: { type: array, items: { type: string, enum: [fakta, bevaegelse, hverdag, efterspoergsel] } }
        buyer_reference: { type: string, description: "Indkøbsordre/rekvirent" }
        ean: { type: [string, "null"], pattern: '^[0-9]{13}$' }
        revisions_included: { type: integer, default: 1, readOnly: true }
        terms_accepted: { type: boolean, const: true }
        terms_version: { type: string }

    Analysis:
      type: object
      additionalProperties: false
      properties:
        analysis_id: { type: string, format: uuid }
        state:
          type: string
          enum: [ORDERED, SCOPED, GENERATING, IN_REVIEW, APPROVED, DELIVERED,
                 ACCEPTED, INVOICED, PAID, REVISION, CANCELLED]
        area_id: { type: string }
        profile_version: { type: integer }
        price_dkk: { type: integer, default: 85000, readOnly: true }
        vat_dkk: { type: integer, default: 21250, readOnly: true }
        total_dkk: { type: integer, default: 106250, readOnly: true }
        delivery_due: { type: string, format: date }

    Invoice:
      type: object
      additionalProperties: false
      properties:
        invoice_no: { type: string, description: "Sekventiel, ingen huller" }
        issue_date: { type: string, format: date }
        delivery_date: { type: string, format: date }
        net_dkk: { type: integer }
        vat_dkk: { type: integer }
        total_dkk: { type: integer }
        terms: { type: string, default: "NET30" }
        ean: { type: [string, "null"] }
        buyer_reference: { type: string }

  responses:
    Conflict:
      description: Konflikt
      content: { application/json: { schema: { $ref: '#/components/schemas/Error' } } }
    Forbidden:
      description: Adgang afvist
      content: { application/json: { schema: { $ref: '#/components/schemas/Error' } } }

paths:
  /areas:
    get:
      tags: [public]
      parameters: [{ name: q, in: query, schema: { type: string } }]
      responses:
        "200":
          description: Områdeliste
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    area_id: { type: string }
                    name: { type: string }
                    dwelling_count: { type: integer }

  /areas/{id}/profile:
    get:
      tags: [public]
      parameters: [{ name: id, in: path, required: true, schema: { type: string } }]
      responses:
        "200":
          description: Zone A profil (cached)
          content: { application/json: { schema: { $ref: '#/components/schemas/AreaProfile' } } }
        "404": { description: Ukendt område }

  /properties/{address_id}:
    get:
      tags: [public]
      parameters: [{ name: address_id, in: path, required: true, schema: { type: string, format: uuid } }]
      responses:
        "200":
          description: Zone A ejendomsopslag
          content: { application/json: { schema: { $ref: '#/components/schemas/Property' } } }
        "404": { description: Ukendt adresse }

  /orders:
    post:
      tags: [orders]
      security: [{ emailSession: [] }]
      parameters: [{ $ref: '#/components/parameters/Idempotency' }]
      requestBody:
        required: true
        content: { application/json: { schema: { $ref: '#/components/schemas/Order' } } }
      responses:
        "201":
          description: Oprettet som CURIOS
          content: { application/json: { schema: { $ref: '#/components/schemas/Order' } } }
        "409": { $ref: '#/components/responses/Conflict' }

  /analyses:
    post:
      tags: [analyses]
      security: [{ orgAuth: [] }]
      parameters: [{ $ref: '#/components/parameters/Idempotency' }]
      requestBody:
        required: true
        content: { application/json: { schema: { $ref: '#/components/schemas/AnalysisScope' } } }
      responses:
        "201":
          description: ORDERED
          content: { application/json: { schema: { $ref: '#/components/schemas/Analysis' } } }
        "409": { $ref: '#/components/responses/Conflict' }

  /analyses/{id}/scope:
    post:
      tags: [analyses]
      security: [{ orgAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } }]
      requestBody:
        required: true
        content: { application/json: { schema: { $ref: '#/components/schemas/AnalysisScope' } } }
      responses:
        "200": { description: SCOPED }
        "409": { $ref: '#/components/responses/Conflict' }

  /analyses/{id}/deliver:
    post:
      tags: [analyses]
      security: [{ staffAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } },
                   { $ref: '#/components/parameters/Idempotency' }]
      responses:
        "200": { description: DELIVERED }
        "409": { $ref: '#/components/responses/Conflict' }

  /analyses/{id}/accept:
    post:
      tags: [analyses]
      security: [{ orgAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } }]
      responses:
        "200": { description: ACCEPTED, audit-ref returneres }

  /analyses/{id}/invoice:
    post:
      tags: [analyses]
      security: [{ staffAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } },
                   { $ref: '#/components/parameters/Idempotency' }]
      responses:
        "201":
          description: INVOICED
          content: { application/json: { schema: { $ref: '#/components/schemas/Invoice' } } }
        "409": { $ref: '#/components/responses/Conflict' }

  /analyses/{id}/revision:
    post:
      tags: [analyses]
      security: [{ orgAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } }]
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                accept_hourly_rate: { type: boolean }
                note: { type: string }
      responses:
        "202": { description: REVISION }
        "409": { $ref: '#/components/responses/Conflict' }

  /internal/claims/{id}/review:
    post:
      tags: [internal]
      security: [{ staffAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } }]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [decision]
              additionalProperties: false
              properties:
                decision: { type: string, enum: [APPROVE, REJECT, EDIT_APPROVE, MERGE, ESCALATE] }
                reason: { type: [string, "null"],
                          enum: [NO_SOURCE, NO_DATE, QUOTE_MISMATCH, OPINION, DUPLICATE, null] }
                edits: { type: [object, "null"] }
                merge_into: { type: [string, "null"], format: uuid }
      responses:
        "200": { description: Review registreret }
        "409": { $ref: '#/components/responses/Conflict' }

  /internal/profiles/{id}/publish:
    post:
      tags: [internal]
      security: [{ staffAuth: [] }]
      parameters: [{ name: id, in: path, required: true, schema: { type: string, format: uuid } },
                   { $ref: '#/components/parameters/Idempotency' }]
      responses:
        "200": { description: PUBLISHED, ny version }
        "409": { $ref: '#/components/responses/Conflict' }

  /webhooks/payment:
    post:
      tags: [internal]
      description: Signaturverificeret, idempotent
      parameters:
        - { name: X-Signature, in: header, required: true, schema: { type: string } }
        - { $ref: '#/components/parameters/Idempotency' }
      responses:
        "202": { description: Modtaget }
        "403": { $ref: '#/components/responses/Forbidden' }
```

## B2. `contracts/events/_envelope.v1.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://optata.dk/contracts/events/_envelope.v1.json",
  "title": "EventEnvelope",
  "type": "object",
  "required": ["event_id","type","schema_version","occurred_at","recorded_at","actor","zone","aggregate","trace_id","payload"],
  "additionalProperties": false,
  "properties": {
    "event_id":       { "type": "string", "format": "uuid" },
    "type":           { "type": "string", "pattern": "^[a-z_]+\\.[a-z_]+$" },
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "occurred_at":    { "type": "string", "format": "date-time" },
    "recorded_at":    { "type": "string", "format": "date-time" },
    "actor": {
      "type": "object",
      "required": ["kind"],
      "additionalProperties": false,
      "properties": {
        "kind":      { "enum": ["USER","STAFF","SYSTEM","PARTNER"] },
        "pseudonym": { "type": ["string","null"] },
        "org_id":    { "type": ["string","null"] }
      }
    },
    "zone":      { "enum": ["A","B","C"] },
    "aggregate": {
      "type": "object",
      "required": ["kind","id"],
      "properties": {
        "kind": { "enum": ["ORDER","DEAL","PROPERTY","IDENTITY","PROFILE","SUBSCRIPTION","ANALYSIS"] },
        "id":   { "type": "string" }
      }
    },
    "trace_id":     { "type": "string" },
    "causation_id": { "type": ["string","null"] },
    "payload":      { "type": "object" }
  },
  "allOf": [
    {
      "$comment": "Ingen direkte identifikatorer i payload",
      "not": {
        "properties": {
          "payload": {
            "anyOf": [
              { "required": ["cpr"] }, { "required": ["name"] },
              { "required": ["email"] }, { "required": ["phone"] },
              { "required": ["document"] }, { "required": ["message_body"] }
            ]
          }
        }
      }
    }
  ]
}
```

## B3. Udvalgte event-skemaer (fuld tekst)

**`order.created.v1.1.json`**
```json
{
  "$id": "https://optata.dk/contracts/events/order.created.v1.1.json",
  "allOf": [{ "$ref": "_envelope.v1.json" }],
  "properties": {
    "type": { "const": "order.created" },
    "schema_version": { "const": "1.1.0" },
    "zone": { "const": "B" },
    "payload": {
      "type": "object",
      "required": ["scope","area_id","level","household_key"],
      "additionalProperties": false,
      "properties": {
        "scope":         { "enum": ["AREA","ADDRESS"] },
        "area_id":       { "type": "string" },
        "address_id":    { "type": ["string","null"] },
        "level":         { "const": "CURIOS" },
        "household_key": { "type": ["string","null"] },
        "criteria_hash": { "type": "string" },
        "channel":       { "type": ["string","null"] }
      }
    }
  }
}
```

**`order.verified.v1.json`**
```json
{
  "$id": "https://optata.dk/contracts/events/order.verified.v1.json",
  "allOf": [{ "$ref": "_envelope.v1.json" }],
  "properties": {
    "type": { "const": "order.verified" },
    "zone": { "const": "B" },
    "payload": {
      "type": "object",
      "required": ["verification_id","method","expires_at"],
      "additionalProperties": false,
      "properties": {
        "verification_id": { "type": "string", "format": "uuid" },
        "method": { "enum": ["BANK_DOCUMENT","BANK_ATTESTATION","BANK_API","EQUITY"] },
        "issuer_code": { "type": ["string","null"] },
        "budget_band": { "type": "string" },
        "expires_at": { "type": "string", "format": "date" },
        "reviewed_by": { "type": "string" }
      }
    }
  }
}
```

**`verification.expired.v1.json`**
```json
{
  "$id": "https://optata.dk/contracts/events/verification.expired.v1.json",
  "allOf": [{ "$ref": "_envelope.v1.json" }],
  "properties": {
    "type": { "const": "verification.expired" },
    "zone": { "const": "B" },
    "payload": {
      "type": "object",
      "required": ["verification_id","new_level"],
      "additionalProperties": false,
      "properties": {
        "verification_id": { "type": "string", "format": "uuid" },
        "new_level": { "const": "QUALIFIED" },
        "removed_from_lead_lists": { "type": "boolean" }
      }
    }
  }
}
```

**`claims.extracted.v1.json`**
```json
{
  "$id": "https://optata.dk/contracts/events/claims.extracted.v1.json",
  "allOf": [{ "$ref": "_envelope.v1.json" }],
  "properties": {
    "type": { "const": "claims.extracted" },
    "zone": { "const": "A" },
    "payload": {
      "type": "object",
      "required": ["profile_id","accepted","rejected","model_version","prompt_version"],
      "additionalProperties": false,
      "properties": {
        "profile_id": { "type": "string", "format": "uuid" },
        "accepted": { "type": "integer", "minimum": 0 },
        "rejected": { "type": "integer", "minimum": 0 },
        "reject_reasons": { "type": "object", "additionalProperties": { "type": "integer" } },
        "model_version": { "type": "string" },
        "prompt_version": { "type": "string" },
        "cache_hit": { "type": "boolean" }
      }
    }
  }
}
```

**`profile.published.v1.json`**
```json
{
  "$id": "https://optata.dk/contracts/events/profile.published.v1.json",
  "allOf": [{ "$ref": "_envelope.v1.json" }],
  "properties": {
    "type": { "const": "profile.published" },
    "zone": { "const": "A" },
    "payload": {
      "type": "object",
      "required": ["profile_id","version","reviewed_by","claim_count"],
      "additionalProperties": false,
      "properties": {
        "profile_id": { "type": "string", "format": "uuid" },
        "version": { "type": "integer" },
        "reviewed_by": { "type": "string" },
        "claim_count": { "type": "integer" },
        "rygte_excluded": { "type": "boolean", "const": true }
      }
    }
  }
}
```

**`vault.accessed.v1.json`** *(sikkerhedskritisk)*
```json
{
  "$id": "https://optata.dk/contracts/events/vault.accessed.v1.json",
  "allOf": [{ "$ref": "_envelope.v1.json" }],
  "properties": {
    "type": { "const": "vault.accessed" },
    "zone": { "const": "B" },
    "payload": {
      "type": "object",
      "required": ["service","purpose","grant_id"],
      "additionalProperties": false,
      "properties": {
        "service": { "type": "string", "description": "P1-alarm hvis != disclosure" },
        "purpose": { "enum": ["REVEAL","ATTEST_REVIEW","OWNERSHIP_REVIEW","SUPPORT_REDACTED"] },
        "grant_id": { "type": ["string","null"] },
        "actor_ref": { "type": "string" },
        "break_glass": { "type": "boolean", "default": false }
      }
    }
  }
}
```

## B4. Resterende katalog (payload-felter, skemaer efter samme mønster)

| Event | Zone | Påkrævede payload-felter |
|---|---|---|
| `area.viewed` / `report.viewed` | A | area_id \| address_id, profile_version, channel |
| `order.qualified` | B | criteria_hash, assurance_level |
| `order.withdrawn` / `order.expired` | B | reason, days_inactive |
| `identity.linked` | B | from_pseudonym, to_pseudonym, reason |
| `identity.erased` | B | pseudonym, tombstone_ref, deleted_categories[] |
| `owner.notified` | B | address_id, channel, legal_basis_ref, aggregated_count |
| `owner.ownership_verified` | B | method, confidence, expires_at |
| `interest.viewed` / `interest.declined` | B | order_pseudonym, address_id |
| `dialog.opened` | B | thread_id |
| `message.sent` | B | thread_id, redaction_flags[], attachment_count |
| `message.redacted` | B | rule, content_hash, repeat_offender |
| `deal.price_agreed` | B | thread_id, agreed_terms_hash |
| `package.accepted` | B | package_id, payment_ref, amount_dkk |
| `reveal.consent_given` | B | party, consent_ref, text_version |
| `identity.revealed` | B | grant_id, audit_ref, stepup_ref |
| `property.changed` | A | address_id, field, valid_from, old_hash, new_hash |
| `subscription.started/expired` | B | product, scope_id, period_end, exclusive |
| `analysis.ordered/delivered/invoiced` | A | analysis_id, area_id, version, invoice_no |

**Versioneringsregel:** nye valgfrie felter = MINOR. Påkrævede/fjernede = MAJOR + upcaster + ADR. Gamle events omskrives aldrig i store.

---

# DEL C — DK-reviewerens checkliste

**Anvendes ved hver PR der rører en CODEOWNERS-sti.** Reviewer må **ikke** være forfatteren. SLA: 24 timer. Ingen merge uden sign-off.

## C1. Fælles indgang (alle røde felter)

- [ ] Issue-ID + ADR-reference angivet i PR
- [ ] Kontrakt (`openapi.yaml` / event-skema) opdateret **før** kode
- [ ] Guards tilføjet i **samme** PR — ikke i en efterfølgende
- [ ] Alle 12 CI-gates grønne, ingen overrides
- [ ] Ingen nye afhængigheder med ukendt licens eller kendt CVE
- [ ] Ingen persondata i logs, fixtures, screenshots eller kommentarer
- [ ] Runbook/ADR opdateret hvis adfærd eller drift ændres

## C2. Vault & reveal (`core/disclosure`, `core/identity`)

**Verificér:**
- [ ] Kun `disclosure_service` har SELECT på vault-tabeller (DB-rolle, ikke app-logik)
- [ ] Alle seks guards evalueres i **én DB-transaktion** med lås på deal-rækken
- [ ] Step-up kræves og er **≤5 minutter** gammel
- [ ] Betaling verificeres **server-side mod provider** — aldrig fra klientpayload
- [ ] Samtykke fra **begge** parter, med `text_version` og `consent_ref`
- [ ] Attest og ejerskab gencheckes inde i transaktionen (TOCTOU)
- [ ] `Idempotency-Key` håndhævet; gentaget kald → samme grant
- [ ] Audit skrives **før** data returneres; audit kan ikke UPDATE/DELETE
- [ ] Ingen admin-/support-endpoint kan kalde reveal

**Tests der skal være grønne:** `reveal_all_six_guards` · `reveal_concurrent_idempotent` · `reveal_toc_tou_expiry` · `vault_only_disclosure` · `agent_cannot_reveal`

**Afvis hvis:** blot én guard er implementeret i UI, i en separat transaktion, eller kan bypasses via intern service.

## C3. Redaction (`core/relay/redaction`)

- [ ] Deterministisk lag (regex → NER → EXIF/OCR → adfærd) kører **før** evt. LLM
- [ ] LLM er supplement, aldrig eneste værn
- [ ] Billeder: EXIF/GPS strippes, OCR-scannes; vedhæftninger typebegrænsede
- [ ] Rate limit + karantæne ved gentagne træff
- [ ] Afsender får forklaring; indhold logges som **hash**, ikke klartekst
- [ ] Ingen LLM-kald med zone B-indhold til endpoint uden for EU

**Tests:** `redaction_corpus` (50+ varianter inkl. tal skrevet med ord, EXIF-billede, URL-varianter)
**Afvis hvis:** sikkerheden afhænger af en model alene, eller et nyt medieformat ikke scannes.

## C4. RLS, zoner og DB-roller (`migrations`, `core/*` policies)

- [ ] Zone B-tabeller har RLS **aktiveret** og politikker testet pr. rolle
- [ ] `PublicProfile` og andre public-schemaer har `additionalProperties: false`
- [ ] Ingen query kan joine fra anonym/B2B-kontekst til vault
- [ ] `order_event` og audit: `REVOKE UPDATE, DELETE` verificeret
- [ ] Zone C: k≥5, afrunding til 5, komplementær suppression, max 3 dimensioner
- [ ] Migration er idempotent, fremad-only, med rollback-plan
- [ ] Bitemporalitet bevares: ingen destruktiv UPDATE på `property`

**Tests:** `no_zone_b_in_public` · `rls_agent_scope` · `k_anonymity` · `complementary_suppression` · `event_append_only`
**Afvis hvis:** en politik kun er håndhævet i applikationskode, eller en migration overskriver historik.

## C5. Samtykke, retention og sletning (`core/consent`)

- [ ] Formåls- og scope-bundet samtykke med `legal_basis_ref` + `text_version`
- [ ] Tilbagekaldelse propagere øjeblikkeligt (suppression + abort af tråde)
- [ ] To-lags sletning: zone B hårdt slettet, pseudonym events + audit + bogføring bevaret
- [ ] Tombstone kan **ikke** mappes til en person i nogen tabel
- [ ] Retention-frister matcher jurist-bilaget (dokument 90 dage, tråde 6 mdr., identitet 12 mdr.)
- [ ] Undtagelser (bogføring/audit) fremgår af privatlivspolitik
- [ ] Fortrydelsesret: waiver-checkbox med versioneret tekst ved øjeblikkelig levering

**Tests:** `erasure_preserves_events` · `tombstone_unmappable` · `consent_revocation_aborts_thread`
**Afvis hvis:** sletning er "soft delete" uden tombstone-garanti, eller en frist er hardcoded uden jurist-reference.

## C6. Finansiel og juridisk logik (refusion, tinglysning, fortrydelse, faktura)

- [ ] Regler skrevet af menneske, med kildehenvisning til gældende ret/praksis
- [ ] Testet mod **rigtige sager** (anonymiserede eksempler leveret af DK/jurist)
- [ ] Refusionsopgørelse: datoer, forbrugsperioder, acontobetalinger, ejerskifteforsikring
- [ ] Tinglysningsrækkefølge: skøde → adkomst → hæftelser; ingen antagelse om øjeblikkelig effekt
- [ ] Fortrydelsesfrist: korrekt beregning, helligdage/weekender, dokumenteret starttidspunkt
- [ ] Faktura: sekventielt nr. uden huller, moms 25 %, EAN valideret (13 cifre), leveringsdato, reference
- [ ] Kreditnota har egen serie; ingen sletning af bogførte bilag
- [ ] Ingen success fee, ingen %-salær, ingen escrow-logik i Optata

**Tests:** `refusion_reference_cases` · `tinglysning_order` · `fortrydelse_deadline` · `invoice_idempotent_sequence` · `vat_calculation`
**Afvis hvis:** logikken er AI-genereret uden menneskelig regelgennemgang, eller et regelsæt mangler juridisk reference.

## C7. Agent og publicering (`core/agent`)

- [ ] LLM-output valideres mod schema; afvigelser kasseres og logges
- [ ] `source_id` findes i DB; `effective_date` gyldig; citat ≤200 tegn og fuzzy-matchet
- [ ] Opinionsliste og RYGTE-håndtering aktiv; RYGTE aldrig i Bevægelse-laget
- [ ] `confidence < 0,6` → manuel kø
- [ ] Publish kræver alle claims APPROVED + `reviewed_by` ≠ NULL
- [ ] `model_version` + `prompt_version` gemt; prompt-ændring kræver ny version + fixtures
- [ ] Input-scanner blokerer zone B i prompts; ingen tool-kald til zone B
- [ ] Leverance (PDF/JSON) scannet for persondata; vandmærke med modtager-id

**Tests:** FX-A1…A6 · `claim_needs_source` · `publish_requires_approved` · `no_zone_b_in_delivery`
**Afvis hvis:** auto-publicering er mulig, eller et citat ikke kan findes i kilden.

## C8. Ejerskab og eksklusivitet

- [ ] Andelsbolig bruger **ikke** EJF-match; manuel/attest-flow findes
- [ ] Ejerskifte i registry tilbagekalder eksisterende verifikation automatisk
- [ ] Sameje: verifikation + samtykke fra **alle** ejere før reveal
- [ ] Navnematch er transient — intet navn i DB, logs eller events
- [ ] Eksklusivitet: unique index + advisory lock ved overlap bydel/postnummer
- [ ] RLS-cache invalideres øjeblikkeligt ved abonnement EXPIRED

**Tests:** `andels_not_ejf` · `ownership_revoked_on_transfer` · `sameje_all_consent` · `exclusive_agent_per_zip` · `rls_invalidation_on_expire`

## C9. Sign-off (kopieres ind i PR)

```
DK-REVIEW
PR: #____   Issue: S_-__   ADR: ___
Rørt felt: [ ] vault/reveal [ ] redaction [ ] RLS/zoner [ ] consent/retention
           [ ] finansiel/juridisk [ ] agent/publish [ ] ejerskab/eksklusivitet
Forfatter ≠ reviewer:            ja / nej
Guards tilføjet i samme PR:      ja / nej
Alle 12 CI-gates grønne:         ja / nej
Tests kørt lokalt (navne):       ______________________
Juridisk reference (hvis relevant): ___________________
Rollback-plan:                   ______________________
Beslutning:  APPROVE / REQUEST_CHANGES
Begrundelse: ______________________
Reviewer / dato: ________________
```

## C10. Eskalering

| Fund | Handling |
|---|---|
| Guard mangler eller kan bypasses | **REQUEST_CHANGES** + blokér merge, ingen undtagelse |
| Zone B-lækage i payload/leverance | **P1** — stop deploy, rollback hvis merged |
| Vault-adgang uden for disclosure | **P1** — spær service-credential, audit-review |
| Finansiel regel uden juridisk reference | Blokér + jurist ind over før merge |
| Prod-data i dev/fixture | **P1** — kontraktbrud, slet + rapportér inden 24 t |
| Uenighed om fortolkning | DK-stifter + jurist afgør; ADR opdateres |

---

## Hvor vi står

S2 er nu specificeret ned til issue-niveau, kontrakterne er skrevet som filer, og review-processen er en checkliste med tænder. **De røde felter er defineret, bemandet og testbare** — det er det, der gør AI-kodegenerering og et ukrainsk team til en fordel i stedet for en risiko.

Tre beslutninger/adgange står stadig åbne og er **kalendertid, ikke kodetid**:
1. **ADR-013** — data engineer fra md. 2 (afgør første krone i md. 4)
2. **Datafordeler + MitID-broker** — bestilles uge 1
3. **Jurist uge 6** — formidlingsvurdering af match+relay+reveal, kontaktgrundlag, retention-bilag

*Næste skridt kan være (a) S3-backloggen (MitID, vault, attest, expiry) som issues, (b) de faktiske guard-testfiler i kode (`tests/guards/*.py`) klar til repo, eller (c) jurist-bilaget: de konkrete spørgsmål der skal besvares i uge 1–6, formuleret så de kan besvares skriftligt.*