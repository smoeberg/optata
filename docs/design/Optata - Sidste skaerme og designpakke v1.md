# OPTATA — (a) De sidste skærme · (b) `docs/design/`-pakken · (c) S3-backlog

---

# DEL A — De tre manglende skærme

## A1 · Mæglerens lead-liste

**Formål:** Bevise at abonnementet er noget, mægleren ikke selv kan bygge. Ingen eksport, ingen kontaktdata.

```
┌──────────────────────────────────────────────────────────────┐
│  ▢· OPTATA          2900 Hellerup        [MitID Erhverv ▾]   │
├──────────────────────────────────────────────────────────────┤
│  Verificerede købere i 2900 Hellerup                         │
│  12 verificerede · eksklusiv adgang · fornyes 04.05.2027     │
│                                                              │
│  Filter: [Boligtype ▾] [Budget ▾] [Horisont ▾]               │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ K-7F3A   ✓ VERIFICERET      Gyldig til 12.06.2026      │  │
│  │ 4,0–4,5 mio. kr. · Villa · 140–180 m² · 4+ v · 3–6 mdr.│  │
│  │ Matcher 3 boliger i postnummeret      [ Åbn dialog ]   │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ K-2B91   ✓ VERIFICERET      Gyldig til 28.04.2026      │  │
│  │ 3,5–4,0 mio. kr. · Villa · 120–160 m² · 4+ v · 0–3 mdr.│  │
│  │ Matcher 5 boliger                     [ Åbn dialog ]   │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  Alle er identificeret med MitID og har dokumenteret         │
│  købeevne. Kontaktoplysninger udleveres ikke.                │
│  Én mægler pr. postnummer. Køberne følger postnummeret.      │
└──────────────────────────────────────────────────────────────┘
```

| Tilstand | Udtryk |
|---|---|
| Ingen leads | "Ingen verificerede købere i dette postnummer lige nu." + tæthedstal + "Vi giver besked" |
| <5 leads i 2 mdr. | Intern kundesucces-opgave (churn-risiko), ikke synlig for mægleren |
| Attest udløber <30 dage | Sand-kant + "Dokumentation udløber snart" |
| Abonnement udløbet | Listen tom, forny-CTA, **RLS invalideret øjeblikkeligt** |

**Forbud:** CSV-eksport, navn, telefon, e-mail, præcist budget, køberens egen adresse, reveal-knap.
**Accept:** `GIVEN andet postnummer → tom liste (RLS)` · `GIVEN udløbet abonnement → tom inden 60 sek.` · `GIVEN reveal-forsøg → 403`.

---

## A2 · Analysebestilling (B2B)

**Formål:** Låse scope, så konsulentmarginen ikke ædes. EAN og reference indsamles **her**, ikke ved fakturering.

```
Bestil områdeanalyse

1  Område        [ 2900 Hellerup ▾ ]  4.212 boliger
2  Omfang        ☑ Fakta  ☑ Bevægelse  ☑ Hverdag  ☑ Efterspørgsel
3  Levering      10 hverdage fra accept · PDF + web · 1 revision inkluderet
4  Fakturering   Virksomhed [CVR]  EAN [13 cifre]  Reference [indkøbsordre]
5  Vilkår        Pris 85.000 kr. + moms 21.250 = 106.250 kr. · netto 30
                 Yderligere revision: 4.500 kr./time
                 ☐ Jeg accepterer omfang og vilkår (v1.2)

                                              [ Bestil analyse ]
```

| Felt | Validering |
|---|---|
| EAN | 13 cifre, påkrævet for offentlig kunde |
| Reference | Fritekst, påkrævet — ellers afvises fakturaen af kundens system |
| Vilkår | Checkbox + `terms_version` gemmes i samtykke-ledger |
| Efterspørgselslag | Deaktiveret hvis området har <5 verificerede (k-anonymitet) |

**Efter bestilling:** statuslinje `ORDERED → SCOPED → GENERATING → IN_REVIEW → DELIVERED → ACCEPTED → INVOICED → PAID`, altid synlig for kunden. Ingen "vi arbejder på det" uden tilstand.

---

## A3 · Min side / data-rettigheder

**Formål:** GDPR som selvbetjening, ikke som supportmail. Det er også et tillidssignal.

```
Min side

Mit ønske            Strandvejen 142 · VERIFICeret til 12.06.2026
Dialoger             1 åben · 0 lukkede
Abonnementer         Ingen

Mine data
  [ Download mine data ]        JSON, øjeblikkelig
  [ Ret mit ønske ]
  [ Slet mine data ]            Sletter identitet og dokumentation.
                                Anonym historik bevares.

Samtykker
  Købsinteresse på adresse      Givet 12.03.2026 (v1.2)   [ Tilbagekald ]
  Behandling af bankbevis       Givet 12.03.2026 (v1.0)   [ Tilbagekald ]
  Dialog                        Givet 04.04.2026 (v1.1)   [ Tilbagekald ]

Sådan behandler vi data · Derfor får du mails · Kontakt
```

**Slet-dialog (ærlig, ikke skræmmende):**
```
Slet dine data?

Vi sletter dit navn, dine kontaktoplysninger, din dokumentation
og dine dialoger. Dit ønske fjernes fra ordrebogen.

Vi bevarer anonym historik (uden navn eller kontakt) og bogførings-
bilag, som vi er lovpligtigt forpligtet til at opbevare i 5 år.

Det kan ikke fortrydes.

              [ Slet mine data ]     [ Annuller ]
```

**Accept:** `GIVEN sletning → zone B væk, events pseudonyme, tombstone kan ikke mappes` · `GIVEN tilbagekaldelse → suppression øjeblikkelig, åben tråd ABORTED` · `GIVEN eksport → kun egne data, ingen andres`.

---

# DEL B — `docs/design/`-pakken

```
docs/design/
├─ README.md                 ← indgang, læses først
├─ DESIGN-BRIEF-001.md       ← opgave, rammer, acceptkriterier
├─ brand/
│  ├─ identity.md            ← wordmark, parcel-mærke, lockups, forbud
│  ├─ optata-wordmark.svg    ← outlines, ikke <text>
│  ├─ optata-mark.svg        ← streg + fyldt + monokrom
│  └─ favicon/               ← svg, 16, 32, 180
├─ foundations/
│  ├─ color.md               ← palette + kontrastmålinger
│  ├─ typography.md          ← Newsreader / Inter / Plex Mono, skala
│  ├─ spacing.md             ← 4px-base, luft som element
│  └─ tokens.css             ← single source of truth
├─ components/
│  ├─ badge.md               ← CURIOS/QUALIFIED/VERIFIED/udløbet
│  ├─ proof-card.md          ← det anonyme bevis, alle tilstande
│  ├─ claim-row.md           ← kilde+dato obligatorisk
│  ├─ data-table.md          ← tabular-nums, kvalitetsflag
│  ├─ cta.md                 ← én Primary pr. skærm
│  ├─ empty-state.md         ← ærlig tomhed
│  ├─ search-field.md        ← én indgang, to intentioner
│  └─ map-marker.md          ← aldrig persondata
├─ screens/
│  ├─ home.md                ← forside, desktop+mobil
│  ├─ property-card.md       ← adressekort, to intentioner
│  ├─ anonymous-proof.md     ← ejerens pengeskærm
│  ├─ agent-leads.md         ← mægler
│  ├─ analysis-order.md      ← B2B bestilling
│  └─ my-data.md             ← rettigheder
├─ voice/
│  ├─ tone.md                ← sprogprincipper, ordliste
│  ├─ emails/                ← A1–A12 + ejer-mail (html/txt)
│  └─ errors.md              ← kode → tekst, 1:1 med OpenAPI
├─ print/
│  └─ analysis-pdf.md        ← A4, grid, sidestruktur, vandmærke
└─ a11y.md                   ← AA-krav, tastatur, skærmlæser, æøå
```

**README.md (indhold):**

> **Læs i denne rækkefølge:** DESIGN-BRIEF → brand/identity → foundations → voice/tone → components → screens.
> **To temperaturer:** *Morgenlyset* (forside, rapport, drøm) og *Matriklen* (attest, data, B2B). Varmen må aldrig røre beviset.
> **Ufravigeligt:** ingen persondata i UI før reveal · kilde+dato på enhver påstand · tal i Plex Mono tabular-nums · afmeld lige så synlig som accept · ingen pres-sprog · WCAG AA.
> **Kontrakt:** `tokens.css` og komponent-specs er specifikationen. Kode er output. Afvigelse kræver DK-review.

**Leveranceregel:** Designeren leverer SVG + tokens + komponentark. UA-teamet implementerer **inden for** det — ingen opfundne farver, størrelser eller tekster. CI-lint fanger hardcodede værdier og dansk strenglitteral i `.tsx`.

---
