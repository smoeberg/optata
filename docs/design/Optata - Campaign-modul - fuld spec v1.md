# OPTATA — Kampagne-modulet: fuld specifikation

## A1 · Datamodel (zone B, RLS)

```sql
CREATE TABLE buyer_marketing_consent (
  buyer_identity  uuid NOT NULL,
  purpose         text NOT NULL DEFAULT 'MATCHED_OPPORTUNITIES',
  scope           jsonb NOT NULL,          -- {area_ids[], types[], budget_band}
  text_version    text NOT NULL,
  legal_basis_ref text NOT NULL,           -- juristens dokument-id
  granted_at      timestamptz NOT NULL,
  revoked_at      timestamptz,
  PRIMARY KEY (buyer_identity, purpose)
);

CREATE TABLE agent_mute (
  buyer_identity uuid, agent_org_id uuid,
  muted_at timestamptz NOT NULL,           -- PERMANENT, ingen udløb
  PRIMARY KEY (buyer_identity, agent_org_id)
);

CREATE TABLE campaign (
  campaign_id     uuid PRIMARY KEY,
  agent_org_id    uuid NOT NULL,
  listing_id      uuid NOT NULL,           -- eget aktivt udbud, license_ref gyldig
  audience_query  jsonb NOT NULL,          -- kun tilladte dimensioner
  audience_size   int  NOT NULL,           -- beregnet, CHECK >= 25
  message         text,                    -- CHECK length <= 400
  relevance_min   int  NOT NULL DEFAULT 70,
  quota_cost      int  NOT NULL DEFAULT 1,
  status          text NOT NULL,           -- DRAFT|REVIEW|APPROVED|SENT|STOPPED|REJECTED
  terms_version   text NOT NULL,
  reviewed_by     text,
  created_at      timestamptz NOT NULL,
  CONSTRAINT audience_floor CHECK (audience_size >= 25),
  CONSTRAINT message_cap    CHECK (message IS NULL OR length(message) <= 400)
);

CREATE TABLE campaign_delivery (
  campaign_id     uuid, buyer_identity uuid,
  relevance_score numeric NOT NULL,
  delivered_at    timestamptz NOT NULL,
  opened_at       timestamptz,
  feedback        text,                    -- RELEVANT|IRRELEVANT|MUTE_AGENT
  PRIMARY KEY (campaign_id, buyer_identity)
);

CREATE TABLE agent_reputation (
  agent_org_id    uuid PRIMARY KEY,
  relevance_rate  numeric,                 -- RELEVANT / (RELEVANT+IRRELEVANT)
  mute_rate       numeric,
  quota_multiplier numeric NOT NULL DEFAULT 1.0,
  under_review    boolean NOT NULL DEFAULT false,
  computed_at     timestamptz NOT NULL
);
```

## A2 · Tilstandsmaskine

```
DRAFT → REVIEW → APPROVED → SENT
          └→ REJECTED (indhold/audience/licens)
SENT → STOPPED (manuel stop, udbud SOLD, omdømme-throttle)
```

**Guards:** `APPROVED` kræver (eget aktivt udbud ∧ gyldig licens ∧ audience ≥25 ∧ indhold scannet ∧ vilkår accepteret). `SENT` kræver godkendelse + kvote. Udbud `SOLD/WITHDRAWN/STALE` → øjeblikkelig `STOPPED`.

## A3 · Leverings-pipeline (rækkefølgen er sikkerheden)

```python
def deliver(campaign):
    require(campaign.status == 'APPROVED')
    require(listing_active_and_licensed(campaign.listing_id))
    require(owns_listing(campaign.agent_org_id, campaign.listing_id))

    for buyer in audience(campaign.audience_query):      # k>=5 pr. celle
        if not consent_active(buyer, 'MATCHED_OPPORTUNITIES'): continue
        if muted(buyer, campaign.agent_org_id):               continue
        if suppressed(buyer):                                 continue
        if not within_cap(buyer, weekly=1, monthly=3):        continue
        if not quiet_hours_ok():                              queue(); continue
        score = relevance(buyer.order, campaign.listing)
        if score < campaign.relevance_min:                    continue   # ingen kvote trukket
        inbox.deliver(buyer, render(campaign, score))         # struktureret + scannet tekst
        emit('campaign.delivered', score=score)
    reputation.recompute(campaign.agent_org_id)
```

**Kvote trækkes kun ved faktisk levering** — ikke ved afvisning pga. samtykke, loft, mute eller lav relevans.

## A4 · API

| Metode | Endpoint | Auth | Guard |
|---|---|---|---|
| POST | `/campaigns` | Erhverv | Eget udbud + licens |
| GET | `/campaigns/{id}/audience-estimate` | Erhverv | ≥25, k≥5, kun antal |
| POST | `/campaigns/{id}/submit` | Erhverv | Indholdscanning, vilkår |
| POST | `/internal/campaigns/{id}/review` | Staff | APPROVE/REJECT |
| POST | `/campaigns/{id}/stop` | Erhverv | Øjeblikkelig |
| GET | `/me/opportunities` | MitID | Kun egne, inbox |
| POST | `/me/opportunities/{id}/feedback` | MitID | RELEVANT/IRRELEVANT |
| POST | `/me/mutes/{agent_org_id}` | MitID | Permanent |
| POST | `/me/marketing-consent` | MitID | Opt-in/tilbagekald, `text_version` |

**Fejlkoder:** `AUDIENCE_TOO_SMALL` · `LISTING_NOT_OWNED` · `LICENSE_INVALID` · `CONTENT_REJECTED` · `QUOTA_EXCEEDED` · `REPUTATION_THROTTLED` · `CONSENT_REQUIRED`.

## A5 · Samtykketekst (opt-in ved ordre-oprettelse)

```
Vil du se boliger, der matcher dit ønske?

Mæglere kan vise dig boliger til salg, der passer til det, du søger —
inden for dit område, din boligtype og dit budget.

· Du får højst én om ugen, og højst tre om måneden
· Du ser altid, hvilken mægler det er, og kan stumme dem permanent
· Dit navn og dine kontaktoplysninger deles aldrig med mægleren
· Du kan slå det fra igen med ét klik

☐ Ja, vis mig matchende boliger fra mæglere (v1.0)
```

**Aldrig forudafkrydset.** Afkrydsning gemmes med `text_version` + `legal_basis_ref`.

## A6 · Guards (menneskeskrevne, `tests/guards/`)

```
campaign_requires_own_listing      # fremmed udbud → 403
license_invalid_blocks_campaign    # udløbet licens → ingen afsendelse
audience_min_25_and_k5             # 24 → AUDIENCE_TOO_SMALL; celle k<5 skjules
consent_required_before_delivery   # uden opt-in → ingen levering
frequency_cap_enforced             # 2. på en uge → afvist, ingen kvote
mute_is_permanent                  # muted agent → aldrig levering igen
no_contact_in_campaign             # telefon/mail/URL i fritekst → CONTENT_REJECTED
sold_listing_stops_campaign        # SOLD → STOPPED øjeblikkeligt
reputation_throttle                # relevance<40% → kvote halveret
quota_only_on_delivery             # afvisning trækker ikke kvote
```

## A7 · Acceptkriterier

```
GIVEN audience 24                 THEN 409 AUDIENCE_TOO_SMALL
GIVEN køber uden opt-in           THEN ingen levering, ingen kvote
GIVEN 4. kampagne på en måned     THEN afvist for den køber
GIVEN mute klikket                THEN aldrig levering fra den mægler igen
GIVEN udbud SOLD                  THEN campaign STOPPED, inbox-marker opdateret
GIVEN relevance 35 % hos mægler   THEN quota_multiplier 0,5 + under_review
GIVEN opt_out efter kampagne >3 % THEN P2-alarm, kampagner pauses globalt
GIVEN mægler ser audience         THEN kun antal, aldrig pseudonymer
```
