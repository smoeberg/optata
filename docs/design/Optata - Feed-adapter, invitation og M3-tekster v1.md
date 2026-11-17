# OPTATA — (a) Feed-adapter · (b) Invitation & gratis-svar · (c) Arkitektur- og ADR-opdatering

## Først: én vigtig forretningskonsekvens ved M3

Når mægleren er modpart, **er mægleren allerede formidler**. Derfor:

| Vej | Modpart | Hvem gennemfører handlen | Optatas indtægt |
|---|---|---|---|
| **M1** (ejer uden mægler) | Privat ejer | Advokatpartner via salgspakke | **10.000 kr. pakke** |
| **M3** (udbud med mægler) | Professionel mægler | **Mægleren** | **Abonnement/lead — ingen pakke** |

**Konsekvens:** Salgspakken må **ikke** tilbydes i M3-flowet. Det ville være dobbelt formidling, dobbelt betaling for kunden og den værste formidlingsrisiko for os. Til gengæld er M3 den rene vej: vi leverer en verificeret køber, mægleren gør arbejdet, vi tager abonnement.

Det gør også **L34 lettere at besvare**: vi formidler ikke en handel — vi leverer en kvalificeret henvendelse til en allerede godkendt formidler.

---

# DEL A — `listing`-adapter: AGENT_FEED v1

## A1 · Transport og drift

| Aspekt | Specifikation |
|---|---|
| Primær | **HTTPS pull** af mæglerens feed-URL (JSON eller XML), `If-Modified-Since` / ETag |
| Sekundær | SFTP-drop (ældre mæglersystemer), filnavn `listings_{cvr}_{YYYYMMDD-HHMM}.xml` |
| Tertiær | Webhook `POST /webhooks/listings` (signeret, idempotent) — for systemer der kan pushe |
| Frekvens | Hver 30. min for aktive feeds; natlig fuld reconciliation |
| Auth | API-nøgle/OAuth2 client credentials pr. mægler-org. **Aldrig i repo** — secret manager |
| Retry | 3 forsøg, eksponentiel backoff. Vedvarende fejl → `feed-failed` runbook |
| Checkpoint | `last_success_at` + `etag` + `highest_changed_at` pr. kilde |

## A2 · Kanonisk format (JSON — XML mappes hertil)

```jsonc
{
  "feed_version": "1.0",
  "agent_org": { "cvr": "12345678", "name": "Eksempel Mægler A/S" },
  "generated_at": "2026-11-16T09:00:00Z",
  "listings": [
    {
      "source_ref": "EDC-2900-00142",        // påkrævet, stabil id hos mægleren
      "status": "ACTIVE",                     // ACTIVE|UNDER_OFFER|SOLD|WITHDRAWN
      "listed_at": "2026-11-10",
      "changed_at": "2026-11-16T08:42:00Z",
      "address": {
        "street": "Strandvejen", "house_no": "142",
        "floor": null, "door": null,
        "zip": "2900", "city": "Hellerup",
        "municipality_code": "0157",          // Gentofte
        "dar_address_id": null                // udfyldes af os via geokodning
      },
      "property": {
        "type": "VILLA",                      // VILLA|RAEKKEHUS|EJERLEJLIGHED|ANDELSBOLIG|FRITID|GRUND
        "living_area_m2": 164,
        "rooms": 5,
        "lot_area_m2": 712,
        "build_year": 1932,
        "energy_label": "C"
      },
      "asking_price_dkk": 4150000,
      "monthly_owner_cost_dkk": 3850,
      "public_url": "https://maegler.dk/sag/00142",
      "media": { "hero_image_url": "https://…", "image_count": 12 },
      "open_house": [{ "from": "2026-11-22T13:00:00Z", "to": "2026-11-22T14:00:00Z" }]
    }
  ]
}
```

## A3 · Feltmapping og validering

| Felt | Påkrævet | Validering | Ved fejl |
|---|---|---|---|
| `source_ref` | ✅ | Stabil, unik pr. org | Karantæne |
| `status` | ✅ | ∈ enum | Karantæne |
| `listed_at` / `changed_at` | ✅ | ISO, `changed_at ≥ listed_at` | Karantæne |
| `address.street` + `house_no` + `zip` | ✅ | Findes i DAR | **Fuzzy-match → manuel kø**, ikke drop |
| `municipality_code` | ✅ | 4 cifre, findes i kommune-register | Karantæne |
| `property.type` | ✅ | ∈ enum | Karantæne |
| `living_area_m2` | ✅ | 10–2000 | Flag `AREA_UNVERIFIED` |
| `rooms` | ✅ | 1–30 | Flag |
| `asking_price_dkk` | ✅ | 50.000–200.000.000 | Flag `PRICE_OUTLIER` |
| `public_url` | ✅ | HTTPS, matcher mæglerens domæne | Karantæne (attribution-krav) |
| `dar_address_id` | ❌ | Vi udleder det | — |
| `media` | ❌ | Kun URL, **vi downloader ikke billeder** uden licens | — |

**Licensregel (hård):** `listing_source.license_ref` skal findes og være aktiv, før **én eneste** record importeres. Ingen licens → adapteren er deaktiveret i config.

## A4 · Geokodning til vores nøgler

```python
def resolve_address(raw) -> Resolution:
    # 1. Eksakt DAR-match på vej+husnr+etage+dør+postnr
    if hit := dar.exact(raw): return Resolution(hit.address_id, hit.bfe, HIGH)
    # 2. Husnr uden etage/dør → hvis én enhed, brug den; ellers manuel kø
    if len(cands := dar.candidates(raw)) == 1: return Resolution(cands[0], ..., MEDIUM)
    # 3. Vej-match (gade-scope virker selv uden adresse-id)
    if street := dar.street(raw.street, raw.zip):
        return Resolution(None, None, LOW, street_id=street.id,
                          municipality_id=raw.municipality_code)
    return Quarantine("ADDRESS_UNRESOLVED")
```

**Vigtigt:** Et udbud uden `address_id` kan stadig matches på **gade- og kommune-scope**. Det må ikke blokere M3 — men det må heller ikke udløse M1 (ejer-kontakt kræver eksakt adresse).

## A5 · Status-livscyklus og propagering

```
ACTIVE ──→ UNDER_OFFER ──→ SOLD
   └─────→ WITHDRAWN ─────→ (genlistet: ny listed_at, samme source_ref)
```

| Hændelse | Handling |
|---|---|
| `SOLD` / `WITHDRAWN` | Sæt `valid_to`, fjern fra alle match, **ingen ny notifikation**, eksisterende tråde markeres "Boligen er ikke længere til salg" |
| Prisændring | Ny bitemporal version, `listing.price_changed` → notifér matchede købere (max 1 pr. 7 dage pr. bolig) |
| Genlistet | Ny `listed_at`, historik bevares |
| Feed forsvinder (mægler opsiger) | Efter 30 dage uden opdatering: `status=STALE`, skjul fra match, bevar historik jf. licens |

## A6 · Idempotens og reconciliation

- **Naturlig nøgle:** `(source, source_ref, changed_at)` → ingen duplikater ved genkørsel.
- **Natlig reconciliation:** alle `ACTIVE` i vores DB, der **ikke** er i feedet, markeres `STALE` (ikke `SOLD` — vi må ikke opdigte et salg).
- **Delta-effektivitet:** kun records med `changed_at > checkpoint` behandles; fuld kørsel kun natligt.

## A7 · XML-variant (ældre systemer)

```xml
<listings version="1.0" cvr="12345678" generatedAt="2026-11-16T09:00:00Z">
  <listing ref="EDC-2900-00142" status="ACTIVE"
           listedAt="2026-11-10" changedAt="2026-11-16T08:42:00Z">
    <address street="Strandvejen" houseNo="142" zip="2900"
             city="Hellerup" municipalityCode="0157"/>
    <property type="VILLA" livingAreaM2="164" rooms="5"
              lotAreaM2="712" buildYear="1932"/>
    <askingPrice currency="DKK">4150000</askingPrice>
    <publicUrl>https://maegler.dk/sag/00142</publicUrl>
  </listing>
</listings>
```

Adapteren normaliserer XML → kanonisk JSON, **derefter samme validering**. Ingen særregler pr. format.

## A8 · Fixtures og acceptkriterier

```
FX-L1  Udbud uden license_ref              → import afvist, adapter deaktiveret
FX-L2  Andelsbolig-udbud (BFE, 40 enheder) → korrekt adresse-id, ikke hele ejendommen
FX-L3  Udbud uden etage/dør, 12 kandidater → manuel kø, men gade-match virker
FX-L4  SOLD i feed                          → match fjernet, tråd markeret, ingen notifikation
FX-L5  Prisændring 4.150.000 → 3.950.000    → ny version, historik bevares, 1 notifikation
FX-L6  Genkørsel af samme feed              → 0 duplikater
FX-L7  ACTIVE forsvundet fra feed           → STALE, ikke SOLD
FX-L8  public_url på fremmed domæne         → karantæne (attribution)
```

---

# DEL B — Invitation og gratis-svar-flow

## B1 · Køberens notifikation (M3 udløses)

```
Emne:      En bolig til salg matcher dit ønske
Preheader: Strandvejen 142, Hellerup — 4.150.000 kr.

En bolig til salg matcher dit ønske.

Strandvejen 142, 2900 Hellerup
Villa · 164 m² · 5 værelser · 4.150.000 kr.
Til salg siden 10.11.2026 · Kilde: [Mægler], se annonce

Dit ønske: Villa, 140–180 m², 4+ værelser, op til 4,2 mio. kr.

    [ Se boligen og dit match ]

Dit navn og dine kontaktoplysninger er ikke delt med mægleren.
Du bestemmer selv, om du vil tage kontakt.
```

**Frekvensloft:** maks. 1 pr. dag pr. køber, samlet liste over nye matches. Prisændring: maks. 1 pr. 7 dage pr. bolig. Aldrig notifikation for `SOLD`/`WITHDRAWN`/`STALE`.

## B2 · Køberens skærm: match + kontaktvalg

```
┌──────────────────────────────────────────────────────────┐
│  Strandvejen 142, 2900 Hellerup                          │
│  Villa · 164 m² · 5 værelser · Opført 1932 · Grund 712 m²│
│  4.150.000 kr. · Til salg siden 10.11.2026               │
│  Kilde: Eksempel Mægler A/S · Se annonce ↗               │
│                                                          │
│  Dit match                                    92 / 100   │
│  ✓ Budget dækker  ✓ Størrelse passer  ✓ Type matcher     │
│  ✓ Verificeret    ✓ Horisont 3–6 måneder                 │
│                                                          │
│  Mægleren er ikke på Optata endnu.                       │
│  Du kan sende en anonym invitation. Det er gratis for dig│
│  og gratis for mægleren at svare på.                     │
│                                                          │
│  [ Send anonym invitation ]                              │
│                                                          │
│  Dit ønske er verificeret til 12.06.2026.                │
└──────────────────────────────────────────────────────────┘
```

**Hvis mægleren allerede er registreret:** knappen er `[ Åbn anonym dialog ]` — samme relay som C5, men **uden salgspakke**.

**Hvis køberen er CURIOS/QUALIFIED:**
```
Dit ønske er ikke verificeret endnu.
Mæglere svarer kun på henvendelser med dokumenteret købeevne.
[ Gør mit ønske verificeret ]
```

## B3 · Invitationsmailen til mægleren

```
Emne:      Verificeret køber til Strandvejen 142
Preheader: Anonym henvendelse. Gratis at se og svare på.

Der er en verificeret køber til en bolig, du har til salg.

Strandvejen 142, 2900 Hellerup · 4.150.000 kr.

Køberen er identificeret med MitID og har dokumenteret købeevne
fra bank eller realkredit.

    Købeevne      4,0–4,5 mio. kr.
    Ønske         Villa · 140–180 m² · 4+ værelser
    Horisont      Inden 3–6 måneder
    Verificeret   12.03.2026 · gyldig til 12.06.2026

Du kan se henvendelsen anonymt og svare gratis.
Køberens navn og kontaktoplysninger deles først, hvis I begge ønsker det.

    [ Se henvendelsen og svar ]

Hvorfor får du denne mail?
En konkret køber har bedt om at kontakte dig om denne bolig.
Vi sender kun henvendelser, der vedrører en bolig, du har til salg.

    [ Afmeld henvendelser fra Optata ]

Optata ApS · CVR [nummer] · [adresse]
```

**Ingen** købernavn, præcist beløb, telefon eller e-mail. **Ingen** pris på abonnementet i første mail — det er acquisition, ikke salg.

## B4 · Gratis-svar-flowet (mæglerens oplevelse)

```
1  Mail → token-landing (ingen login endnu)
   ┌────────────────────────────────────────────┐
   │ Verificeret køber til Strandvejen 142      │
   │ K-7F3A · ✓ VERIFICERET                     │
   │ 4,0–4,5 mio. kr. · Villa 140–180 m² · 3–6 m│
   │                                            │
   │ For at svare skal du bekræfte, at du er    │
   │ mægler for denne bolig. Det tager 30 sek.  │
   │ [ Bekræft med MitID Erhverv ]              │
   └────────────────────────────────────────────┘

2  MitID Erhverv → CVR matches mod udbuddets agent_org
   ✓ Match → gratis svar åbnes
   ✗ Mismatch → "Du er ikke registreret som mægler for denne bolig"

3  Gratis anonym dialog (relay, redaction aktiv)
   ┌────────────────────────────────────────────┐
   │ Dialog om Strandvejen 142 · anonym         │
   │ Køberen er verificeret. Kontaktoplysninger │
   │ udveksles, hvis I begge ønsker det.        │
   │ [ Skriv et svar ]                          │
   └────────────────────────────────────────────┘

4  Efter første svar (blød konvertering, ikke pres)
   "Der er 11 andre verificerede købere i 2900 Hellerup.
    Vil du se dem? [ Læs om adgang ]   [ Ikke nu ]"
```

**Guards:**
1. Gratis svar kræver **MitID Erhverv + CVR-match** til udbuddets mægler — ellers kan hvem som helst udgive sig for mægleren.
2. Kun **VERIFIED** køber må udløse invitation.
3. Maks. **1 invitation pr. bolig pr. 14 dage** til samme mægler-org (flere købere aggregeres: "3 verificerede købere til Strandvejen 142").
4. Afmeld suppression på **mægler-org**, ikke på enkeltbolig.
5. **Ingen salgspakke i M3** — handlen gennemføres af mægleren.

## B5 · Kontaktudveksling i M3 (anden vej end M1)

| | M1 (privat ejer) | M3 (mægler) |
|---|---|---|
| Udløser | Pakke accepteret + betaling | **Gensidigt samtykke + step-up** — ingen betaling |
| Guards | 6 (inkl. pakke + betaling) | **4**: gensidigt samtykke ∧ frisk step-up ∧ gyldig attest ∧ CVR-match på mægler |
| Hvem får data | De to parter | Køber ↔ mægler (ikke ejeren direkte) |
| Audit | `identity.revealed` | `identity.revealed` med `channel=AGENT` |

**Vigtigt:** Reveal-protokollen får en **variant**, ikke en undtagelse. Samme vault-indgang, samme audit, færre guards fordi der ikke er en pakke. Det skal skrives eksplicit i ADR-008, ellers bygger nogen den forkerte guard-sæt.

## B6 · Acceptkriterier

```
GIVEN CURIOS/QUALIFIED køber    THEN ingen invitation mulig, opgraderings-CTA vist
GIVEN VERIFIED + ACTIVE udbud   THEN invitation tilladt
GIVEN udbud SOLD/WITHDRAWN/STALE THEN ingen invitation, match skjult
GIVEN mægler uden CVR-match     THEN 403, intet køberdata vist
GIVEN 3 købere til samme bolig  THEN 1 invitation med antal, ikke 3
GIVEN mægler afmeldt            THEN ingen invitation, uanset matches
GIVEN M3-dialog                 THEN salgspakke tilbydes ALDRIG
GIVEN reveal i M3               THEN 4 guards, ingen betalingscheck, audit channel=AGENT
GIVEN invitationsmail           THEN ingen købernavn, præcist beløb eller kontakt
```
