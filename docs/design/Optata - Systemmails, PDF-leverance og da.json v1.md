# OPTATA — (a) Systemmails · (b) PDF-leverancen · (c) `da.json`

---

# DEL A — De resterende systemmails

## A0 · Fælles regler (gælder alle)

| Regel | Håndhævelse |
|---|---|
| Ingen persondata i mail | Aldrig navn, præcist beløb, telefon, e-mail, CPR |
| **Aldrig beskedindhold** | "Du har fået et svar" — ikke hvad der står |
| Ingen tracking-pixel | Kun logo som eksternt billede |
| Token | Engangs, scope-bundet, udløb 30 dage (dialog: 7 dage) |
| Quiet hours | 08–20 lokal tid |
| Frekvensloft | Ejer: 1 pr. 14 dage pr. adresse · Køber: maks. 3 pr. uge, samlede |
| Afmeld | Synlig i alle mails; virker på **adressen** (ejer) eller **formålet** (køber) |
| Plain text | Obligatorisk, fuldt forståelig alene |
| Footer | Optata ApS · CVR · fysisk adresse · kontakt |

---

## A1 · Verifikation godkendt (køber)

```
Emne:      Dit ønske er verificeret
Preheader: Ejere kan nu se det anonymt.

Dit ønske er verificeret.

Strandvejen 142, 2900 Hellerup
Villa · 140–180 m² · 4+ værelser

Ejere kan nu se dit ønske anonymt — med beløbsinterval, boligtype
og hvornår du vil flytte. Dit navn og dine kontaktoplysninger deles
kun, hvis I begge siger ja.

Verificeret til 12.06.2026

    [ Se mit ønske ]

Vi giver besked, hvis en ejer åbner en dialog.
```

---

## A2 · Verifikation udløber (køber, 30 og 7 dage)

```
Emne:      Din dokumentation udløber om 21 dage
Preheader: Forny den, hvis du stadig søger.

Din dokumentation udløber 12.06.2026.

Herefter bliver dit ønske ikke vist til ejere, før du har fornyet den.
Det tager få minutter at uploade en ny forhåndsgodkendelse.

    [ Forny dokumentation ]

Søger du ikke længere, kan du trække ønsket tilbage.

    [ Træk ønsket tilbage ]
```

**7-dages variant:** emne `Din dokumentation udløber om 7 dage`. Ingen tredje påmindelse.

---

## A3 · Verifikation udløbet (køber)

```
Emne:      Dit ønske er ikke længere verificeret
Preheader: Det vises ikke til ejere lige nu.

Din dokumentation er udløbet.

Dit ønske ligger stadig hos os, men det bliver ikke vist til ejere,
før du har uploadet en ny forhåndsgodkendelse.

    [ Forny dokumentation ]     [ Træk ønsket tilbage ]
```

---

## A4 · Ejer har åbnet dialog (køber)

```
Emne:      En ejer har åbnet en dialog
Preheader: Om Strandvejen 142. I er begge anonyme.

Ejeren af Strandvejen 142 har åbnet en anonym dialog.

I er begge anonyme. Kontaktoplysninger udveksles først, hvis I bliver
enige og begge accepterer.

    [ Åbn dialogen ]

Du bestemmer selv, om du vil svare.
```

---

## A5 · Nyt svar i dialog (begge parter)

```
Emne:      Du har fået et svar
Preheader: Dialog om Strandvejen 142.

Der er et nyt svar i din dialog om Strandvejen 142.

Vi gengiver ikke indholdet i mailen. Log ind for at læse det.

    [ Åbn dialogen ]

Samlesvar: Har du flere ulæste svar, sender vi én mail — ikke én pr. svar.
```

**Regel:** Maks. 1 pr. 6 timer pr. tråd. Ingen notifikation hvis bruger er aktiv i appen.

---

## A6 · Enighed bekræftet af modparten (begge)

```
Emne:      Modparten har bekræftet enighed
Preheader: Mangler kun din bekræftelse.

Modparten har bekræftet, at I er enige om pris og vilkår.

Pris            4.100.000 kr.
Overtagelse     01.09.2026

Når du også bekræfter, kan I få handlen gjort færdig.

    [ Se vilkårene ]

Du er ikke bundet af at bekræfte her. Det er enighed om at gå videre.
```

---

## A7 · Pakke accepteret, afventer modpart (begge)

```
Emne:      Handlen kan gøres færdig
Preheader: Vi mangler accept fra den anden part.

Du har accepteret pakken til at gennemføre handlen.

Vi mangler accept fra modparten. Der er ikke trukket betaling,
og ingen kontaktoplysninger er delt.

    [ Se status ]
```

---

## A8 · Kontaktoplysninger udvekslet (begge)

```
Emne:      I har nu hinandens kontaktoplysninger
Preheader: Advokaten kontakter jer inden for én hverdag.

I har begge accepteret, og kontaktoplysningerne er udvekslet.

Modpart:
    [Navn]
    [Telefon]
    [E-mail]

Advokaten er orienteret og kontakter jer inden for én hverdag.
Sagen og dokumenterne følges på Optata.

    [ Åbn sagen ]

Udvekslingen er registreret og kan ikke trækkes tilbage.
```

**Eneste mail der indeholder persondata** — afsendes kun efter `IDENTITY_REVEALED`, til de to parter, over TLS, uden tredjepart i kopi.

---

## A9 · Afmeld-kvittering (ejer)

```
Emne:      Du er afmeldt
Preheader: Vi kontakter dig ikke om denne adresse.

Du er afmeldt.

Vi sender ikke flere henvendelser om Strandvejen 142, 2900 Hellerup.

Registrerede interesser bliver liggende anonymt i vores ordrebog,
men du kontaktes ikke. Du kan altid slå adressen op igen på optata.dk.

Har du flere boliger, gælder afmeldingen kun denne adresse.
```

---

## A10 · Ejerside udløber / udløbet

```
Emne:      Din adgang udløber om 7 dage
Preheader: 12 uger på Strandvejen 142.

Din adgang til interesse på Strandvejen 142 udløber 04.12.2026.

Vil du fortsætte med at se interessen, kan du forny adgangen.
Registrerede interesser bliver liggende, men du kan ikke se dem
uden adgang.

    [ Forny adgang ]
```

---

## A11 · Analyse leveret (B2B)

```
Emne:      Områdeanalyse leveret — 2900 Hellerup
Preheader: Version 1 · 16.11.2026 · kildehenvisninger vedlagt.

Områdeanalysen for 2900 Hellerup er leveret.

Version         1
Leveret         16.11.2026
Omfang          Fakta · Bevægelse · Hverdag · Efterspørgsel
Revisioner      1 inkluderet, jf. aftalen

Hver påstand i analysen har kilde og dato. Metoden og forbeholdene
står i afsnit 2.

    [ Åbn analysen ]

Faktura fremsendes separat med jeres reference [reference].
```

---

## A12 · Acceptkriterier for mails

```
GIVEN hvilken som helst mail undtagen A8
      THEN ingen navn, telefon, e-mail eller præcist beløb i indhold
GIVEN dialog-mail                THEN intet beskedindhold gengives
GIVEN 5 ulæste svar samme tråd   THEN 1 mail pr. 6 timer, ikke 5
GIVEN kl. 23                     THEN kø til 08:00
GIVEN afmeldt adresse            THEN ingen ejer-mail, uanset hændelse
GIVEN token udløbet              THEN "Linket er udløbet. Slå adressen op igen."
GIVEN A8 afsendt                 THEN audit-log med grant_id + begge samtykker
GIVEN plain text alene           THEN fuldt forståelig og handlingsbar
```

---

# DEL B — PDF-leverancen: områdeanalysen

**Formål:** Et dokument der kan ligge i et kreditudvalg eller en bestyrelse. Ikke en salgsbrochure.

## B1 · Format og typografi

| Element | Specifikation |
|---|---|
| Format | A4 stående, 210×297 mm |
| Margener | Top 24 · Bund 22 · Yder 20 · Indbinding 24 mm |
| Grid | 12 kolonner, 4 mm gutter |
| Brødtekst | Inter 10,5 pt / 15 pt leading |
| Overskrifter | Newsreader 22 / 16 / 12 pt |
| Tal og ID | IBM Plex Mono 9,5 pt, tabular-nums |
| Metadata/kilder | Inter 8,5 pt, Skifer |
| Farve | Blæk på hvid. Rav kun til markering. Mose/Sand til status |
| Sidetal | Plex Mono 8,5 pt, yderkant |
| Løber | Område · version · dato (Skifer 8 pt) |

**Print-regel:** Ingen store farveflader. Dokumentet skal være læsbart i sort/hvid udskrift — status formidles med **tekst + ikon**, ikke farve alene.

---

## B2 · Sidestruktur (14–18 sider)

```
1   Forside
2   Resumé (én side, beslutningsklar)
3   Metode, kilder og forbehold
4–6 Fakta — boligmasse, ejerformer, priser, demografi
7–9 Bevægelse — vedtaget / på vej / stoppet
10  Hverdag — institutioner, indkøb, transport
11  Efterspørgsel — ordrebogen (aggregeret)
12  Gap-analyse
13  Konklusion og usikkerhed
14+ Bilag A: Claims med kildehenvisninger
    Bilag B: Datakvalitet og dækning
    Bilag C: Ordliste og metodeversioner
```

---

## B3 · Forside

```
                    ▢·  OPTATA



                    Områdeanalyse
                    2900 Hellerup


                    Fakta · Bevægelse · Hverdag · Efterspørgsel



                    Version 1
                    Leveret 16.11.2026
                    Udarbejdet til [Kundenavn], reference [ref]


                    ─────────────────────────────────────────
                    Fortroligt · Må ikke videredistribueres
                    Vandmærke: [modtager-id] · [org-id]
```

**Spec:** Wordmark stakket, 32 mm bredt. Titel Newsreader 32 pt. Resten Inter 10 pt. Parcel-mærket som vandmærke i 8 % opacity, 120 mm, centreret nederst.

---

## B4 · Resumé (side 2) — den side der læses

```
Resumé

Boligmasse          4.212 boliger · 44 % ejerlejlighed · 15 % andel
Prisniveau          2,8–4,6 mio. kr. (2024-vurderinger)
Flytteaktivitet     3,1 % årligt (3-årigt gennemsnit, tinglyste handler)

Bevægelse           3 vedtagne planer · 1 under anlæg · 1 stoppet
                    Størst: Lokalplan 214, 80 etageboliger, vedtaget 12.03.2026

Efterspørgsel       47 verificerede købere følger området
                    Primært ejerlejlighed 90–120 m², 3,0–3,5 mio. kr.
                    Verifikationsgrad 11 % · datagrundlag MEDIUM

Gap                 Ejerlejlighed 90–120 m² i 3,0–3,5 mio.:
                    62 verificerede · 11 årligt udbud · coverage 0,18

Væsentligste usikkerhed
                    Vurderinger er fra 2024. To celler skjult (k<5).
                    Efterspørgsel er et øjebliksbillede, ikke en forpligtelse.
```

**Regel:** Resuméet må **ikke** indeholde en anbefaling. Kun observationer med tal og usikkerhed.

---

## B5 · Metode, kilder og forbehold (side 3)

```
Metode

Datakilder
    BBR — Bygnings- og Boligregistret, hentet 16.11.2026
    DAR — Danmarks Adresseregister, hentet 16.11.2026
    Matriklen — hentet 14.11.2026
    Ejendomsvurderingen — 2024-vurderinger, offentliggjort 2025
    Tingbogen — overdragelser 2023–2026, hentet 14.11.2026
    Planregistre — kommunale lokalplaner, manuelt kurateret 12.11.2026
    Danmarks Statistik — befolkning og flytninger, Q3 2026
    Medier — licenserede uddrag, [leverandør]
    Optata ordrebog — verificerede ønsker, rullende 3 måneder

Verifikation af efterspørgsel
    Kun ønsker med dokumenteret købeevne fra bank eller realkredit
    medregnes. Identitet bekræftet med MitID. Dokumentation udløber
    efter 90 dage og nedgraderes automatisk.

Anonymisering
    Efterspørgsel vises aggregeret. Celler med færre end 5 registrerede
    skjules. Totaler afrundes til nærmeste 5. Komplementær suppression
    anvendes. Ingen enkeltpersoner kan identificeres.

Forbehold
    DEMAND_NOT_COMMITTED  Verificeret købeevne er ikke købsforpligtelse
    GEO_SUBSTITUTION      Købere kan acceptere tilstødende områder
    PRICE_ELASTICITY      Efterspørgsel målt ved nuværende prisniveau
    VUR_LAG               Vurderinger forsinket; suppleret med tinglyste handler
    K_SUPPRESSION         En eller flere celler skjult; totaler afrundet
    TIME_WINDOW           Øjebliksbillede med 3-måneders rullende vindue

Versioner
    Profil v1 · Model [version] · Prompt [version] · Metode v3
```

---

## B6 · Bevægelse-laget (side 7–9)

Hver påstand som række med **status, dato og klikbar kilde**:

```
VEDTAGET                                    12.03.2026
Lokalplan 214 — 80 etageboliger, maks. 5 etager
Kilde: Kommunens planregister, sagsnr. 2024-0214  ↗

UNDER ANLÆG                                 04.01.2026
Cykelsti langs Amagerbrogade, etape 2
Kilde: Kommunens vejregister  ↗

STOPPET                                     22.09.2025
Udvidelse af [institution] — projekt trukket tilbage
Kilde: Kommunalbestyrelsens referat, pkt. 118  ↗
```

**Regler:**
- `RYGTE` indgår **aldrig** i dette lag.
- Ingen påstand uden kilde og dato — heller ikke i PDF.
- Citat max 200 tegn i bilag A, ikke i hovedteksten.

---

## B7 · Gap-analysen (side 12)

```
Gap-analyse
Ejerlejlighed · 90–120 m² · 3,0–3,5 mio. kr. · horisont 3–6 måneder

Verificeret efterspørgsel        62
Boligmasse i segmentet          418
Årligt udbud (3,1 % omsætning)   13
Coverage ratio                  0,21
Absorption                      29 måneder
Datagrundlag                    MEDIUM

Fortolkning
    Det årlige udbud i segmentet dækker 21 % af den registrerede,
    verificerede efterspørgsel. Ved uændret udbud ville det tage
    29 måneder at optage den nuværende efterspørgsel.

    Dette er en observation af et mismatch — ikke en anbefaling
    om at bygge, og ikke en prognose for afsætning.

Usikkerhed
    To tilstødende budgetceller er skjult (k<5). Efterspørgslen
    kan substituere til Gentofte og Charlottenlund. Nybyggeri
    prissættes typisk over eksisterende masse i segmentet.
```

**Layout:** Vandret søjlegraf i Blæk/Sten med Rav-markering. Ingen 3D, ingen farvekodning uden tekstlabel.

---

## B8 · Bilag A — claims med proveniens

Tabel, én række pr. påstand:

| ID | Subject | Status | Dato | Kilde | Confidence |
|---|---|---|---|---|---|
| C-001 | Lokalplan 214 | VEDTAGET | 12.03.2026 | Planregister 2024-0214 | 0,92 |
| C-002 | Cykelsti etape 2 | UNDER_ANLÆG | 04.01.2026 | Vejregister | 0,88 |

Med kort citat (≤200 tegn) og fuld URL under hver række. **Dette bilag er det, der gør analysen reviderbar.**

---

## B9 · Bilag B — datakvalitet

```
Dækning pr. register
    BBR       99,4 %      DAR      100 %      Matrikel   98,1 %
    VUR       94,2 %      EJF       71,0 %    Plan       manuelt kurateret

Kvalitetsflag
    VUR_FORSINKET       2024-vurderinger, ikke 2026
    BBR_UNVERIFIED      38 boliger med usikkert areal
    PLAN_MANUAL         Kurateret 12.11.2026, ikke automatiseret

Karantæne
    14 poster afvist ved validering, ikke medregnet i statistik
```

**Regel:** Usikkerhed vises, ikke skjules. Det er et salgsargument over for en bank.

---

## B10 · Produktion og sikkerhed

| Krav | Implementering |
|---|---|
| Vandmærke | Modtager-id + org-id i sidefod på **alle** sider + 8 % parcel-mærke |
| Versionering | Ny version ved revision; gammel bevares uændret |
| Ingen persondata | Automatisk scanning af PDF-tekstlag før levering (CI-gate) |
| Godkendelse | Kan ikke genereres før `profile.review_state = APPROVED` |
| Metadata | PDF-metadata: title, version, genereret-dato, model_version |
| Tilgængelighed | Tagget PDF, læserækkefølge, alt-tekst på grafik |
| Filnavn | `optata_analyse_2900-hellerup_v1_2026-11-16.pdf` |

---

# DEL C — `apps/web/i18n/da.json`

```json
{
  "common": {
    "appName": "Optata",
    "loading": "Henter…",
    "retry": "Prøv igen",
    "save": "Gem",
    "cancel": "Annuller",
    "close": "Luk",
    "back": "Tilbage",
    "next": "Videre",
    "confirm": "Bekræft",
    "yes": "Ja",
    "no": "Nej",
    "optional": "valgfrit",
    "readMore": "Læs mere",
    "contactUs": "Kontakt os",
    "source": "Kilde",
    "updated": "Opdateret {date}",
    "version": "Version {version}",
    "verifiedUntil": "Verificeret til {date}",
    "validUntil": "Gyldig til {date}",
    "expiresInDays": "Udløber om {days} dage",
    "currency": "{amount} kr.",
    "budgetBand": "{min}–{max} mio. kr.",
    "squareMeters": "{value} m²",
    "rooms": "{count} værelser",
    "dwellingCount": "{count} boliger",
    "dataDisclaimer": "Data fra BBR, Danmarks Adresseregister, Matriklen og Ejendomsvurderingen. Opdateret {date}. Felter markeret med ● er ikke verificeret af registeret."
  },

  "nav": {
    "areas": "Områder",
    "howItWorks": "Sådan virker det",
    "professionals": "Til professionelle",
    "myOrder": "Mit ønske",
    "login": "Log ind",
    "logout": "Log ud"
  },

  "home": {
    "hero": {
      "title": "Hvor vil du bo?",
      "searchPlaceholder": "Søg på område, postnummer eller adresse",
      "subtitle": "Markedet begynder med det, du ønsker. Ikke med det, der tilfældigvis er til salg."
    },
    "areasNow": {
      "title": "Tre områder lige nu",
      "meta": "{dwellings} boliger · {plans} planer vedtaget"
    },
    "ownerEntry": {
      "title": "Bor du allerede der?",
      "body": "Se, om der er registreret verificeret interesse på din adresse. Du vælger selv, om du vil svare.",
      "cta": "Slå din adresse op"
    },
    "howItWorks": {
      "title": "Sådan virker det",
      "step1Title": "Du registrerer, hvor du vil bo",
      "step1Body": "Område eller adresse, boligtype, budget og hvornår.",
      "step2Title": "Du dokumenterer din købeevne",
      "step2Body": "En forhåndsgodkendelse fra din bank. Det tager få minutter.",
      "step3Title": "Ejeren ser det anonymt",
      "step3Body": "Dit navn og dine kontaktoplysninger deles først, hvis I begge siger ja."
    },
    "professionals": {
      "title": "Til professionelle",
      "body": "Områdeanalyser og efterspørgselsdata til udviklere, banker og mæglere. Hver påstand har kilde og dato."
    }
  },

  "area": {
    "tabs": {
      "facts": "Fakta",
      "movement": "Bevægelse",
      "everyday": "Hverdag",
      "demand": "Efterspørgsel"
    },
    "facts": {
      "stock": "Boligmasse",
      "ownership": "Ejerformer",
      "builtYear": "Opført",
      "valuation": "Vurdering",
      "valuationNote": "{year}-vurderinger, offentliggjort {published}"
    },
    "movement": {
      "empty": "Ingen vedtagne planer eller byggesager registreret i området.",
      "status": {
        "VEDTAGET": "Vedtaget",
        "FORESLAET": "Foreslået",
        "UNDER_BYGNING": "Under anlæg",
        "STOPPET": "Stoppet"
      }
    },
    "everyday": {
      "schools": "Skoler",
      "daycare": "Dagtilbud",
      "groceries": "Dagligvarer",
      "transport": "Transport",
      "withinMeters": "{count} inden for {meters} m"
    },
    "demand": {
      "summary": "{count} verificerede købere følger dette område.",
      "detail": "De søger primært {type} på {size} i intervallet {band}.",
      "empty": "Ingen verificerede købere følger dette område endnu.",
      "emptyCta": "Vær den første",
      "suppressed": "For få registrerede ønsker til at vise dette uden at enkeltpersoner kan genkendes."
    },
    "followCta": "Følg området — få besked, når noget matcher"
  },

  "property": {
    "valuation": "Vurdering",
    "landValue": "Grundværdi",
    "matrikel": "Matrikel",
    "localPlan": "Lokalplan",
    "noPlanChanges": "Ingen vedtagne ændringer",
    "intentBuyer": "Jeg vil bo her",
    "intentOwner": "Jeg bor her",
    "qualityFlag": "Ikke verificeret af registeret"
  },

  "order": {
    "form": {
      "title": "Hvor vil du bo?",
      "type": "Boligtype",
      "sizeLabel": "Størrelse",
      "sizeMin": "{value} m² eller mere",
      "roomsMin": "{count} værelser eller flere",
      "budget": "Budget",
      "budgetMax": "Op til {amount} kr.",
      "horizon": "Hvornår",
      "email": "Din e-mail",
      "submit": "Registrer mit ønske",
      "privacyNote": "Vi sender et link, så du kan komme tilbage. Ingen reklamer."
    },
    "horizon": {
      "0-3M": "Inden 3 måneder",
      "3-6M": "Inden 3–6 måneder",
      "6-12M": "Inden 6–12 måneder",
      "12M+": "Om et år eller mere"
    },
    "receipt": {
      "title": "Dit ønske er registreret.",
      "body": "Det er endnu ikke verificeret. Ejere ser kun ønsker med dokumenteret købeevne.",
      "upgradeCta": "Gør mit ønske verificeret",
      "later": "Senere"
    },
    "level": {
      "CURIOS": "Registreret",
      "QUALIFIED": "Kvalificeret",
      "VERIFIED": "Verificeret"
    },
    "status": {
      "ACTIVE": "Aktivt",
      "PAUSED": "Sat på pause",
      "MATCHED": "Matchet",
      "IN_DIALOG": "I dialog",
      "AGREED": "Enige",
      "WITHDRAWN": "Trukket tilbage",
      "EXPIRED": "Udløbet"
    },
    "mine": {
      "title": "Mit ønske",
      "awaitingOwner": "Ejeren har set dit ønske. Afventer svar.",
      "noMatch": "Dit ønske matcher ingen boliger lige nu. Vi giver besked, når det ændrer sig.",
      "pause": "Pause",
      "withdraw": "Træk ønsket tilbage",
      "erase": "Slet mine data",
      "edit": "Redigér ønske",
      "renew": "Forny dokumentation"
    }
  },

  "identity": {
    "mitidTitle": "Bekræft, at det er dig.",
    "mitidBody": "Vi bruger MitID til at sikre, at hvert ønske kommer fra en virkelig person. Vi gemmer ikke dit CPR-nummer.",
    "mitidCta": "Fortsæt med MitID",
    "stepUpTitle": "Bekræft med MitID for at fortsætte.",
    "stepUpBody": "Det kræver en ny bekræftelse, fordi handlingen deler eller viser følsomme oplysninger."
  },

  "verification": {
    "title": "Dokumentér din købeevne.",
    "body": "Upload din forhåndsgodkendelse fra bank eller realkredit. Vi tjekker den inden for én hverdag.",
    "requirementsTitle": "Krav til dokumentet",
    "requirement1": "Udstedt af bank eller realkreditinstitut",
    "requirement2": "Dit navn, dato og godkendt beløb",
    "requirement3": "Gyldig i mindst 30 dage",
    "upload": "Upload dokument",
    "requestBank": "Anmod min bank",
    "retentionNote": "Dokumentet slettes 90 dage efter gennemgang. Ejere ser kun beløbsintervallet.",
    "pending": "Vi gennemgår din dokumentation. Typisk inden for én hverdag. Du får besked, når det er gjort.",
    "approved": "Dit ønske er verificeret.",
    "approvedBody": "Ejere kan nu se det anonymt — med beløbsinterval, boligtype og hvornår du vil flytte. Dit navn og dine kontaktoplysninger deles kun, hvis I begge siger ja.",
    "expiringSoon": "Din dokumentation udløber om {days} dage. Forny den, hvis du stadig søger — ellers bliver ønsket ikke vist til ejere.",
    "expired": "Din dokumentation er udløbet. Forny den for at blive vist igen.",
    "rejected": "Vi kunne ikke godkende dokumentet. {reason}"
  },

  "owner": {
    "verifyTitle": "Bekræft, at du ejer boligen.",
    "verifyBody": "Vi tjekker det mod de offentlige registre. Det tager få sekunder. Vi gemmer ikke dit CPR-nummer.",
    "verifyCta": "Bekræft med MitID",
    "andelsTitle": "Din bolig er en andelsbolig.",
    "andelsBody": "Ejerfortegnelsen viser foreningen, ikke den enkelte andelshaver. Upload dit andelsbevis eller en bekræftelse fra administrator. Vi gennemgår den inden for to hverdage.",
    "interestTitle": "Verificeret interesse på {address}",
    "interestCount": "{count} registrerede interesser på din bolig.",
    "proof": {
      "buyer": "Køber",
      "budget": "Købeevne",
      "documented": "Dokumenteret",
      "validUntil": "Gyldig til",
      "horizon": "Horisont",
      "wish": "Ønske"
    },
    "proofNote": "Køberen er identificeret med MitID og har dokumenteret købeevne. Ingen kontaktoplysninger udveksles, før I begge accepterer.",
    "openDialog": "Åbn anonym dialog",
    "decline": "Afvis",
    "unsubscribe": "Afmeld fremtidige henvendelser på denne adresse",
    "noInterest": "Der er ikke registreret verificeret interesse på din adresse.",
    "notifyMe": "Giv mig besked",
    "declineAll": "Nej tak",
    "pass": {
      "title": "Interesse på din adresse",
      "subtitle": "12 ugers adgang · {price} kr.",
      "includes": "Du ser:",
      "item1": "Hvor mange verificerede købere der følger din adresse",
      "item2": "Deres beløbsintervaller og boligønsker",
      "item3": "Hvornår de vil flytte",
      "item4": "Udviklingen over tid",
      "anonymityNote": "Alt er anonymt. Du vælger selv, om du vil åbne en dialog.",
      "buy": "Køb adgang",
      "withdrawal": "14 dages fortrydelsesret. Adgangen åbnes med det samme, hvis du accepterer.",
      "waiver": "Jeg accepterer, at adgangen åbnes straks.",
      "expired": "Din adgang er udløbet. Forny for at se interessen igen.",
      "renew": "Forny adgang"
    },
    "unsubscribed": {
      "title": "Du er afmeldt.",
      "body": "Vi sender ikke flere henvendelser om {address}. Registrerede interesser bliver liggende anonymt, men du kontaktes ikke.",
      "note": "Du kan altid slå adressen op igen på optata.dk."
    }
  },

  "dialog": {
    "title": "Dialog om {address}",
    "anonymityBanner": "I er begge anonyme. Køberen er identificeret med MitID og har dokumenteret købeevne. Kontaktoplysninger udveksles først, når I er enige og begge accepterer.",
    "placeholder": "Skriv en besked",
    "redactionNote": "Beskeder med telefonnummer, e-mail eller adresse sendes ikke.",
    "redacted": "Beskeden blev ikke sendt. Den indeholder kontaktoplysninger. Dem udveksler vi automatisk, når I er enige.",
    "empty": "Dialogen er åben. Skriv, når du er klar.",
    "aborted": "Dialogen er lukket.",
    "agreeCta": "Vi er enige",
    "continueCta": "Fortsæt dialogen"
  },

  "deal": {
    "agreeTitle": "Er I enige?",
    "price": "Pris",
    "takeover": "Overtagelse",
    "otherTerms": "Øvrige vilkår",
    "termsFromDialog": "Som beskrevet i dialogen",
    "agreeNote": "Når I begge bekræfter, kan I få handlen gjort færdig.",
    "notBinding": "Du er ikke bundet af at bekræfte her. Det er enighed om at gå videre.",
    "awaitingOther": "Vi mangler accept fra den anden part."
  },

  "package": {
    "title": "Gør handlen færdig.",
    "intro": "I er enige. Vi sørger for det praktiske — sammen med en advokat.",
    "item1": "Købsaftale og skøde",
    "item2": "Tinglysning",
    "item3": "Refusionsopgørelse",
    "item4": "Tilstandsrapport og elinstallationsrapport",
    "item5": "Ejerskifteforsikring",
    "item6": "Håndtering af fortrydelsesfrist",
    "priceNote": "Fast pris {price} kr. Uafhængigt af boligens pris.",
    "paymentNote": "Betaling sker, når I accepterer — ikke som andel af salget.",
    "accept": "Accepter og fortsæt",
    "notNow": "Ikke nu",
    "revealTitle": "Udveksl kontaktoplysninger.",
    "revealBody": "Når I begge accepterer, deler vi navn, telefon og e-mail med hinanden. Det kan ikke trækkes tilbage, når det er sket.",
    "revealConsent": "Jeg accepterer, at mine kontaktoplysninger deles med modparten.",
    "revealConfirm": "Bekræft med MitID",
    "revealedTitle": "I har nu hinandens kontaktoplysninger.",
    "revealedBody": "Advokaten er orienteret og kontakter jer inden for én hverdag. Sagen følges her.",
    "openCase": "Åbn sagen"
  },

  "agent": {
    "title": "Verificerede købere i {area}",
    "summary": "{count} verificerede købere · eksklusiv adgang til postnummeret",
    "note": "Alle er identificeret med MitID og har dokumenteret købeevne. Kontaktoplysninger udleveres ikke. Dialog foregår anonymt her på platformen.",
    "openDialog": "Åbn dialog",
    "empty": "Ingen verificerede købere i dette postnummer lige nu.",
    "exclusiveNote": "Én mægler pr. postnummer. Køberne følger postnummeret.",
    "expired": "Dit abonnement er udløbet."
  },

  "analysis": {
    "title": "Områdeanalyse",
    "scope": "Omfang",
    "delivered": "Leveret",
    "revisions": "{count} revision inkluderet, jf. aftalen",
    "methodNote": "Hver påstand i analysen har kilde og dato. Metoden og forbeholdene står i afsnit 2.",
    "open": "Åbn analysen",
    "notApproved": "Analysen er ikke gennemgået endnu.",
    "reference": "Jeres reference {reference}"
  },

  "gap": {
    "title": "Gap-analyse",
    "verifiedDemand": "Verificeret efterspørgsel",
    "stock": "Boligmasse i segmentet",
    "annualSupply": "Årligt udbud",
    "coverage": "Coverage ratio",
    "absorption": "Absorption",
    "absorptionValue": "{months} måneder",
    "confidence": "Datagrundlag",
    "interpretation": "Fortolkning",
    "notRecommendation": "Dette er en observation af et mismatch — ikke en anbefaling om at bygge, og ikke en prognose for afsætning.",
    "insufficient": "For få registrerede ønsker til at beregne dette segment."
  },

  "empty": {
    "noOrdersInArea": "Ingen verificerede købere følger dette område endnu.",
    "noInterestOnAddress": "Der er ikke registreret verificeret interesse på din adresse.",
    "noPlans": "Ingen vedtagne planer eller byggesager registreret i området.",
    "noValuation": "Vurderinger for {year} er endnu ikke offentliggjort. Seneste: {lastYear}.",
    "noMatches": "Dit ønske matcher ingen boliger lige nu. Vi giver besked, når det ændrer sig.",
    "noMessages": "Dialogen er åben. Skriv, når du er klar.",
    "dataUnavailable": "Vi kan ikke hente registerdata lige nu. Prøv igen om lidt.",
    "linkExpired": "Linket er udløbet. Slå din adresse op igen."
  },

  "errors": {
    "ORDER_ALREADY_ACTIVE": "Du har allerede et ønske på denne adresse. Vil du redigere det?",
    "OWNERSHIP_NOT_VERIFIED": "Vi kunne ikke bekræfte, at du ejer boligen. Upload dokumentation, så tjekker vi det.",
    "VERIFICATION_EXPIRED": "Din dokumentation er udløbet. Forny den for at blive vist igen.",
    "MISSING_CONSENT": "Vi mangler accept fra den anden part. Kontaktoplysninger deles først, når I begge accepterer.",
    "STEP_UP_REQUIRED": "Bekræft med MitID for at fortsætte.",
    "REVEAL_BLOCKED": "Kontaktoplysninger kan ikke udveksles endnu.",
    "MESSAGE_REDACTED": "Beskeden indeholder kontaktoplysninger og blev ikke sendt.",
    "SUBSCRIPTION_EXPIRED": "Din adgang er udløbet. Forny for at se interessen igen.",
    "PROFILE_NOT_APPROVED": "Analysen er ikke gennemgået endnu.",
    "K_ANONYMITY_BLOCKED": "For få registrerede ønsker til at vise dette uden at enkeltpersoner kan genkendes.",
    "RATE_LIMITED": "Vent et øjeblik, og prøv igen.",
    "EAN_REQUIRED": "Faktura til offentlige kunder kræver et EAN-nummer.",
    "SCOPE_INCOMPLETE": "Aftalens omfang og vilkår skal accepteres, før analysen kan bestilles.",
    "REVISION_NOT_ACCEPTED": "Yderligere revision kræver accept af timeprisen.",
    "TOO_MANY_DIMENSIONS": "For mange filtre til at vise data anonymt. Fjern et filter.",
    "GENERIC": "Noget gik galt. Vi har registreret det. Prøv igen, eller kontakt os."
  },

  "footer": {
    "company": "Optata ApS · CVR {cvr}",
    "address": "{street}, {zip} {city}",
    "privacy": "Privatliv",
    "terms": "Vilkår",
    "dataProcessing": "Sådan behandler vi data",
    "whyThisMessage": "Derfor får du denne mail",
    "contact": "Kontakt"
  },

  "a11y": {
    "logoAlt": "Optata",
    "parcelMarkAlt": "Optata mærke",
    "verifiedIcon": "Verificeret",
    "pendingIcon": "Afventer gennemgang",
    "expiredIcon": "Udløbet",
    "qualityFlagIcon": "Ikke verificeret af registeret",
    "openSource": "Åbn kilde",
    "skipToContent": "Spring til indhold"
  }
}
```

**Regler for filen:**
- Ingen hardcodede tekster i komponenter — CI-lint fanger dansk strenglitteral i `.tsx`.
- Pladsholdere i `{snake}`-form; ingen string-sammenkædning i UI.
- Nye nøgler kræver PR med DK-review (copy er en del af produktet, ikke pynt).
- `errors.*` mapper 1:1 til `Error.code` i OpenAPI — ingen opfundne koder.

---

## Hvor vi står

Tekst, mails, PDF og i18n er nu konsistente med brandet og juraen: **mærket er et stempel, teksten er en kvittering, mailen er en invitation uden pres, og PDF'en er et dokument med proveniens.** UA-teamet kan bygge uden at opfinde copy, og designeren kan tegne uden at opfinde tone.

*Næste skridt kan være (a) de sidste manglende skærme i designsystemet (mæglerens lead-liste, analysebestilling, Min side/data-rettigheder), (b) en samlet `docs/design/`-pakke så designer og UA-team har ét referencepunkt, eller (c) tilbage til kode: S3-backloggen med MitID, vault og attest — den sprint der gør "verificeret" til virkelighed.*
