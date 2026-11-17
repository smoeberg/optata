# Optata — produktlukning, handelsrejse og udviklingsparathed

**Version:** 1.0 · **Dato:** 17. november 2026  
**Status:** Audit og anbefalinger · ikke en godkendt produktbaseline

> Dette dokument samler repository-gennemgangen og input fra to eksterne AI-analyser. Det ændrer ikke v5.2, godkender ikke juridiske gates og giver ikke tilladelse til produktionsbehandling. Det skal bruges som sidste beslutningsgrundlag før konceptet låses.

## 1. Konklusion

Optata har en tydelig strategisk retning: Struktur C, hvor Optata ejer efterspørgselsrelationen, mandatoplevelsen og budrails, mens godkendte partnere/mæglere udfører afgrænsede opgaver. Den tekniske retning er også forholdsvis moden: modulær monolit, datazoner, bitemporal registerhistorik, append-only events, least privilege, audit og eksplicitte juridiske release gates.

Men dokumentationen beskriver endnu ikke et komplet, sammenhængende kundeprodukt fra første interesse til gennemført og registreret handel.

De største produktmangler er:
1. Salgsklargøring og præsentation af en bolig, der ikke allerede findes i et licenseret feed.
2. Fremvisning, spørgsmål/svar og sikker praktisk dialog.
3. Den fulde proces efter budaccept: købsaftale, finansiering, rådgivere, skøde, tinglysning, refusion, overtagelse og afslutning.
4. En samlet service-/fulfillmentmodel med tydeligt ansvar, partnerroller og support.
5. En gennemarbejdet køber- og sælgerrejse med skærme, mikrocopy, tomme tilstande, fejl og recovery.
6. Pris-, betalings- og enhedsøkonomi.
7. En konkret plan for markedsopstart og likviditet pr. geografi og boligsegment.
8. En skalerbar driftsmodel for verifikation, sagsbehandling, support, tvister og partnerkapacitet.

**Vurdering:** Optata kan fortsætte afgrænset teknisk udvikling på S0/S1 og syntetiske data. Konceptet er ikke klar til at blive låst som en komplet handelsplatform, og S3–S7 må ikke bygges som produktionsflows, før de respektive sikkerheds- og juridiske forudsætninger er opfyldt.

## 2. Grundlag og status

Gennemgangen omfatter den aktuelle dokumentationsstruktur på main, herunder:
- Projektgrundlag v5.2, arkitektur v2.1 og Architecture Contracts v1.0.
- ADR-016 til ADR-020 samt den dobbelte ADR-017.
- S0/S1 og S3–S6 backlogs, dokumentationsindeks og CI-gates.
- Designoplæg, skærm-/tekstmateriale, Campaign, listings, efterspørgselsgravitation og SaleMandate/OfferLedger.
- Bilag 06–16, juridiske spørgsmål L1–L48, feed-aftale og runbook-indeks.
- Repository-audit af 17. november 2026.

PR #10 er merged og indeholder Zone A least-privilege-rettelsen A-01. Auditdokumentet blev skrevet før denne rettelse og skal opdateres: A-01 er implementeret i kode, men skal stadig have dokumenteret uafhængigt DB-/sikkerhedsreview, før det betragtes som produktionsgodkendt.

PR #11 (RelocationCase) og PR #12 (Role & Authority Model) er merged. ADR-019, ADR-020 og selve rollemodellen står fortsat som Proposed. Architecture Contracts v1.0 står ligeledes som Proposed. Merged betyder derfor ikke, at disse forslag er endeligt reviewet, implementeret eller juridisk godkendt.

## 3. Vurdering af de to AI-agenters input

### Enighed — fund der bekræftes

Begge analyser rammer rigtigt på følgende:
- Den komplette køber- og sælgerrejse er ikke beskrevet som ét end-to-end-produkt.
- Accept i OfferLedger er ikke det samme som en gennemført handel.
- DIRECT er et mål for en udførelsesvej, ikke en færdig leverancebeskrivelse.
- Der mangler udbudsproduktion, fremvisning og en praktisk erstatning for fri relay-dialog.
- Notifikationskanaler, betaling, priser, support og tvister er ikke afklaret.
- 20 %-ambitionen mangler en bottom-up markeds-, kapacitets- og enhedsøkonomimodel.
- En klikbar prototype med syntetiske data er en god måde at afsløre huller, før der investeres i omfattende featurekode.

### Nuancer og rettelser

1. **Der findes designmateriale.** Forside, adressekort, områdeprofil, proof-card, B2B-bestilling, min side, e-mailtekster og enkelte flows er beskrevet. Problemet er, at materialet er fragmenteret og delvist baseret på forældede produktmodeller. Det er ikke en samlet, gældende handelsrejse.
2. **MitID er ikke en købergaranti.** Identitet, QUALIFIED, VERIFIED, finansieringsdokumentation, dokumentets gyldighed og konkret finansieringsforbehold skal være adskilte begreber.
3. **Mandat er ikke salgsproduktion.** Et mandat giver en autoriseret proces; det skaber ikke automatisk fotos, dokumenter, salgsopstilling eller fremvisning.
4. **Ingen fri relay-chat betyder ikke ingen dialog.** Der skal være sikker, afgrænset bolig-Q&A og fremvisningskoordinering, mens formelle bud alene går i OfferLedger.
5. **20 % kræver mere end mæglerafhængighed.** Kundeværdi, gennemførelseskvalitet, forsyning af boliger, partnerkapacitet og tillid skal være stærkere end den nuværende proces.
6. Forslaget om 25 verificerede købere og 3 sælgere kan bruges som en pilot-hypotese, men ikke som en generel likviditetsregel. Tæthed skal måles pr. geografi, boligtype og prisinterval.

## 4. Den komplette handelsrejse — produktkrav

Optata skal fremstå som ét sammenhængende forløb. Kunden skal ikke forstå de interne moduler, partnere eller juridiske arbejdsgange. Kunden skal kende sin status, sin næste handling, hvem der har ansvaret, og hvad det koster.

| Fase | Køberens oplevelse | Sælgerens oplevelse | Manglende produktkapacitet |
|---|---|---|---|
| 1. Opdagelse | Forstår markedet og finder relevante områder/boliger uden unødigt login | Kan finde sin bolig og forstå Optatas tilbud | Indhold, SEO, acquisition, ærlige tomme tilstande og markedstilgængelighed |
| 2. Købsønske | Angiver område, boligtype, behov, økonomisk ramme og tidshorisont | — | Endeligt onboardingflow, QUALIFIED/VERIFIED-definitioner, finansieringsbevisets livscyklus |
| 3. Sælgerens start | — | Finder bolig, beviser rådighed/ejerskab og ser troværdig efterspørgsel | Claim-flow, EJF/Tingbog/andel/selskab/dødsbo/fuldmagt og manuel review |
| 4. Salgsklargøring | Kan se en fuldstændig og troværdig boligpræsentation | Får hjælp til at gøre boligen salgsklar | Fotos, plantegning, beskrivelse, dokumentindsamling, rapporter, kvalitetssikring og publicering |
| 5. Fremvisning og spørgsmål | Kan anmode om, booke og gennemføre fremvisning; få svar | Kan koordinere adgang og spørgsmål uden uønsket kontakt | Booking, kalender, adgang, aflysning, Q&A, ansvar og sikker kommunikation |
| 6. Bud og forhandling | Afgiver og følger bud, frister og modbud | Sammenligner bud og træffer beslutning; alle nødvendige ejere godkender | Budregler, synlighed, runder, frister, betingelser, attestudløb, konflikter og race/replay |
| 7. Aftale og gennemførelse | Ved hvad der skal underskrives, hvornår og af hvem | Ved hvem der håndterer dokumenter og forpligtelser | Købsaftale, rådgivere, finansiering, forbehold, skøde, tinglysning, refusion, betaling og forsikring |
| 8. Overtagelse og efterforløb | Følger overtagelse, nøgler og praktiske opgaver | Afslutter handlen og får dokumentation | Overtagelsescheckliste, aflæsning, nøgler, fejl/klager, support, retention og afslutning |

### 4.1 Køberens kerneflow

1. Besøg Optata og søg uden at oprette konto.
2. Opret en købsintention med få, forståelige spørgsmål.
3. Log ind med MitID, når identitet er nødvendig.
4. Dokumentér købeevne via en godkendt metode; vis tydeligt status, kilde, udløb og eventuelle forbehold.
5. Se relevante aktive listings/mandater med forklaring på match og datakvalitet.
6. Se boligmateriale og anmod om fremvisning.
7. Stil spørgsmål i en afgrænset boligdialog.
8. Afgiv et struktureret bud.
9. Følg modbud, accept, afvisning og frister.
10. Følg købsaftale, finansiering, rådgiveropgaver og overtagelse i samme sagsoversigt.

**Produktkrav:** Køberen må ikke forveksle et match med tilgængelighed, et VERIFIED-stempel med ubetinget finansiering eller en platformaccept med en juridisk bindende købsaftale.

### 4.2 Sælgerens kerneflow

1. Find egen bolig via adresseopslag.
2. Identificér sig med MitID og dokumentér ejerskab/rådighed.
3. Få en forståelig forklaring af, hvad efterspørgselsdata viser, hvor friske data er, og hvad de ikke beviser.
4. Vælg om boligen skal klargøres og bringes i markedet.
5. Vælg præcist mandat, vilkår, varighed og udførelsesvej.
6. Alle nødvendige ejere/parter godkender individuelt samme vilkårsversion.
7. Gennemfør boligklargøring og godkend præsentationen.
8. Håndtér fremvisninger og spørgsmål.
9. Modtag sammenlignelige bud og vælg næste handling.
10. Følg aftale og overtagelse frem til afsluttet handel.

**Produktkrav:** Det skal være tydeligt, hvad sælgeren overlader til Optata/partneren, hvad sælgeren selv skal gøre, hvad der koster penge, og hvordan suspension/tilbagekaldelse virker. En tilbagekaldelse kan stoppe fremtidige platformshandlinger, men kan ikke nødvendigvis ophæve allerede indgåede aftaler eller tilbagekalde lovligt videregivne kopier.

### 4.3 Boligpræsentation, fremvisning og dialog — manglende domæne

Listings fra licenserede feeds løser ikke DIRECT-sælgerens behov. Der skal være en selvstændig capability til:
- Oprettelse og versionering af salgsopstilling.
- Fotos, plantegning, boligbeskrivelse og strukturerede boligfakta.
- Dokumentliste og dokumentstatus med ansvarlig part.
- Kvalitetskontrol, kilde/proveniens og sælgerens godkendelse.
- Fremvisningsanmodning, tidsforslag, bekræftelse, aflysning og fremmøde.
- Strukturerede spørgsmål/svar og dokumentdeling med korrekt scope.
- Statusændringer, der stopper match og kampagner, når boligen ikke længere er tilgængelig.

**Anbefaling:** Opret en produkt-/domænespecifikation for PropertyPresentation og Viewing eller tilsvarende tydelige capabilities. De må ikke blandes ind i OfferLedger. Formelle bud er transaktioner; spørgsmål og fremvisninger er boligservice.

### 4.4 Efter accept — Fulfillment/Completion mangler

Et accepteret bud skal oprette et synligt gennemførelsesforløb. Det skal som minimum definere:
- Hvornår og af hvem der udarbejdes købsaftale.
- Hvem der kontrollerer vilkår, bilag og forbehold.
- Købers bank-/realkreditproces og sælgers indfrielse.
- Advokatens/berigtigelsespartnerens opgaver og ansvar.
- Tilstandsrapport, elinstallationsrapport, energimærke og forsikringsvalg, hvor relevant.
- Skøde, tinglysning, refusionsopgørelse og afregning.
- Betalingens parter og betalingsvej. Optata må ikke utilsigtet komme til at holde købesum.
- Overtagelsesdato, nøgler, måleraflæsning og dokumenteret aflevering.
- Hvad der sker ved afslag fra bank, forbehold, fristoverskridelse, tvist eller ophævelse.

**Anbefaling:** Specificér et FulfillmentCase/completion-workflow som koordinator. Det skal ikke eje den juridiske købsaftale eller erstatte advokat/mægler/bank; det skal vise ansvar, opgaver, frister, dokumentstatus og eskalering. Det skal følge saga-/outbox-kontrakterne og have eksplicit manuel recovery.

## 5. Budprocessen: hvad skal besluttes ud over state machine?

S5 beskriver append-only bud, modbud, accept, afvisning, tilbagetrækning og udløb. Det er et godt teknisk udgangspunkt, men følgende produktregler mangler:

1. Er bud åbne eller lukkede for andre købere? Hvilke oplysninger ser sælger, køber og udfører?
2. Kan sælger modtage og sammenligne flere samtidige bud? Hvordan vises betingelser og finansieringsstatus?
3. Er der budrunder, frister, forlængelser eller en fast svarfrist?
4. Kan køber ændre/erstatte eget bud, og hvordan bevares kæden?
5. Hvilke betingelser er tilladt som strukturerede felter, og hvilke kræver juridisk review?
6. Hvad sker der med et aktivt bud, hvis køberens attest udløber eller ændres?
7. Hvad sker der med åbne bud ved mandatets suspension, tilbagekaldelse eller udløb?
8. Hvilke handlinger kræver godkendelse fra alle sælgere/medejere?
9. Må en mægler/udfører afgive eller acceptere bud på vegne af en part, og med hvilken verificeret authority?
10. Hvornår er der alene tale om platformstatus, og hvornår er der indgået en juridisk bindende aftale?

De syv race-/fejlscenarier fra agentinputtet skal være førsteklasses accepttests: dobbelt accept, accept mod mandattilbagekaldelse, accept mod bududløb, modbud under accept, attestudløb, manglende medejeraccept og replay. Tilføj også partner-handoff-fejl, manglende dokumenter og manuel tvist/recovery.

**Vigtigt:** Reglen om ét aktivt bud pr. køber pr. mandat må ikke vedtages automatisk. Den kan være uhensigtsmæssig i en konkurrencesituation. Beslut først den ønskede budmekanik og test derefter reglen.

## 6. Simpel kundeoplevelse — produktprincipper

Optata skal skjule organisatorisk kompleksitet, ikke skjule konsekvenser.

1. Én konto og én samlet sagsoversigt for hver person.
2. Én tydelig næste handling ad gangen; ingen lange formularer uden behov.
3. Oplysninger indtastes én gang og genbruges kun med lovligt grundlag og relevant samtykke.
4. Hvert objekt viser status, ansvarlig, næste frist og hvad der mangler.
5. Alle økonomiske vilkår og gebyrer vises før accept.
6. Verificerede fakta, estimater, mulige match og uafklarede forhold vises forskelligt.
7. Kunden kan altid se, hvem der har adgang til hvilke oplysninger og hvorfor.
8. Ingen skjulte standard-samtykker eller dark patterns; afvisning, pause og tilbagekaldelse skal være forståelige.
9. Ingen blindgyder: hver fejl har en forklaring, en genoptagelsesvej eller en menneskelig eskalering.
10. Mobil-først, WCAG AA, tastatur, skærmlæser og letforståeligt dansk.
11. Partneren arbejder i Optatas opgave-/sagsflade; kunden skal ikke koordinere via parallelle mails og regneark.
12. En synlig menneskelig hjælpevej er nødvendig i kritiske situationer.

### Tillidssignaler, der skal være synlige

- Hvem er verificeret, og hvad er konkret verificeret?
- Hvornår er oplysningerne senest kontrolleret?
- Hvem har adgang til sagen og til hvilke data?
- Hvad er Optatas rolle, og hvem er juridisk ansvarlig udfører?
- Hvad koster næste skridt, og hvad kan refunderes?
- Hvad betyder accept juridisk?
- Hvordan stopper eller eskalerer kunden processen?

## 7. Kanaler, dialog og notifikationer

Dokumentationen blander tre forskellige spørgsmål: e-mail som identitet, e-mail som ordrekanal og e-mail som notifikation. v5.2 forbyder e-mail-identitet/-ordre, mens S0-backloggen siger "ingen e-mail nogen steder", og ældre designmateriale indeholder e-mailflows.

**Beslutning før UX og S3/S6:** Fastlæg kanalpolitik:
- Optata-inbox som autoritativ kilde til alle sagsmeddelelser.
- Om push/SMS/e-mail må bruges som diskrete påmindelser uden følsomt indhold.
- Om eksterne kanaler kræver særskilt opt-in, og hvordan afmelding/frekvens/quiet hours fungerer.
- Hvordan kunden modtager kritiske frist- og sikkerhedsmeddelelser, hvis vedkommende ikke logger ind.
- Hvilke samtaletyper der findes: boligspørgsmål, fremvisning, dokumentafklaring, formelle bud og support. De må ikke blandes.

Anbefalet retning: ingen e-mail som identitet eller ordre; inbox er sandhedskilden. Eksterne kanaler bør kun være valgfrie, minimale alarmer efter eksplicit kanalvalg og juridisk review. Den endelige kanalpolitik skal være én beslutning i v5.2 og afspejles i samtykke, rollemodel og design.

## 8. Pris, betaling og forretningsmodel

v5.2 siger korrekt, at v5.1-priser er historiske hypoteser. Det er dog ikke nok til at designe produktet. Før konceptet låses, skal betalingsarkitekturen og betalingsøjeblikkene være besluttet, selv om alle priser ikke nødvendigvis er endeligt valideret.

Beslut:
- Hvem betaler i DIRECT: sælger, køber eller begge?
- Hvad betaler kunden for: mandat, klargøring, fremvisning, juridisk fulfillment, abonnement eller afsluttet handel?
- Hvad betaler en AGENT_EXECUTED-sælger, og hvad betaler mægleren?
- Hvilke ydelser er gratis, betalte eller betinget af gennemført handel?
- Hvornår opkræves beløb: ved bestilling, aktivering, levering eller gennemført handel?
- Fortrydelse, refundering, delvis levering, aflysning, tilbagekaldelse og tvister.
- Faktura, moms, betalingsudbyder, chargeback og bogføring.
- Hvem bærer omkostningen ved manuel review, partneropgaver, support og mislykket handel?

Byg enhedsøkonomien pr. gennemført handel: omsætning minus betaling/partnerhonorar, verifikation, support, kundetilgang, data, drift, forsikring og juridisk/compliance. Ingen historisk pris fra v5.1 må bruges som valideret pris.

## 9. 20 %-ambitionen — markeds- og kapacitetsmodel

Boligsidens opgørelse angiver 100.294 solgte boliger i 2025. 20 % svarer til ca. 20.059 handler. Villaer/rækkehuse og ejerlejligheder udgjorde tilsammen 81.253 handler, svarende til ca. 16.251 ved 20 %. Kilde: https://www.boligsiden.dk/pressemeddelelser/2025-boed-paa-100000-bolighandler-og-ny-rekord-i-storbyernes-boligssalg

Før målet bruges i en forretningsplan, skal nævneren defineres: helårsboliger alene eller også sommerhuse, andelsboliger, grunde og øvrige boligtyper? Markedsandel skal måles på gennemførte handler, ikke ordrer, matches, mandater eller bud.

Ved 20.059 handler årligt svarer det til ca. 55 handler pr. kalenderdag eller ca. 80 pr. arbejdsdag ved 250 arbejdsdage. Det er et nationalt driftskrav, ikke blot et serverkrav.

### Den manglende bottom-up-model

Modellen skal regne baglæns fra gennemførte handler:
- Antal gennemførte handler pr. år og boligsegment.
- Konvertering fra besøgende → købsintention → QUALIFIED → VERIFIED.
- Matchrate pr. geografi, boligtype og prisinterval.
- Sælger-inbound → ejerskabsverifikation → mandat → aktiv listing.
- Listing → fremvisning → bud → accept → underskrevet aftale → registreret handel.
- Gennemsnitlig tid i hvert trin og andel der falder fra.
- Partnerkapacitet, manuel verifikation, supporttimer og tvistfrekvens.
- CAC for køber og sælger, dækningsbidrag pr. handel og kapitalbehov.

### Lokal likviditet og cold start

Start ikke med at antage, at landsdækkende dækning giver værdi. Vælg et pilotområde og et afgrænset boligsegment. Mål matchbar efterspørgsel og reelt udbud i samme geografiske/prismæssige celler. 25 købere og 3 sælgere kan være en testhypotese, men succeskriteriet skal være, at der opstår relevante matches, fremvisninger, bud og en gennemført handel.

Acquisition skal respektere P-04: ingen uopfordret ejerkontakt. Mulige kanaler er inbound, områdesider, indhold, betalt annoncering, anbefalinger og frivillige partnerkanaler. Optata skal kunne give køberen værdi, selv om der endnu ikke er et aktivt mandat i præcis det ønskede område.

### Foreslåede skaleringsmilepæle

1. Én gennemført handel fra ende til ende i ét pilotsegment.
2. Ti handler med gentagelig proces og målbar kundetilfredshed.
3. 100 handler med dokumenteret partner- og supportkapacitet.
4. 1.000 årlige handler med positivt dækningsbidrag pr. relevant segment.
5. 5.000 årlige handler med regional playbook og kontrolleret kvalitet.
6. 15.000–20.000 årlige handler med national kapacitet.

Milepælene er styringsforslag, ikke prognoser eller løfter.

## 10. Roller, autoritet og partnere

Role & Authority Model v1.0 er et godt fundament, men Proposed-status skal respekteres. Før transaktionsflows implementeres, skal følgende være entydigt:
- Personens relation til den konkrete sag: køber, sælger, medejer, medkøber, husstandsmedlem, fuldmægtig, bobestyrer mv.
- Organisation og medlemskab: mæglerfirma, advokatfirma, bank, vurderings-/inspektionspartner.
- Professionel udpegning og aktiv authority på det konkrete mandat/arbejdsopgave.
- Teknisk service principal adskilt fra menneskelig identitet.
- Capability, resource scope, purpose, juridisk grundlag, consent, assurance og gyldighed.
- Delegation, tilbagekaldelse, break-glass og audit.

Partnerkataloget skal også konkretiseres: ejendomsmægler, advokat/berigtigelsespartner, bank/realkredit, fotograf, plantegning, byggesagkyndig, energimærke, forsikring og eventuelle andre leverandører. For hver partner skal opgaver, ansvar, datadeling, SLA, betaling, forsikring og eskalering være beskrevet.

En RelocationCase må koordinere flytningen, men må ikke give en husstandsmedlem adgang til en andens identitet, bankbevis, bud eller mandat. Hver handel forbliver selvstændig.

## 11. Juridiske, data- og sikkerhedsgates

Følgende må ikke omgås for at få en hurtig MVP:
- LG-1: Optatas og partnerens formidlerrolle og ansvar.
- LG-2: persondata, MitID, identitet, attest, vault, retention og DPIA.
- LG-3: register-, medie-, IP- og tredjelandsrettigheder.
- LG-4: listing/feed-licens og attribution.
- LG-5: mandat, bud, accept, udførerrolle og deltagelsesvilkår.
- LG-6: Campaign, profilering, marketing-samtykke og retention.
- LG-7: betaling, AML og forbrugerret.

Særligt L38–L42 afgør, om og hvordan Struktur C kan drives. L1–L5 er også grundlæggende for platformens samlede rolle. Et svar skal omsættes til konkrete handlingsregler, ansvar, vilkår og kodekonsekvenser. “Afventer jurist” er fortsat en blocker.

Teknisk skal A-02–A-12 håndteres efter audit/Architecture Contracts: event-authoritative order state, kanonisk scope, ADR-oprydning, identitets-/sessionsikkerhed, menneskelig migration review, adresseintegritet, eventkatalog, atomic writes, single-writer ingestion, datakvalitet og Zone C-release. A-01 har en merged kodeændring, men mangler uafhængig review og opdateret auditstatus.

## 12. Dokumentationskonflikter, der skal lukkes

| ID | Problem | Krævet handling |
|---|---|---|
| D-01 | v5.2 header siger stadig "til stiftergodkendelse" og "når PR er godkendt" | Ret status til faktisk gældende beslutningsbaseline, hvis stiftergodkendelsen er givet |
| D-02 | ADR-017 er dobbeltbrugt; gammel M3 står Accepted | Omdøb/renummerér, markér gammel beslutning Superseded/Retired og opret et entydigt ADR-register |
| D-03 | ADR-018 er Accepted, men fastholder M1-ejerkontakt og ældre scope | Ret eller markér Superseded; align med P-04 og kanonisk scope i C-04 |
| D-04 | Ældre designfiler har M3, e-mail, CURIOS, reveal og gamle priser | Sæt tydelige historiske bannere i selve filerne; indeks alene er ikke nok |
| D-05 | CI-gates, backlog og audit har forskellige statusbilleder | Én statuskilde med commit, testbevis, reviewer og rest-risiko pr. fund |
| D-06 | Der findes ikke en samlet ADR-statusoversigt | Tilføj register med ID, titel, status, dato, erstatter/erstattet af og ejer |
| D-07 | S0/S1 er delvist implementeret, men backlogstatus er ikke fuldt synkroniseret med merged A-01 | Opdatér S0/S1 og audit efter verificering |
| D-08 | Runbooks README siger, at ingen runbooks er skrevet | Skriv minimumsrunbooks for data-/zonefejl, attestudløb, mandat/offer, handoff, support og incident |
| D-09 | S2 og S7 har ikke aktuelle selvstændige backlogs; S7 fulfillment er kun omtalt som senere fase | Opret scope, afhængigheder, acceptkriterier og ejerskab for de manglende leverancer |

## 13. Hvad skal være besluttet før konceptet kan låses?

Følgende beslutningspakke er minimum. Den kan udarbejdes parallelt, men må ikke efterlades som implicitte antagelser.

| # | Beslutning | Skal indeholde |
|---|---|---|
| C-01 | Marked og v1-scope | Boligtyper, geografisk pilot, kundegrupper og hvad der eksplicit er ude |
| C-02 | Kundeløfte og handelsansvar | Hvad Optata leverer selv, hvad partner leverer, hvem der er formel ansvarlig |
| C-03 | Køberrejse | Onboarding, QUALIFIED/VERIFIED, dokumentation, match, visning, bud og gennemførelse |
| C-04 | Sælgerrejse | Claim, ejerskab, efterspørgsel, mandat, klargøring, fremvisning, bud og gennemførelse |
| C-05 | Property presentation/viewing | Salgsopstilling, medier, dokumenter, spørgsmål, fremvisning og status |
| C-06 | Offer rules | Budsynlighed, frister, samtidige bud, modbud, betingelser, udløb og accept |
| C-07 | Completion/fulfillment | Købsaftale, rådgivere, bank, skøde, tinglysning, refusion, overtagelse og tvister |
| C-08 | Kanaler | Inbox, push/SMS/e-mail-politik, opt-in, kritiske beskeder og support |
| C-09 | Pris og betaling | Betaler, prislogik, betalingsøjeblik, refundering og unit economics |
| C-10 | Rolle-/authority-model | Person, sag, organisation, professionel authority, delegation og service principal |
| C-11 | Partner- og driftsmodel | Partnerkatalog, ansvar, SLA, kapacitet, kvalitet og eskalering |
| C-12 | Cold start og vækst | Acquisition, lokal likviditet, pilotmål, markedsandelstragt og milepæle |
| C-13 | Tillid og service | Trust-signaler, dataproveniens, klager, tvister, fraud og incidentkommunikation |
| C-14 | RelocationCase v1 | Deltagere, salg-/købsspor, scenarier, deling og grænser |

## 14. Hvad kan udvikles nu?

### Kan starte nu — på syntetiske data

1. S0-hardening og opdatering af auditfund.
2. S1-register, geometri, datakvalitet og område-API inden for dokumenterede datakilde-/licensrettigheder.
3. Frontend/designsystemets tekniske grundlag og klikbar prototype med syntetiske data.
4. Service blueprint for én konkret køber og én konkret sælger hele vejen til overtagelse.
5. Domænekontrakter og testmodeller for S3–S7, uden rigtige personer eller produktionsaktivering.
6. Partnerinterviews, pris-/betalingsresearch og pilotforhandlinger uden at love en juridisk uafklaret ydelse.

### Skal vente på review eller skriftlig gate

- Rigtige persondata, MitID-produktion, attest/vault og ejerskabsbeviser: LG-2 og sikkerhedsreview.
- Rigtige udbud og listings: licens-/datakildeafklaring og LG-3/LG-4.
- SaleMandate, OfferLedger og executor access i produktion: LG-1/LG-5.
- Campaign delivery: LG-6.
- Transaktionsrelaterede gebyrer/betaling: LG-7.
- DIRECT/AGENT_EXECUTED fulfillment: juridisk rolle, kontrakter, partneraftaler, ansvar, forsikring og operationel readiness.

## 15. Anbefalet afsluttende konceptforløb

### Milepæl A — Beslutningsworkshop og konceptbaseline
Luk C-01 til C-14. Marker hvert punkt som besluttet, åbent med ejer/fristen eller eksplicit ude af v1. Opdatér v5.2 og ADR'er først, når beslutningerne er truffet.

### Milepæl B — Én komplet service blueprint
Design to konkrete forløb:
- En privat køber, der finder og køber en bolig.
- En privat sælger, der bringer boligen i markedet og gennemfører salget.

For hvert trin beskrives skærm, brugerbeslutning, systemhandling, ansvarlig person/partner, data, dokument, betaling, frist, fejltilstand og recovery.

### Milepæl C — Klikbar prototype og brugertest
Prototype hele rejsen fra første besøg til overtagelse med syntetiske data. Test med potentielle købere og sælgere, også personer med lav digital tryghed. Mål gennemførelsestid, forståelse, frafald, tillid og fejl. Målet er ikke pixel-perfektion; det er at bevise, at processen forstås og kan gennemføres.

### Milepæl D — Teknisk og juridisk readiness
- A-01–A-12 status opdateret med testbevis og review.
- Migrationer, guards og identitetsgrænse menneskeligt reviewet.
- ADR- og kontraktstatus entydig.
- LG-1–LG-7 placeret på konkret kritisk vej.
- Hosting, CI, branch protection, staging, backup/restore, observability og runbooks planlagt.
- Pilotdata- og partnerrettigheder dokumenteret.

### Milepæl E — Første vertikale handel
Når lovlige og tekniske gates er lukket: én bolig, ét mandat, én eller flere verificerede købere, en dokumenteret budproces og én gennemført handel i et afgrænset pilotområde. Først derefter skaleres playbooken til ti handler og videre.

## 16. Definition af "konceptet er låst"

Konceptet kan først erklæres låst, når:
- v1-marked, boligtyper og eksplicitte fravalg er vedtaget.
- Køber og sælger er beskrevet fra første besøg til efter overtagelse.
- Salgsklargøring, fremvisning, bud og completion har navngivne ejere og leverancer.
- Hver vigtig handling har en rolle-/authority-regel.
- Juridiske gates og tekniske forudsætninger er tydeligt adskilt.
- Pris- og betalingslogik er designbar og kan testes.
- Kanaler, support, tvister og recovery er besluttet.
- 20 %-målet har en defineret nævner, funnel, kapacitetsmodel og milepæle.
- Der findes én klikbar prototype, som potentielle kunder kan gennemføre og forstå.
- Dokumentationen er ryddet for modstridende normative beslutninger.

## 17. Endelig anbefaling

**Lås ikke konceptet alene på baggrund af v5.2, SaleMandate og OfferLedger.** De beskriver Optatas markedsmotor, men ikke hele den service, der skaber en tryg og gennemført bolighandel.

Den rigtige sidste konceptleverance er en samlet **Optata Product & Service Blueprint v1.0** med:
1. Køberrejse.
2. Sælgerrejse.
3. Property presentation og viewing.
4. OfferLedger-regler og fejl-/raceforløb.
5. Fulfillment/completion til overtagelse.
6. Rolle-, partner- og ansvarsmatrix.
7. Kanal-, pris-, support- og tillidsmodel.
8. Pilot-/cold-start-plan og 20 %-kapacitetsmodel.
9. Klikbar prototype og testresultater.
10. Beslutningsregister med juridiske og tekniske gates.

Derefter kan v5.2 opdateres til den endelige konceptbaseline, og udviklingen kan begynde i kontrollerede vertikale leverancer.

**Kort sagt:** Byg ikke bare en platform, der kan registrere efterspørgsel, mandat og bud. Byg den platform, hvor en almindelig dansker kan købe eller sælge sin bolig med færrest mulige bekymringer — og hvor Optata tager ansvaret for at koordinere kompleksiteten uden at overskride sin juridiske rolle.
