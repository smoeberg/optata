# OPTATA — Udbudsmatch (M3): integration, match og mæglerinvitation

Det er en rigtig udvidelse — og den løser et problem, vi har slås med hele vejen: **køberen får værdi dag ét, uden at en ejer skal reagere først.** Men den tilføjer også en ny datakilde, en ny match-retning og en ny juridisk grænse. Nedenfor er det bygget ind i arkitekturen uden at bryde invarianterne.

---

## 1. Hvad det ændrer — og hvad det ikke ændrer

**Det ændrer:** Ordrebogen kan nu matches mod *eksisterende udbud*, ikke kun mod skjult efterspørgsel. Køberen ser med det samme, om noget af det, der allerede er til salg, matcher ønsket. Det er en reel aktivering — og det gør P0 (tæthed) lettere, fordi køberen får noget igen med det samme.

**Det ændrer ikke:** Anonymiteten, verifikationen og moaten. Udbuddet er offentligt (zone A-lignende), men **køberen er stadig anonym**, og kontakten til mægleren går stadig via relay.

**Ny match-retning (M3):**

| Match | Fra → til | Udløser |
|---|---|---|
| M1 | Adresse-ordre → ejer | Ejer-notifikation (kun VERIFIED) |
| M2 | Område-ordre → boligmasse | Intern lead-liste, ingen kontakt |
| **M3 (ny)** | **Udbud → ordre** | **Køber-notifikation → invitation/dialog med mægler** |

**Vigtig regel:** M3 kontakter **køberen**, ikke ejeren. Ejeren har allerede en mægler — det er mægleren, der er modparten her.

---

## 2. Datakilden: Boligsiden er ikke en gratis kilde

Det skal siges klart, før der bygges: **Boligsiden er ejet af mæglerstanden** (EDC, Nybolig, home m.fl. via Dansk Ejendomsmæglerforening). At hente deres udbud systematisk uden aftale er et **databasebeskyttelses-brud** — præcis det, ADR og §9 forbyder. Og de er en potentiel konkurrent til jeres ordrebog.

**Tre veje, i prioriteret rækkefølge:**

| Vej | Beskrivelse | Realistisk |
|---|---|---|
| **A — Mægler-feed som del af abonnementet** | Mægleren giver jer deres udbud (XML/JSON-feed) som en del af Optata-abonnementet. De får ordrebogen, I får udbuddet. | **Bedst.** Ingen fjende, gensidig værdi, lovligt |
| **B — Kommerciel licensaftale med Boligsiden** | Betalt API/feed-adgang | Mulig, men de kan afslå (konkurrent) eller kræve vilkår der begrænser jer |
| **C — Andre licenserede kilder** | home, EDC, Nybolig direkte; eller en aggregator med rettigheder | Kræver flere aftaler, men spreder afhængigheden |

**Anbefaling:** Byg **adapter-rammen** nu (så I er klar), men **start med vej A** — mæglerens eget feed. Det vender fjenden til en leverandør og passer perfekt ind i "mægleren er kunde, ikke kanal". Boligsiden-aftalen forhandles parallelt, men **må ikke være en blocker for S1–S5**.

**Arkitekturkrav:** `listing_source`-adapter med licensfelt, kildehenvisning og rettigheds-flag — præcis som `source_document` i agenten. Ingen kilde uden `license_ref` må importeres.

---

## 3. Datamodel: `listing` (zone A+/B-grænse)

```sql
CREATE TABLE listing (
  listing_id      uuid PRIMARY KEY,
  source          text NOT NULL,          -- AGENT_FEED | BOLIGSIDEN | HOME | ...
  source_ref      text NOT NULL,          -- ekstern id
  license_ref     text NOT NULL,          -- 🔴 ingen import uden
  address_id      text,                   -- DAR-match, kan være NULL før geokodning
  bfe             text,
  area_id         text NOT NULL,
  street_id       text,                   -- til gade-scope
  municipality_id text,                   -- til kommune-scope
  agent_org_id    uuid,                   -- mæglerens CVR/org, hvis kendt
  attrs           jsonb NOT NULL,         -- type, areal, værelser, pris, etage
  asking_price    bigint,
  status          text NOT NULL,          -- ACTIVE | UNDER_OFFER | SOLD | WITHDRAWN
  listed_at       date NOT NULL,
  changed_at      timestamptz NOT NULL,
  valid_from      date NOT NULL,
  valid_to        date,                   -- bitemporal: prishistorik bevares
  recorded_at     timestamptz NOT NULL,
  UNIQUE (source, source_ref, recorded_at)
);
CREATE INDEX listing_area_ix   ON listing(area_id) WHERE status='ACTIVE';
CREATE INDEX listing_street_ix ON listing(street_id) WHERE status='ACTIVE';
CREATE INDEX listing_geom_gix  ON listing USING gist(geom);
```

**Bemærk:**
- Udbudsdata er **offentligt tilgængelige annoncer** → behandles som zone A, men **med licens**. Mæglerens kontaktoplysninger (hvis ikke offentlig) er zone B.
- **Bitemporal** også her: prishistorik og statusændringer er værdifulde (og en del af overvågningsproduktet).
- `SOLD`/`WITHDRAWN` skal propagere: et match mod en solgt bolig må ikke blive liggende.

---

## 4. Scope-udvidelse: kommune og gade

Ordren får to nye scopes, så den matcher det, køberen faktisk tænker i:

```
scope: AREA | ADDRESS | STREET | MUNICIPALITY
```

| Scope | Nøgle | Eksempel |
|---|---|---|
| MUNICIPALITY | `municipality_id` | "Jeg vil bo i Gentofte Kommune" |
| AREA | `area_id` (postnr/bydel) | "2900 Hellerup" |
| STREET | `street_id` | "Strandvejen" |
| ADDRESS | `address_id` | "Strandvejen 142" |

**Hierarki:** MUNICIPALITY ⊃ AREA ⊃ STREET ⊃ ADDRESS. Et udbud matches mod det **mest specifikke** scope, køberen har valgt. En kommune-ordre matcher alle udbud i kommunen; en gade-ordre kun den gade.

---

## 5. M3-match og flow

```
Nyt udbud (ACTIVE) ──→ M3-match mod aktive ordrer i scope
                          │  hard filters + score (samme model som M1/M2)
                          ▼
                  Køber notificeres: "Ny bolig matcher dit ønske"
                          │  køberen åbner udbuddet (zone A + licens)
                          ▼
              ┌───────────────────────────────────┐
              │ Er mægleren registreret på Optata? │
              └───────────────┬───────────────────┘
                     ja        │        nej
                     ▼         │        ▼
            [ Åbn anonym dialog ]   [ Send invitation til mægler ]
                     │                        │
                     ▼                        ▼
              Relay (som C5)          Mægler-invitation (mail)
                                              │  mægler klikker → MitID Erhverv
                                              ▼
                                      Registrering → anonym dialog
```

**To nye tilstande i ordren:** `LISTING_MATCHED` (udbud fundet) og `AGENT_INVITED` (invitation sendt, afventer mægler).

**Guards:**
1. M3-match kræver **aktiv ordre** (CURIOS må gerne se udbud, men **kun VERIFIED må kontakte mægler** — samme regel som ejer-siden).
2. Udbud skal være `ACTIVE` og `license_ref` gyldig.
3. Invitation til mægler kræver **VERIFIED** køber (ellers spam til mæglere).
4. Al dialog via relay — ingen direkte kontakt før enighed.

---

## 6. Mægler-invitationen (den nye acquisition-kanal)

Dette er en **vækstmekanisme**: hver gang en køber vil kontakte en uregistreret mægler, får mægleren en invitation — og ser samtidig, at der findes en verificeret køber, de ikke selv havde.

```
Emne:      En verificeret køber er interesseret i din bolig til salg
Preheader: Strandvejen 142 — anonym henvendelse via Optata.

Der er en verificeret køber til en bolig, du har til salg.

Strandvejen 142, 2900 Hellerup · 4.150.000 kr.

Køberen er identificeret med MitID og har dokumenteret købeevne.
Du kan se interessen anonymt og vælge, om du vil svare.

    [ Se interessen ]

Det er gratis at se og svare på denne henvendelse.
Vil du have adgang til alle verificerede købere i 2900 Hellerup,
kan du læse om abonnementet her.

    [ Afmeld henvendelser fra Optata ]
```

**Regler:**
- Ingen købernavn/beløb i mailen (samme som ejer-mailen).
- **Gratis at svare på den enkelte** — det er acquisition, ikke betaling. Abonnementet sælges bagefter.
- Afmeld synlig; suppression på mægler-org.
- Mægleren registrerer sig med **MitID Erhverv** → bliver til en lead i systemet → kan konverteres til abonnement.

**Forretningsgevinst:** I får mæglerens **udbud-feed** (vej A) og en **ny abonnent** i samme bevægelse. Det er den bedste måde at løse Boligsiden-problemet på: gør mægleren til leverandør i stedet for fjende.

---

## 7. Nye juridiske spørgsmål (til juristen, uge 6)

| # | Spørgsmål | Blokerer |
|---|---|---|
| **L32** 🔴 | Må vi importere og vise udbud fra **mæglerens eget feed** som del af abonnementet? Kræves særskilt databehandler-/licensaftale? | M3 |
| **L33** 🔴 | Er en **Boligsiden-licens** nødvendig, eller er mægler-feed tilstrækkeligt? Hvad er vores rettigheder ved videresalg i analyser? | M3 |
| **L34** 🔴 | Er **køber→mægler-invitation** formidling? Vi bringer en køber til en mægler med en bolig til salg — er det anderledes end køber→ejer? | M3/relay |
| **L35** | Må vi kontakte en **uregistreret mægler** på deres offentlige forretnings-e-mail med en konkret køberhenvendelse? Grundlag? | Invitation |
| **L36** | Kræver **pris- og statusdata** fra udbud attribution/kildevisning? Hvad skal stå ved hvert udbud? | UI |
| **L37** | Må vi bruge udbudsdata i **Demand Pro/gap-analyse** (aggregeret), eller kræver licensen særskilt vederlag? | B2B |

**L34 er den vigtige:** køber→mægler kan være *mindre* formidlingsagtigt end køber→ejer, fordi mægleren allerede er professionel formidler. Men det skal bekræftes — ikke antages.

---

## 8. Ny backlog: S6 (udbudsmatch) — indskudt før mægler-abonnement

**Omfang:** ~24 persondage · **Afhængigheder:** S5 (relay) · licensaftale (vej A) · L32–L37 besvaret

| ID | Issue | Est. | Ejer |
|---|---|---|---|
| S6-01 | `listing`-model + bitemporal + licensfelt | 2,0 | DE+DK |
| S6-02 | Adapter-ramme + **mægler-feed-adapter** (XML/JSON) | 3,0 | DE |
| S6-03 | Geokodning af udbud → DAR/adresse/vej/kommune | 2,0 | DE |
| S6-04 | Scope-udvidelse (STREET/MUNICIPALITY) + hierarki-match | 2,0 | FS+DE |
| S6-05 | **M3-match** + score + reason_codes | 2,0 | DE |
| S6-06 | Køber-notifikation "ny bolig matcher" + frekvensloft | 2,0 | FS+DK |
| S6-07 | Udbudsvisning (zone A + licens/attribution) | 2,0 | FS |
| S6-08 | **Mægler-invitation** + gratis-svar-flow + MitID Erhverv-onboarding | 3,0 | FS+DK |
| S6-09 | Status-propagering (SOLD/WITHDRAWN fjerner match) | 1,5 | DE |
| S6-10 | Guard-tests + fixtures (licens, VERIFIED-gate, sold-match) | 2,0 | DK |
| S6-11 | Metrics (match-rate, invitation→registrering) + runbook | 0,5 | DE |

**Acceptkriterier (uddrag):**
```
GIVEN udbud uden license_ref      THEN import afvist
GIVEN CURIOS-ordre                THEN ser udbud, men må IKKE kontakte mægler
GIVEN VERIFIED + ACTIVE udbud     THEN invitation/dialog tilladt
GIVEN udbud SOLD                  THEN match fjernet, ingen notifikation
GIVEN uregistreret mægler         THEN invitation med gratis-svar, ingen køberdata
GIVEN mægler afmeldt              THEN ingen invitation, uanset nye matches
GIVEN gade-ordre                  THEN kun udbud på den gade, ikke hele postnummeret
```

---

## 9. Hvad det gør ved forretningen (kort)

| Effekt | Vurdering |
|---|---|
| **Køberen får værdi dag ét** | ✅ Løser cold-start — P0 bliver lettere |
| **Mægleren bliver leverandør** | ✅ Løser Boligsiden-problemet uden fjende |
| **Ny acquisition-kanal** | ✅ Hver invitation er en potentiel abonnent |
| **Ekstra juridisk arbejde** | ⚠️ L32–L37 skal besvares før S6 |
| **Licensafhængighed** | ⚠️ Start med mægler-feed, ikke Boligsiden |

**Det ændrer ikke moaten:** ordrebogen er stadig aktivet. Udbuddet er en *trigger*, ikke produktet. Men det gør ordrebogen **mere værdifuld**, fordi den nu kan matches mod begge sider af markedet.

---

## Konklusion

Udbudsmatch (M3) er en **stærk udvidelse**, der løser cold-start og gør mægleren til leverandør i stedet for fjende. Men den kræver:

1. **Licensieret kilde** — start med mæglerens eget feed (vej A), ikke scraping af Boligsiden.
2. **Ny juridisk afklaring** — især L34 (køber→mægler = formidling?).
3. **VERIFIED-gate** — kun verificerede købere må kontakte mæglere, ellers bliver det spam.
4. **Anonymitet bevaret** — relay og gensidig afsløring gælder også her.

Byg adapter-rammen nu, men **lad ikke Boligsiden-aftalen blokere S1–S5**. Mægler-feedet er den hurtige, lovlige vej — og den gør mægleren til en del af løsningen.

*Vil du have, at jeg (a) skriver mægler-feed-adapterens specifikation (XML/JSON-format, felter, validering), (b) laver invitationsmailen + gratis-svar-flowet i fuld tekst, eller (c) opdaterer ARCHITECTURE.md og ADR'erne, så M3 og listing-modellen er indarbejdet?*
