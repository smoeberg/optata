# OPTATA — (a) Tekstdeck · (b) Mærke-specifikation · (c) Ejer-mailen

Alt på dansk, klar til brug. Teksterne er skrevet til at blive læst af en ejer på 62 og en udvikler på 45 — uden at nogen af dem føler sig solgt til.

---

# DEL A — Tekstdeck

## A1 · Sprogprincipper

| Regel | Eksempel |
|---|---|
| Sig hvad der sker, ikke hvad det betyder | "Der er registreret interesse på din adresse" — ikke "Din bolig er eftertragtet" |
| Ingen udråbstegn, ingen knaphed | Aldrig "skynd dig", "sidste chance", "kun i dag" |
| Tal er fakta, ikke salg | "3 verificerede købere" — ikke "masser af interesse!" |
| Ejeren bestemmer — sig det | "Du vælger selv, om du vil svare." |
| Tomhed er ærlig | "Ingen verificerede købere endnu." Ikke "spændende ting på vej" |
| Kilde og dato følger påstanden | Altid, også i UI-tekst |

**Ordliste (brug / brug ikke)**

| ✅ Brug | ❌ Undgå |
|---|---|
| ønske, ordre, registrere | lead, kunde, emne |
| verificeret, dokumenteret købeevne | godkendt kunde, seriøs køber |
| anonym dialog | chat med køber, kontakt køber |
| udveksle kontaktoplysninger | afsløre, låse op, frigive |
| interesse på din adresse | nogen vil købe dit hus |
| område, bolig, adresse | ejendom (i forbrugertekst), objekt |
| Du bestemmer selv | Vi hjælper dig videre |

---

## A2 · Forside

```
Hvor vil du bo?

[ Søg på område, postnummer eller adresse ]

Markedet begynder med det, du ønsker.
Ikke med det, der tilfældigvis er til salg.
```

**Sektion: Tre områder lige nu**
```
Amager          4.212 boliger · 3 planer vedtaget
Nordvest        6.880 boliger · 1 plan vedtaget
Valby           5.104 boliger · 2 planer vedtaget
```

**Sektion: Bor du allerede der?**
```
Se, om der er registreret verificeret interesse på din adresse.
Du vælger selv, om du vil svare.

[ Slå din adresse op ]
```

**Sektion: Sådan virker det**
```
1. Du registrerer, hvor du vil bo
   Område eller adresse, boligtype, budget og hvornår.

2. Du dokumenterer din købeevne
   En forhåndsgodkendelse fra din bank. Det tager få minutter.

3. Ejeren ser det anonymt
   Dit navn og dine kontaktoplysninger deles først, hvis I begge siger ja.
```

**Sektion: Til professionelle**
```
Områdeanalyser og efterspørgselsdata til udviklere, banker og mæglere.
Hver påstand har kilde og dato.

[ Kontakt os ]
```

**Footer**
```
Optata ApS · CVR [nummer] · [adresse]
Privatliv · Vilkår · Sådan behandler vi data · Kontakt
```

---

## A3 · Områderapport

```
Amager
4.212 boliger · 1.842 ejerlejligheder · 612 andelsboliger

Fakta · Bevægelse · Hverdag · Efterspørgsel
```

**Fakta**
```
Boligmasse        4.212
Ejerformer        Ejerlejlighed 44 % · Andel 15 % · Leje 41 %
Opført            1930–1960: 52 % · 1960–1990: 28 % · Efter 1990: 20 %
Vurdering         2,8–4,6 mio. kr. (2024-vurderinger, offentliggjort 2025)
```

**Bevægelse**
```
Lokalplan 214 vedtaget                            12.03.2026
80 etageboliger, maks. 5 etager
Kilde: Kommunens planregister

Cykelsti langs Amagerbrogade under anlæg          04.01.2026
Kilde: Kommunens vejregister
```

**Hverdag**
```
Skoler            6 folkeskoler · 3 privatskoler
Dagtilbud         14 institutioner
Dagligvarer       9 inden for 800 m
Transport         Metro 4 min. · Bus 6 linjer
```

**Efterspørgsel**
```
47 verificerede købere følger dette område.
De søger primært ejerlejligheder på 90–120 m² i intervallet 3,0–3,5 mio. kr.

[ Følg området ]
```

**Sticky CTA:** `Følg området — få besked, når noget matcher`

---

## A4 · Adressekort

```
Strandvejen 142, 2900 Hellerup
Villa · 164 m² · 5 værelser · Opført 1932 · Grund 712 m²

Vurdering         4.150.000 kr. (2024)
Grundværdi        2.400.000 kr.
Matrikel          7a, Hellerup By, Gentofte
Lokalplan         Ingen vedtagne ændringer

[ Jeg vil bo her ]     [ Jeg bor her ]
```

**Under kortet**
```
Data fra BBR, Danmarks Adresseregister, Matriklen og Ejendomsvurderingen.
Opdateret 16.11.2026. Felter markeret med ● er ikke verificeret af registeret.
```

---

## A5 · Ordre-flow

**Trin 1 — e-mail**
```
Hvor vil du bo?

Boligtype     [ Villa ▾ ]
Størrelse     [ 140 ] m² eller mere · [ 4 ] værelser eller flere
Budget        Op til [ 4.200.000 ] kr.
Hvornår       [ Inden 3–6 måneder ▾ ]

Din e-mail    [ dig@eksempel.dk ]

[ Registrer mit ønske ]

Vi sender et link, så du kan komme tilbage. Ingen reklamer.
```

**Kvittering**
```
Dit ønske er registreret.

Det er endnu ikke verificeret. Ejere ser kun ønsker med dokumenteret købeevne.

[ Gør mit ønske verificeret ]     [ Senere ]
```

**Trin 2 — MitID**
```
Bekræft, at det er dig.

Vi bruger MitID til at sikre, at hvert ønske kommer fra en virkelig person.
Vi gemmer ikke dit CPR-nummer.

[ Fortsæt med MitID ]
```

**Trin 3 — dokumenteret købeevne**
```
Dokumentér din købeevne.

Upload din forhåndsgodkendelse fra bank eller realkredit.
Vi tjekker den inden for én hverdag.

Krav til dokumentet:
· Udstedt af bank eller realkreditinstitut
· Dit navn, dato og godkendt beløb
· Gyldig i mindst 30 dage

[ Upload dokument ]     [ Anmod min bank ]

Dokumentet slettes 90 dage efter gennemgang. Ejere ser kun beløbsintervallet.
```

**Under gennemgang**
```
Vi gennemgår din dokumentation.
Typisk inden for én hverdag. Du får besked, når det er gjort.
```

**Godkendt**
```
Dit ønske er verificeret.

Ejere kan nu se det anonymt — med beløbsinterval, boligtype og hvornår du vil flytte.
Dit navn og dine kontaktoplysninger deles kun, hvis I begge siger ja.

Verificeret til 12.06.2026
```

---

## A6 · Min ordre

```
Mit ønske                        [ ✓ VERIFICERET ]

Strandvejen 142, 2900 Hellerup
Villa · 140–180 m² · 4+ værelser · Op til 4,2 mio. kr. · Inden 3–6 måneder

Verificeret til 12.06.2026
[ Forny dokumentation ]

Status: Ejeren har set dit ønske. Afventer svar.

[ Pause ]     [ Træk ønsket tilbage ]     [ Slet mine data ]
```

**Ved udløb om <30 dage**
```
Din dokumentation udløber om 21 dage.
Forny den, hvis du stadig søger — ellers bliver ønsket ikke vist til ejere.
```

---

## A7 · Anonym dialog

```
Dialog om Strandvejen 142

I er begge anonyme. Køberen er identificeret med MitID og har dokumenteret købeevne.
Kontaktoplysninger udveksles først, når I er enige og begge accepterer.

[ Skriv en besked ]

Beskeder med telefonnummer, e-mail eller adresse sendes ikke.
```

**Ved redaction**
```
Beskeden blev ikke sendt.
Den indeholder kontaktoplysninger. Dem udveksler vi automatisk, når I er enige.
```

**Enighed**
```
Er I enige?

Pris            4.100.000 kr.
Overtagelse     01.09.2026
Øvrige vilkår   Som beskrevet i dialogen

Når I begge bekræfter, kan I få handlen gjort færdig.

[ Vi er enige ]     [ Fortsæt dialogen ]
```

---

## A8 · Pakke og kontaktudveksling

```
Gør handlen færdig.

I er enige. Vi sørger for det praktiske — sammen med en advokat.

Købsaftale og skøde
Tinglysning
Refusionsopgørelse
Tilstandsrapport og elinstallationsrapport
Ejerskifteforsikring
Håndtering af fortrydelsesfrist

Fast pris 10.000 kr. Uafhængigt af boligens pris.
Betaling sker, når I accepterer — ikke som andel af salget.

[ Accepter og fortsæt ]     [ Ikke nu ]
```

**Samtykke**
```
Udveksl kontaktoplysninger.

Når I begge accepterer, deler vi navn, telefon og e-mail med hinanden.
Det kan ikke trækkes tilbage, når det er sket.

☐ Jeg accepterer, at mine kontaktoplysninger deles med modparten.

[ Bekræft med MitID ]
```

**Gennemført**
```
I har nu hinandens kontaktoplysninger.

Advokaten er orienteret og kontakter jer inden for én hverdag.
Sagen følges her.
```

---

## A9 · Ejerens skærme

**Ejerskabsverifikation**
```
Bekræft, at du ejer boligen.

Vi tjekker det mod de offentlige registre. Det tager få sekunder.
Vi gemmer ikke dit CPR-nummer.

[ Bekræft med MitID ]
```

**Andelsbolig**
```
Din bolig er en andelsbolig.
Ejerfortegnelsen viser foreningen, ikke den enkelte andelshaver.

Upload dit andelsbevis eller en bekræftelse fra administrator.
Vi gennemgår den inden for to hverdage.

[ Upload dokument ]
```

**Interesse — ingen**
```
Der er ikke registreret verificeret interesse på din adresse.

Vi giver besked, hvis der kommer — hvis du ønsker det.

[ Giv mig besked ]     [ Nej tak ]
```

**Ejerside (betalt)**
```
Interesse på din adresse
12 ugers adgang · 1.495 kr.

Du ser:
· Hvor mange verificerede købere der følger din adresse
· Deres beløbsintervaller og boligønsker
· Hvornår de vil flytte
· Udviklingen over tid

Alt er anonymt. Du vælger selv, om du vil åbne en dialog.

[ Køb adgang ]

14 dages fortrydelsesret. Adgangen åbnes med det samme, hvis du accepterer.
☐ Jeg accepterer, at adgangen åbnes straks.
```

---

## A10 · Mægler

```
Verificerede købere i 2900 Hellerup

12 verificerede købere · eksklusiv adgang til postnummeret

K-7F3A    4,0–4,5 mio. kr.    Villa · 140–180 m²    3–6 mdr.
K-2B91    3,5–4,0 mio. kr.    Villa · 120–160 m²    0–3 mdr.
K-9C4D    5,0–5,5 mio. kr.    Villa · 180–220 m²    6–12 mdr.

Alle er identificeret med MitID og har dokumenteret købeevne.
Kontaktoplysninger udleveres ikke. Dialog foregår anonymt her på platformen.

[ Åbn dialog ]
```

---

## A11 · Tomme tilstande

| Situation | Tekst | Handling |
|---|---|---|
| Ingen ordrer i område | "Ingen verificerede købere følger dette område endnu." | Vær den første |
| Ingen interesse på adresse | "Der er ikke registreret verificeret interesse på din adresse." | Giv mig besked |
| Ingen planer | "Ingen vedtagne planer eller byggesager registreret i området." | — |
| Vurdering mangler | "Vurderinger for 2026 er endnu ikke offentliggjort. Seneste: 2024." | — |
| Ingen matches | "Dit ønske matcher ingen boliger lige nu. Vi giver besked, når det ændrer sig." | Redigér ønske |
| Ingen beskeder | "Dialogen er åben. Skriv, når du er klar." | — |
| Data utilgængelig | "Vi kan ikke hente registerdata lige nu. Prøv igen om lidt." | Prøv igen |

---

## A12 · Fejlbeskeder (kode → tekst)

| Kode | Tekst til brugeren |
|---|---|
| `ORDER_ALREADY_ACTIVE` | "Du har allerede et ønske på denne adresse. Vil du redigere det?" |
| `OWNERSHIP_NOT_VERIFIED` | "Vi kunne ikke bekræfte, at du ejer boligen. Upload dokumentation, så tjekker vi det." |
| `VERIFICATION_EXPIRED` | "Din dokumentation er udløbet. Forny den for at blive vist igen." |
| `MISSING_CONSENT` | "Vi mangler accept fra den anden part. Kontaktoplysninger deles først, når I begge accepterer." |
| `STEP_UP_REQUIRED` | "Bekræft med MitID for at fortsætte." |
| `MESSAGE_REDACTED` | "Beskeden indeholder kontaktoplysninger og blev ikke sendt." |
| `SUBSCRIPTION_EXPIRED` | "Din adgang er udløbet. Forny for at se interessen igen." |
| `PROFILE_NOT_APPROVED` | "Analysen er ikke gennemgået endnu." *(intern)* |
| `K_ANONYMITY_BLOCKED` | "For få registrerede ønsker til at vise dette uden at enkeltpersoner kan genkendes." |
| `RATE_LIMITED` | "Vent et øjeblik, og prøv igen." |
| Generisk | "Noget gik galt. Vi har registreret det. Prøv igen, eller kontakt os." |

---

# DEL B — Mærke-specifikation

## B1 · Wordmark

**Konstruktion:** "Optata" i **Newsreader 400**, optical size 48, tracking **+20/1000 em**. Kun stort O — resten minuskler. Ingen ligaturer, ingen effekter.

| Størrelse | Brug |
|---|---|
| 32 px højde | Header desktop |
| 24 px højde | Header mobil |
| 16 px højde | Minimum. Under dette: brug parcel-mærket |

**Frirum:** Afstand = højden af "O" på alle sider. Ingen tekst, kant eller grafik inden for.

**SVG-skabelon** *(konvertér tekst til outlines i Figma/Illustrator før produktion — fonten må ikke være en afhængighed i logoet)*

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 48" role="img" aria-label="Optata">
  <title>Optata</title>
  <text x="0" y="36"
        font-family="Newsreader, Georgia, serif"
        font-size="40" font-weight="400"
        letter-spacing="0.8"
        fill="#14181B">Optata</text>
</svg>
```

> **Produktionskrav:** Erstat `<text>` med `<path>` (outlines). Logoet skal rendere identisk uden webfont.

---

## B2 · Parcel-mærket

**Idé:** En matrikelparcel med et afskåret hjørne og et udpeget punkt. *Et sted, der er valgt* — ikke et hus.

**Geometri på 24×24 grid:**
- Ydre form: firkant fra (3,3) til (21,21)
- Afskæring: øverste højre hjørne, fra (15,3) til (21,9)
- Punkt: center (12, 13,5), radius 2,25
- Streg: 1,5 px, afrundede hjørner (`stroke-linejoin="round"`)

**Streg-version** *(favicon, kortmarkør, UI)*
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-label="Optata">
  <title>Optata</title>
  <path d="M3 3 H15 L21 9 V21 H3 Z"
        fill="none" stroke="#14181B" stroke-width="1.5"
        stroke-linejoin="round"/>
  <circle cx="12" cy="13.5" r="2.25" fill="#B4643C"/>
</svg>
```

**Fyldt version** *(app-ikon, vandmærke)*
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-label="Optata">
  <title>Optata</title>
  <path d="M3 3 H15 L21 9 V21 H3 Z" fill="#14181B"/>
  <circle cx="12" cy="13.5" r="2.25" fill="#F7F5F1"/>
</svg>
```

**Monokrom** *(vandmærke på PDF, 8 % opacity)*
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
  <path d="M3 3 H15 L21 9 V21 H3 Z" fill="none" stroke="#14181B"
        stroke-width="1.5" stroke-linejoin="round" opacity="0.08"/>
  <circle cx="12" cy="13.5" r="2.25" fill="#14181B" opacity="0.08"/>
</svg>
```

---

## B3 · Lockups og varianter

| Variant | Sammensætning | Brug |
|---|---|---|
| **Horisontal** | Mærke 24 px + 12 px gap + wordmark 32 px | Header, mailsignatur |
| **Stakket** | Mærke 32 px over wordmark 24 px, 8 px gap | Forside, PDF-forside |
| **Mærke alene** | 16–48 px | Favicon, app, kortmarkør, vandmærke |

**Favicon-sæt**
```
favicon.svg          streg-version, Rav-punkt
favicon-32.png       32×32
favicon-16.png       16×16 (punkt forstørres til r=2,75 for læsbarhed)
apple-touch-icon.png 180×180, fyldt version på Papir
```

**App-ikon:** Fyldt version, Blæk på Papir, mærke centreret i 60 % af fladen. Ingen afrundede hjørner i SVG — platformen tilføjer dem.

---

## B4 · Farvevarianter

| Baggrund | Wordmark | Mærke-streg | Punkt |
|---|---|---|---|
| Papir `#F7F5F1` | Blæk | Blæk | Rav |
| Hvid `#FFFFFF` | Blæk | Blæk | Rav |
| Blæk `#14181B` | Papir | Papir | Rav |
| Foto | Papir + 40 % Blæk-scrim | Papir | Rav |

**Aldrig:** Rav wordmark. Gradient. Skygge. Omrids på fyldt version. Rotation. Stræk.

---

## B5 · Forbud

- Ingen hustag, nøgle, hjerte, pin med prik-i-cirkel, SOLGT-skilt
- Ingen afrunding af parcel-formens hjørner ud over `stroke-linejoin`
- Ingen ændring af afskæringens vinkel (den er 45°, fast)
- Ingen placering af punkt uden for firkanten
- Ingen brug af mærket som punktum i brødtekst
- Ingen animation af mærket i UI — det er et stempel, ikke en loader

---

# DEL C — Ejer-mailen

Den vigtigste tekst i hele produktet. Den skal bære jura, anonymitet og drøm på 120 ord.

## C1 · Krav

| Krav | Implementering |
|---|---|
| Ingen persondata om køber | Kun antal + "verificeret". Ingen navn, beløb, kontakt |
| Saglig og afgrænset | Én emne, ingen krydssalg, ingen nyhedsbrev-indhold |
| Afmeld synlig | Link i top og bund, virker på **adressen** |
| Forklaring på hvorfor | "Derfor får du denne mail" → side med behandlingsgrundlag |
| Ingen pres | Ingen tidsfrist, ingen "svar inden" |
| Aggregering | 3 interesser → én mail, ikke tre |
| Frekvensloft | Maks. 1 pr. 14 dage pr. adresse |
| Afsendelse | 08–20 lokal tid |
| Afsender | Optata ApS, fysisk adresse, CVR i footer |

---

## C2 · Emne og preheader

**Én interesse**
```
Emne:      Registreret interesse på Strandvejen 142
Preheader: Du vælger selv, om du vil se den.
```

**Flere interesser**
```
Emne:      3 registrerede interesser på Strandvejen 142
Preheader: Alle er verificeret. Du vælger selv, om du vil svare.
```

**Ingen emne-varianter med:** "Nogen vil købe dit hus", "Din bolig er eftertragtet", "Vigtigt!", "Svar nødvendig".

---

## C3 · Brødtekst (én interesse)

```
Der er registreret verificeret købsinteresse på din bolig.

Strandvejen 142, 2900 Hellerup

Køberen er identificeret med MitID og har dokumenteret købeevne
fra bank eller realkredit.

Du kan se interessen anonymt. Dit navn og dine kontaktoplysninger
deles ikke. Køberens deles heller ikke.

Hvis I begge ønsker det, kan I åbne en anonym dialog.
Kontaktoplysninger udveksles først, hvis I bliver enige.

Du bestemmer selv, om du vil svare.

    [ Se interessen ]

Har du ikke lyst, kan du afvise eller afmelde fremtidige
henvendelser på denne adresse.

    [ Afmeld på denne adresse ]
```

---

## C4 · Brødtekst (flere interesser)

```
Der er registreret 3 verificerede købsinteresser på din bolig.

Strandvejen 142, 2900 Hellerup

Alle tre er identificeret med MitID og har dokumenteret købeevne
fra bank eller realkredit.

Du kan se dem anonymt og vælge, om du vil åbne en dialog med nogen af dem.
Ingen kontaktoplysninger udveksles, før I begge accepterer.

    [ Se interesserne ]

    [ Afmeld på denne adresse ]
```

---

## C5 · Plain text (obligatorisk alternativ)

```
OPTATA

Der er registreret verificeret købsinteresse på din bolig.
Strandvejen 142, 2900 Hellerup

Køberen er identificeret med MitID og har dokumenteret købeevne
fra bank eller realkredit.

Du kan se interessen anonymt. Ingen kontaktoplysninger udveksles,
før I begge accepterer. Du bestemmer selv, om du vil svare.

Se interessen:
https://optata.dk/interesse/[token]

Afmeld fremtidige henvendelser på denne adresse:
https://optata.dk/afmeld/[token]

Derfor får du denne mail:
https://optata.dk/hvorfor/[token]

--
Optata ApS · CVR [nummer]
[Adresse], [Postnr] [By]
kontakt@optata.dk
```

---

## C6 · HTML (tabelbaseret, inline styles, tokens)

```html
<!doctype html>
<html lang="da">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Registreret interesse på Strandvejen 142</title>
</head>
<body style="margin:0;padding:0;background:#F7F5F1;">
  <!-- preheader (skjult) -->
  <div style="display:none;max-height:0;overflow:hidden;color:#F7F5F1;">
    Du vælger selv, om du vil se den.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
         style="background:#F7F5F1;padding:32px 16px;">
    <tr><td align="center">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
             style="max-width:560px;background:#FFFFFF;border:1px solid #E8E4DC;border-radius:4px;">

        <!-- header -->
        <tr><td style="padding:28px 32px 0;">
          <img src="https://optata.dk/brand/optata-lockup.png" width="132" height="28"
               alt="Optata" style="display:block;border:0;">
        </td></tr>

        <!-- body -->
        <tr><td style="padding:28px 32px 0;font-family:Georgia,'Newsreader',serif;
                       font-size:24px;line-height:1.25;color:#14181B;">
          Der er registreret verificeret købsinteresse på din bolig.
        </td></tr>

        <tr><td style="padding:16px 32px 0;font-family:-apple-system,'Inter',Arial,sans-serif;
                       font-size:15px;line-height:1.6;color:#14181B;">
          <strong>Strandvejen 142, 2900 Hellerup</strong>
        </td></tr>

        <tr><td style="padding:16px 32px 0;font-family:-apple-system,'Inter',Arial,sans-serif;
                       font-size:15px;line-height:1.6;color:#14181B;">
          Køberen er identificeret med MitID og har dokumenteret købeevne
          fra bank eller realkredit.
        </td></tr>

        <tr><td style="padding:16px 32px 0;font-family:-apple-system,'Inter',Arial,sans-serif;
                       font-size:15px;line-height:1.6;color:#14181B;">
          Du kan se interessen anonymt. Ingen kontaktoplysninger udveksles,
          før I begge accepterer. Du bestemmer selv, om du vil svare.
        </td></tr>

        <!-- CTA -->
        <tr><td style="padding:28px 32px 0;">
          <a href="https://optata.dk/interesse/[token]"
             style="display:inline-block;background:#B4643C;color:#FFFFFF;
                    font-family:-apple-system,'Inter',Arial,sans-serif;
                    font-size:15px;font-weight:500;text-decoration:none;
                    padding:13px 22px;border-radius:2px;">Se interessen</a>
        </td></tr>

        <!-- afmeld: lige så synlig -->
        <tr><td style="padding:20px 32px 0;font-family:-apple-system,'Inter',Arial,sans-serif;
                       font-size:14px;line-height:1.6;color:#5C6670;">
          Har du ikke lyst, kan du
          <a href="https://optata.dk/afmeld/[token]" style="color:#5C6670;">
            afmelde fremtidige henvendelser på denne adresse</a>.
        </td></tr>

        <!-- divider -->
        <tr><td style="padding:28px 32px 0;">
          <div style="height:1px;background:#E8E4DC;"></div>
        </td></tr>

        <!-- footer -->
        <tr><td style="padding:20px 32px 32px;font-family:-apple-system,'Inter',Arial,sans-serif;
                       font-size:12px;line-height:1.6;color:#5C6670;">
          <a href="https://optata.dk/hvorfor/[token]" style="color:#5C6670;">
            Derfor får du denne mail</a><br><br>
          Optata ApS · CVR [nummer]<br>
          [Adresse], [Postnr] [By]<br>
          <a href="mailto:kontakt@optata.dk" style="color:#5C6670;">kontakt@optata.dk</a>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
```

**Bemærk:** Ingen tracking-pixel, ingen eksterne billeder ud over logoet, ingen links med persondata i query-strings. Token er engangs, adresse-scopet og udløber efter 30 dage.

---

## C7 · Brev / Digital Post (ejer uden e-mail)

```
Optata ApS
[Adresse] · [Postnr] [By]

                                    [Dato]

Vedrørende: Strandvejen 142, 2900 Hellerup


Der er registreret verificeret købsinteresse på din bolig.

Køberen er identificeret med MitID og har dokumenteret købeevne
fra bank eller realkreditinstitut.

Du kan se interessen anonymt på optata.dk. Ingen kontaktoplysninger
udveksles, før I begge accepterer. Du bestemmer selv, om du vil svare.

Sådan gør du:
  1. Gå til optata.dk/adresse
  2. Indtast din adresse
  3. Bekræft med MitID, at du ejer boligen

Ønsker du ikke fremtidige henvendelser på denne adresse, kan du
framelde dig på optata.dk/afmeld eller ved at kontakte os på
telefon [nummer].

Derfor modtager du dette brev: Der er registreret en konkret,
verificeret interesse på din bolig i vores ordrebog. Du kan læse
om behandlingsgrundlaget på optata.dk/hvorfor.


Venlig hilsen
Optata ApS
```

---

## C8 · Acceptkriterier for mailen

```
GIVEN mailen renderes            THEN ingen købernavn, beløb, telefon eller e-mail
GIVEN 3 interesser samme adresse THEN 1 mail med antal, ikke 3 mails
GIVEN adresse afmeldt            THEN ingen mail, uanset nye interesser
GIVEN kl. 22                     THEN kø til næste dag 08:00
GIVEN sidste mail < 14 dage      THEN kø til næste samlede afsendelse
GIVEN token udløbet              THEN venlig side: "Linket er udløbet. Slå din adresse op igen."
GIVEN afmeld klikket             THEN øjeblikkelig suppression + kvitteringsside
GIVEN HTML ikke understøttes     THEN plain text er fuldt forståelig alene
GIVEN skærmlæser                 THEN læserækkefølge er logisk, alt-tekst på logo
GIVEN kontrastmåling             THEN alle tekst/flader ≥ 4,5:1
```

**Kvitteringsside ved afmeld**
```
Du er afmeldt.

Vi sender ikke flere henvendelser om Strandvejen 142.
Registrerede interesser bliver liggende anonymt, men du kontaktes ikke.

Du kan altid slå adressen op igen på optata.dk.
```

---

## Hvor vi står

Tekst, mærke og den vigtigste mail er nu defineret. De tre ting hænger sammen: **mærket er et stempel, teksten er en kvittering, og mailen er en invitation uden pres.** Det er den kombination, der skal få en ejer til at tænke *det her er seriøst* — og en køber til at tænke *endelig et sted, hvor jeg kan sige, hvad jeg vil*.

*Næste skridt kan være (a) de resterende systemmails (verifikation godkendt/udløber, dialog åbnet, enighed, kontaktudveksling, afmeld-kvittering), (b) PDF-leverancens forside og layout til områdeanalysen — den der skal kunne ligge i et kreditudvalg, eller (c) en komplet tekstfil til repoet (`apps/web/i18n/da.json`) så UA-teamet ikke opfinder copy undervejs.*
