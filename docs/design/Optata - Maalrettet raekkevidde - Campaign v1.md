# OPTATA — Målrettet rækkevidde: mægleren betaler for adgang til efterspørgslen

Det er den rigtige måde at lade mægleren bruge ordrebogen på — og det er **den modsatte bevægelse af M3-lite**. Her får de ikke data med hjem. De betaler for at blive vist, inde i vores rails, til købere de ikke selv kan finde.

**Reach, ikke data.** Det er forskellen på at sælge dem et værktøj og at gøre dem afhængige af et marked.

---

## 1. Hvorfor det styrker tyngdepunktet

| Mægleren bruger i dag | Hvad de får hos os |
|---|---|
| Boligsiden-annonce til alle | **Verificerede købere med budget, horisont og geografi** |
| Facebook-interesser | **Faktisk købsintention, dokumenteret købeevne** |
| Eget køberkartotek | **Købere de aldrig selv har mødt** |

Ingen andre kan tilbyde det. Og de kan ikke tage det med hjem — for de får aldrig at vide, hvem de ramte, før køberen selv svarer.

**Loopet der låser markedet:**
```
Kampagne → køberen ser en relevant bolig i Optata
        → køberen sender forespørgsel eller BUD
        → buddet ligger i OfferLedger
        → mægleren må svare inde i Optata
```
Kampagnen er ikke endepunktet. Den er **indgangen til budbogen**.

---

## 2. Den hårde risiko — og designprincippet

**Spam dræber tætheden.** Hvis 12 mæglere kan sende til de samme 250 købere, melder køberne fra, ordrebogen tømmes, og moaten dør. Det er den eneste måde dette produkt kan ødelægge forretningen på.

**Princip:** Køberen skal opleve det som *relevante muligheder*, ikke som reklame. Derfor er alt nedenfor begrænsning, ikke funktion.

---

## 3. Ny primitiv: `Campaign`

```sql
CREATE TABLE campaign (
  campaign_id     uuid PRIMARY KEY,
  agent_org_id    uuid NOT NULL,          -- MitID Erhverv, CVR
  listing_id      uuid NOT NULL,          -- SKAL være eget aktivt udbud
  audience_query  jsonb NOT NULL,         -- kun tilladte dimensioner
  audience_size   int NOT NULL,           -- beregnet, ≥25
  message         text,                   -- max 400 tegn, scannet
  status          text NOT NULL,          -- DRAFT|REVIEW|APPROVED|SENT|STOPPED
  quota_cost      int NOT NULL,
  terms_version   text NOT NULL,
  created_at      timestamptz NOT NULL
);

CREATE TABLE campaign_delivery (
  campaign_id     uuid, buyer_identity uuid,
  relevance_score numeric, delivered_at timestamptz,
  opened_at timestamptz, feedback text,   -- RELEVANT|IRRELEVANT|MUTE_AGENT
  PRIMARY KEY (campaign_id, buyer_identity)
);

CREATE TABLE buyer_marketing_consent (
  buyer_identity uuid, purpose text,      -- MATCHED_OPPORTUNITIES
  scope jsonb, granted_at timestamptz, revoked_at timestamptz,
  text_version text, legal_basis_ref text
);
```

**Hård regel:** `listing_id` skal være mæglerens **eget aktivt udbud** med gyldig `license_ref`. Ingen kampagner for boliger, de ikke har mandat på. Ingen generel branding.

---

## 4. Targeting: kun det, køberen selv har sagt

| Tilladt dimension | Eksempel |
|---|---|
| Geografi | postnummer, gade, kommune |
| Boligtype | villa, ejerlejlighed, andel |
| Areal / værelser | 140–180 m², 4+ |
| Budgetbånd | 4,0–4,5 mio. |
| Horisont | 0–3, 3–6, 6–12 mdr. |
| Verifikation | kun VERIFIED (default) |

**Forbudt:** navn, køn, alder, indkomst, familiestatus, adfærd uden for ordren, frie søgninger, upload af egne lister, lookalikes.

**To anonymitetsgulve:**
- **Minimumsaudience ≥ 25** — ellers kan en kampagne de facto ramme én person
- **k≥5 på enhver celle** i audience-estimater (samme maskineri som Demand Pro)

Mægleren ser: *"Din kampagne rammer ca. 40 verificerede købere i 2900 Hellerup."* Aldrig hvem.

---

## 5. Levering: inbox, caps og mute

```
Kampagne → relevans-score pr. køber (samme model som M3)
        → kun købere over tærskel + med samtykke + under loft
        → Optata-inbox: "Ny mulighed, der matcher dit ønske"
        → valgfri e-mail: kun "du har en ny mulighed", aldrig indhold
```

| Begrænsning | Værdi |
|---|---|
| Samtykke | **Eksplicit opt-in** til "relevante muligheder fra mæglere". Aldrig default |
| Loft pr. køber | maks. **1 pr. uge, 3 pr. måned** |
| Relevans-tærskel | score ≥ 70 (ellers leveres ikke, ingen kvote trukket) |
| Mute | Køberen kan **permanent** stumme en mægler — ét klik |
| Feedback | "Ikke relevant" → sænker mæglerens omdømme |
| Quiet hours | 08–20 |
| Ingen kontakt | Aldrig navn, telefon, e-mail i kampagnen |

**Notifikation følger v5.1:** frivilligt tilvalg. Inboxen er altid primær.

---

## 6. Indhold: struktureret, scannet, attribueret

```
┌──────────────────────────────────────────────┐
│  Ny mulighed, der matcher dit ønske          │
│                                              │
│  Strandvejen 142, 2900 Hellerup              │
│  Villa · 164 m² · 5 værelser · 4.150.000 kr. │
│  Dit match: 92/100                           │
│  ✓ Budget ✓ Størrelse ✓ Type ✓ Horisont      │
│                                              │
│  "Vi holder åbent hus søndag kl. 13.         │
│   Boligen har netop fået nyt køkken."        │
│                                              │
│  Eksempel Mægler A/S · Se annonce ↗          │
│  [ Send forespørgsel ]  [ Afgiv bud ]        │
│  [ Ikke relevant ]  [ Stum denne mægler ]    │
└──────────────────────────────────────────────┘
```

**Regler:** boligkortet er struktureret data fra feedet · fritekst max 400 tegn, scannet for kontaktinfo og eksterne links · attribution obligatorisk · **kun handlinger inde i Optata**.

---

## 7. Pris og omdømme

| Produkt | Indhold | Pris |
|---|---|---|
| Postnummer 2.900/md. | 2 kampagner/md. til matchet segment | inkluderet |
| Bydel 6.900/md. | 6 kampagner/md. + feed + API | inkluderet |
| Ekstra kampagne | 1 pr. udbud | **1.500 kr.** |

**Aldrig betaling pr. lead, pr. kontakt eller pr. handel.** Vi sælger rækkevidde — det er markedsføring, ikke formidling. Det holder den juridiske position ren.

**Omdømme styrer volumen:**
```
relevance_rate = RELEVANT / (RELEVANT + IRRELEVANT)
mute_rate      = MUTE_AGENT / deliveries
```
`relevance_rate < 40 %` eller `mute_rate > 5 %` → halveret kvote, manuel review af næste kampagner. Det beskytter køberen og tvinger mægleren til at være relevant.

---

## 8. Tre nye invarianter (18–20)

```
18. Al mægler→køber-kommunikation går gennem Optatas inbox.
    Ingen kontaktdata eksporteres. Audience ≥25 og k≥5 på alle celler.

19. Køberens markedsføringssamtykke er eksplicit, formålsbundet og
    tilbagekaldeligt. Loft og mute håndhæves i domænet, ikke i UI.

20. Kampagner kræver eget aktivt udbud med gyldig licens, struktureret
    indhold, attribution og scanning. Ingen eksterne kontaktveje.
```

**Guards (menneskeskrevne):**
`campaign_requires_own_listing` · `audience_min_25_and_k5` · `consent_required_before_delivery` · `frequency_cap_enforced` · `mute_is_permanent` · `no_contact_in_campaign` · `reputation_throttle`

---

## 9. Juridiske spørgsmål (L43–L48)

| # | Spørgsmål | Afgør |
|---|---|---|
| **L43** 🔴 | Hvilket **samtykke** kræves for at vise købere markedsføring fra tredjepart (mægler)? Er Optata afsender på mæglerens vegne, eller formidler af indhold? Hvem er dataansvarlig? | Hele produktet |
| **L44** 🔴 | Er målretning mod **købsintention + budget** profilering der udløser særlige krav? Er audience ≥25 + k≥5 tilstrækkeligt til at undgå individuel målretning? | Targeting-model |
| **L45** | Er kampagne→forespørgsel→bud **formidling**, eller markedsføring af et udbud? Vi tager intet honorar pr. handel | Positionering |
| **L46** | Krav til **indhold og attribution**: pris, "solgt"-status, åbent hus, vildledende udsagn | Indholdsregler |
| **L47** | **P2B / platform-forordningen**: krav til gennemsigtighed i rangering, omdømmescoring og kvotetildeling over for erhvervskunder | Omdømmemodel |
| **L48** | Retention af **kampagne-interaktion** (åbnet, feedback, mute) — formål og frist | Datamodel |

**L43 og L44 skal besvares før kampagne-modulet bygges.** Resten kan afklares parallelt.

---

## 10. Hvor det passer i sekvensen

Kampagner er **juridisk lettere end mandat og budbog** — det er markedsføring af et eksisterende udbud, ikke gennemførelse af en handel. Og det giver mægleren øjeblikkelig ROI.

| Fase | Leverance | Kontrolpunkt |
|---|---|---|
| 1 | Register + analyse | Cash |
| 2 | Verificeret ordrebog (MitID + attest) | **Origination** |
| **3** | **Feed + kampagner + inbox** | **Mægleren betaler for rækkevidde** |
| 4 | SaleMandate | **Mandat** |
| 5 | OfferLedger | **Budproces + prisdannelse** |
| 6 | Fulfillment via partner | Gebyr + sagsmappe |

**Fase 3 er acquisition-motoren.** Fase 4+5 er låsen. Kampagnerne rekrutterer mæglerne og finansierer os — mandatet og budbogen gør dem afhængige.

**Det må ikke blive produktet.** Hvis vi stopper ved fase 3, er vi et annonceværktøj. Kampagnerne er kun strategisk rigtige, fordi de fører ind i budbogen.

---

## 11. Metrics og kill-kriterier

```
campaign_relevance_rate{agent}       # mål ≥60 %
buyer_mute_rate{agent}               # alarm >5 %
marketing_consent_rate               # andel købere der opt-in'er
campaigns_per_buyer_per_month        # skal holde sig under loft
inquiry_to_offer_rate                # loopet virker?
agent_roi_reported                   # fornyelsesdriver
opt_out_after_campaign_rate          # alarm >3 %
```

| Signal | Handling |
|---|---|
| `opt_out_after_campaign > 3 %` | **Stop kampagner** — produktet skader tætheden |
| `consent_rate < 30 %` | Opt-in præsenteres forkert ved ordre-oprettelse |
| `relevance < 40 %` pr. mægler | Kvotenedsættelse + review |
| `inquiry_to_offer ≈ 0` | Kampagner fører ikke ind i budbogen → loopet er brudt |

---

## Konklusion

Målrettet rækkevidde er **den korrekte måde at lade mægleren bruge efterspørgslen på**: de betaler for at blive vist til verificerede købere, de aldrig selv kan finde, og de får aldrig data med hjem. Hver kampagne skubber køberen dybere ind i vores inbox og videre mod budbogen.

Det er også den bedste acquisition-kanal for mæglere, vi har — bedre end invitationen, fordi den giver dem målbar ROI med det samme.

**Men det er det farligste modul at bygge forkert.** Ét loft for meget, én irrelevant kampagne for mange, og køberne melder fra — så forsvinder det aktiv, hele forretningen hviler på. Derfor er begrænsningerne ovenfor ikke features. De er produktet.

*Vil du have, at jeg skriver (a) kampagne-modulet som fuld spec (API, states, guards, samtykketekst), (b) den korrigerede ARCHITECTURE.md v2.0 med 20 invarianter og de nye moduler `mandates`, `offers`, `campaigns`, eller (c) L38–L48 som samlet jurist-bilag?*
