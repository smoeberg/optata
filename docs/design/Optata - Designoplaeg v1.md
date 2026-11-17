# OPTATA — Designoplæg: visuel identitet, forside og proces

Tre svar først, derefter oplægget.

**Har I en identitet?** Nej — ikke i det materiale, jeg har set. Der er et navn, en positionering og en arkitektur, men ingen logo, palette eller skrift. Det skal laves, og det haster faktisk: de to skærme, der tjener pengene (adresserapporten og det anonyme bevis), kræver et troværdigt udtryk for at konvertere.

**Hvem er forsiden til?** Køberen — men ikke af den grund, du tror. Ejeren betaler 1.495 kr., men **køberen skaber aktivet**. Uden tæthed har ejeren intet at købe og mægleren intet at abonnere på. Forsiden skal derfor maksimere ordrebogen. Løsningen er ikke to forsider, men **ét søgefelt med to intentioner**.

**Design før kode?** Ja. Tre artefakter, fem dage, ingen repo-ændring før I har reageret.

---

## 1. Brandets bærende idé

**Optata er latin for "det ønskede"** (af *optare* — at ønske, at vælge). Det er ikke et opdigtet navn; det er præcis forretningen. Ordrebogen er det ønskede, før det findes.

Det giver en brandhistorie, de fleste boligbrands ikke har — og den skal styre designet:

| Lag | Følelse | Udtryk |
|---|---|---|
| **Drømmen** — hero, billeder, sprog | Ro, længsel, mulighed | Luft, varmt papir, redaktionel serif, store billeder |
| **Beviset** — data, attester, tal | Sikkerhed, præcision, autoritet | Struktur, tabeller, monospace-tal, kilde + dato |

**I sælger drømme med kvittering.** Det er differentieringen — ikke drømmen alene (det gør alle portaler) og ikke data alene (det gør DinGeo).

**Brandord:** *Rolig. Præcis. Nordisk. Diskret. Aldrig sælgende.*

**Den hårde regel:** Drømmen må aldrig love, hvad beviset ikke kan holde. Ingen "find dit drømmehjem" over en tabel med tre ordrer. Tomme tilstande skal være ærlige og smukke.

---

## 2. Visuel identitet

### 2.1 Logo

**Wordmark som primært mærke.** "Optata" i en redaktionel serif, let løftet bogstavafstand. Seriffer signalerer autoritet og arv — det modsatte af en portal.

**Sekundært mærke: "parcellen".** En abstrakt matrikel-grundrids — en firkant med et lille hak og en prik. Det læses som *et sted, der er udpeget*, ikke som et hus. Bruges som favicon, kortmarkør, app-ikon og vandmærke på leverancer.

```
OPTATA        ← wordmark, serif, tracking +2%
▢·            ← parcellen: grundrids + punkt
```

**Bevidst fravalgt:** hustage, nøgler, hjerter, "SOLGT"-skilte, smilende familier, regnbue-pins. Det er mægler-estetik, og I er ikke mæglere.

### 2.2 Farver

Blæk, varmt papir, sten — og én varm accent. Ingen blå tech-gradient.

| Rolle | Navn | Hex | Brug |
|---|---|---|---|
| Primær tekst | **Blæk** | `#14181B` | Brødtekst, wordmark |
| Baggrund | **Papir** | `#F7F5F1` | Standardflade (varm, ikke hvid) |
| Sekundær flade | **Sten** | `#E8E4DC` | Kort, tabeller, skel |
| Dæmpet tekst | **Skifer** | `#5C6670` | Metadata, kilder, datoer |
| Accent | **Rav** | `#B4643C` | CTA, aktiv tilstand, fokus |
| Verificeret | **Mose** | `#3F6B52` | VERIFIED-badge, gyldig attest |
| Afventer | **Sand** | `#9A8C6E` | PENDING, til review |
| Udløbet/afvist | **Tegl** | `#9B3B32` | Kun fejl og udløb — aldrig dekorativt |

**Kontrast:** Blæk/Papir ≈ 14:1. Rav/Papir ≈ 4,6:1 → AA til normal tekst. Mose bruges med hvid tekst eller som kant + ikon, aldrig som lille farvet tekst alene.

**Ingen mørk tilstand i v1.** Papir-tonen *er* identiteten.

### 2.3 Typografi

Tre skrifttyper, alle open source — **nul licensomkostning**, kommerciel brug uden bekymring.

| Rolle | Skrift | Hvorfor |
|---|---|---|
| Display / redaktionel | **Newsreader** (variable) | Alvorlig, redaktionel serif. Avis, ikke annonce. |
| UI / brødtekst | **Inter** | Neutral, ekstremt læsbar, fuldt dansk tegnsæt |
| Data / ID / tal | **IBM Plex Mono** | Attest-ID, beløb, datoer, kildehenvisninger |

```
Hero:       40 → 72px   Newsreader 400, line-height 1.05
Sektion:    28 → 40px   Newsreader 400
Kort-titel: 20px        Inter 500
Brød:       16 → 17px   Inter 400, line-height 1.6
Metadata:   13px        Inter 400, Skifer
Tal/ID:     14px        Plex Mono, tabular-nums
```

**Regel:** Alle beløb, datoer og tæthedstal i **Plex Mono med tabular-nums**. Det får data til at ligne data — og det er hele troværdigheden.

### 2.4 Billedsprog

- **Steder, ikke mennesker.** Morgenlys på en vej, en gårdhave, et vindue, en kystlinje, en stationsperron. Genkendeligt dansk.
- **Ingen mennesker i hero** — køberen skal kunne indsætte sig selv.
- Naturligt lys, lav mætning, let korn. Aldrig HDR, drone-glans eller vidvinkel.
- **Kortet er et designelement.** Matrikelgrænser i Sten, udpeget parcel i Rav. Smukt nok til at være hero-baggrund.

### 2.5 Tone of voice

| ✅ Sådan | ❌ Ikke sådan |
|---|---|
| "Hvor vil du bo?" | "Find dit drømmehjem nu!" |
| "Der er registreret verificeret interesse på din adresse." | "Nogen vil købe dit hus!!" |
| "Ingen data endnu for dette område." | "Spændende ting på vej!" |
| "Kilde: Lokalplan 214, vedtaget 12.03.2026" | "Alt tyder på vækst i området" |
| "Du bestemmer, om du vil svare." | "Skynd dig — køberen venter" |

Ingen udråbstegn. Ingen kunstig knaphed. Ingen "gratis vurdering" som lokkemad — det bryder også §2.3 i forretningsplanen.

---

## 3. Forsiden: køberen primær, ejeren elegant med

### 3.1 Beslutningen

Køberen er primær, fordi **tæthed er flaskehalsen** (25 verificerede pr. 1.000 boliger). Ejeren kan ikke betale for noget, der ikke findes.

Men ejeren må ikke begraves. Løsningen: **adresseopslaget er fælles indgang** — samme handling, to intentioner.

```
                 ┌──────────────────────────┐
                 │    Hvor vil du bo?       │
                 │ [ område eller adresse ] │
                 └────────────┬─────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
    Søger på OMRÅDE                     Søger på ADRESSE
    → områderapport                     → adresserapport
    → "Følg området"                    → ┌────────────────┐
                                          │ Jeg vil bo her │
                                          │ Jeg bor her    │
                                          └────────────────┘
```

Ejeren når sin indgang via **"Jeg bor her"** på adressekortet. Ingen separat forside, ingen MitID før der er noget at beskytte.

### 3.2 Wireframe

```
┌──────────────────────────────────────────────────────────┐
│  OPTATA                        Områder  Sådan virker det │  ← ingen login
├──────────────────────────────────────────────────────────┤
│                                                          │
│              Hvor vil du bo?                             │  ← Newsreader 72
│                                                          │
│   ┌────────────────────────────────────────────────┐     │
│   │ Søg på område, postnummer eller adresse        │     │  ← Rav fokus
│   └────────────────────────────────────────────────┘     │
│                                                          │
│   Markedet begynder med det, du ønsker.                  │
│   Ikke med det, der tilfældigvis er til salg.            │
│                                                          │
│              [ kort: matrikelgrænser, dæmpet ]           │
├──────────────────────────────────────────────────────────┤
│  Tre områder lige nu                                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐            │
│  │ Amager     │ │ Nordvest   │ │ Valby      │            │
│  │ 4.212 bol. │ │ 6.880 bol. │ │ 5.104 bol. │            │
│  │ 3 planer   │ │ 1 plan     │ │ 2 planer   │            │
│  └────────────┘ └────────────┘ └────────────┘            │
├──────────────────────────────────────────────────────────┤
│  Bor du allerede der?                                    │  ← ejer-indgang
│  Se om der er verificeret interesse på din adresse.      │
│  [ Slå din adresse op ]                                  │
├──────────────────────────────────────────────────────────┤
│  Sådan virker det                                        │
│  1. Du registrerer, hvor du vil bo                       │
│  2. Du dokumenterer din købeevne                         │
│  3. Ejeren ser det anonymt — og vælger selv              │
├──────────────────────────────────────────────────────────┤
│  Til professionelle                                      │
│  Områdeanalyser og efterspørgselsdata.   [ Kontakt ]     │
└──────────────────────────────────────────────────────────┘
```

**Bevidst fravalgt i hero:** MitID-knap, "opret bruger", pris, store tællere, cookie-wall ud over det nødvendige. P0-porten (≥8 % konvertering) afhænger af det.

---

## 4. De to skærme, der faktisk tjener penge

Forsiden skaffer trafik. Disse to skaffer indtægt — **design dem først**.

### A. Adressekortet (anonym, zone A)

BBR, vurdering, matrikel, plan, område. Kvalitetsflag hvor data er usikkert. To CTA'er: *"Jeg vil bo her"* / *"Jeg bor her"*.

### B. Det anonyme bevis (ejeren, zone B)

Skærmen der udløser A2 og 1.495 kr.:

```
┌──────────────────────────────────────────────┐
│  Verificeret interesse på                    │
│  Strandvejen 142, 2900 Hellerup              │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  K-7F3A                  ✓ VERIFICERET │  │  ← Mose
│  │                                        │  │
│  │  Købeevne      4,0–4,5 mio. kr.        │  │  ← Plex Mono
│  │  Dokumenteret  12.03.2026              │  │
│  │  Gyldig til    12.06.2026              │  │
│  │  Horisont      3–6 måneder             │  │
│  │  Ønske         Villa, 140–180 m², 4+ v │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  Køberen er identificeret med MitID og har   │
│  dokumenteret købeevne. Ingen kontaktoplys-  │
│  ninger udveksles, før I begge accepterer.   │
│                                              │
│  [ Åbn anonym dialog ]   [ Afvis ]           │  ← Rav / neutral
│  Afmeld fremtidige henvendelser på adressen  │  ← altid synlig
└──────────────────────────────────────────────┘
```

**Designkrav:** Ingen navne. Ingen præcise beløb. Ingen billeder af personer. Ingen pres. Afmeld skal være lige så synlig som accept — det er både etik og konvertering.

---

## 5. Design tokens (klar til repo, når I har godkendt)

```css
:root {
  /* Farve */
  --ink:      #14181B;
  --paper:    #F7F5F1;
  --stone:    #E8E4DC;
  --slate:    #5C6670;
  --amber:    #B4643C;
  --moss:     #3F6B52;
  --sand:     #9A8C6E;
  --brick:    #9B3B32;

  /* Typografi */
  --font-display: "Newsreader", Georgia, serif;
  --font-ui:      "Inter", system-ui, sans-serif;
  --font-data:    "IBM Plex Mono", monospace;

  /* Rum — 4px base, luftig */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;
  --space-4: 16px;  --space-6: 24px;  --space-8: 32px;
  --space-12: 48px; --space-16: 64px; --space-24: 96px;

  /* Form */
  --radius-sm: 2px;  --radius-md: 4px;  --radius-lg: 8px;
  --border: 1px solid var(--stone);
  --shadow-card: 0 1px 2px rgba(20,24,27,.04);

  /* Bevægelse — rolig, aldrig legende */
  --ease: cubic-bezier(.2,.6,.2,1);
  --dur-fast: 120ms;  --dur: 200ms;
}
```

**Formprincip:** Lav radius (2–8px), hårde kanter, tynde linjer, næsten ingen skygger. Nordisk præcision, ikke SaaS-bobler.

---

## 6. Proces: design før kode

**Ja — og det er billigt.** Fem dage, tre artefakter, ingen repo-ændring før godkendelse.

| Dag | Leverance | I reagerer på |
|---|---|---|
| 1 | **Moodboard + wordmark + parcel-mærke** (2 retninger) | Er udtrykket rigtigt? |
| 2–3 | **Forside-hero + adressekort** (desktop + mobil) | Konverterer det? Er det troværdigt? |
| 4 | **Det anonyme bevis** (ejerens skærm) | Ville jeg svare på det her? |
| 5 | **Tokens + komponentark** (badge, kort, tabel, CTA, tom tilstand) | Kan UA-teamet bygge det konsistent? |

**Derefter:** tokens og komponenter lægges i repo som `apps/web/design-system/`, og UA-teamet bygger inden for det — samme princip som kontrakterne: **designsystemet er kontrakten, komponenterne er output.**

**Hvad jeg ikke anbefaler:** at designe hele sitet nu. Forside + to pengeskærme er nok til at validere udtrykket og nå P0/P1. Resten følger, når tætheden er bevist.

---

## 7. Fem ting, der ville ødelægge det

1. **Blå gradient + rundede kort + "AI-powered"** — gør jer til endnu en startup, ikke en markedsinfrastruktur.
2. **Mægler-ikonografi** (nøgler, hustage, SOLGT) — I er ikke mæglere, og det er hele pointen.
3. **MitID eller login i hero** — halverer konverteringen og dermed tætheden.
4. **Optimistiske tomme tilstande** — "spændende ting på vej" underminerer troværdigheden, som er produktet.
5. **Præcise køberbeløb til ejeren** — bryder anonymiteten og øger re-identifikationsrisikoen. Intervaller, altid.

---

## Konklusion

**Identitet:** Wordmark i redaktionel serif + parcel-mærke. Blæk, varmt papir, sten, rav. Newsreader + Inter + Plex Mono. Steder, ikke mennesker.

**Forside:** Køberen primær ("Hvor vil du bo?"), ejeren med via adresseopslagets "Jeg bor her". Ingen login i hero.

**Proces:** Fem dage, tre artefakter — moodboard/wordmark, forside + adressekort, det anonyme bevis. Tokens i repo bagefter.

Det samler sig i én sætning, der kan styre alt designarbejde:

> **Optata skal ligne noget, man kan stole på med den største handel i sit liv — og samtidig føles som begyndelsen på noget, man ønsker sig.**

*Vil du have, at jeg (a) skriver de to moodboard-retninger som konkrete designbeskrivelser med referenceæstetik, (b) laver det fulde komponentark (badge, kort, tabel, CTA, tom tilstand) som specifikation, eller (c) skriver designbriefet som et dokument, UA-teamet eller en designer kan arbejde direkte ud fra?*

 automatisk `EXPIRED`, når datoen er passeret — håndhævet i komponenten, ikke i den enkelte skærm.

---

## B2 · ProofCard (det anonyme bevis)

Ejerens skærm. Den der udløser A2 og 1.495 kr.

```
┌────────────────────────────────────────────┐
│  K-7F3A                    [✓ VERIFICERET] │  ← Plex Mono 16 / badge
│  ─────────────────────────────────────────  │  ← 1px Sten
│  Købeevne        4,0–4,5 mio. kr.          │  ← label Inter 13 Skifer
│  Dokumenteret    12.03.2026                │     værdi Plex Mono 14 Blæk
│  Gyldig til      12.06.2026                │
│  Horisont        3–6 måneder               │
│  Ønske           Villa · 140–180 m² · 4+ v │
└────────────────────────────────────────────┘

Spec:  bg Papir · border 1px Sten · radius 4px · padding 24px
       label-kolonne 140px fast · værdier tabular-nums
       skygge: --shadow-card (næsten usynlig)
```

**Forbud i komponenten:** navn, præcist beløb, foto af person, kontaktinfo, "skynd dig"-tekst. Alt andet end ovenstående felter afvises af komponentens props-type.

**Tilstande:** `valid` · `expiring_soon` (<30 dage, Sand-kant + forny-CTA til køberen) · `expired` (Tegl-kant, handlinger deaktiveret).

---

## B3 · ClaimRow (påstand med kilde)

Agentens output. Troværdigheden står og falder her.

```
Lokalplan 214 vedtaget                          [VEDTAGET]
80 etageboliger, max 5 etager
Kilde: Kommunens planregister · 12.03.2026 · ↗
```

| Felt | Typografi | Farve |
|---|---|---|
| Subject | Inter 500 16px | Blæk |
| Value | Inter 400 15px | Blæk 80 % |
| Status-badge | Inter 500 11px | Mose (VEDTAGET) / Sand-700 (FORESLÅET) / Skifer (STOPPET) |
| Kilde + dato | Inter 400 13px | Skifer, understregning ved hover |

**Regler:**
- Kilde og dato er **obligatoriske props** — komponenten kan ikke renders uden.
- `RYGTE` må ikke kunne indsættes i Bevægelse-laget (type-niveau).
- Citat vises ved klik, max 200 tegn, med link til kilde.
- Ingen påstand uden klikbar kilde. Ingen "alt tyder på".

---

## B4 · DataTable (registerdata)

```
Spec:  header  Inter 500 12px uppercase tracking +0.06em Skifer
       række   Inter 400 14px Blæk · højde 44px
       tal     Plex Mono 14px tabular-nums, højrestillet
       skel    1px Sten mellem rækker, ingen lodrette linjer
       zebra   ingen — brug luft og skel
       hover   Sten 40 % baggrund
       flag    kvalitetsflag som lille Sand-prik + tooltip
```

**Regel:** Usikre data vises **med flag**, aldrig skjules. `VUR_FORSINKET` og `BBR_UNVERIFIED` er synlige — det er et salgsargument, ikke en svaghed.

---

## B5 · CTA

| Variant | Fyld | Tekst | Brug |
|---|---|---|---|
| Primary | Amber-700 | Hvid | Én pr. skærm: "Åbn anonym dialog", "Følg området" |
| Secondary | Transparent | Blæk, 1px Blæk-kant | "Afvis", "Se rapport" |
| Quiet | Ingen | Skifer, understregning | "Afmeld", "Læs mere" |
| Destructive | Transparent | Tegl, 1px Tegl-kant | "Træk ordre tilbage" |

```
Spec:  height 44px (mobil 48) · padding 0 20px · radius 2px
       Inter 500 15px · ingen skygge · ingen gradient
       hover: fyld mørknes 8 % · focus: 2px Rav-offset-ring
       disabled: 40 % opacity, cursor not-allowed
```

**Regler:**
- **Én Primary pr. skærm.** Ellers konkurrerer drømmen med beviset.
- Afmeld/afvis skal være **synlig og lige stor** som accept — aldrig Quiet-gemt væk.
- Ingen pres-sprog. "Åbn anonym dialog", ikke "Svar før det er for sent".

---

## B6 · EmptyState (den sværeste komponent)

Her dør troværdigheden oftest.

| Situation | Tekst | Handling |
|---|---|---|
| Ingen ordrer i område | "Ingen verificerede købere følger dette område endnu." | "Vær den første" |
| Ingen interesse på adresse | "Der er ikke registreret verificeret interesse på din adresse." | "Få besked, hvis der kommer" |
| Ingen claims | "Ingen vedtagne planer eller byggesager registreret i dette område." | Ingen opdigtet aktivitet |
| Data forsinket | "Vurderinger for 2026 er endnu ikke offentliggjort." | Vis sidste kendte + dato |

```
Spec:  centreret · max-width 420px · padding 64px 0
       titel Newsreader 24px Blæk
       brød Inter 15px Skifer
       ikon: parcel-mærket i Sten, 32px — aldrig en illustration
```

**Forbud:** "Spændende ting på vej!", "Kom snart tilbage", tomme grafer med opdagede tal, skeleton der aldrig fyldes. **En ærlig tom tilstand er et troværdighedssignal.**

---

## B7 · SearchField (forsidens vigtigste element)

```
Spec:  height 56px · radius 4px · border 1px Sten · bg hvid
       placeholder Inter 400 16px Skifer
       focus: 2px Amber-700 ring, ingen glow
       autocomplete: DAR-adresser + områder, dropdown Sten-kant
       ingen login, ingen cookie-wall foran
```

**Regel:** Én indgang, to intentioner. Træff på adresse → adressekort med "Jeg vil bo her" / "Jeg bor her". Træff på område → områderapport.

---

## B8 · MapMarker (parcel-mærket)

| Tilstand | Udtryk |
|---|---|
| Neutral | Sten-fyld, 0,5px Blæk-kant |
| Udpeget | Amber-700-fyld + hvid prik |
| Verificeret interesse | Mose-kant + prik |
| Klynge | Cirkel med antal i Plex Mono |

**Regel:** Markører viser **aldrig** persondata. Kun ejendomsgeometri og aggregeret antal (k≥5).

---

## B9 · Tilgængelighedskrav (alle komponenter)

- Kontrast ≥4,5:1 til normal tekst, ≥3:1 til stor tekst og UI-kant
- Fokus-ring altid synlig, aldrig `outline: none`
- Status formidles med **ikon + tekst**, ikke farve alene
- Tastatur: alle handlinger nås med Tab, aktiveres med Enter/Space
- Skærmlæser: attester læses som sammenhængende sætning, ikke som løsrevne tal
- Dansk tegnsæt (æøå) verificeret i alle tre skrifttyper
- Reduceret bevægelse respekteres (`prefers-reduced-motion`)

---

# DEL C — Designbrief

**Dokument:** `DESIGN-BRIEF-001` · lægges i `/docs/design/` · gives til designer eller UA-team

---

## C1 · Opgaven

Design Optatas visuelle identitet og de tre skærme, der afgør forretningen:
1. **Forside** (skaffer tæthed)
2. **Adressekort** (fælles indgang for køber og ejer)
3. **Anonymt bevis** (udløser ejerrespons og betaling)

Alt andet design følger efter, når disse tre er godkendt.

## C2 · Hvad Optata er

En platform der **inverterer boligmarkedet**: fra at købe det, der tilfældigvis er til salg, til at registrere det, man ønsker — og lade ejere og udviklere reagere på verificeret efterspørgsel.

Vi er **ikke** en boligportal, ikke en mægler, ikke en annonceplatform. Vi er markedsinfrastruktur.

## C3 · Brandets bærende idé

**Optata er latin for "det ønskede".** Navnet er forretningen.

| Lag | Følelse | Udtryk |
|---|---|---|
| Drømmen | Ro, længsel, mulighed | Luft, varmt papir, serif, store billeder |
| Beviset | Sikkerhed, præcision | Struktur, tabeller, monospace-tal, kilde + dato |

> **Vi sælger drømme med kvittering.**

**Den hårde regel:** Varmen må aldrig røre beviset. Så snart en skærm viser en attest, et beløb eller en kilde, skifter den til Matriklen-temperaturen.

## C4 · Målgrupper og hvad de skal føle

| Målgruppe | Skærm | Skal føle |
|---|---|---|
| Køber | Forside, rapport | "Her kan jeg sige, hvad jeg vil — uden at blive solgt til" |
| Ejer | Anonymt bevis | "Det her er seriøst, og jeg bestemmer selv" |
| Mægler | Lead-liste | "Det her kan jeg ikke selv bygge" |
| Developer/bank | Analyse, Demand Pro | "Det her kan jeg lægge i et kreditudvalg" |

## C5 · Leverancer

| # | Leverance | Format |
|---|---|---|
| 1 | Wordmark + parcel-mærke | SVG, sort/hvid + farve, favicon |
| 2 | Farvepalette med kontrastmåling | Tokens + dokumenterede ratios |
| 3 | Typografiskala | Tre skrifttyper, alle vægte, dansk tegnsæt |
| 4 | Forside | Desktop 1440 + mobil 390 |
| 5 | Adressekort | Desktop + mobil, begge intentioner |
| 6 | Anonymt bevis | Desktop + mobil, alle tilstande |
| 7 | Komponentark | Badge, ProofCard, ClaimRow, DataTable, CTA, EmptyState, SearchField, MapMarker |
| 8 | Tokens | CSS custom properties, klar til repo |

## C6 · Rammer (ufravigelige)

**Skal:**
- Nordisk, seriøs, elegant. Luft som designelement.
- Papir-tone som standardflade — ikke hvid, ikke mørk tilstand
- Tre open source-skrifttyper: Newsreader, Inter, IBM Plex Mono
- Alle tal i Plex Mono med tabular-nums
- Kilde + dato på enhver påstand
- Dansk tegnsæt verificeret
- WCAG AA på alle komponenter

**Må ikke:**
- Blå gradient, rundede SaaS-kort, "AI-powered"-æstetik
- Mægler-ikonografi: nøgler, hustage, SOLGT-skilte, hjerter
- Mennesker i hero — køberen skal indsætte sig selv
- Login eller MitID i hero
- Præcise køberbeløb til ejeren — kun intervaller
- Pres-sprog, udråbstegn, kunstig knaphed
- Optimistiske tomme tilstande
- Stock-fotos af smilende familier

## C7 · Acceptkriterier

```
Forside:      Ingen login synlig · søgefelt over fold · én Primary CTA
              Mobil: søgefelt nås uden scroll
              Kontrastmåling vedlagt for alle tekst/flade-kombinationer

Adressekort:  To intentioner synlige ("Jeg vil bo her" / "Jeg bor her")
              Kvalitetsflag vist hvor data er usikre
              Ingen persondata synlig for anonym bruger

Anonymt bevis: Ingen navn, præcist beløb eller kontaktinfo
              Gyldighedsdato synlig · badge skifter automatisk ved udløb
              Afmeld lige så synlig som accept
              Læses forståeligt af en 65-årig uden teknisk erfaring

Komponenter:  Alle tilstande tegnet (default, hover, focus, disabled, error, empty)
              Status formidlet med ikon + tekst, ikke farve alene
              Tokens brugt konsekvent — ingen hardcodede værdier
```

## C8 · Proces

| Dag | Leverance | Review |
|---|---|---|
| 1 | Moodboard + wordmark, begge retninger | Vælg retning |
| 2–3 | Forside + adressekort | Konverterer det? |
| 4 | Anonymt bevis, alle tilstande | Ville jeg svare på det? |
| 5 | Komponentark + tokens | Kan UA bygge konsistent? |

**Ingen repo-ændring før godkendelse.** Derefter lægges tokens og komponenter i `apps/web/design-system/` og behandles som kontrakt: **designsystemet er specifikationen, komponenterne er output.**

## C9 · Hvad succes ser ud som

En ejer på 62 år åbner en mail om interesse på sin bolig, ser det anonyme bevis og tænker: *"Det her er troværdigt — og jeg bestemmer selv."*

En køber på 34 år lander på forsiden og tænker: *"Endelig et sted, hvor jeg kan sige, hvad jeg faktisk vil have."*

En udvikler åbner en områdeanalyse og tænker: *"Det her kan jeg tage med til bestyrelsen."*

**Alle tre skal være sande samtidig.** Det er hele designopgaven.

---

## Næste skridt

Vælg retning — **Morgenlyset på forbrugersider, Matriklen på bevis og B2B** er min anbefaling. Så er briefet klar til at blive givet videre, og de tre skærme kan tegnes.

*Vil du have, at jeg (a) skriver de faktiske hero- og skærmtekster på dansk (alle tilstande, tomme tilstande, fejlbeskeder, mails), (b) laver SVG-specifikationen for wordmark og parcel-mærke, eller (c) udarbejder notifikationsmailen til ejeren — den der skal bære både jura, anonymitet og drøm?*
