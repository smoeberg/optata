# Optata — handelsmodel og Product & Service Blueprint

**Version:** 0.1 · **Dato:** 17. november 2026  
**Status:** Stifterinput indarbejdet · arbejdsgrundlag til produktdesign · ikke juridisk godkendt

> Dokumentet omsætter stifterens seneste beslutningsretning til en samlet produkt- og servicearkitektur. Det er ikke en ændring af den normative v5.2-baseline, før beslutningerne er godkendt og indarbejdet dér. Juridisk selskabsstruktur, formidlerstatus, advokatetik, databeskyttelse og forbrugerret skal vurderes skriftligt af uafhængig rådgiver.

## 1. Stifterens styrende retning

Følgende er styrende produktretning for den videre specifikation:

1. **Optata-platformen skal ikke være juridisk part i bolighandlen.** Optata leverer den digitale platform, markedsplads, matching, køber-/sælgerrejser, mandat- og budworkflow, status, dokumenteret samtykke og abonnementstjenester. Platformen skal ikke udarbejde eller indgå købsaftalen, berigtige handlen, modtage købesummen eller optræde som kundens juridiske rådgiver.
2. **Et selvstændigt advokatselskab håndterer de juridiske ydelser.** Kunden får kontakt til advokatselskabet gennem Optata, men advokatselskabet skal have sit eget klientforhold, engagement, rådgivningsansvar, sagsstyring, journal, honorar og forsikring. Selskabets juridiske uafhængighed og relation til platformen skal være reel og dokumenteret.
3. **DIRECT skal kunne fungere uden traditionel ejendomsmægler.** Sælgeren skal kunne få boligen salgsklar, præsenteret, besigtiget og fremvist via særskilte serviceydelser. Salgsklargøring kan bestilles hos advokatselskabet/serviceselskabet eller dets eksterne leverandører, men skal være en særskilt, frivillig ydelse med tydelig leverandør og pris.
4. **Optata skal tjene penge på platformen frem til og uafhængigt af den afsluttede handel.** Den primære retning er abonnementsforretning. Der kan desuden være B2B-abonnementer eller særskilt betalt B2B-adgang til samtykkebaserede købermuligheder. Platformens indtægt må ikke utilsigtet blive en skjult success fee for juridisk formidling.
5. **Serviceselskabet kan tilbyde ekstra ydelser.** Eksempelvis juridisk rådgivning, berigtigelse, dokumentindhentning, koordinering, salgsklargøring og adgang til eksterne boligservices. Kunden skal kunne vælge og fravælge hver ydelse.
6. **Markedsopstart og endelig prissætning fastlægges senere.** Nu skal vi definere abonnementslogik, betalingspunkter, datagrænser og produktmæssige muligheder – ikke fastlåse beløb eller pilotområde.

### Vigtig juridisk præcisering

Det er en ønsket selskabs- og ansvarsmodel, ikke en juridisk konklusion. Det afgørende er, hvad Optata faktisk gør, lover, kontrollerer og modtager betaling for – ikke alene hvad der står i vilkårene eller hvilket selskab der fakturerer. Matching, annoncering, mandatopsætning, budfacilitering og transaktionsnær koordinering kan udløse regulatoriske spørgsmål afhængigt af den konkrete udformning. Advokatselskabets rolle, uafhængighed, interessekonflikter, henvisningsbetalinger, fælles ejerskab/ledelse, datadeling og markedsføring skal vurderes samlet. Ingen produktionslancering af handelsflows før skriftlig juridisk afklaring.

## 2. Selskabs- og ansvarsarkitektur

### 2.1 Optata-platformen

Optata leverer:
- Oprettelse og drift af køberprofiler og købsintentioner.
- Oprettelse af sælgerens boligprofil og platformbaserede salgsmandat.
- Matching mellem boligmuligheder og købsintentioner.
- Struktureret markedsplads, budindsendelse, modbud, frister og statuslog.
- Boligpræsentationens digitale ramme, dokumentstatus og fremvisningsbooking.
- Kundeinbox, notifikationer og sagsoversigt.
- Adgangsstyring, audit, samtykkestyring og dataproveniens.
- Abonnementer og B2B-produkter inden for lovlige data-/adgangsrammer.

Optata skal ikke:
- Være køber eller sælger eller part i købsaftalen.
- Yde individuel juridisk rådgivning.
- Udarbejde, godkende eller underskrive købsaftale/skøde på kundens vegne.
- Modtage, opbevare eller videreformidle købesummen.
- Træffe beslutninger om finansiering eller kredit.
- Give indtryk af, at en platformstatus i sig selv er juridisk rådgivning eller bindende aftale.
- Overtage advokatens, bankens, mæglers eller øvrige fagpersoners professionelle ansvar.

### 2.2 Selvstændigt advokatselskab/serviceselskab

Advokatselskabet indgår særskilt aftale direkte med kunden om de ydelser, kunden vælger. Det kan efter særskilt juridisk og operationel afklaring levere:
- Juridisk køber- eller sælgerrådgivning.
- Gennemgang og udarbejdelse af købsaftale og bilag.
- Håndtering af finansierings-, rådgiver- og øvrige forbehold.
- Skøde, tinglysning, refusionsopgørelse og berigtigelse.
- Dialog med bank, realkredit, administrator, forening og øvrige parter.
- Dokument- og proceskoordinering.
- Tilbudte salgsklargøringspakker og bestilling af eksterne leverandører, hvis dette er foreneligt med selskabets regler og juridiske struktur.

Advokatselskabet skal selvstændigt fastlægge:
- Om det påtager sig sagen og hvem der er ansvarlig advokat.
- Klientidentifikation, interessekonfliktkontrol og engagement letter.
- Rådgivningsomfang, honorar, forsikring og klagevej.
- Hvilke dokumenter og oplysninger der modtages fra Optata, på hvilket grundlag og med hvilket samtykke.
- Hvilke opgaver der udføres af advokater, ansatte eller eksterne leverandører.

Platformen må ikke fremstille advokatselskabet som en automatisk del af Optata-kontoen eller som en juridisk funktion, der allerede er engageret. Kunden skal aktivt vælge at kontakte/engagere selskabet.

### 2.3 Øvrige partnere

| Partner | Typiske leverancer | Ansvar og grænse |
|---|---|---|
| Fotograf | Fotos, evt. video og drone efter regler | Kvalitet, rettigheder, samtykke og levering |
| Plantegningsleverandør | Opmåling og plantegning | Korrekt metode, mål og ansvarsforbehold |
| Byggesagkyndig | Besigtigelse og rapporter | Fagligt ansvar for egen rapport |
| Energikonsulent | Energimærke | Autorisation og korrekt registrering |
| Fremvisningsvært | Praktisk adgang og fremvisning | Identitet, adgang, sikkerhed, instruktion og hændelser |
| Rengøring/styling/håndværker | Klargøring | Tilbud, udførelse, kvalitet, skade og reklamation |
| Bank/realkredit | Finansiering og kreditafgørelse | Egen kreditvurdering og finansieringsansvar |
| Ejendomsmægler | Valgfri AGENT_EXECUTED-vej | Eget mægleransvar og særskilt mandat/engagement |
| Advokatselskab | Juridiske ydelser og evt. koordination | Eget klientforhold og professionelt ansvar |

Partnerne er ikke automatisk Optata-agenter. Hver bestilling skal vise leverandør, opgave, pris, datadeling, afbestilling, ansvar og reklamationsvej.

## 3. DIRECT — salg uden traditionel mægler

DIRECT er ikke “sælger gør alting selv”. Det er en digitalt koordineret salgsvej, hvor sælgeren kan købe præcis den praktiske hjælp, der er nødvendig, uden at engagere en traditionel ejendomsmægler.

### 3.1 DIRECT-forløbet

1. **Bolig og rådighed:** Sælger finder boligen, logger ind og dokumenterer ejerskab/rådighed. Sameje, andelsret, fuldmagt og dødsbo håndteres særskilt.
2. **Valg af salgsvej:** Sælger vælger DIRECT og ser tydeligt, hvad der er inkluderet, hvad sælger selv skal levere, og hvilke ekstra services der kan bestilles.
3. **Salgsklargøring:** Digital tjekliste viser anbefalede opgaver: oprydning, rengøring, styling, mindre reparationer, have/udearealer og adgangsforhold. Ingen opgave bestilles automatisk.
4. **Boligmateriale:** Fotos, plantegning, beskrivelse, boligfakta, energimærke og relevante rapporter/dokumenter indsamles. Hvert element har kilde, dato, ansvarlig og status.
5. **Kvalitetssikring:** Sælger gennemser og godkender præsentationen. Fejl, mangler og usikre oplysninger må ikke skjules. Optata viser forskel på verificerede registerdata, sælgeroplysninger og partnerdokumenter.
6. **Publicering:** Boligen bliver synlig efter de nødvendige rettigheder, mandatgodkendelser og datakontroller. Sælger kan se, hvad der publiceres, og hvor.
7. **Besigtigelse/fremvisning:** Køber anmoder om tidspunkter. Sælger eller en bestilt fremvisningsvært bekræfter. Adgang, aflysning, påmindelse og gennemført fremvisning registreres.
8. **Spørgsmål:** Køber stiller strukturerede spørgsmål om boligen. Sælger eller udpeget servicepartner svarer. Formelle bud holdes adskilt i OfferLedger.
9. **Bud og valg:** Sælger sammenligner pris, betingelser, finansieringsstatus og frister. Alle nødvendige sælgere godkender den konkrete beslutning.
10. **Juridisk gennemførelse:** Køber og sælger kan vælge advokatselskabet eller en anden rådgiver. Der oprettes et selvstændigt klientforhold.
11. **Afslutning:** Platformen viser overordnet processtatus, men advokaten/berigtigelsespartneren er ansvarlig for de juridiske leverancer, de har påtaget sig.

### 3.2 DIRECT-pakker og bestillinger

Produktet skal kunne understøtte:
- **Selvbetjent DIRECT:** Sælger udfører selv praktiske opgaver og bestiller kun nødvendige enkeltservices.
- **DIRECT med klargøring:** En samlet, men specificeret bestilling af foto, plantegning, dokumenthjælp, rengøring/styling mv.
- **DIRECT med fremvisningshjælp:** En leverandør håndterer fysisk adgang og fremvisning.
- **DIRECT med juridisk hjælp:** Sælger engagerer advokatselskabet særskilt.
- **AGENT_EXECUTED:** Sælger vælger i stedet en konkret ejendomsmægler med eget mandat og ansvar.

Pakker er kommercielle sammensætninger, ikke en fælles juridisk ydelse. Kunden skal kunne se, hvem der leverer hver komponent.

### 3.3 DIRECT-kritiske fejlscenarier

- Fotos eller dokumenter mangler, er forældede eller har uklar rettighed.
- Sælger godkender ikke præsentationen.
- Medejer nægter eller svarer ikke.
- Fremvisning aflyses, adgang kan ikke etableres eller nøgle/adgangskode kompromitteres.
- Køber stiller spørgsmål, der kræver fagligt/juridisk svar.
- Boligen trækkes tilbage, bliver solgt andetsteds eller ikke længere er tilgængelig.
- Leverandør udebliver, leverer mangelfuldt eller forårsager skade.
- Sælger skifter fra DIRECT til mægler.
- Mandat suspenderes eller tilbagekaldes under aktive fremvisninger/bud.

Hver fejl skal have ansvarlig part, synlig status, kundebesked, genbestilling/aflysning og økonomisk konsekvens.

## 4. Køberrejse — komplet produktflow

Dette er en produktrejse, ikke en juridisk konklusion om, hvornår en aftale indgås.

### 4.1 Fra første besøg til kvalificeret køber

1. Køber kan søge og orientere sig uden at oprette konto.
2. Køber beskriver område, boligtype, prisinterval, behov, overtagelsestid og eventuelle særlige krav.
3. Køber opretter en købsintention. QUALIFIED betyder, at de krævede oplysninger er til stede; det betyder ikke, at identitet eller økonomi er verificeret.
4. Når et identitetsbærende trin kræver det, logger køber ind med MitID.
5. Købeevne dokumenteres via en godkendt metode. VERIFIED skal vise præcist, hvad der er kontrolleret, af hvem, hvornår og hvornår det udløber. Det er ikke en garanti for bankens endelige finansiering.
6. Køber kan invitere medkøber. Hver voksen har egen identitet og egne samtykker. Husstandsrelation giver ikke automatisk adgang til bankdokumenter eller andre private data.

### 4.2 Match, præsentation og fremvisning

7. Køber får relevante boligmatch med forklaring på match, datakilde og seneste opdatering.
8. Køber ser boligpræsentation, dokumentstatus, kendte forbehold og fremvisningsmuligheder.
9. Køber anmoder om fremvisning og vælger blandt bekræftede tider.
10. Køber kan stille afgrænsede spørgsmål. Sælgeridentitet og kontaktoplysninger vises ikke uden relevant grundlag.
11. Køber kan aflyse eller ændre fremvisning efter synlige regler.

### 4.3 Bud og forhandling

12. Køber afgiver bud med pris, ønsket overtagelse, gyldighed, finansieringsstatus og strukturerede forbehold.
13. Køber ser, om buddet er modtaget, åbent, mødt med modbud, afvist, trukket tilbage eller udløbet.
14. Modbud er en ny, versionsbundet hændelse med reference til tidligere bud; historikken overskrives ikke.
15. Køber kan trække eget bud tilbage, så længe den gældende juridiske og produktmæssige regel tillader det.
16. En acceptstatus i Optata må ikke beskrives som juridisk bindende købsaftale, før den konkrete retsvirkning er afklaret og kommunikationen er godkendt.
17. Køber engagerer advokat/rådgiver særskilt og følger efterfølgende dokumenter og forbehold i completion-forløbet.

### 4.4 Køberens særlige scenarier

| Scenarie | Produktadfærd |
|---|---|
| Medkøber | Hver voksen identificeres og godkender egne forpligtelser. Primær køber kan koordinere, men kan ikke automatisk binde medkøber. |
| Finansieringsforbehold | Struktureret betingelse med præcis frist, dokumentationskrav, ansvarlig og konsekvens. Standardtekst skal juridisk godkendes. |
| Attest udløber | Nye bud kan blokeres. Aktive bud sættes ikke automatisk til side uden en besluttet og juridisk vurderet regel; køber og sælger informeres. |
| Bank afslår | Forløbet sættes i relevant betingelses-/juridisk spor. Platformen afgør ikke, om aftalen bortfalder. |
| Køber trækker bud tilbage | Append-only WITHDRAWN-hændelse; den oprindelige budhistorik bevares. |
| Køber fortryder efter accept | Ingen generisk “fortryd”-knap. Kunden henvises til advokatens vurdering af aftale, lovbestemt fortrydelsesret og eventuelle omkostninger. |
| Køber aflyser fremvisning | Booking aflyses, relevante parter informeres, og eventuelle gebyrer følger den synlige servicebestilling. |
| Andelsbolig | Køber får synlig status på forenings-/administratorgodkendelse og dokumenter; det er et særskilt spor efter bud/accept. |

## 5. Sælgerrejse — komplet produktflow

### 5.1 Fra bolig til aktivt mandat

1. Sælger finder boligen via adresseopslag og vælger “Jeg vil sælge”.
2. Sælger logger ind med MitID og gennemgår, hvilken ejendoms-/boligret der skal dokumenteres.
3. Optata viser mulige ejer-/rådighedsrelationer som forslag, ikke som endelig juridisk afgørelse.
4. Ejerforhold verificeres. Ejerbolig, andelsbolig, selskabseje, sameje og dødsbo følger forskellige evidensspor.
5. Sælger ser aggregeret efterspørgsel med tydelig forklaring af datagrundlag, aktualitet, usikkerhed og privacy-grænser.
6. Sælger vælger DIRECT eller AGENT_EXECUTED og ser leverancer, prisstruktur og ansvar.
7. Mandatets præcise scope, gyldighed, udfører, vilkår og version vises.
8. Alle nødvendige ejere eller lovligt bemyndigede repræsentanter godkender den samme mandatversion.
9. Først derefter aktiveres mandatet og den aftalte publicering/boligproduktion kan fortsætte.

### 5.2 Bud og afslutning

10. Sælger ser bud med pris, vilkår, frist, finansieringsstatus og dokumenteret verifikationsniveau.
11. Sælger kan afvise, acceptere inden for den juridisk godkendte proces eller give modbud.
12. Ved sameje kræves godkendelse fra alle nødvendige parter eller en gyldig, dokumenteret fuldmagt.
13. Ved accepteret bud oprettes et completion-forløb. Det juridiske engagement er fortsat særskilt.
14. Sælger følger dokumenter, forbehold, indfrielse, overtagelse og aflevering via platformens statusvisning.
15. Sælger kan se, hvilke opgaver der tilhører advokatselskabet, bank, partner eller sælger selv.

### 5.3 Sælgerens særlige scenarier

| Scenarie | Produktadfærd |
|---|---|
| Sameje | Alle nødvendige ejere identificeres. Mandat og accept af konkret bud kræver individuel godkendelse eller gyldig repræsentation. |
| Fuldmagt | Dokument, omfang, udsteder, modtager, gyldighed og tilbagekaldelse registreres. Fuldmagten giver kun de konkrete beføjelser, den dokumenterer. |
| Fuldmagt tilbagekaldes | Nye handlinger fra fuldmægtigen blokeres straks. Igangværende kritiske handlinger sættes i bero og eskaleres. Tidligere gyldige handlinger ændres ikke automatisk. |
| Andelsbolig | Andelsret og sælgerens rådighed dokumenteres særskilt; EJF/Tingbog er ikke tilstrækkelig dokumentation for andelsretten. Foreningens/administrators krav er separat fulfillment. |
| Mandat tilbagekaldes før accept | Fremtidige platformshandlinger og nye bud stoppes efter den aftalte regel. Eksisterende bud markeres med korrekt status; juridiske rettigheder afgøres ikke automatisk af platformen. |
| Tilbagekaldelse efter accept | Ingen automatisk annullering. Oprettes som anmodning om juridisk afklaring/ophævelse. |
| Skift DIRECT ↔ AGENT_EXECUTED | Kræver ny udfører-/mandatversion og relevante parters godkendelse. Åbne bud og bestilte services håndteres efter eksplicit overgangsregel. |
| Sælger aflyser | Skel mellem aflysning af service, tilbagekaldelse af mandat og juridisk ophævelse af allerede indgået aftale. |
| Flere samtidige bud | Alle bud bevares og kan sammenlignes. Ingen automatisk “først til mølle”-accept uden en vedtaget regel. |

## 6. Dødsboer og arvinger

Dødsboer skal være et særskilt repræsentations- og evidensspor. MitID alene giver ikke rådighed over boets bolig.

### 6.1 Fælles invariants

- Boet er den relevante sælgende part; den enkelte arving handler kun med dokumenteret bemyndigelse.
- Eksisterende mandat suspenderes, når Optata får troværdig besked om dødsfald eller tvivl om repræsentation. Systemet må ikke automatisk overføre mandatet.
- MitID identificerer personen, men beviser ikke skifteretlig rådighed.
- Skifteattest, skiftefuldmagt, beskikkelse eller anden relevant dokumentation kontrolleres manuelt i første version.
- Ved tvivl, uenighed eller utilstrækkelig dokumentation: fail-closed.
- Alle ændringer i repræsentation, mandat og budstatus auditeres.
- Ingen unødvendige personlige oplysninger om dødsfaldet deles med købere.

### 6.2 Scenarier

| Scenarie | Håndtering |
|---|---|
| Ene arving, privat skifte | Manuel review af skifteattest og rådighed. Nyt mandat eller ny version med ny accept; gammelt mandat overtages ikke automatisk. |
| Flere arvinger | Alle nødvendige arvinger godkender, eller gyldig fuldmagt/bobestyrer dokumenteres. Uenighed blokerer mandat og budaccept. |
| Bobestyrer | Beskikkelse og præcist mandat kontrolleres. Begrænsninger registreres som authority-constraints. |
| Dødsfald under aktivt mandat | Mandat suspenderes; nye bud og accept stoppes. Åbne bud sættes i bero/markeres afventende efter juridisk godkendt regel. |
| Dødsfald efter platformaccept | Manuel juridisk behandling. Ingen automatisk gennemførelse eller annullering. |
| Arving vil overtage boligen | Internt arveudlæg holdes uden for almindelig OfferLedger i v1. |
| Tvist mellem arvinger | Status ESTATE_DISPUTED eller tilsvarende; ingen nye mandathandlinger eller bud. |
| Andelsbolig i dødsbo | Både boets rådighed over andelen og foreningens/administratorens regler skal håndteres. |

### 6.3 V1-afgrænsning

V1 kan understøtte:
- Enearving med tydelig skifteattest og manuel godkendelse.
- Bobestyrer med klar beskikkelse og dokumenteret bemyndigelse.

Flere arvinger uden enighed, omstridte boer, uklare fuldmagter og interne arveudlæg håndteres manuelt uden for automatiseret bud-/mandatflow. Det er en sikkerhedsafgrænsning, ikke et udsagn om at scenarierne aldrig skal understøttes.

## 7. Budmekanik og skjult minimumspris

### 7.1 Minimumspris / sælgers bundgrænse

Stifterens retning:
- Sælger kan angive en minimumspris/bundgrænse.
- Bundgrænsen er fortrolig og må ikke vises direkte til potentielle købere.
- Optata må ikke afsløre den via API, HTML, metadata, fejlsvar, analytics, B2B-eksport eller partneradgang.
- Sælger kan se, hvor bud ligger i forhold til egen bundgrænse.
- Køber kan eventuelt få et neutralt procent-/intervalsignal om buddets position uden at få selve bundgrænsen.

**Åbent fortolkningspunkt:** Stifterens formulering om, hvem der skal se en procentvis “match” mod minimumsprisen, er ikke helt entydig. Arbejdshypotesen her er, at køber kan se et groft signal om, hvor tæt eget bud ligger på sælgers fortrolige bundgrænse, uden at grænsen kan udregnes. Det skal bekræftes før UX og API designes. Alternativt vises procenten kun til sælger.

Et procenttal kan lække bundgrænsen gennem gentagne bud, kendt budpris, afrunding eller små intervaller. Derfor skal disclosure-modellen testes mod rekonstruktion og differencing. Sikker standard indtil beslutning: kun sælger ser den præcise procentuelle afstand; køber får alene almindelig budstatus eller et groft, ikke-inverterbart signal.

### 7.2 Budregler, der skal fastlægges

- Åbne/lukkede bud og hvilke felter andre købere kan se.
- Samtidige bud og sælgers sammenligningsvisning.
- Budrunder, frister, forlængelser og svarfrister.
- Modbudskæde, accept af konkret vilkårsversion og tilbagetrækning.
- Betingelser: finansiering, salg af egen bolig, overtagelsesdato, foreningsgodkendelse mv.
- Minimumsprisens scope, ændring, versionshistorik og hvem der må se den.
- Hvordan minimumspris fungerer sammen med flere ejere og fuldmagt.
- Hvad der sker ved mandatets suspension/udløb, attestudløb, dødsfald og fuldmagtstilbagekaldelse.
- Hvornår platformen alene registrerer en intention, og hvornår parterne juridisk bindes.

### 7.3 Ufravigelige tekniske accepttests

- To samtidige acceptkommandoer: præcis én kan vinde.
- Accept mod mandattilbagekaldelse.
- Accept mod bududløb.
- Modbud mod accept i samme tidsvindue.
- Attest udløber under aktivt bud.
- Medejer mangler accept.
- Fuldmagt tilbagekaldes under accept.
- Dødsbo suspenderes under accept.
- Idempotent replay af samme command.
- Minimumspris kan ikke udledes fra API, log, partnerrolle eller gentagne bud.
- Udfører-/advokathandoff fejler og kan genoptages uden dobbelt handling.

## 8. Fra accepteret bud til afsluttet handel

### 8.1 FulfillmentCase

Der etableres et selvstændigt **FulfillmentCase** (arbejdstitel) som koordinerende sagsforløb. Det ejer ikke købsaftalen, klientforholdet, skødet eller købesummen. Det koordinerer status, ansvar, dokumenter, deadlines og overdragelser mellem parter.

### 8.2 Typisk gennemførelsesforløb

1. **Platformstatus:** Et bud når den aftalte platformstatus. Systemet opretter et FulfillmentCase med reference til bolig, budversion og parter.
2. **Juridisk engagement:** Køber og sælger vælger advokat/rådgiver. Advokatselskabet gennemfører konfliktkontrol, klientidentifikation og indgår særskilt aftale. Ingen sag antages automatisk.
3. **Købsaftale:** Ansvarlig juridisk part udarbejder/gennemgår købsaftale og bilag. Parterne underskriver gennem godkendt løsning.
4. **Forbehold:** Finansierings-, rådgiver-, salg-af-egen-bolig- og øvrige forbehold registreres med frist, ansvarlig og dokumentation. Advokaten rådgiver om retsvirkning.
5. **Finansiering:** Købers bank/realkredit foretager egen kreditbehandling. Sælgers bank håndterer indfrielse/panteforhold.
6. **Boligdokumenter:** Relevante rapporter, forsikring, ejer-/foreningsdokumenter og øvrige bilag kontrolleres af de ansvarlige fagpersoner.
7. **Skøde:** Den ansvarlige berigtigelsespartner udarbejder og indhenter underskrifter på skøde.
8. **Tinglysning:** Berigtigelsespartner følger tinglysning, anmærkninger og eventuel frist/rettelse.
9. **Økonomisk afregning:** Købesum går mellem de relevante parter via den lovlige og aftalte betalings-/deponeringsordning. Optata må ikke modtage eller holde købesummen.
10. **Refusionsopgørelse:** Relevant partner udarbejder og afklarer fordeling af løbende udgifter.
11. **Overtagelse:** Parterne koordinerer dato, nøgler, aflæsning, adgang og eventuelle mangler.
12. **Afslutning:** Advokat/berigtigelsespartner bekræfter de opgaver, vedkommende har påtaget sig. Optata lukker platformens workflow og bevarer kun data efter fastlagt retention.
13. **Efterforløb:** Kunden kan frivilligt købe yderligere juridiske eller praktiske ydelser. Ingen automatisk krydssalg baseret på fortrolige klientoplysninger.

### 8.3 Stop- og afvigelsesforløb

- Finansiering afslås eller forbehold opfyldes ikke.
- En part underskriver ikke.
- Dokumenter er mangelfulde eller modstridende.
- Tinglysning afvises eller får anmærkning.
- En part ønsker ophævelse/fortrydelse.
- Dødsfald, konkurs, værgemål eller fuldmagtstilbagekaldelse opstår.
- Andelsforening/administrator godkender ikke køber.
- Overtagelse forsinkes eller der opstår tvist.

Optata registrerer status og eskalering, men afgør ikke juridiske konsekvenser. Advokaten eller anden ansvarlig fagperson rådgiver inden for sit engagement.

## 9. Forretningsmodel — abonnement først

### 9.1 Platformens indtægter

Primær retning:
- Privat køberabonnement eller betalte niveauer for avancerede søge-/matchfunktioner.
- Privat sælgerabonnement eller betalte niveauer for markedsindsigt, mandatværktøjer og boligworkflow.
- B2B-abonnementer for professionelle kunder og organisationer.
- B2B-køb af adgang til samtykkebaserede muligheder for at komme i kontakt med relevante købere, hvis lovligt grundlag, transparens og konkret købersamtykke foreligger.
- Eventuelle tillægsfunktioner til analyse, portefølje, rapportering og integration.

### 9.2 B2B-adgang til købermuligheder — vigtige grænser

“B2B-køb af potentielle købere” må ikke implementeres som salg af en personliste eller rå persondata. Der skal skelnes mellem:
1. **Aggregeret efterspørgselsindsigt:** ingen identificerbare personer og underlagt Zone C-kontroller.
2. **Match-/mulighedsnotifikation:** B2B-kunden får besked om, at der findes relevant efterspørgsel, uden identitet eller kontaktoplysninger.
3. **Køberinitieret kontakt/introduktion:** køberen vælger aktivt at dele konkrete oplysninger med en bestemt virksomhed/recipient til et bestemt formål.
4. **Rå lead-/persondataeksport:** ikke tilladt som standard og kræver særskilt juridisk, privacy- og produktgodkendelse; bør ikke være en del af baseline.

Køberens identitet, økonomi, bud og dokumenter må ikke følge med et B2B-abonnement som standard. Samtykke skal være specifikt, informeret, frivilligt, modtager- og formålsafgrænset og kunne trækkes tilbage fremadrettet.

### 9.3 Serviceselskabets indtægter

Advokatselskabet/serviceselskabet kan have separate indtægter fra:
- Juridisk rådgivning og berigtigelse.
- Dokument- og sagsbehandling.
- Salgsklargøring og koordinering af leverandører.
- Fremvisnings- og boligservices, hvis selskabs- og professionsregler tillader det.
- Andre særskilt bestilte ydelser.

Platform og advokatselskab skal have separate aftaler, fakturaer, regnskaber, ansvarsforhold og dataadgang. Eventuelle henvisnings-/koncernbetalinger skal være gennemsigtige og juridisk vurderede.

### 9.4 Hvad skal besluttes nu – og hvad kan vente?

**Skal besluttes nu:**
- Abonnement er platformens primære indtægtsretning.
- Platformens betaling er ikke betinget af, at en bestemt handel gennemføres.
- B2B-adgang må ikke indebære automatisk salg/eksport af køberidentitet eller fortrolige oplysninger.
- Advokatselskabets ydelser bestilles og faktureres særskilt.
- Ingen købesum eller klientmidler går gennem Optata.

**Kan vente:**
- Priser og abonnementsniveauer.
- Gratis prøveperioder, rabatter og årlig/månedlig betaling.
- Konkrete B2B-segmenter og pakker.
- Pilotområde, acquisition-budget og likviditetsplan.
- Endelig partnerprovision og leverandørkatalog.

## 10. Fælles roller, rettigheder og evidens

Rollemodellen skal skelne mellem:
- Personens relation til sagen: køber, medkøber, sælger, medejer, arving, fuldmægtig.
- Professionel rolle: advokat, bobestyrer, mægler, bank, fotograf, fremvisningsvært.
- Organisation: advokatfirma, mæglerfirma, bank, leverandør.
- Teknisk principal: Optata-system, partnerintegration, review-service.

Ingen rolle giver automatisk global adgang. Adgang kræver konkret sag, formål, scope, gyldig authority, relevant samtykke/retsgrundlag og udløb. Hver voksen godkender egne handlinger. Fuldmagt skal være dokumenteret, afgrænset og tilbagekaldelig. Dødsbo kræver særskilt skifteretlig dokumentation.

## 11. Prioritering og udviklingsrækkefølge

| Prioritet | Leverance | Hvad skal være på plads |
|---|---|---|
| P1 | Handelsmodel og selskabs-/ansvarsgrænse | Optata-platform, advokatselskab og øvrige partnere; juridisk vurdering af faktisk aktivitet |
| P2 | DIRECT | Salgsklargøring, boligpræsentation, dokumenter, fremvisning, Q&A, servicebestilling |
| P3 | Fulfillment | Fra platformaccept til købsaftale, skøde, tinglysning, betaling og overtagelse |
| P4 | Komplette køber-/sælgerrejser | Sameje, medkøber, andel, fuldmagt, finansieringsforbehold, aflysning, fortrydelse, dødsbo |
| P5 | Budmekanik | Budrunder, frister, synlighed, samtidige bud, modbud og fortrolig minimumspris |
| P6 | Forretning/drift | Abonnementsarkitektur, B2B, support, tvister, forsikring og kapacitet; konkrete priser senere |
| P7 | Markedsopstart | Pilot, acquisition, likviditet og geografisk udrulning; udskydes til produktmodenhed |

### Udvikling kan begynde parallelt

- S0/S1 teknisk hardening og registerfundament fortsætter.
- UX/service blueprint og klikbar prototype kan bygges på syntetiske data.
- Domænemodeller for PropertyPresentation, Viewing, FulfillmentCase og OfferLedger kan specificeres.
- Juridisk rådgiver kan parallelt vurdere selskabsmodellen, faktisk platformadfærd, advokatselskabets uafhængighed, henvisningsmodellen og bud-/mandatvirkning.
- Ingen real-data transaktionsflow eller offentlig DIRECT-lancering før relevante gates er lukket.

## 12. Beslutningsregister

| ID | Punkt | Status |
|---|---|---|
| B-01 | Optata skal være platform og ikke part i købsaftalen eller juridisk rådgiver | Stifterretning; juridisk vurdering af faktisk rolle mangler |
| B-02 | Selvstændigt advokatselskab håndterer de juridiske ydelser via særskilt klientforhold | Stifterretning; selskabs-/professionsretlig vurdering mangler |
| B-03 | DIRECT skal tilbyde salg uden traditionel mægler med valgfri klargøring og fremvisning | Produktretning |
| B-04 | Salgsklargøring kan bestilles gennem advokatselskab/serviceselskab eller dets leverandører | Afhænger af selskabs-/professionsretlig vurdering |
| B-05 | Platformens primære forretning er abonnement; betaling ikke betinget af afsluttet handel | Stifterretning |
| B-06 | B2B kan købe adgang til samtykkebaserede købermuligheder | Produktretning; præcis data-/kontaktmodel kræver privacy/juridisk review |
| B-07 | Sælger kan angive fortrolig minimumspris | Produktretning |
| B-08 | Procentvis match mod minimumspris | Åbent: hvem ser signalet, og hvor præcist? |
| B-09 | Priser og abonnementspakker | Udskydes |
| B-10 | Pilotområde og markedsopstart | Udskydes |
| B-11 | Dødsbo: v1 med manuel review af klare ene-arving-/bobestyrerforløb | Foreslået scope; juridisk review |
| B-12 | Platformstatus vs. juridisk bindende aftale | Åbent juridisk release gate |
| B-13 | Optata håndterer aldrig købesum eller klientmidler | Stifterretning; betalingsarkitektur skal håndhæve det |

## 13. Næste konkrete arbejde

1. Færdiggør en juridisk selskabs-/ansvarsmatrix for Optata, advokatselskabet, mægler og servicepartnere.
2. Tegn DIRECT som en fuld service blueprint med bestilling, levering, prisvisning, kvalitet, aflysning og reklamation.
3. Beskriv FulfillmentCase som trin, ansvar, dokumenter, deadlines, status og eskalering.
4. Omsæt køber- og sælgerrejserne til skærm-for-skærm-flow og acceptance criteria.
5. Specificér OfferLedger-regler inklusive skjult minimumspris og disclosure-tests.
6. Opret et samlet scenariekatalog for sameje, andel, fuldmagt, dødsbo, finansiering, aflysning og fortrydelse.
7. Opdatér først derefter v5.2, ADR'er, architecture contracts og S3–S7 backlogs.

**Konceptets mål:** Kunden skal opleve én enkel digital rejse. Optata koordinerer platformens proces; advokatselskabet og de øvrige leverandører leverer deres egne, tydeligt afgrænsede ydelser og bærer deres respektive faglige ansvar.
