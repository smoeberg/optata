# OPTATA — Samlet projektgrundlag

**Version 5.0 · 16. november 2026 · Soeren Moeberg**

Dette er masterskumentet. Forretning, koncept, data, mekanismer, sikkerhed, jura og leveranceplan står samlet her. De elleve tekniske bilag, forretningsplan v4.2 og arkitekturreviewet er indarbejdet — ikke refereret. Hvor bilagene modsagde hinanden eller forretningen, er der valgt ét svar, og valget er begrundet.

---

## 0. Læsevejledning

### 0.1 Struktur

| Del | Indhold | Læses af |
|---|---|---|
| 1 | Forretningen: produkt, priser, enhedsøkonomi, økonomi | investor, bank, stifter |
| 2 | Konceptet: zoner, ordrebog, moat | alle |
| 3 | Datagrundlaget: kilder, bitemporalitet, agent, gap-analyse | UA, data, DK |
| 4 | Mekanismer: matching, notifikation, verifikation, relay, faktura, abonnement | UA, DK |
| 5 | Sikkerhed og jura: invarianter, STRIDE, retention, formidling | DK, jurist, bank |
| 6 | Leveranceplan: faser, sprints, kritisk vej, kapacitet | UA, stifter |
| 7 | Governance: kravspec, CI-gates, ADR | UA, DK |
| 8 | Næste 14 dage | stifter |

### 0.2 Hvad v5 retter

| # | Fejl i v4.2 / bilagene | Rettelse i v5 |
|---|---|---|
| 1 | **MitID giver pseudonymt PID, ikke CPR.** Bilagene specificerer både »aldrig CPR« og `EJF_MATCH` — de to kan ikke begge være sande, og EJF's ejerfortegnelse er nøglet på CPR/CVR | Ejerskabsverifikation er **primært adressekode pr. brev** (§4.4). CPR-opløsning er en senere optimering, ikke en forudsætning |
| 2 | **EJF-adgang er ikke givet.** Planen byggede en guard på en adgang, der måske ikke findes | Multi-metode med eksplicit fallback: EJF (hvis adgang) → tinglyst adkomst → andelsattest → manuel kø. Adgang bekræftes i uge 1, ikke antages (§3.1) |
| 3 | **»MitID-broker bestilles uge 1 — kritisk vej«.** Brokeren var kritisk vej for alt, også for produkter uden identitet | Kritisk vej er nu **Datafordeler-adgang + medielicens**. Broker bestilles, men blokerer ikke piloten (§6.4) |
| 4 | **Verifikation er en stilling, ikke en funktion.** 10 min/attest × ~6.000 gennemløb/år = 0,6 årsværk, usynligt i §7 | Reviewer ansat md. 8; loft 150 verifikationer/md. i piloten; bankvalidering (V2/V3) skal være klar før bydel 3 (§4.9) |
| 5 | **Byggeordenen var S1–S7 lineært.** S3–S5 (MitID, ejerside, relay) lå før den første krone og blokerede alt | Byg **A før B**: 49 % af md.-36-omsætningen kræver ingen zone B. A1 md. 1–4, A2 md. 4–8, B1 md. 6–11, B2 md. 11–15 (§6.2) |
| 6 | **Matching var ikke specificeret** — nævnt i repo-strukturen, aldrig defineret, men matching *er* produktet | §4.1: to match-typer, hard filters, score 0–100 med påkrævede reason codes, tærskel 60, idempotens (§4.1) |
| 7 | **Husstands-dedup nøglet på `buyer_id`.** Samboende medkøbere blev to ordrer på samme husstand | Dedup på `household_key` med delvist unikt index + co-buyer på samme ordre (§4.2) |
| 8 | **k-anonymitet i materialized view** — et snapshot skjuler ikke en celle, der falder fra 6 til 4 | k≥5, afrunding og komplementær suppression håndhæves **i forespørgslen** (§4.8) |
| 9 | **Pseudonym var globalt og stabilt** — en link-nøgle på tværs af tråde | Pseudonym er **parvist**: `HMAC(thread_id)`. Global identitet vises aldrig (§4.5) |
| 10 | **Medieovervågning 6.000 kr./md. antog arkivadgang.** Infomedia/Retriever koster 15–30.000 kr./md. | 6.000 dækker offentlige feeds og licenserede uddrag. Arkiv er en Demand Pro-omkostning (§3.3) |
| 11 | **Bankpartner md. 9.** Behandlet som datasamarbejde | Bankpartner **md. 3**. V3-webhook er kapacitetsforudsætning for at skalere verifikation (§4.9) |
| 12 | **Arbejdskapital var ikke i planen** | WC 0,2–0,4 mio. oveni bundpunktet; kapitalbehov **2,1 mio.** med følsomhed 1,7/1,9/2,1 (§1.5) |
| 13 | **Mæglerprisen var selvmodsigende** (2.900 »eksklusivt postnummer« vs. 6.900 »eksklusiv bydel«) og bindingen 12 mdr. | To produkter, ikke en trappe: 2.900 = postnummer, 6 mdr.; 6.900 = bydel + feed + API, 12 mdr. Overvågning lægges ikke oveni (§4.7) |
| 14 | **»Fuld historik« vs. sletteret** var uløst | To-lags sletning med tombstone; bogføring og audit kan ikke slettes og undtagelserne står i privatlivspolitikken (§5.3) |
| 15 | **Teaseren sagde ~90.000 bolighandler/år** | 70–90.000 (§1.1) |

### 0.3 De fem åbne beslutninger

| # | Beslutning | Frist | Konsekvens hvis sen |
|---|---|---|---|
| 1 | Data engineer ansat fra **md. 2** | uge 6 | Første krone skrider md. 4 → md. 6–7 |
| 2 | **Datafordeler-adgang** + bekræftelse af EJF-berettigelse | uge 1–2 | S1 kan ikke starte; byg mod syntetiske data imens |
| 3 | **Medielicens** (feeds + uddrag) | uge 2 | S2 kan ikke levere en analyse, der tåler et bankkreditmøde |
| 4 | **Jurist:** formidlingsvurdering + kontaktgrundlag | uge 6, møde bestilt nu | S4/S5 må ikke lanceres; byg bag feature-flag |
| 5 | **Model A/B/C** for formidling (advokatpartner som formel formidler) | uge 6 | Hele relay-arkitekturen afhænger af svaret |

De fem beslutninger er ikke arkitektur. De er adgang og jura, og de koster kalendertid, ikke kodetid.

---

## 1. Forretningen

### 1.1 Problemet

Boligmarkedet i Danmark har 70–90.000 handler om året og et strukturelt informationsproblem: **efterspørgslen er usynlig, indtil den bliver en handel.** En køber, der er forhåndsgodkendt i banken og klar til at byde på en bestemt vej, findes ikke i noget register. En ejer, der overvejer at sælge om seks måneder, findes heller ikke.

Det giver tre tab:

- **Ejer:** sælger uden at vide, at der står tre finansierede købere i kø. Går glip af pris og tid.
- **Køber:** byder på det, der er til salg, ikke det, der matcher. Betaler for mæglerens annonce, ikke for adgang.
- **Mægler og bank:** bruger markedsføringskroner på at fange efterspørgsel, de kunne have fået struktureret.

Optata gør efterspørgslen til en **registreret, verificeret og anonymiseret størrelse** — og sælger adgang til den indsigt, ikke til personerne.

### 1.2 Positionering: to sætninger, der ikke må blandes

I pitchet: **ordrebogen**. En samlet, verificeret efterspørgsel pr. område — let at forstå, let at huske.

I kontrakten: **verificeret efterspørgsel**. Ikke ordrer.

Forskellen er ikke akademisk. En ordrebog forudsætter en vare med ensartede enheder og én pris. En bolig er unik og har én sælger. Det, vi har, er *signaler om købsintention med dokumenteret købeevne*. En mægler, der køber en »ordrebog« og forventer ordrer, churner i måned 3 — og fortæller det til de næste. Så: ordrebog i samtalen, verificeret efterspørgsel i aftalen.

**Vi er ikke en boligportal.** Portalen sælger opmærksomhed på udbud. Vi sælger indsigt i efterspørgsel. Det er den modsatte side af markedet, og det er derfor, dataene har værdi: alle kan se, hvad der er til salg; ingen kan se, hvem der vil købe.

### 1.3 Produkter og priser

| Produkt | Kunde | Pris | Type | Fase |
|---|---|---|---|---|
| **Områdeanalyse** | developer, bank, pension, kommune | 85.000 kr. + moms = **106.250** | engang | A1 |
| **Områdeovervågning** | samme | 4.500 kr./md. | abonnement | A2 |
| **Demand Pro** | bank, developer,rådgiver | 9.500 kr./md. | abonnement | C |
| **Ejerside** (adresseadgang) | ejer | 1.495 kr. | engang | B1 |
| **Salgspakke** | ejer | 10.000 kr. fast gebyr | engang | B2 |
| **Mægler, postnummer** | mægler | 2.900 kr./md., 6 mdr. binding | abonnement | B2 |
| **Mægler, bydel** | mægler | 6.900 kr./md., 12 mdr. binding | abonnement | B2 |

To ting om priserne:

**Salgspakken er et fast gebyr, aldrig en success fee.** En procentdel af handlen gør Optata til formidler og trækker hvidvasklov og god skik ind. Det er både den lovlige og den bedre sælgende konstruktion: ejeren køber en pakke — dokumenter, vurdering, foto, annonce, forhandlingsstøtte — uafhængigt af, om handlen lukkes.

**Mæglerprodukterne er to produkter, ikke en trappe.** 2.900 kr. giver eksklusivitet på postnummerniveau. 6.900 kr. giver hele bydelen plus overvågningsfeed og API. Overvågning (4.500) lægges ikke oveni et bydel-abonnement — den er inkluderet. Ellers sælger sælgeren 2.900 + 4.500 = 7.400 for det, der ligner 6.900, og økonomien holder ikke.

### 1.4 Enhedsøkonomi pr. bydel

En moden bydel: ca. 10.000 boliger, 250 verificerede ordrer (25 pr. 1.000).

| Strøm | Beregning | Årlig omsætning |
|---|---|---|
| Områdeovervågning | 4.500 × 12 | 54.000 |
| Mæglerabonnement | 1,5 × 2.900 × 10,2 mdr. | 44.370 |
| **Recurring i alt** | | **98.370** |
| Ejerside | 15 × 1.495 | 22.425 |
| Salgspakker | 3 × 10.000 | 30.000 |
| **Transaktion i alt** | | **52.425** |
| **Samlet pr. bydel/år** | | **150.795** |

Plus engangsanalysen på 85.000 kr. i år 1.

**Den vigtigste linje i tabellen er ikke de 30.000 kr. — det er de 120 kr.** Salgspakken er resultatet af fem rater i serie: 40 % adresse-specifikke ordrer × 15 % dialog × 40 % pris-enighed × 55 % køb af pakken. Ganget sammen: 0,9–1,2 % af de verificerede ordrer. Det giver **~120 kr. i pakkeomsætning pr. verificeret ordre om året**. Det er ikke et hovedben. Det er en mulighed, der opstår, fordi vi ejer efterspørgslen.

**Mæglerabonnementet er til gengæld et væddemål på tæthed** — én rate, vi kan styre. Salgspakken er et væddemål på konvertering — fem rater, vi ikke kan. Deraf rækkefølgen: abonnement først, pakke bagefter.

Forudsætningen for de 44.370 kr. er en **fornyelsesrate på 70 %**. Falder den til 50 %, er recurring-benet 30 % mindre. Det er den mest følsomme antagelse i hele planen og skal måles som P3-kriterium: *faktisk fornyelse efter de første 6 måneders binding er det første rigtige bevis på, at abonnementet er et abonnement.*

### 1.5 Økonomi, kapital og break-even

Indtægterne er de samme i begge leverancemodeller: **0,99 / 2,37 / 4,11 mio. kr.** i år 1–3. Forskellen er omkostningsbasen.

| | A: direkte omkostninger | B: + arbejdsgiverbidrag, G&A, uforudset |
|---|---|---|
| Omkostning pr. md., år 1 | 153.700 | 169.100 |
| Bundpunkt | −1,07 mio. (md. 21) | **−1,46 mio. (md. 23)** |
| Varigt break-even | md. 24–26 | **md. 27–29** |
| Kumulativ likviditet md. 36 | +0,34 mio. | **−0,37 mio.** |

**B er budgettet.** De 10–12 % arbejdsgiverbidrag og feriepenge på danske lønninger, plus selskabsadministration, forsikring, regnskab, rejser og uforudset, er ikke pessimisme — det er den normale danske arbejdsgiverhverdag. Planen indeholder selv testen: de tre UA-tilbud i uge 1–2. Lander de på 25–30.000 kr./md. for GIS-seniorer, er A rigtig. Lander de højere, er B rigtig, og så skæres der i produktplanen, ikke i juraen.

**Kapitalbehovet er 2,1 mio. kr.**, ikke 1,8. De 1,46 mio. er EBITDA-bundpunktet; dertil kommer arbejdskapital:

| Post | Størrelse |
|---|---|
| Debitorer (30–60 dages betaling) | 150.000–300.000 |
| Moms (faktureres før betaling) | 50.000–150.000 |
| **WC i alt** | **200.000–400.000** |

| WC-scenarie | Kapitalbehov |
|---|---|
| 0,2 mio. | 1,7 mio. |
| 0,3 mio. | 1,9 mio. |
| 0,4 mio. | **2,1 mio.** |

Tranche 1: 1,0 mio. nu. Tranche 2: 1,1 mio. ved P2/P3. Spændet lukkes med en kassekredit, ikke ved at vælge midt i det.

**Læs modellen på rullende tre måneder.** Omsætningen hopper mellem 180.000 og 350.000 kr./md., fordi bydele sælges og modnes i ryk. Første positive måned er md. 12 (enkeltstående), men varigt break-even er md. 27–29. Ellers ser md. 12 ud som en sejr, den ikke er.

### 1.6 Fordelingen og hvad den betyder

Ved md. 36: **79 % B2B**, 21 % B2C. Recurring 1,18 mio. + transaktion 0,63 mio. = 1,81 mio. kr.

Det betyder noget for, hvem vi bygger for. B2C-produkterne (ejerside, pakke) er ikke forretningen — de er **dataindsamling og likviditet**. B2B er forretningen. Og det er derfor, køberen skal have noget gratis: områderapporten er den vare, der gør, at tosidet likviditet kan opstå, før der er noget at sælge.

### 1.7 Go-to-market: distribution, ikke annoncer

250 verificerede ordrer kræver ~31.000 lokale besøgende ved 8 % konvertering og 10 % verifikationsrate — stort set alle voksne i et postnummer. Det kan ikke købes for 12–32.000 kr./md.

To greb ændrer matematikken:

| Greb | Effekt |
|---|---|
| **Hæv verifikationsraten 10 % → 25 %** | Rå ordrer 2.500 → 1.000; besøg 31.000 → **12.500** |
| **Distributionspartnere i stedet for annoncer** | Besøg via foreninger, mægler, bank — ikke betalt trafik |

Verifikationsraten hæves ved at gøre **bank-forhåndsgodkendelsen til indgangsværdien**: *»Bliv forhåndsgodkendt og kom i ordrebogen — ejere ser dig først, når din købeevne er dokumenteret.«* Køberen får noget for besværet.

| # | Kanal | Reach pr. krone |
|---|---|---|
| 1 | Andels- og grundejerforeninger | 2.000–6.000 husstande |
| 2 | Bank/realkreditpartner | 300–800 godkendte/år lokalt |
| 3 | Lokal mægler (pilot, eksklusiv) | 200–500 |
| 4 | Områderapport som SEO/indhold | 1.000–4.000/md. over tid |
| 5 | Lejebolig-ventelister | 500–2.000 |
| 6 | Betalt lokal annoncering | sidst |

Foreninger: gratis område- og adresseindsigt til bestyrelsen, medlemmerne får før-adgang til rapporten. Ingen betaling, ingen kommission — ren distribution.

---

## 2. Konceptet: zoner, ordrebog og moat

### 2.1 Tre zoner — ufravigelige

| Zone | Indhold | Udvikling | Eksport |
|---|---|---|---|
| **A** | Offentlige data: DAR, BBR, EBR, VUR, matrikel, planer, claims, rapporter | ✅ tilgængelig | ✅ |
| **B** | Identitet, ordrer, bankbeviser, ejerrespons, relay-tråde | ❌ aldrig | ❌ aldrig |
| **C** | Aggregeret, k≥5, afrundet | ✅ syntetisk | ✅ licenseret |

Zone-adskillelsen håndhæves i **DB-roller og row level security**, ikke i applikationslogik. Det er den ene beslutning, der gør det forsvarligt at lade et eksternt team bygge systemet: front-end kan ikke joine til vault, fordi databasen ikke tillader det.

### 2.2 Hvad moaten er — og ikke er

Moaten er ikke koden. Koden kan en konkurrent skrive på et år. Moaten er:

1. **Historikken.** Al registerdata er bitemporal. En konkurrent, der starter i dag, kan ikke genskabe, hvad vi vidste i marts.
2. **Ordrebogens integritet.** Verificerede, deduplikerede, finansierede købsintentioner — med attest og ejerskab bag.
3. **Den lokale distribution.** Foreninger, mægler, bank. Det tager år at opbygge og kan ikke købes.
4. **Den juridiske position.** Kontaktgrundlag, samtykke-ledger, formidlingsmodel. Det er en adgangsbillet, ikke en differentiator — men uden den er der ingen forretning.

### 2.3 Ordrebogens fire integritetsregler

En ordrebog, der kan spammes, er ikke et aktiv. Uden disse regler tæller den samme køber tolv gange, den første mægler churner i md. 3, og tæthedstallet er fup.

1. **Én aktiv ordre pr. husstand pr. scope.** Håndhæves med delvist unikt index, ikke i applikationen.
2. **Tre niveauer: CURIOS, QUALIFIED, VERIFIED.** Kun VERIFIED tælles i tæthed og udløser ejer-kontakt.
3. **Fuld historik, ingen sletning af hændelser.** Tilbagetrækning er en ny hændelse.
4. **Ingen konkurrencer eller lokkemidler** som incitament til at oprette en ordre.

Konsekvensen: tæthed måles **kun på verificerede ordrer**.

---

## 3. Datagrundlaget

### 3.1 Kilder og adgang

| Kilde | Indhold | Adgang | Bemærkning |
|---|---|---|---|
| **DAR** | Adresser, adgangsadresser, koordinater | Datafordeler, aftale | Rygraden. Adresse-id er nøglen til alt |
| **BBR** | Bygninger, boliger, anvendelse, areal | Datafordeler | Boligkoder styrer tællingen |
| **EBR** | Virksomheder, CVR-ejerskab | Datafordeler | Selskabsejede ejendomme |
| **VUR** | Vurderinger | Datafordeler, **forsinket** | Kun reference, aldrig sandhed |
| **EJF** | Ejerfortegnelse | **Kræver berettigelse — ikke givet** | Bekræftes uge 1. Fallback: tingbogen |
| **Tingbogen** | Adkomst, skøder, servitutter | Offentlig | Tinglysningsforsinkelse giver huller |
| **Plansystem** | Lokalplaner, kommuneplaner | Offentlig/API | Bevægelseslaget |
| **Medier** | Artikler om byggesager | **Licens påkrævet** | Arkiv koster 15–30.000/md. |

**Om de fire links, der startede det hele:** de er ikke fire integrationer. »Find Ejeren« (GeoInfo) henter matrikel, ejerfortegnelse og beliggenhed via Datafordeleren. OIS er Skatteforvaltningens visning af de samme grunddata. Dingeo er samme data pakket til forbrugeren — en konkurrent, ikke en kilde. GeoInfo er Esri-partner og en mulig **distributionskanal**, ikke en datakilde. Vi skal ikke integrere med dem; vi skal bygge oven på de samme offentlige registre, som de bygger på.

**Konsekvens for planen:** EJF-adgang må ikke være en forudsætning. Se §4.4.

### 3.2 Bitemporal model og tælling

Al registerdata har `valid_from`/`valid_to` (hvornår det gjaldt i virkeligheden) og `recorded_at` (hvornår vi vidste det). En opdatering **lukker** den gamle version og indsætter en ny. Historik overskrives aldrig.

Tre invarianter:

- **BFE → adresse-id er 1:mange.** En ejendom kan have mange adresser (FX-01: 40 andelsenheder). Tæller man BFE, tæller man 1 i stedet for 40.
- **`dwelling_count` = aktive DAR-adresser med BBR-boliganvendelse.** Nævneren i tæthed. Ændrer den sig mere end 2 % fra en kørsel til den næste, fryses tætheds-KPI'en og årsagen undersøges — ellers måler P2-porten på et forkert tal.
- **`property.changed` emitteres ved enhver versionsændring.** Det driver overvågningsproduktet, agent-cachen og — vigtigst — tilbagekaldelse af ejerskabsverifikation ved ejerskifte.

### 3.3 Agenten: claim-pipeline med tvungen proveniens

Agenten producerer **påstande med kilde og dato**, ikke prosa. Fire lag:

```
kilder → udtræk (LLM, struktureret JSON) → deterministisk validering → menneskelig review → publicering
```

**Valideringsreglerne (afvisning, ikke advarsel):** `source_id` skal findes i databasen · `effective_date` skal være gyldig · citat maks. 200 tegn og fuzzy-matchet i kilden · påstande uden for skemaet kasseres · meningsytringer afvises som `OPINION` · rygter bevares men må aldrig i bevægelseslaget · confidence under 0,6 går til manuel kø.

**Publicering kræver `reviewed_by`.** Ingen undtagelse, ingen auto-publish. `model_version` og `prompt_version` gemmes, så en leverance kan reproduceres.

**Omkostning:** 6.000 kr./md. dækker offentlige feeds, licenserede uddrag og LLM-kald. Arkivsøgning (Infomedia/Retriever) er ikke med — den hører til Demand Pro, når kunden betaler for den.

### 3.4 Gap-analysen: det kunden faktisk betaler for

Gap-analysen kombinerer zone A (hvad findes) med zone C (hvad efterspørges). Fire tal:

| Tal | Betydning | Eksempel |
|---|---|---|
| **Verificeret efterspørgsel** | Finansierede købere i segmentet | 62 |
| **Coverage ratio** | Årligt udbud ÷ efterspørgsel | 0,18 → kraftigt underdækket |
| **Absorption** | Måneder til at optage efterspørgslen | 34 |
| **Confidence** | Datagrundlagets styrke | MEDIUM |

Udbyttet er ikke en anbefaling. Det er et **observeret mismatch**: *»der er 62 verificerede købere til 4-værelses i båndet 4,0–4,5 mio., og det årlige udbud i segmentet er 11 enheder.«* Et projekt på 40–80 enheder kan ikke mættes af det eksisterende udbud. Det er den indsigt, en developer betaler 85.000 kr. for.

**Obligatoriske forbehold** (skrives i hver leverance): efterspørgsel er ikke forpligtelse · geografisk substitution mulig · prisfølsomhed ikke målt · VUR er forsinket · celler skjult ved k<5 · øjebliksbillede med rullende 3-måneders vindue.

Uden forbeholdene er analysen en holdning. Med dem er den et dokument, en bank kan lægge i et kreditindstilling.

---

## 4. Mekanismerne

### 4.1 Matching

Matching er produktet. Uden den er ejer-notifikationen en spamkanal.

**To typer, der aldrig må blandes:**

| Type | Fra → til | Formål | Udløser |
|---|---|---|---|
| **M1 Adresse-match** | Ordre (scope=ADDRESS) → ejer | Fremkald udbud | Kun VERIFIED |
| **M2 Område-match** | Ordre (scope=AREA) → ejendomme/mæglere | Lead-liste, indsigt | Løbende, ingen ejer-kontakt |

**Regel:** M2 må aldrig udløse kontakt til en ejer. Det er kun M1, på den konkrete adresse. Ellers er det massehenvendelser — juridisk og troværdighedsmæssigt fatalt.

**Hard filters før scoring:** adresse-id ved ADDRESS-scope · geometri-indhold ved AREA · boliganvendelse · type · areal · værelser. **Budget filtreres ikke hårdt** — en ejer skal kunne se interesse, selv om budgettet ligger under vurderingen. Det er information, ikke støj.

**Score 0–100, forklarbar:**

| Signal | Vægt | Beregning |
|---|---|---|
| Budgetdækning | 30 | `min(1, budget_max / reference_pris)`; reference = VUR suppleret med tinglyste overdragelser |
| Størrelsesfit | 20 | Gauss om ønsket areal, σ = 20 % |
| Typefit | 15 | eksakt = 1, beslægtet = 0,5 |
| Horisont | 15 | 0–3M 1,0 · 3–6M 0,8 · 6–12M 0,5 · 12M+ 0,2 |
| Verifikation | 15 | VERIFIED 1,0 · QUALIFIED 0,4 · CURIOS 0 |
| Friskhed | 5 | decay over 90 dage |

**`reason_codes` er påkrævet i API-svaret** — fx `["BUDGET_DAEKKER","STOERRELSE_FIT","VERIFICERET","HORISONT_3_6M"]`. En mægler og en ejer skal kunne se *hvorfor*. Uden det er scoren et gæt, og produktet mister troværdighed.

**Tærskler:** M1 notifikation ved score ≥ 60 **og** level = VERIFIED. M2 lead-liste viser alle VERIFIED, sorteret efter score.

**Kørsel:** event-drevet (`order.verified`, `property.changed`, `owner.ownership_verified`) plus natlig fuld genberegning pr. område. Idempotensnøgle: `(order_id, address_id, criteria_hash, property_version)`. Uændret input giver ingen ny notifikation.

### 4.2 Tæthed og dedup

**Tæthed er KPI'en, hele forretningen hviler på.** Formlen er enkel; nævneren er det svære.

```
per_1000 = 1000 × antal VERIFIED og ACTIVE ordrer i området / dwelling_count
```

`dwelling_count`: aktive DAR-adresser med BBR-boliganvendelse. FX-01 med 40 andelsenheder tæller 40. Viewet refreshes efter ingestion og ved `order.verified/expired/withdrawn` — aldrig i request-pathen.

**Dedup i tre lag:**

| Lag | Nøgle | Håndhævelse |
|---|---|---|
| Person | `identity.pseudonym` (MitID) | Broker-sub unik |
| Husstand | `household_key` = købers nuværende DAR-adresse | Delvist unikt index + co-buyer |
| Scope | (husstand, scope, adresse/område) | Unikt index på aktive ordrer |

Samboende medkøbere tilføjes som `order_party` på samme ordre — ikke som ny ordre. Ved identitetslink (e-mail → MitID) merges ordren **in-place** med `causation_id`. Aldrig slet-og-genskab; det ville bryde historikken og tællingen.

### 4.3 Notifikation og samtykke

Ejer-kontakt er den mest følsomme handling i systemet. Den skal være **lovlig, dæmpet og sjælden** — ellers dør produktet på afmeldinger.

**Syv betingelser, alle påkrævet, før en ejer kontaktes:**

1. Ordren er VERIFIED og attesten er gyldig.
2. Scope er ADDRESS, og adressen er præcis denne.
3. Matchscore ≥ 60.
4. Adressen er ikke suppressed (afmelding vinder altid).
5. `legal_basis_ref` findes — juristens dokument-id, ikke en antagelse.
6. Frekvensloft overholdt.
7. Klokken er 08–20 lokal tid.

**Kanaler:** e-mail primært. Brev/digital post til ejere uden e-mail i kontaktregisteret — sagligt, afgrænset, afmelding via URL + kode. In-app til aktive brugere, uden persondata i push-teksten. **SMS ikke i år 1:** for indgribende, for dyrt, svært at afmelde pænt.

**Aggregering er et krav, ikke en nice-to-have.** Flere interesser på samme adresse samles til én notifikation: *»Der er 3 verificerede købere til din adresse.«* Det sænker støj, hæver oplevet værdi og reducerer afmeldinger.

| Regel | Værdi |
|---|---|
| Maks. pr. adresse | 1 pr. 14 dage |
| Maks. pr. ejer på tværs af adresser | 2 pr. måned |
| Ny interesse inden for loftet | med i næste samlede notifikation |
| Afmelding | **permanent på adressen** |
| Afvisning af konkret køber | suppression på (adresse, pseudonym) |
| Hard bounce eller klage | øjeblikkelig suppression + review |

**Skabelonen må ikke indeholde:** købernavn, præcist budget, telefon, e-mail, dokumentvedhæftning eller formuleringspres (»skynd dig«, »sidste chance«). Køberen er »identificeret og har dokumenteret købeevne« — intet mere.

**Samtykke-ledger, append-only.** Hvert samtykke gemmer formål, scope, `legal_basis_ref`, `text_version` (hvad brugeren faktisk så), kanal, tidspunkt og tilbagekaldelse. Formål er adskilte: `OWNER_INTEREST_NOTIFICATION`, `DIALOG`, `IDENTITY_REVEAL`, `BANK_ATTESTATION_PROCESSING`, `B2B_AGGREGATION`. Reveal kræver **separat samtykke fra begge parter**. Tilbagekaldelse propagerer øjeblikkeligt til suppression og aborterer åbne tråde.

**Alarm:** afmelingsrate over 5 % pr. område betyder, at produktet er for støjende. Skru loftet **ned**, ikke op.

### 4.4 Ejerskabsverifikation — rettet

Dette er den guard, der beskytter alt andet, og den var bygget på en forkert forudsætning.

**Fejlen:** bilagene specificerede både »MitID, aldrig CPR« og `EJF_MATCH`. MitID returnerer et pseudonymt PID; EJF's ejerfortegnelse er nøglet på CPR/CVR. De to kan ikke forbindes uden en CPR-opløsning, som kræver dataudvekslingsaftale og GDPR-vurdering — 3–6 måneder, ikke 6 uger. Uden den kan systemet ikke afgøre, om MitID-brugeren er den registrerede ejer. Det rammer 42 % af omsætningen ved md. 36.

**Løsningen: adressekode pr. brev.** Ejeren anmoder om adgang til sin adresse. Systemet genererer en kode og sender den med post til den adresse, EJF/tingbogen har registreret. Ejeren indtaster koden. Det tager to dage i stedet for femten sekunder, men:

- det kræver ingen CPR-opløsning og ingen ekstern leverance,
- det er et **stærkere** bevis end en app-bekræftelse (kun den, der kontrollerer adressen, kan svare),
- det kan bygges i md. 8 uden at vente på en aftale.

CPR-opløsning bliver en optimering i md. 12+, ikke en forudsætning i md. 9.

**Multi-metode, i prioriteret rækkefølge:**

| Metode | Hvornår | Konfidens | TTL |
|---|---|---|---|
| `EJF_PERSON` / `EJF_CVR` | hvis berettigelse opnås | HØJ | 180 dage |
| `DEED` (tinglyst adkomst) | EJF utilgængelig | MEDIUM | 90 dage |
| `ADDRESS_CODE` (brev) | standard i piloten | HØJ | 90 dage |
| `ANDELS_ATTEST` | andelsbolig | MEDIUM | 90 dage |
| `MANUAL` / `POWER_OF_ATTORNEY` | dødsbo, værge, sameje | varierer | 90 dage |

**Ejerskabstyper, der ikke kan behandles ens:**

| Type | Hvem er »ejer« | Metode |
|---|---|---|
| Parcelhus/ejerlejlighed, privat | fysisk person | EJF, adkomst eller adressekode |
| **Andelsbolig** | **foreningen** ejer ejendommen; andelshaver har andelen | EJF dur ikke. Andelsbevis + administratorattest |
| Selskabsejet (CVR) | juridisk person | MitID Erhverv + CVR-match + tegningsret |
| Udlejningsejendom | selskab/privat | kun ejeren ser efterspørgsel, ikke lejerne |
| Dødsbo | boet | skifteretsattest + kontakt til advokat |
| Værge/fuldmagt | ejeren, repræsenteret | fuldmagt + beskikkelse, altid manuelt |
| **Sameje** | 2+ personer | én verifikation pr. ejer; **alle** skal samtykke til reveal |

Andelsboliger er en stor del af storbyens boligmasse. Uden andels-flowet er pilotområdet reelt halvt dækket. Det bygges i B1, ikke som senere tilføjelse.

**Genverifikation ved ejerskifte er kritisk.** `property.changed` med nyt ejerskab skal **automatisk tilbagekalde** eksisterende verifikation. Ellers kan en tidligere ejer blive ved med at se efterspørgsel på en bolig, han har solgt. Det er både en datalækage og et konkurrentens gratis lead-katalog. Der er en guard-test på det, og den er ikke valgfri.

**Kapacitet — den usynlige flaskehals.** Manuel behandling er ca. 10 minutter pr. sag, og ~25 % af ejerne ender i fallback-køen. Ved 100 ejere i piloten: 25 sager ≈ 6 timer. Overkommeligt. Ved 12 bydele: ~75 timer/år bare i fallback, plus alle adressekoder. Derfor:

- **Loft: 150 verifikationer pr. md.** i piloten.
- **Reviewer ansat md. 8** — 15 timer/uge, ca. 120.000 kr./år. Ikke en udvikler; en person, der kan læse et andelsbevis.
- **Bankvalidering (V2/V3) klar før bydel 3.** Ellers bliver review den flaskehals, der stopper skaleringen.

**Adgangskontrol:** uverificeret bruger får 403 uden interesse-data. Navnematch mellem MitID og register sker transiente i hukommelsen og **gemmes eller logges aldrig** — kun resultatet (VERIFIED, metode, tidspunkt).

**Manglende EJF-adgang er ikke et projektstop.** Det er en dyrere vej til det samme: adressekode og manuel kø. Beslutningen om at investere i CPR-opløsning træffes, når volumen retfærdiggør den.

### 4.5 Relay, redaction og reveal

Al kommunikation mellem køber og ejer går gennem relay. Ingen kontaktoplysninger udveksles, før begge parter accepterer.

**Redaction er en sikkerhedskomponent, ikke et filter.** Deterministisk først: regex for telefon, e-mail, CPR-mønster, adresse; derefter NER; derefter EXIF/OCR i vedhæftninger; til sidst adfærdsmønstre (»ring til mig på to nul fire fem…«). LLM kun som supplement — den må ikke være eneste lag, fordi den kan prompts. Ved gentagne træf: karantæne.

**Pseudonymet skal være parvist.** `HMAC(thread_id)`, ikke et globalt id. Et globalt pseudonym er en link-nøgle: to ejere i samme postnummer ser samme kode og taler sammen, og mægleren ser samme køber over 18 måneder. Det er billigt at gøre rigtigt nu og dyrt at rette senere, fordi det rammer event-katalog, PublicProfile og audit.

**Reveal — det mest følsomme kald i systemet.** Seks guards, alle i **én transaktion** med lås:

1. Salgspakken er accepteret.
2. Betalingen er captured (verificeret server-side, ikke fra klienten).
3. Begge parter har samtykket.
4. Frisk MitID step-up, maks. 5 minutter gammelt.
5. Attesten er gyldig.
6. Ejerskabet er verificeret.

Kun `disclosure`-servicerollen må læse vault. Ingen admin-endpoint til reveal. Idempotensnøgle, så to samtidige kald giver ét grant og én audit-linje. Time-of-check/time-of-use: alle checks og selve læsningen sker under samme lås, ellers kan attesten udløbe mellem guard og brug.

**Mægleren er aldrig `deal.party`.** Mægleren køber adgang til anonym dialog, ikke til en kontaktliste. Forsøg på reveal som mægler giver 403.

### 4.6 Leverance og faktura — den første krone

**Tilstandsmaskine:**

```
ORDERED → SCOPED → GENERATING → IN_REVIEW → APPROVED → DELIVERED → ACCEPTED → INVOICED → PAID
                        └→ REVISION (1 inkluderet) → IN_REVIEW
         └→ CANCELLED (før GENERATING, uden faktura)
```

`DELIVERED` kræver `review_state = APPROVED`. `INVOICED` kræver `DELIVERED`. **Ingen faktura før leverance** — det er god skik og lavere debitorrisiko.

**Scope-kontrakten beskytter margenen.** Analysen er et produkt, ikke en åben konsulentopgave. Fast scope i ordren: område (geometri), lag (fakta, bevægelse, hverdag, efterspørgsel), dybde (antal claims, byggesager, institutionsdækning), format (PDF + web, versioneret), **1 revision inkluderet**, herefter 4.500 kr./time, levering 10 hverdage fra SCOPED, kilde + dato på hver påstand, ingen prognoser. Uden det æder scope creep de 53 % dækningsbidrag. Skriv det i ordren, ikke i en mail.

**Leverance-pakken:** `rapport.pdf` (vandmærket, versioneret, kildehenvisninger) · `faktaark.csv` (zone A + C, k≥5) · `claims.json` (proveniens) · `metode.md` (kilder, friskhed, modelversion, forbehold) · leverancekvittering (accept-tidsstempel, audit-ref). **Aldrig zone B-data i en leverance.** Vandmærket bærer modtager-id, så en lækage kan spores.

**Faktura, danske krav:** sælger med CVR og IBAN · køber med CVR · **EAN (13 cifre) hvor krævet** · sekventielt, uafbrudt fakturanummer · dato og leveringsdato · ydelse specificeret · 85.000 + 21.250 moms = **106.250 kr.** · netto 30 (forhandling: netto 14 mod 2 % rabat) · **indkøbsreference/rekvirent**. Manglende EAN eller reference er den hyppigste årsag til, at B2B-fakturaer ikke betales til tiden. Indsaml det i SCOPED, ikke ved fakturering.

**Debitorstyring:** DSO over 45 dage er alarm. Rykkerflow: dag 31 venlig påmindelse → dag 45 rykker + 100 kr. → dag 60 inkassovarsel, automatiseret med manuel pause på strategiske kunder. Kreditnota har eget sekventielt nummer.

### 4.7 Abonnement, eksklusivitet og churn

**Eksklusivitet håndhæves i databasen, ikke i forretningslogikken:**

```sql
CREATE UNIQUE INDEX exclusive_agent_per_zip
  ON subscription (scope_id)
  WHERE product IN ('AGENT_ZIP','AGENT_DISTRICT') AND status='ACTIVE';
```

Bydel og postnummer overlapper: bydel (1–2 postnumre) blokerer postnummer i samme område og omvendt. Det løses med overlap-check plus advisory lock, så to samtidige salg ikke begge lykkes.

**Livscyklus:** `PENDING → ACTIVE → RENEWAL_DUE(d-30) → RENEWED`, med `CANCEL_NOTICE → PENDING_CANCEL → EXPIRED` og `PAYMENT_FAILED → DUNNING → SUSPENDED → EXPIRED`.

To ting, der skal testes: ved `EXPIRED` skal RLS-cachen invalideres inden for 60 sekunder, ellers ser en tidligere mægler stadig leads. Og **køberne følger postnummeret, ikke mægleren** — leads frigives til næste kunde. Det er både rimeligt og det, der gør, at eksklusiviteten kan sælges igen.

**Binding:** 6 måneder på 2.900 (en mindre mægler underskriver ikke et år på et produkt uden historik), 12 måneder på 6.900.

| Metric | Mål |
|---|---|
| `subscription_renewal_rate` | ≥ 70 % (AGENT_ZIP) |
| `leads_per_subscription_per_month` | < 5 i to måneder → kundesucces-opgave |
| `churn_reason` | PRICE / NO_LEADS / NO_DEALS / SWITCHED |
| `dunning_recovery_rate` | følges pr. måned |

### 4.8 Demand Pro og k-anonymitet

Kunden køber aggregeret efterspørgsel pr. område, type og budgetbånd. Ikke identitet, ikke enkeltordrer, ikke præcise beløb. Kontraktformulering: *»Leverancen er aggregeret, anonymiseret efterspørgselsstatistik. Kunden må ikke forsøge re-identifikation. Overtrædelse ophæver adgang uden refusion.«*

**Tre angreb, der skal forsvares mod:**

| Angreb | Eksempel | Modtræk |
|---|---|---|
| Lille celle | 3 villakøbere i 4,0–4,5 mio. | suppress ved k<5 |
| **Komplementær afsløring** | total vises, alle andre celler vises → den skjulte kan udregnes | skjul også nærmeste celle/total |
| **Differencing over tid** | måned 1: 5, måned 2: 6 → én person kan kobles til en hændelse | kvartal eller rullende 3 mdr., afrund til nærmeste 5 |

**Reglen ligger i forespørgslen, ikke i et view.** Et materialized view er et snapshot; en celle med 4 bliver ikke skjult, fordi den faldt fra 6. Maks. 3 dimensioner pr. forespørgsel, mindste geografiske enhed er postnummer, ingen rå rækker i eksport.

**Trusselsmodel, der mangler i bilagene:** i et postnummer med seks verificerede købere er lead-listen ikke anonym, uanset hvad payloaden siger. k≥5 er anvendt på zone C-aggregater, men ikke på det, mægleren faktisk ser. Enten skjules felter ved lav tæthed, eller også skal minimumstætheden for at sælge et postnummer hæves. Det er et salgsargument: *vi sælger ikke et postnummer, hvor vi ikke kan beskytte køberne.*

**Salgsargumentet er gap-analysen** (§3.4) — den kombinerer, hvad der findes, med hvad der efterspørges, og svarer på det spørgsmål en developer faktisk stiller: *skal vi bygge 40 eller 80 — og hvilken type?*

**Datakvalitet vises, ikke skjules.** `coverage` (BBR 0,99 / VUR 0,94 / EJF 0,71), `quality_flags` (VUR forsinket, plan manuelt kurateret), `freshness` og metodereference. En bank stoler mere på data, der indrømmer sin usikkerhed, end på data, der lader som om den er perfekt.

### 4.9 Onboarding til 250 verificerede

Flaskehalsen er ikke teknisk. Regnet baglæns: 250 VERIFIED kræver ~2.500 rå ordrer ved 10 % verifikationsrate, som kræver ~31.000 lokale besøg. Det kan ikke købes. Det skal distribueres — og verifikationsraten skal op.

**Aktiveringsstigen:**

| Trin | Oplevelse | Friktion | Konvertering |
|---|---|---|---|
| 1 | Ser områderapport (anonym) | ingen | 100 % |
| 2 | »Følg området« — e-mail | ét felt | 8–15 % |
| 3 | 4 spørgsmål → QUALIFIED | 60 sek. | 40 % af trin 2 |
| 4 | MitID | 30 sek. | 70 % af trin 3 |
| 5 | Bankbevis upload **eller** »anmod min bank« | 2–10 min. | **35–60 %** af trin 4 |
| 6 | VERIFIED + badge | review 1 hverdag | — |

**Trin 5 er hvor 65 % falder fra.** Derfor: »anmod min bank« som alternativ til upload · vis hvad køberen får (»ejere åbner dialog 3× oftere med verificerede købere« — mål det, brug det) · gem delvist udfyldt ordre · påmindelse efter 48 timer med ét klik tilbage.

**Kill-kriterier:** verifikationsrate under 10 % efter 4 uger betyder, at problemet er onboarding, ikke markedsføring — forenkl trin 5, byg ikke videre. P0 under 8 %: skift budskab eller område. Én kanal over 60 % af de verificerede: fordobl der, drop de andre.

---

## 5. Sikkerhed og jura

### 5.1 Ti invarianter, der aldrig må brydes

1. BFE → adresse-id er **1:mange**.
2. Registerdata er **bitemporal**; historik overskrives aldrig.
3. `order_event` er **append-only**; skemaændringer håndteres ved upcasting ved læsning.
4. **Kun `disclosure` må læse vault.**
5. Kun **VERIFIED med gyldig attest** udløser ejer-kontakt.
6. **Ejerskabsverifikation** kræves, før interesse vises.
7. **Reveal** kræver alle seks guards i én transaktion.
8. Zone C: **k≥5, afrunding, komplementær suppression**.
9. **Én aktiv ordre pr. husstand + scope**; co-buyers på samme ordre.
10. Sletning er **to-lags**: zone B væk, pseudonym event-historik bevaret.

Hver invariant har en guard-test. De tests skrives af mennesker, køres på hver PR, og en rød test blokerer merge uden undtagelse.

### 5.2 Trusselsmodel — de tre kritiske komponenter

| Komponent | Største trussel | Modtræk |
|---|---|---|
| **Vault** | Udvikler eller support udgiver sig for disclosure-service | mTLS + service-identitet; kun `disclosure_service` har DB-rolle; al adgang auditeres i 5 år |
| **Relay** | Lækage af kontaktinfo i fritekst | Deterministisk redaction først, NER/OCR/EXIF, LLM som supplement; karantæne ved gentagne træf |
| **Reveal** | Reveal uden modpartens samtykke, eller med stjålet session | Seks guards i én transaktion, frisk step-up, ingen admin-endpoint, idempotens |

**Tværgående:** re-identifikation i små områder (budget**intervaller**, k≥5, ingen præcis adresse) · insider-adgang (ingen prod-adgang til UA, break-glass med audit og tidsgrænse) · supply chain i AI-genereret kode (afhængigheds- og licensscan, SAST, lockfiles, CODEOWNERS på guards) · prompt injection i agenten (input er zone A, output valideres mod skema, ingen tool-kald til zone B) · backup-lækage (krypteret, EU-only, restore-test, samme adgang som prod) · enumeration (UUID'er, rate limit, ingen sekventielle id'er i public API).

**Race conditions, der skal testes eksplicit:** to samtidige reveal-kald må ikke give to grants · attest kan udløbe mellem check og brug · to samtidige abonnementskøb på samme postnummer.

### 5.3 Retention og sletning

| # | Kategori | Zone | Formål | Retention |
|---|---|---|---|---|
| 1 | Offentlige ejendomsdata | A | analyse | versioneres, ingen persondata |
| 2 | Claims + kildedokumenter | A | områdeprofil | kildelicens; claims 5 år |
| 3 | Køberidentitet (pseudonym, MitID-sub) | B | ordrebog, dedup | aktiv ordre + 12 mdr. |
| 4 | Bankbevis (PDF) | B | verifikation | **90 dage efter review** |
| 5 | Attestfelter | B | kvalitet | til udløb + 12 mdr. |
| 6 | Ejeridentitet + ejerskabsbevis | B | adgangskontrol | verifikation + 90 dage |
| 7 | Ejerrespons | B | matching | 12 mdr. fra sidste aktivitet |
| 8 | Relay-beskeder (redacted) | B | forhandling | 6 mdr. efter lukket tråd |
| 9 | RevealGrant + samtykke | B | bevis | **5 år** |
| 10 | Event-log (pseudonym) | B→C | historik, KPI | **5 år**, bevares ved sletning |
| 11 | Audit (vault/reveal) | B | compliance | **5 år** |
| 12 | Faktura/bogføring | B | bogføringslov | **5 år fra regnskabsårets udløb** |
| 13 | Aggregeret efterspørgsel (k≥5) | C | B2B-produkt | ubegrænset, genberegnes |

**Konflikten skal stå i privatlivspolitikken:** kategori 9, 11 og 12 kan **ikke** slettes på brugeranmodning. Ellers lover vi noget, vi ikke kan holde.

**To-lags sletning:** zone B slettes hårdt (identitet, beviser, tråde); pseudonym event-historik, audit og bogføring bevares. `identity.erased` emitterer en tombstone, og zone C genberegnes. **Tombstone-garantien:** efter sletning findes pseudonymet stadig i events, men ingen tabel kan mappe det til en person. Det er definitionen på anonymiseret historik — og det er det, der gør moaten lovlig.

**Jobs:** dokumenter (dagligt 04:00), tråde, identiteter, ejerrespons, verifikationsudløb (03:00), insights-refresh efter sletning, månedlig retention-rapport. **Ethvert fejlet retention-job er P2.** Et system, der ikke sletter, bryder sit eget løfte.

**Registreredes rettigheder:** indsigt (selvbetjening, øjeblikkelig) · berigtigelse (1 hverdag) · sletning (30 dage, typisk under 1) · tilbagekaldelse (øjeblikkelig, propagerer til suppression) · dataportabilitet (JSON-eksport) · indsigelse (30 dage).

### 5.4 Formidling: den beslutning der ikke kan udskydes

Et fast gebyr er **ikke** et værn. Formidlingsbegrebet handler om aktiviteten — at bringe parter sammen mod vederlag. Match + relay + betalt identitetsafsløring er tættere på formidling end nogen tidligere version af konceptet.

Det gør ikke produktet dårligt. Det gør **model A (advokat eller mægler som formel formidler) til en forudsætning, ikke en mulighed.** Beslutningen i uge 6 kan ikke udskydes til md. 12, fordi hele relay-arkitekturen afhænger af svaret.

**Tre modeller:**

| Model | Konstruktion | Konsekvens |
|---|---|---|
| **A** | Advokat/mægler er formel formidler; Optata leverer teknologi og data | Kræver partneraftale; mindst risiko; mindst margin |
| **B** | Optata er formidler | Kræver tilladelse, god skik, hvidvask-compliance; høj risiko |
| **C** | Optata er ren data-/teknologileverandør; ingen parring mod vederlag | Kræver at reveal ikke er betalt milepæl — ændrer forretningsmodellen |

**Spørgsmålene til juristen** (mødet bestilles nu, ikke i uge 6):

1. Er en betalt identitetsafsløring efter gensidig accept formidling efter ejendomsmæglerloven?
2. Ændrer det sig, hvis betalingen er et fast gebyr for en pakke og ikke en procentdel?
3. Kan Optata levere match og relay uden at være part, hvis afsløringen sker hos en advokat?
4. Hvad kræver et kontaktgrundlag til ejere for interessehenvendelser — og er adressekode nok til at identificere den registrerede ejer?
5. Er sammeje og dødsbo dækket af samme grundlag, eller kræver de separat behandling?
6. Hvad er fortrydelsesretten ved ejerside og pakke, og hvordan dokumenterer vi øjeblikkelig levering?
7. Kan vi opbevare bankbeviser i 90 dage, eller skal de slettes ved afsluttet review?
8. Hvilke krav stiller hvidvaskloven, hvis vi på noget tidspunkt rører penge i en handel? (Svar forventes: ingen — og derfor rører vi dem ikke.)

### 5.5 Forbrugerret og GDPR-dokumenter

**Fortrydelsesret:** ejerside (1.495) og salgspakke (10.000) er fjernsalg af tjenesteydelser med 14 dages fortrydelse. Løsningen er udtrykkeligt samtykke til **øjeblikkelig levering** plus bekræftelse af, at fortrydelsesretten derved bortfalder eller afkortes forholdsmæssigt. En checkbox med gemt `text_version`. Uden den er hver eneste ejerside-salg en potentiel klagesag. Lille checkbox, stor juridisk vægt.

**Dokumenter, der skal findes før lancering:** DPIA · fortegnelse over behandlingsaktiviteter (art. 30) · DPA-skabelon til B2B · subprocessorliste med varsling · privatlivspolitik med undtagelserne · versionerede samtykketekster · juridisk grundlag pr. notifikationstype · beredskab for databrud (72 timer).

**Underdatabehandlere:** MitID-broker (DK/EU) · hosting (EU) · LLM (EU-endpoint, ingen træning på data) · betaling (EU) · medieovervågning (DK/EU) · advokatpartner (DK, selvstændig dataansvarlig) · **UA-udviklingsteam (Ukraine, kun syntetiske data)**.

**Sætningen, der gør due diligence mulig:** *»Udvikling i Ukraine behandler ikke persondata. Produktion er EU-only. Adgang er auditeret og tidsbegrænset.«*

---

## 6. Leveranceplan

### 6.1 Kapacitet

| Rolle | Fra | Kapacitet |
|---|---|---|
| Stifter A (DK) | md. 1 | 50 % byg / 50 % salg |
| Stifter B (DK) | md. 1 | 30 % byg / 70 % salg |
| **Data engineer (UA senior)** | **md. 2** | 100 % |
| Fullstack (UA senior) | md. 3 | 100 % |
| DK-reviewer (fractional) | md. 3 | ~20 % |
| Verifikations-reviewer (DK) | **md. 8** | ~15 t/uge |
| Data/product (UA) | md. 20 | 100 % |

Effektiv byggekapacitet år 1: ~2,3 FTE plus AI-løft. Estimatet er i persondage inkl. AI-assistance, men **ekskl. review og guard-tests** — de lægges oveni som DK-tid.

**Beslutningen, der afgør md. 4:** 90-dages-planen kræver datamodellen i uge 4–7, men omkostningsbasen ansætter data engineer i md. 4 (uge 13). Det kan ikke begge være sandt. **Ansæt fra md. 2.** Merudgift ~60.000 kr. i år 1 og den billigste måde at beskytte den eneste indtægt, der findes i år 1.

### 6.2 Faserne — A før B

Den vigtigste ændring i leveranceplanen: 49 % af omsætningen ved md. 36 kræver **ingen** zone B.

| Produkt | Andel md. 36 | Zone |
|---|---|---|
| Områdeanalyser | 37 % | A |
| Områdeovervågning | 12 % | A |
| Demand Pro | 21 % | A + C |
| Ejerside, pakke, mægler | 28 % | B |

| Fase | Indhold | Måned | Afhængighed |
|---|---|---|---|
| **Spike** | Ét postnummer, DAR+BBR+EJF/tingbog+EBR indlæst, én rapport et menneske kan forsvare | 0–0,75 | Datafordeler |
| **A1** | Registry, bitemporalitet, PostGIS, tæthed, rapport, landing, e-mail-ordre, analyse + faktura | 1–4 | S0, Datafordeler, medielicens |
| **A2** | Overvågning, agent i drift, change-feed | 4–8 | A1 |
| **B1** | Identitet, adressekode, ejerside, notifikation, samtykke, andels-flow, reviewer | 6–11 | A1 + jurist |
| **B2** | Relay, redaction, deal-state, pakke, reveal, mæglerabonnement, eksklusivitet | 11–15 | B1 + formidlingsmodel |
| **C** | Insights, k-anonymitet, Demand Pro | 18–24 | 12 mdr. historik |

**Konsekvens:** første krone i md. 4 hviler ikke på MitID, vault eller jura. Den hviler på et register og en PDF. Det er den eneste måde, tre personer kan levere på fire måneder.

**Sprint-mapping** (bilagenes S1–S7 bevaret som indholdsbeskrivelse):

| Sprint | Fase | Indhold | Estimat |
|---|---|---|---|
| S0 | – | Repo, IaC, zoner, syntetiske data, CI-gates 1–12 | 12 pd |
| S1 | A1 | Registry, tæthed, zone A API, rapport, landing, CURIOS-ordre | 30 pd |
| S2 | A1 | Agent, review-UI, leverance-PDF, faktura | 22 pd |
| S3 | B1 | Identitet, adressekode, ejerside, notifikation, andels-flow | 26 pd |
| S4 | B1 | Samtykke-ledger, betaling 1.495, verifikationskø, genverifikation | 22 pd |
| S5 | B2 | Relay, redaction, deal-state, pakke, reveal, audit | 30 pd |
| S6 | B2 | MitID Erhverv, eksklusivitet, lead-liste, abonnement, dunning | 20 pd |
| S7 | A1→ | Withdraw, expire, afmeld, sletning, retention-jobs (designet i S0) | 16 pd |
| S8 | C | Insights, k-anonymitet, Demand Pro | 26 pd |

Sum år 1: ~184 persondage kerne + ~40 pd DK-review ≈ **224 pd**. Med 2,3 FTE og 250 arbejdsdage minus møder og salg er planen **stram men mulig** — forudsat at S0 og adgangene ikke skrider.

### 6.3 S0, S1 og S2 — det der skal bygges først

**S0 (uge 1–3):** monorepo med modulgrænser og import-lint · IaC med EU-miljøer · CI-gates 1–12 som kørbare jobs · zone-model, DB-roller og RLS · syntetisk datagenerator med vandmærke · kontraktskelet (OpenAPI, event-envelope, upcaster) · append-only audit med trace-id · P1-alarmer · CODEOWNERS og ADR-skabelon.

*Definition of done:* `make dev` giver en fuld database uden persondata. `app_role` kan ikke UPDATE/DELETE på `order_event`. `disclosure_service` er den eneste rolle med SELECT på kontaktdata. En PR med rød guard-test kan ikke merges, og der er ingen override-knap.

**S1 (uge 3–8):** adapter-framework med checkpoint, idempotens og quarantine · DAR, EBR, BBR, VUR · bitemporal upsert og `property.changed` · BFE↔adresse-samling og `dwelling_count` · PostGIS og tile-cache · tæthedsview · zone A API · områderapport · landing og adressesøgning · CURIOS-ordre med magic link og dedup · FX-01/02/03-fixtures og guard-tests.

**S2 (uge 6–10):** kilde-register med licensfelt · claim-tabel med DB-constraints · agent-runner mod EU-LLM med cache · **deterministisk validator** · dedup på tværs af kilder · review-UI med citat-highlight · **publish-gate** med `reviewed_by` · leverance-render med vandmærke · scope-kontrakt med EAN og reference · accept-kvittering · faktura med sekvensnummer, moms og idempotens · guard-tests FX-A1…A6.

**Røde felter — må ikke AI-genereres:** den deterministiske validator, publish-gaten, ejerskabsverifikationen, reveal-guards, RLS, k-anonymitet, sletning og finansiel logik. Det er præcis dér, pengene og risikoen er.

### 6.4 Kritisk vej — kalendertid, ikke kodetid

```
Uge 1: Datafordeler-aftale ─┬─→ spike ─→ S1 ─→ S2 ─→ første krone (md. 4)
Uge 1: EJF-berettigelse?   ─┘
Uge 2: Medielicens ─────────┘
Uge 6: Jurist (kontakt + formidling) ─→ S3/S4 ─→ S5/S6
Uge 6: Data engineer ansat (md. 2) ───┘
```

| Blokerer | Hvis sen | Modtræk |
|---|---|---|
| Datafordeler-adgang | S1 kan ikke starte | Bestil uge 1; byg mod syntetiske data og offentlige dumps |
| EJF afvist | kun langsommere verifikation | Adressekode + manuel kø fra dag 1 — **ikke** et projektstop |
| Medielicens | S2 kan ikke levere | Brug offentlige feeds og kommunale sager indtil |
| Jurist | S3/S4 må ikke lanceres | Byg bag feature-flag; tænd først efter godkendelse |
| Data engineer | første krone md. 6–7 | Ansæt md. 2 |

**Rækkefølge-regler:** S0 før alt · guards skrives i samme PR som domænekoden, aldrig bagefter · alt juridisk ufærdigt deployes mørkt · retention designes i S0 og bygges sidst · ingen mæglerprodukter før P2-tæthed er bevist.

---

## 7. Leverancemodel og governance

### 7.1 Kravspecifikation til UA-teamet

**Kerneprincip: kontrakten er specifikationen, koden er output, CI er dommeren.**

| Part | Ejer |
|---|---|
| Optata (DK) | kravspec, kontrakter, guards, kundekontakt, salg, juridisk grundlag, prod-drift |
| UA-team | implementation inden for kontrakterne, tests, adapters, UI, workers |
| DK-reviewer | godkendelse af al finansiel, juridisk og sikkerhedskritisk logik |

| Område | Må de? |
|---|---|
| UI-komponenter, layouts, kort, autocomplete | ✅ frit, AI-assisteret |
| CRUD, DTO'er, API-klienter, integrationer | ✅ inden for OpenAPI |
| Ingestion-adapters, feltmapping, transformation | ✅ med fixtures |
| Workers, jobs, observability | ✅ |
| **Guards, RLS, vault, reveal, økonomi, faktura, sletning** | ❌ **kun DK, menneskeligt skrevet** |
| Prod-adgang | ❌ aldrig; kun break-glass med audit |

**Definition of done:** alle guard-tests grønne · CI-gates 1–12 bestået · audit dækker zone B · ADR skrevet ved større beslutning · runbook opdateret · DK-review på CODEOWNERS-stier · ingen prod-persondata uden for EU-prod.

### 7.2 CI-gates og guard-indeks

Gates 1–12 dækker: kontraktkonformitet · modulgrænser · schema-validering med `additionalProperties: false` · zone-lækage i public payload · ingen CPR i nogen tabel eller log · syntetiske data i dev · append-only på event og audit · RLS-dækning · migrations-review · ingen prod-lignende data i fixtures · tekstlint mod anbefalingssprog i leverancer · guard-suite grøn.

**Guard-tests (skrives af mennesker):**

```
vault_only_disclosure          reveal_all_six_guards         reveal_concurrent_idempotent
reveal_toc_tou_expiry          redaction_corpus              rls_agent_scope
k_anonymity                    complementary_suppression     too_many_dimensions
no_zone_b_in_public            erasure_preserves_events      tombstone_unmappable
ownership_revoked_on_transfer  address_code_single_use       andels_not_ejf
sameje_all_consent             exclusive_agent_per_zip       concurrent_purchase
order_one_per_household        claim_needs_source            publish_requires_approved
invoice_sequential_idempotent  density_denominator           no_prod_like_data
```

### 7.3 ADR-register

| ADR | Beslutning | Status |
|---|---|---|
| 001 | Modulær monolit (Python/FastAPI + Next.js), ikke microservices | Accepteret |
| 002 | Postgres + PostGIS, bitemporal via ranges | Accepteret |
| 003 | Event-sourcet ordrebog, append-only, upcasting ved læsning | Accepteret |
| 004 | Tre zoner håndhævet i DB-roller og RLS | Accepteret |
| 005 | MitID via broker; **pseudonymt PID, ingen CPR lagret** | Accepteret |
| 006 | Progressiv identitet: anonym → e-mail → MitID → attest | Accepteret |
| 007 | Anonym front-end, relay, gensidig reveal, parvist pseudonym | Accepteret |
| 008 | Reveal som betalt milepæl, **fast gebyr** | Accepteret — **juridisk afklaring uge 6** |
| **009** | **Ejerskab: adressekode pr. brev som primær; EJF og tingbog som supplerende; andelsattest og manuel kø** | **Accepteret (rettet i v5)** |
| 010 | k-anonymitet k=5, afrunding, komplementær suppression, håndhævet i forespørgsel | Accepteret |
| 011 | Agent: claim-pipeline med tvungen proveniens og menneskelig publish-gate | Accepteret |
| 012 | UA-udvikling på syntetiske data, EU-only produktion | Accepteret |
| **013** | **Data engineer fra md. 2** | **Til beslutning — afgør første krone** |
| 014 | Eksklusivitet håndhævet med unikt index; køberne følger postnummeret | Accepteret |
| 015 | To-lags sletning med tombstone | Accepteret |
| 016 | Byg A før B: zone A-produkter før al identitetsinfrastruktur | Accepteret |
| 017 | Verifikations-reviewer fra md. 8; loft 150/md. i pilot | Accepteret |
| 018 | Bankpartner som kapacitetsforudsætning, md. 3 | Til beslutning |

---

## 8. De næste 14 dage

| # | Handling | Hvem | Frist |
|---|---|---|---|
| 1 | Bestil **Datafordeler-adgang** og bekræft EJF-berettigelse skriftligt | Stifter A | dag 1 |
| 2 | Bestil **medielicens** (feeds + uddrag) — ikke arkiv | Stifter B | dag 3 |
| 3 | Bestil **møde med jurist** til uge 6; send de otte spørgsmål i §5.4 | Stifter A | dag 2 |
| 4 | Indhent **tre UA-tilbud** (data engineer, fullstack) og afgør scenarie A/B | Stifter B | dag 10 |
| 5 | Ansættelsesproces data engineer igangsat | Stifter A | dag 5 |
| 6 | Byg **spike**: ét postnummer, fire kilder, én rapport | Data engineer | dag 21 |
| 7 | Kontakt fem foreninger i pilotområdet; to møder i kalenderen | Stifter B | dag 14 |
| 8 | Åbn banksamtale om forhåndsgodkendelse som indgang | Stifter A | dag 14 |
| 9 | Beslut pilotområde (8–15.000 boliger) ud fra tæthed og foreningsdækning | begge | dag 7 |
| 10 | Send teaser til de tre investorer med rettet tal (70–90.000 handler) | Stifter B | dag 10 |

**Det, der ikke kan vente:** Datafordeler, juridisk møde og data engineer. Alt andet i planen tåler en uge.

**Det, der bevidst ikke gøres nu:** CPR-opløsning, MitID-produktionsaftale, fuld event-versionering, 5-års audit som krav i S1, Postgres-bus, 24 måneders syntetisk historik. Alt sammen rigtigt senere. Intet af det bør stå i vejen for md. 4.

---

## 9. Hvad dette dokument ikke løser

Ærlighed hører med i et mastersk dokument.

1. **Fornyelsesraten på 70 % er ikke testet.** Den bærer 44.370 kr. pr. bydel. Falder den til 50 %, er recurring-benet 30 % mindre, og bundpunktet flytter sig. Det er P3-kriteriet, der afgør, om abonnementet er et abonnement.
2. **Tætheden på 25/1.000 er ikke bevist noget sted.** Den kræver ~12.500 lokale besøg pr. postnummer. Hvis distributionen ikke virker, virker forretningen ikke — og det opdages først i md. 5–7.
3. **Formidlingsspørgsmålet kan ende i model C**, hvor reveal ikke må være en betalt milepæl. Så ændrer forretningsmodellen sig, ikke bare juraen.
4. **Arbejdskapitalen er et skøn**, ikke en beregning fra en faktisk debitorbog. Den lukkes med en kassekredit.
5. **DMU'en er ikke kortlagt.** Alle tal bygger på, at en developer, en bank og en mægler køber det samme produkt af den samme sælger. Det gør de ikke nødvendigvis.
6. **Konkurrenten er ikke analyseret.** Dingeo, OIS og mæglernes egne køberkartoteker findes allerede. Vores svar er anonymisering, verifikation og historik — men det er en antagelse, ikke en måling.

---

## Bilag A — Kontraktprincipper

**Event-envelope** (alle hændelser, uanset type): `event_id`, `type` (`domæne.hændelse`), `schema_version` (semver), `occurred_at`, `recorded_at`, `actor`, `zone`, `aggregate`, `trace_id`, `payload`. `additionalProperties: false` overalt — det er en sikkerhedskontrol, ikke pedanteri: et felt, der ikke er i skemaet, kan ikke lække.

**Fejlkoder** er del af kontrakten, ikke fritekst: `ORDER_ALREADY_ACTIVE`, `OWNERSHIP_NOT_VERIFIED`, `VERIFICATION_EXPIRED`, `MISSING_CONSENT`, `STEP_UP_REQUIRED`, `REVEAL_BLOCKED`, `PROFILE_NOT_APPROVED`, `SUBSCRIPTION_EXPIRED`, `MESSAGE_REDACTED`, `K_ANONYMITY_BLOCKED`, `RATE_LIMITED`, `NO_SOURCE`, `NO_DATE`, `QUOTE_MISMATCH`, `OPINION`, `EAN_REQUIRED`, `SCOPE_INCOMPLETE`, `REVISION_NOT_ACCEPTED`, `TOO_MANY_DIMENSIONS`, `GEO_TOO_GRANULAR`.

**API-flade:**

| Område | Endpoints |
|---|---|
| Public (zone A) | `/areas`, `/areas/{id}/profile`, `/properties/{address_id}` |
| Ordrer | `POST /orders` (idempotent, e-mail-session) |
| Analyser | `POST /analyses`, `/scope`, `/deliver`, `/accept`, `/invoice`, `/revision` |
| Demand Pro | `/v1/demand/areas/{id}/summary`, `/matrix`, `/history`, `/v1/areas/{id}/changes`, `/claims`, `/exports` |
| Internt | `/internal/claims/{id}/review`, `/internal/profiles/{id}/publish`, `/webhooks/payment` |

**Auth-niveauer:** anonym · e-mail-session · MitID (OIDC) · MitID step-up (≤5 min) · MitID Erhverv (CVR) · staff. Følsomme kald kræver step-up, ikke bare login.

---

## Bilag B — Dokumentkort

| Fil | Rolle |
|---|---|
| **Optata - Projektgrundlag v5.0.md** | dette dokument — master |
| Optata - Forretningsplan v4.2.md | forretningsdelen i sin oprindelige form (historik) |
| Optata - Arkitekturreview v4.2.md | reviewet af S1–S5-specifikationen (historik) |
| Optata - Finansiel Model 36 Mdr.xlsx | 36-måneders model, leverancemodel A/B, ordrebog, cash-flow & WC |
| attachments/altf73/*.txt | de elleve tekniske bilag, som dette dokument konsoliderer |

Ved uenighed mellem dette dokument og bilagene gælder dette dokument. Ved uenighed mellem dette dokument og regnearket gælder regnearket for tal, dette dokument for antagelser.
