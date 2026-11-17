# Optata — Service & Responsibility Architecture v1.0

**Version:** 1.0 · **Dato:** 17. november 2026  
**Status:** Proposed · produkt- og driftsdesign · kræver stifterbeslutninger, juridisk review og arkitekturreview  
**Arbejdsgren:** `docs/service-responsibility-architecture-v1`  
**Autoritativt udgangspunkt:** Projektgrundlag v5.2, Product Closure v1.0, Transaction Model & Service Blueprint v0.2, Architecture Contracts v1.0 og Role & Authority Model v1.0.

> Dette dokument omsætter den vedtagne produktretning til en operationel ansvars- og servicearkitektur. Det ændrer ikke i sig selv den normative baseline. Det er ikke juridisk rådgivning, en tilladelse til ejendomsformidling eller dokumentation for, at den foreslåede selskabsstruktur er lovlig. Ingen transaktionsfunktion må frigives til rigtige kunder, før de relevante juridiske og tekniske gates er lukket.

## 1. Formål og styrende principper

Målet er én enkel kundeoplevelse med flere tydeligt adskilte leverandører og ansvarsområder. Kunden skal kunne forstå, hvem der leverer en ydelse, hvem der træffer en faglig beslutning, hvem der har adgang til oplysninger, hvem der fakturerer, og hvem kunden skal kontakte ved fejl.

### 1.1 Styrende produktretning

1. **Optata er platformen.** Optata leverer digital adgang, bolig- og købermatch, strukturerede workflows, præsentation, booking, dokumentstatus, beskeder, notifikationer, samtykkestyring og abonnementsprodukter.
2. **Optata er ikke part i købsaftalen.** Platformen må ikke optræde som køber, sælger, juridisk rådgiver, klientmiddelforvalter eller betalingsmodtager af købesummen.
3. **Advokatselskabet er selvstændig juridisk leverandør.** Det indgår eget klientforhold, foretager konfliktkontrol, fastlægger rådgivningsomfang, fører egen sag/journal, fakturerer selv og bærer sit professionelle ansvar.
4. **Serviceleverandører er selvstændige leverandører.** Fotograf, rengøring, styling, byggesagkyndig, fremvisningsvært og øvrige leverandører har afgrænsede opgaver, egne vilkår og ansvar for egne leverancer.
5. **DIRECT er en komplet servicevej.** Kunden kan få hjælp til klargøring, boligmateriale, besigtigelse, fremvisning og praktisk koordinering uden at engagere en traditionel ejendomsmægler.
6. **Platformindtægt er abonnementsbaseret og ikke betinget af gennemført handel.** Priser, niveauer og betalingsintervaller fastlægges senere.
7. **Kunden vælger aktivt ydelser.** Et Optata-login er ikke et advokatengagement, en servicebestilling eller et samtykke til ubegrænset datadeling.
8. **Ingen skjult juridisk virkning.** En status som `SUBMITTED`, `COUNTERED` eller `PLATFORM_ACCEPTED` er en platformshændelse. Den juridiske virkning skal følge særskilt godkendte vilkår og aftaledokumenter.
9. **Fail closed.** Uklar identitet, rådighed, fuldmagt, samtykke, konflikt, betaling eller dokumentstatus stopper den relevante handling og sendes til manuel afklaring.
10. **Én digital rejse er ikke ét fælles ansvar.** Optata må gerne vise en samlet oversigt, men hvert selskab og hver professionel er ansvarlig for egne leverancer.

### 1.2 Dokumenthierarki

- Projektgrundlag v5.2 er fortsat normativ produktbaseline.
- Architecture Contracts v1.0 og Role & Authority Model v1.0 er Proposed, indtil de er reviewet og accepteret.
- Transaction Model & Service Blueprint v0.2 beskriver stifterretningen.
- Dette dokument konkretiserer roller, serviceleverancer, kunderejser og handoffs.
- Ingen foreslået proces bliver automatisk en accepteret ADR, lovlig aktivitet eller implementeret kontrol.

## 2. Selskabs- og leverandørmodel

### 2.1 Optata-platformselskabet

**Formål:** Drive softwareplatformen og dens abonnementsprodukter.

**Platformen kan levere:**
- Konti, autentifikation via godkendt identitetsløsning og adgangsstyring.
- Køberprofiler, købsintentioner og køberordrer.
- Sælgerens boligprofil, dokumentindsamling og platformmandat.
- Matching, søgning, boligpræsentation og markedspladsfunktioner.
- Struktureret budindsendelse, modbud, frister og statuslog.
- Booking og koordinering af fremvisninger og bestilte services.
- Kundeinbox, notifikationer, samtykke- og auditspor.
- Abonnement, fakturering af egne platformprodukter og B2B-funktioner inden for godkendte datagrænser.
- Koordineret statusvisning for FulfillmentCase.

**Platformen må ikke uden særskilt juridisk godkendelse:**
- Markedsføre sig som kundens ejendomsmægler, advokat eller juridiske repræsentant.
- Give individuel juridisk, finansiel eller kreditmæssig rådgivning.
- Udarbejde, forhandle, godkende eller underskrive købsaftale/skøde på kundens vegne.
- Afgøre, om et bud eller en accept er juridisk bindende.
- Modtage, holde, disponere over eller videreformidle købesummen eller klientmidler.
- Foretage kreditvurdering eller træffe bankens finansieringsbeslutning.
- Love, at en bolig er juridisk fri, finansieret, godkendt eller tilgængelig alene ud fra registerdata eller platformstatus.
- Bruge kundens fortrolige sagsoplysninger til uvedkommende B2B-salg eller krydssalg.

**Vigtigt:** Listen beskriver produktets ønskede grænse, ikke en juridisk safe harbour. Den faktiske aktivitet, kontrol, markedsføring, indtægtsmodel, kundeløfter og arbejdsgange afgør den regulatoriske vurdering.

### 2.2 Advokatselskabet

Advokatselskabet er en selvstændig juridisk leverandør, ikke en indbygget funktion i Optata.

Før et klientforhold eksisterer, skal selskabet selv:
- Modtage en aktiv henvendelse eller anmodning fra kunden.
- Identificere klient(er) og relevante modparter.
- Gennemføre konfliktkontrol og vurdere, om sagen kan påtages.
- Fastlægge klient, opdrag, rådgivningsomfang, ansvarlig advokat og honorar.
- Give kunden engagement letter/vilkår og klage-/kontaktoplysninger.
- Fastlægge eget behandlingsgrundlag, journal, opbevaring og adgang.
- Acceptere eller afvise sagen uafhængigt af Optata.

Efter særskilt engagement kan advokatselskabet blandt andet:
- Rådgive køber eller sælger juridisk.
- Gennemgå og udarbejde købsaftale og bilag.
- Rådgive om forbehold, frister, fortrydelse og ophævelse.
- Håndtere skøde, tinglysning, refusionsopgørelse og berigtigelse, hvis opgaven påtages.
- Kommunikere med bank, administrator, forening og modpart inden for klientens mandat.
- Bekræfte til Optata alene de workflow-statusser og oplysninger, der er nødvendige og lovligt kan deles.

Advokatselskabet bestemmer selv, om det påtager sig en opgave, og må ikke være forpligtet til at anbefale Optata, en bestemt partner eller en bestemt handel.

### 2.3 Serviceselskab og eksterne leverandører

**Serviceselskab og advokatselskab må ikke behandles som samme juridiske enhed i produktet, før selskabs- og professionsreglerne er afklaret.** Ikke-juridiske ydelser som styling, rengøring, fotografering, fremvisning og håndværk bør modelleres som selvstændige serviceordrer med identificeret leverandør. Om advokatselskabet selv må sælge, koordinere eller fakturere sådanne ydelser, kræver særskilt skriftlig vurdering.

Hver leverandør skal have:
- Identificeret juridisk leverandør og kontaktvej.
- Beskrivelse af opgave, omfang, leverance og acceptkriterier.
- Pris, betalingsmodtager, afbestillings- og reklamationsvilkår.
- Oplysning om underleverandører og eventuel videreoverdragelse.
- Datakategorier, adgangsformål, opbevaring og sletning.
- Ansvar for kvalitet, skade, forsinkelse, fejl og forsikring.
- Dokumenteret kundegodkendelse før bestilling.

### 2.4 Mægler og øvrige professionelle

En traditionel ejendomsmægler kan være en særskilt valgfri udførelsesvej (AGENT_EXECUTED). Mæglerens mandat, lovpligter, rådgivning, annoncering, budhåndtering og ansvar skal være direkte og tydeligt adskilt fra Optatas platformvilkår. Partnerstatus i Optata giver ikke i sig selv ret til at repræsentere kunden eller handle på dennes vegne.

Bank/realkredit, administrator/andelsboligforening, byggesagkyndig, energikonsulent, fotograf og fremvisningsvært har tilsvarende egne faglige kompetencer og ansvar.

## 3. Ansvars- og RACI-matrix

RACI betyder: **A** = endeligt ansvarlig for leverancen/beslutningen, **R** = udfører, **C** = konsulteres, **I** = informeres. Tabellen beskriver den ønskede driftsmodel; den er ikke en juridisk ansvarsfraskrivelse.

| Aktivitet/leverance | Optata | Advokatselskab | Serviceleverandør | Kunde | Bank/forening/mægler |
|---|---|---|---|---|---|
| Platform, konto og adgang | A/R | I | I | R for egne kontooplysninger | I |
| MitID-identifikation/session | R for integration og teknisk kontrol | R for egen klientkontrol | R for egen kundekontrol | R for autentifikation | R for egne kontroller |
| Køberprofil og købsintention | A/R for platformfunktion | I efter særskilt grundlag | – | A for egne oplysninger og valg | I efter konkret samtykke |
| Købers finansieringsbevis | R for sikker modtagelse/status | R/C hvis engageret | – | A for korrekt og rettidig dokumentation | A for kreditvurdering og bankbeslutning |
| Sælgers ejerskab/rådighed | R for workflow/evidensstatus | R/C ved juridisk vurdering | – | A for fremlagt dokumentation | C for autoritative registre/foreningsbekræftelse |
| Mandat og repræsentationsrettigheder | R for digital version, signaturspor og adgang | R/C for juridisk rådgivning, hvis engageret | – | A for beslutning og godkendelse | C efter rolle |
| Boligdata og præsentation | A/R for platformvisning/proveniens | C ved juridisk gennemgang | R for egne materialer | A for sælgergodkendelse og egne udsagn | C for autoritative data |
| DIRECT klargøring | R for bestillings-/statusinterface | Kun hvis lovligt og særskilt engageret | A/R for udført ydelse | A for valg og adgang til boligen | – |
| Fotos/plantegning/rapport | R for upload/status | C hvis engageret | A/R for faglig leverance | C/godkender publicering | C efter fagrolle |
| Fremvisningsbooking | A/R for platformbooking | I | R for fysisk fremvisning | A for tilgængelighed og adgang | R hvis mægler har opgaven |
| Fysisk adgang/nøgler/sikkerhed | R for registrering af proces, ikke fysisk kontrol | – | A/R for egen adgangsopgave | A for tilladelse og instruktion | R efter egen aftale |
| Strukturerede boligspørgsmål | A/R for kanal og log | C hvis juridisk spørgsmål og engageret | R for eget fagområde | A for egne svar/oplysninger | R for egne svar |
| Bud og modbud | A/R for platformregistrering og tekniske regler | C/R for juridisk rådgivning, hvis engageret | – | A for budbeslutning | R hvis særskilt mæglermandat |
| Platformnotifikation om bud | A/R | I efter lovligt grundlag | – | R for egne notifikationsvalg | I efter rettighed |
| Juridisk vurdering af accept/fortrydelse | – | A/R for egen klient | – | A for beslutning efter rådgivning | C |
| Købsaftale og bilag | – | A/R hvis engageret | – | A for egne underskrifter | C/R hvis særskilt aftalt |
| Finansiering og kredit | – | C/R for juridisk klientrådgivning | – | R for ansøgning og oplysninger | A/R |
| Andels-/foreningsgodkendelse | R for statusvisning | C/R for juridisk bistand | – | R for ansøgning/oplysninger | A/R |
| Skøde og tinglysning | R for statusreference | A/R hvis engageret | – | R for underskrifter | R efter egen rolle |
| Købesum/deponering/afregning | Ingen rolle eller adgang | A/R kun hvis særskilt lovligt påtaget | Ingen rolle | R for betaling efter aftale | A/R: bank/autoriseret betalings-/deponeringspart |
| Refusionsopgørelse | Statusvisning | A/R hvis engageret | – | C/godkender | C |
| Overtagelse og nøgler | R for checkliste/status | C hvis engageret | R for bestilt praktisk opgave | A for modtagelse/aflevering | R efter aftale |
| Klage over platform | A/R | I | I | R for indgivelse | I |
| Klage over juridisk ydelse | – | A/R for egen klageproces | – | R for indgivelse | Relevant advokatinstans efter regler |
| Klage over serviceleverance | R for routing, hvis bestilt i platform | – | A/R | R for indgivelse | – |

**RACI-regel:** Hvis en aktivitet ikke har en entydig A, må den ikke automatiseres eller præsenteres som dækket. Optata kan være A for platformens tekniske levering, men ikke dermed A for den underliggende juridiske, finansielle eller håndværksmæssige ydelse.

## 4. Kundens fælles oplevelse og leverandørskift

### 4.1 Én oversigt, flere selvstændige sager

Kunden ser én Optata-oversigt med:
- Næste handling og ansvarlig part.
- Hvad der er gennemført, afventer, er forsinket eller blokeret.
- Hvilke oplysninger/dokumenter der mangler.
- Hvem kunden har en aftale med.
- Hvem der fakturerer, og hvor kunden skal henvende sig.
- Hvilke data der er delt med hvilken modtager og til hvilket formål.

Den samlede oversigt er en **read model**, ikke en fælles sagsjournal. Advokatselskabets fortrolige klientjournal, bankens kreditoplysninger og serviceleverandørens interne arbejdsnotater bliver ikke automatisk synlige i Optata.

### 4.2 Handoff-kontrakt

Ethvert handoff fra Optata til en ekstern part skal have:
1. Identificeret afsender og modtager.
2. Konkret sag og formål.
3. Kundens aktive anmodning eller andet dokumenteret behandlingsgrundlag.
4. Felter/dokumenter, der må deles – ikke en hel kontoeksport.
5. Modtagerens accept eller afvisning.
6. Tidspunkt, version, udløb og tilbagekaldelsesregel.
7. Statuskvittering uden unødvendigt indblik i modtagerens interne sagsdata.
8. Fejl-, timeout- og genforsøgsadfærd uden dobbeltbestilling.

Handoff må ikke automatisk oprette et klientforhold, en serviceaftale, en fuldmagt eller et samtykke til markedsføring.

### 4.3 Kontakt og notifikationer

Platformens inbox er den kanoniske historik for platformshændelser. E-mail/SMS/push kan bruges som lavdetalje-alarm, hvis kunden har valgt det og lovligt grundlag foreligger. Beskeder må ikke indeholde fortrolige bud, økonomiske oplysninger, dokumenter eller detaljer om dødsbo. Ekstern rådgivning foregår i den respektive leverandørs egen sikre kanal, medmindre der er etableret en godkendt integration.

## 5. DIRECT — service blueprint

DIRECT betyder salg uden traditionel mægler, ikke at sælgeren skal udføre alle opgaver selv.

| Trin | Kundens oplevelse / handling | Optata-platformens ansvar | Ekstern udfører / ansvar | Evidens og afslutningskriterium |
|---|---|---|---|---|
| 1. Start | Sælger vælger “Jeg vil sælge” og logger ind | Viser proces, bolig og nødvendige trin | – | Identitet/session og oprettet kladde |
| 2. Rådighed | Sælger dokumenterer ejerskab, andelsret eller repræsentation | Indsamler begrænset evidens og viser reviewstatus | Advokat/administrator kan kontrollere efter særskilt opdrag | Rådighed godkendt eller manuel blokering |
| 3. Valg af DIRECT | Sælger ser hvad der er inkluderet, selvbetjening og tilvalg | Viser scope, leverandør, pris, ansvar og vilkår | Leverandører viser kapacitet og egne vilkår | Aktivt valg og versioneret mandat |
| 4. Klargøringsplan | Sælger vælger opgaver og tidspunkter | Opretter serviceordrer og afhængigheder | Rengøring, styling, håndværker mv. udfører | Bestilling accepteret og leverance dokumenteret |
| 5. Boligmateriale | Sælger uploader fakta og godkender indhold | Proveniens, status, versionsstyring og publiceringspreview | Fotograf, opmåler, energikonsulent mv. leverer fagmateriale | Materiale leveret, rettigheder afklaret, sælger godkendt |
| 6. Kvalitet | Sælger gennemser præsentation og fejl | Marker kilde: register, sælger, fagpartner, verificeret/ubekræftet | Fagpartner retter egne leverancer | Obligatoriske felter og review lukket |
| 7. Publicering | Sælger bekræfter publicering | Kontrollerer mandat, samtykke, rettigheder og release-gates | Mægler kun hvis særskilt AGENT_EXECUTED | Publiceret version og audit-event |
| 8. Fremvisning | Køber anmoder om tider | Booking, kalender, bekræftelse, påmindelse, aflysning | Sælger eller fremvisningsvært gennemfører | Bekræftet/gennemført/aflyst med tidsstempel |
| 9. Spørgsmål | Køber stiller strukturerede spørgsmål | Kanal, kategorisering, log og routing | Sælger eller fagpartner svarer inden for eget område | Svar knyttet til spørgsmål og afsender |
| 10. Bud | Køber afgiver bud | OfferLedger, frister, skjult tærskel og notifikationer | Juridisk rådgiver efter særskilt engagement | Budversion og parternes handlinger |
| 11. Overdragelse | Parterne vælger juridisk rådgiver | Viser valgfri rådgiverkontakt og FulfillmentCase-status | Advokater/bank/berigtigelsespartner udfører | Særskilt engagement og accepteret handoff |

### 5.1 DIRECT-bestilling og betaling

- Hver opgave er en separat serviceordre med leverandør, pris, scope, tidsvindue og afbestillingsvilkår.
- Kunden skal kunne bestille kun de ydelser, der ønskes; ingen automatisk pakke eller skjult bundling.
- Før bestilling vises, hvem der indgår aftalen, hvem der modtager betaling, og hvem der behandler reklamation.
- Optata kan vise ordren og status. Betaling går direkte til leverandøren eller via en godkendt betalingsudbyder med klart afgrænset rolle. Optata må ikke holde leverandørmidler eller klientmidler.
- Refundering, udeblivelse, skade og reklamation håndteres af den kontraktuelle leverandør. Optata kan registrere og route klagen, men må ikke foregive at afgøre leverandørens faglige ansvar.

### 5.2 Fremvisningssikkerhed

Før fysisk fremvisning skal der være:
- Bekræftet booking og identificerede deltagere efter proportionalt behov.
- Klar aftale om hvem der åbner, er til stede og lukker boligen.
- Instruktion om nøgler, alarm, kæledyr, værdigenstande og private rum.
- Ingen offentlig visning af adgangskoder, nøglebokskoder eller præcise adgangsdetaljer.
- Hændelsesvej ved skade, uønsket adfærd, udeblivelse eller sikkerhedsproblem.
- Begrænset adgang til fremvisningsoplysninger med automatisk udløb.

Ingen fremvisningsvært må få bred adgang til køberens økonomi, budhistorik eller sælgerens fortrolige minimumspris.

## 6. Køberrejse — fra interesse til overtagelse

| Fase | Kundens handling og skærmbillede | Optata gør | Selvstændig part / beslutning | Stopregel |
|---|---|---|---|---|
| 1. Opret | Køber opretter konto og købsbehov | Identitet, profil, præferencer og samtykker | Køber ejer egne oplysninger | Uafklaret identitet/session |
| 2. Husstand | Køber inviterer medkøber | Separate konti og eksplicitte relationer | Hver voksen godkender egne handlinger | Ingen adgang alene via husstandsrelation |
| 3. Finansiering | Køber sender dokumentation | Sikker modtagelse, adgangsbegrænsning og udløbsstatus | Bank afgør kredit; reviewer verificerer kun defineret evidens | Udløbet/uklar dokumentation |
| 4. Match | Køber ser relevante boliger og usikkerhed | Matcher på godkendte kriterier og viser proveniens | Sælger/udbyder kontrollerer faktisk tilgængelighed | Match må ikke fremstilles som garanti |
| 5. Besigtigelse | Køber booker og gennemfører fremvisning | Booking og praktiske instruktioner | Sælger/fremvisningsvært står for adgang | Manglende adgangsbekræftelse |
| 6. Spørgsmål | Køber sender spørgsmål | Struktureret kanal | Sælger/fagpartner svarer | Juridiske spørgsmål routes til egen rådgiver |
| 7. Bud | Køber indsender pris, vilkår og frist | Validerer felter, mandatstatus, evidens og idempotens | Køber træffer budbeslutning | Ugyldigt mandat eller nødvendig evidens |
| 8. Modbud | Køber accepterer, afviser eller afgiver nyt bud | Bevarer versionskæde og status | Sælger træffer egen beslutning | Ingen skjult minimumspris-feedback |
| 9. Platformstatus | Køber ser modtaget/afventer/platformaccept | Viser præcis status og dens begrænsning | Advokat afklarer juridisk virkning | Ingen “handel gennemført” alene på platformaccept |
| 10. Juridisk engagement | Køber vælger rådgiver | Sender kun valgte data efter aktivt samtykke | Advokat konfliktkontrollerer og accepterer klientforhold | Intet automatisk klientforhold |
| 11. Forbehold | Køber følger frister og dokumenter | Viser frist, ansvarlig og status | Bank/advokat vurderer og handler | Fristoverskridelse eskaleres; systemet afgør ikke retsvirkning |
| 12. Afslutning | Køber følger skøde, betaling og overtagelse | Read-only status og påmindelser | Advokat/berigtigelsespartner, bank og sælger udfører | Ingen betaling gennem Optata |
| 13. Efterforløb | Køber bekræfter modtagelse og evt. servicebehov | Lukker platformforløb og retention | Leverandører håndterer egne reklamationer | Ingen automatisk krydssalg på fortrolige data |

### 6.1 Købers undtagelser

- **Medkøber kan ikke godkende:** Den relevante handling står som afventende; primær køber kan ikke omgå medkøberens nødvendige godkendelse.
- **Finansieringsbevis udløber:** Nye bud kan blokeres efter en vedtaget regel. Eksisterende bud må ikke automatisk slettes eller annulleres; status og konsekvens skal være eksplicit.
- **Bank afslår finansiering:** Platformen registrerer kun en dokumenteret status/meddelelse. Kontraktens forbehold og juridiske konsekvenser vurderes af advokat.
- **Køber vil trække bud tilbage:** Append-only tilbagetrækningshændelse; historikken bevares. Om tilbagetrækningen har juridisk virkning afhænger af gældende vilkår og aftale.
- **Køber ønsker at træde tilbage efter accept:** Ingen generisk fortryd-knap. Opret anmodning om juridisk afklaring.
- **Andelsbolig:** Forenings-/administratorgodkendelse er et selvstændigt fulfillment-spor.
- **Dødsfald, værgemål eller ændret repræsentation:** Handlinger sættes i bero, og authority kontrolleres på ny.

## 7. Sælgerrejse — fra bolig til afsluttet salg

| Fase | Kundens handling og skærmbillede | Optata gør | Selvstændig part / beslutning | Stopregel |
|---|---|---|---|---|
| 1. Start | Sælger vælger bolig og “Jeg vil sælge” | Opretter kladde og viser datakilder | Sælger oplyser formål | Uklar bolig/identitet |
| 2. Rådighed | Sælger dokumenterer ejer-/andelsret | Indsamler og viser evidensstatus | Advokat/administrator kan verificere | Ingen antagelse ud fra MitID alene |
| 3. Parter | Medejere inviteres | Registrerer partsroller og individuelle approvals | Hver ejer godkender | Uafklaret ejer eller manglende godkendelse |
| 4. Mandat | Sælger vælger DIRECT eller mæglervej | Viser scope, version, udfører og varighed | Mægler/advokat indgår eget mandat hvis relevant | Ingen publicering uden gyldigt platformmandat og nødvendige aftaler |
| 5. Klargøring | Sælger vælger tilvalg | Bestillinger og status | Serviceleverandører udfører | Ingen bestilling uden accept |
| 6. Præsentation | Sælger gennemser boligmateriale | Proveniens, rettigheder, versioner og preview | Fagpartnere står for egne dokumenter | Fejl/manglende rettigheder |
| 7. Publicering | Sælger godkender | Publicerer tilladt version | Mægler kun efter eget engagement | Samtykke/mandat udløbet |
| 8. Bud | Sælger sammenligner bud | Viser budvilkår, frister og status | Sælger træffer valg | Fortrolig minimumspris skjules for køber |
| 9. Godkendelse | Medejere/fuldmægtige godkender konkret version | Kontrollerer authority og approvals | Hver nødvendig part godkender | Manglende authority |
| 10. Handoff | Sælger vælger advokat/rådgiver | Opretter begrænset handoff | Advokat accepterer/afviser klientforhold | Ingen automatisk sagsoprettelse hos advokat |
| 11. Fulfillment | Sælger følger forbehold og dokumenter | Status, frister og næste handling | Advokat, bank, forening og partner udfører | Juridisk tvist/uklarhed routes |
| 12. Overtagelse | Sælger afleverer bolig/nøgler | Checkliste og status | Parterne og relevante partnere gennemfører | Optata håndterer ikke købesum |

### 7.1 Sælgers undtagelser

- **Sameje:** Alle nødvendige ejere godkender samme mandat- og budversion, medmindre gyldig fuldmagt dækker den konkrete handling.
- **Fuldmagt:** Omfang, udsteder, modtager, gyldighed, dokumentation og tilbagekaldelse registreres. En fuldmagt giver ikke bredere adgang end dens dokumenterede scope.
- **Andelsbolig:** Andelsret dokumenteres særskilt; EJF/Tingbog er ikke i sig selv tilstrækkeligt bevis. Foreningens godkendelser er separat.
- **Mandat tilbagekaldes før accept:** Nye handlinger og publicering stoppes efter vedtaget regel; eksisterende bud bevares med korrekt status.
- **Mandat tilbagekaldes efter platformaccept:** Ingen automatisk annullering af juridisk aftale; opret juridisk afklaringsforløb.
- **Skift DIRECT/mæglervej:** Kræver ny udfører-/mandatversion, relevante godkendelser og eksplicit overgang for åbne bud og bestilte services.
- **Dødsbo:** Se §8. Mandat overføres aldrig automatisk til arving.

## 8. Dødsbo, arvinger og repræsentation

Dødsbo er et særskilt authority-forløb. MitID identificerer personen, men dokumenterer ikke rådighed over boets bolig.

| Scenarie | Platformens reaktion | Nødvendig kontrol/ansvar |
|---|---|---|
| Ene arving, privat skifte | Eksisterende mandat suspenderes; nyt repræsentationsforløb | Skifteattest og rådighed kontrolleres manuelt; nyt mandat/ny accept |
| Flere arvinger | Mandat og budaccept blokeres indtil authority er klar | Alle nødvendige arvinger godkender eller gyldig fuldmagt/bobestyrer dokumenteres |
| Bobestyrer | Begrænset ESTATE_ADMINISTRATOR-relation | Beskikkelse, scope og begrænsninger kontrolleres |
| Dødsfald under aktivt mandat | Suspender mandat og stop nye bud/accept | Juridisk vurdering af eksisterende bud og aftaler |
| Dødsfald efter platformaccept | Sæt fulfillment i bero | Advokat vurderer aftale og boets repræsentation |
| Tvist mellem arvinger | ESTATE_DISPUTED / fail closed | Ingen automatisk afgørelse; manuel juridisk håndtering |
| Arving vil købe boligen | Ikke almindeligt OfferLedger-flow i v1 | Særskilt arve-/boafklaring |
| Andelsbolig i bo | Separat andels- og foreningsspor | Boets rådighed og foreningens regler kontrolleres |

**Invariants:**
- Mandat og bud overføres ikke automatisk.
- Boet er den relevante part; en arving handler kun med dokumenteret authority.
- Alle ændringer i repræsentation og mandat logges append-only.
- Ingen unødvendige oplysninger om dødsfaldet vises til købere.
- Uenighed eller uklar dokumentation stopper automatiserede handlinger.

## 9. FulfillmentCase — fra platformstatus til overtagelse

FulfillmentCase koordinerer fremdrift. Den ejer ikke købsaftalen, klientforholdet, skødet, deponeringskontoen eller købesummen.

### 9.1 Trin og ansvar

| Trin | Optata workflow | Ansvarlig ekstern part | Minimumsevidens/status |
|---|---|---|---|
| 1. Platformaccept | Opretter case fra præcis budversion | Køber/sælger; juridisk rådgiver afklarer virkning | Budversion, vilkår, aktører, tidsstempel |
| 2. Engagement | Viser valg og status for rådgiver | Advokat accepterer klient, konfliktkontrollerer og indgår aftale | Engagement status; ingen klienthemmeligheder i platformen |
| 3. Købsaftale | Viser dokumentstatus og underskriftsprogress | Advokat udarbejder/gennemgår; parter underskriver | Dokumentversion og signaturstatus |
| 4. Forbehold | Frister, ansvarlig og reminders | Advokat rådgiver; bank/part opfylder | Type, frist, status og begrænset evidens |
| 5. Finansiering | Statusmarkør | Bank/realkredit træffer beslutning | Kun nødvendig status; ikke kreditmodel |
| 6. Forenings-/administratorforhold | Separat andels-/godkendelsesspor | Forening/administrator | Ansøgning og godkendelsesstatus |
| 7. Skøde | Dokumentstatus | Advokat/berigtigelsespartner | Skødeversion og signaturstatus |
| 8. Tinglysning | Status og frister | Berigtigelsespartner | Kvittering/status fra autoritativ kilde |
| 9. Købesum/deponering | Ingen betalingsfunktion | Bank/autoriseret deponeringspart | Betalings-/deponeringsstatus uden midler gennem Optata |
| 10. Refusion | Status og dokumentlink | Ansvarlig rådgiver/berigtigelsespartner | Refusionsopgørelse og godkendelsesstatus |
| 11. Overtagelse | Checkliste og tidsplan | Køber/sælger og aftalt servicepartner | Nøgle-/adgangsstatus, aflæsning og protokol |
| 12. Lukning | Lukker platformforløb efter bekræftelse | Hver leverandør bekræfter egne leverancer | Lukkegrund, retention og åbne reklamationer |

### 9.2 Stop- og afvigelsesforløb

Følgende skal have særskilte statusser, ansvarlige og eskaleringer:
- Finansiering afslås eller forbehold udløber.
- En part underskriver ikke.
- Købsaftale eller bilag ændres efter godkendelse.
- Tinglysning afvises eller får anmærkning.
- Forening/administrator afviser køber.
- En part ønsker ophævelse/fortrydelse.
- Dødsfald, konkurs, værgemål eller fuldmagtstilbagekaldelse.
- Overtagelse forsinkes, skade opstår eller der opstår tvist.
- Advokat/partner afviser eller afslutter engagement.

Platformen skal kunne pause, genoptage, eskalere og dokumentere. Den må ikke selv afgøre juridisk konsekvens eller automatisk ændre parternes rettigheder.

## 10. Data, adgang, samtykke og selskabsadskillelse

### 10.1 Datazoner og minimumsdeling

- Zone A register-/ejendomsfakta følger eksisterende least-privilege-regler.
- Zone B efterspørgsels- og sagsdata er lukket som udgangspunkt og kræver konkret adgangsgrundlag.
- Zone C er ikke automatisk anonym, fordi et aggregat har k≥5. Disclosure-kontroller, suppression, differencing og formålsvurdering er påkrævet.
- Købers identitet, økonomi, dokumenter og bud deles ikke med B2B som standard.
- Advokatens klientjournal og rådgivningsnotater forbliver i advokatselskabets systemer; Optata modtager kun eksplicitte statusser eller dokumenter, der lovligt og nødvendigt kan deles.
- Servicepartner får kun de oplysninger, der er nødvendige for den konkrete opgave. Fotograf behøver eksempelvis ikke køberens finansieringsstatus.

### 10.2 Samtykke og retsgrundlag

Samtykke er ikke en universel erstatning for behandlingsgrundlag. For hver dataoverførsel skal ansvarlig part dokumentere:
- Formål og modtager.
- Datakategorier og nødvendighed.
- Behandlingsgrundlag og eventuel oplysningspligt.
- Om modtageren er selvstændig dataansvarlig, fælles dataansvarlig eller databehandler.
- Opbevaringsperiode, sletning og adgangslog.
- Tilbagekaldelse og konsekvenser for fremtidig behandling.

Kunden skal kunne se, hvilke data der deles, og med hvem. Et samtykke til at sende en henvendelse til advokatselskabet er ikke samtykke til markedsføring, lead-salg eller deling med andre partnere.

### 10.3 B2B og købermuligheder

Tre adskilte produkter kan undersøges:
1. Aggregeret efterspørgselsindsigt uden identificerbare personer, underlagt Zone C-kontrol.
2. Match-/mulighedsnotifikation uden identitet eller kontaktoplysninger.
3. Køberinitieret introduktion, hvor køberen aktivt vælger en konkret modtager og et bestemt formål.

Rå persondata-/lead-eksport er ikke standardprodukt og må ikke bygges uden særskilt juridisk, privacy- og produktgodkendelse.

### 10.4 Selskabsrelationer

Hvis selskaberne har fælles ejere, ledelse, kontorer, systemer eller kommercielle aftaler, skal dette vurderes og dokumenteres. Adskillelse i CVR-numre alene beviser ikke reel uafhængighed. Der skal være:
- Separate kunde-/klientaftaler og fakturaer.
- Separate beslutninger om klientaccept og leverance.
- Dokumenteret konfliktkontrol og professionel uafhængighed.
- Adgangsbegrænsning og adskilte journal-/sagsrum.
- Klare dataansvarsroller og databehandleraftaler hvor relevante.
- Gennemsigtig markedsføring og ingen automatisk antagelse om engagement.
- Juridisk vurdering af henvisningsbetaling, koncernbetaling, fælles markedsføring og servicepakker.

## 11. Betaling og økonomiske grænser

| Pengestrøm | Modtager | Optatas rolle | Gate |
|---|---|---|---|
| Privat/B2B platformabonnement | Optata | Fakturerer egne softwareydelser | Vilkår, moms, forbrugerret og betalingsflow |
| Advokathonorar | Advokatselskab | Ingen opkrævning på vegne af advokat som standard | Egen klientaftale og lovlig fakturering |
| DIRECT serviceordre | Den navngivne serviceleverandør | Viser ordre/status; evt. teknisk PSP-integration efter review | Ingen custody; klare refundering-/reklamationsvilkår |
| Mæglerhonorar | Mæglerfirma | Ingen opkrævning som standard | Separat mægleraftale |
| Købesum/deponering | Parter via bank/autoriseret deponeringspart | Ingen rolle, konto eller disposition | Absolut teknisk og operationel blokering |

Platformens abonnementsbetaling må ikke beregnes som procent af købesum, udløses af closing eller på anden måde reelt være betinget af en bestemt handel uden forudgående juridisk vurdering og ændring af denne model.

## 12. Kundeservice, klager og hændelser

Kunden skal kunne vælge “Hjælp” fra hver sag. Optata klassificerer henvendelsen og sender den til den ansvarlige part uden at love at afgøre den.

| Henvendelsestype | Første modtager | Ansvarlig for løsning | Optatas rolle |
|---|---|---|---|
| Login, datafejl, platform, notifikation | Optata support | Optata | Ejer og løser |
| Budstatus/teknisk fejl | Optata support | Optata for systemadfærd; juridisk part for retsvirkning | Sikrer audit og eskalering |
| Juridisk rådgivning eller tvist | Advokatselskabet, hvis klient | Advokatselskabet/egen rådgiver | Ingen adgang til fortrolig rådgivning |
| Finansiering | Bank | Bank | Viser kun nødvendig status |
| Foto, rapport, rengøring, håndværk | Leverandøren | Leverandøren | Ruter klage, viser kontakt og ordre |
| Fremvisningshændelse/sikkerhed | Optata akut kontakt + leverandør | Ansvarlig fysisk udfører; myndigheder ved akut fare | Bevarer hændelseslog og eskalerer |
| Persondatasikkerhed | Relevant dataansvarlig | Den dataansvarlige efter incident-plan | Koordinerer kun egne forpligtelser |

Supportmedarbejdere får ikke generel adgang til Zone B/C, bud eller dokumenter. “Break glass” skal være tidsbegrænset, begrundet, logget og efterkontrolleret.

## 13. Teknisk domæne- og modulopdeling

Følgende er foreslåede bounded contexts; ejerskab og kontrakter skal godkendes før implementering.

| Modul/kontekst | Ejer | Ansvarsområde | Må ikke eje |
|---|---|---|---|
| Identity & Authority | Platform security/identity | Principal, relation, capability, fuldmagt og authority-evidens | Juridisk konklusion om ejendomsret |
| Buyer Demand | Buyer domain | Købsintention, køberordre og husstandsrelationer | Bankens kreditbeslutning |
| Seller & SaleMandate | Seller/mandate domain | Sælgerparter, mandatversioner, godkendelser og suspension | Advokatengagement |
| Property Registry | Registry domain | Proveniens, bitemporal ejendoms-/registerfakta | Kundens juridiske rådighed alene |
| PropertyPresentation | Listing/presentation domain | Boligmateriale, kilde, version, publicering | Fagpartnerens professionelle ansvar |
| ServiceOrder | Service orchestration | Bestilling, leverandør, status, vilkår og reklamation-reference | Leverandørens interne drift |
| Viewing | Viewing domain | Booking, adgangsinstruktioner med begrænset scope, attendance | Nøgler/adgangsmidler som varig master |
| OfferLedger | Offer domain | Bud, modbud, frister, acceptstatus, skjult tærskel | Juridisk bindende aftale |
| FulfillmentCase | Workflow domain | Afhængigheder, frister, handoffs og read model | Købsaftale, klientjournal, købesum |
| Consent & Disclosure | Privacy domain | Formål, modtager, scope, version, tilbagekaldelse | Automatisk juridisk vurdering |
| Subscription & Billing | Commercial domain | Platformens abonnementer og fakturaer | Advokat-/leverandørhonorar som egne indtægter |
| Partner Directory | Partner domain | Leverandørprofil, kompetencer, status, aftaleversion | Professionel autorisation uden verificering |

### 13.1 Cross-module workflow

- Hvert domæne ejer egne commands, events og data.
- FulfillmentCase og RelocationCase er koordinatorer/read models, ikke master for de underliggende transaktioner.
- Handoff bruger versionerede kontrakter, idempotency keys, audit-before-side-effect og transactional outbox.
- Ingen modulopdaterer et andet moduls tabeller direkte.
- Eksterne svar behandles som ubetroede input og valideres mod konkret sag, modtager og forventet tilstand.
- Fejl kan genoptages uden dobbeltbestilling eller dobbeltaccept.

## 14. Produktmæssige acceptance criteria

Følgende skal kunne demonstreres i syntetisk miljø før produktionsdesign godkendes.

### 14.1 Selskabs- og ansvarsskel
- [ ] En kunde kan bruge Optata uden at blive klient hos advokatselskabet.
- [ ] Advokatkontakt kræver aktiv handling; klientforhold oprettes først efter advokatens egne kontroller og accept.
- [ ] Hver bestilling viser kontraktuel leverandør, pris, betalingsmodtager og klagevej.
- [ ] Ingen platformtekst antyder, at Optata er kundens advokat, mægler eller repræsentant.
- [ ] Ingen transaktionsbetaling eller klientmidler kan gå gennem Optatas konti.

### 14.2 DIRECT
- [ ] Sælger kan gennemføre DIRECT med kun de serviceydelser, vedkommende selv vælger.
- [ ] Klargøring, foto, dokumenter, fremvisning og Q&A har hver en ansvarlig og en afslutningsstatus.
- [ ] Sælger kan se og godkende præcis den boligversion, der publiceres.
- [ ] Fremvisningsadgang og sikkerhedsoplysninger udløber og er ikke synlige for uvedkommende.
- [ ] Serviceaflysning og reklamation routes til korrekt leverandør.

### 14.3 Køber/sælger og bud
- [ ] Medejer-/medkøbergodkendelse kan ikke omgås via primær bruger.
- [ ] Ugyldig eller tilbagekaldt fuldmagt stopper nye handlinger.
- [ ] Dødsbo suspenderes ved tvivl og genaktiveres ikke automatisk.
- [ ] Bud på præcis 80 % af fortrolig minimumspris udløser kun sælgernotifikation.
- [ ] Bud under tærsklen bevares i oversigten, men udløser ikke tærskelnotifikation.
- [ ] Køber kan ikke udlede minimumspris via API, UI, timing, fejlbesked, gentagne bud eller partneradgang.
- [ ] Samtidige accept-/tilbagekaldelseskommandoer giver en entydig, auditeret rækkefølge.

### 14.4 Fulfillment og betaling
- [ ] Platformaccept kan ikke forveksles med juridisk underskrift eller closing.
- [ ] Hver frist har ansvarlig part, kilde og eskalering.
- [ ] Advokat-/bank-/foreningsafvisning sætter relevante trin i bero uden at slette historik.
- [ ] Optata har ingen konto, API eller supportprocedure, der kan modtage/disponere købesum.
- [ ] Handoff er idempotent og kan genoptages efter timeout uden dobbeltoprettelse.

### 14.5 Data og rettigheder
- [ ] En partner ser kun felter og dokumenter, der er nødvendige for den konkrete opgave.
- [ ] Tilbagekaldelse stopper fremtidig deling, hvor det er relevant, uden at omskrive lovlig historik.
- [ ] Advokatens fortrolige klientmateriale er ikke synligt for Optata-support eller andre partnere.
- [ ] B2B kan ikke eksportere køberidentitet, økonomi eller budhistorik som standard.
- [ ] Alle adgangs- og delingshændelser kan auditeres.

## 15. Juridiske og regulatoriske release gates

Før et reelt handelsflow kan lanceres, skal uafhængig dansk rådgiver skriftligt vurdere mindst:

1. Om Optatas konkrete matching, annoncering, mandatopsætning, budfacilitering, fremvisningskoordinering og indtægtsmodel udgør eller nærmer sig reguleret ejendomsformidling eller anden reguleret aktivitet.
2. Hvilke aktiviteter platformen må udføre, og hvilke der skal udføres af en registreret/autoriseret professionel.
3. Advokatselskabets selskabsform, uafhængighed, ejerskab/ledelse, interessekonflikter, klientforhold, henvisninger og markedsføring.
4. Om advokatselskabet kan levere eller koordinere ikke-juridiske serviceydelser, og om særskilt serviceselskab er nødvendigt.
5. Dataansvar, fælles dataansvar, databehandlerforhold, behandlingsgrundlag, DPIA, oplysningspligt og datadeling mellem selskaber.
6. Forbrugerret, abonnementsvilkår, digitale tjenester, servicebestillinger, fortrydelse, afbestilling og klager.
7. Bud, modbud, platformaccept, elektronisk signatur, forbehold, fortrydelse og aftalebinding.
8. Betalingsflow, PSP, deponering, klientmidler, moms og fakturering.
9. Partneraftaler, ansvar, forsikring, underleverandører og markedsføringsudsagn.
10. B2B-produkter og eventuel adgang til købermuligheder, herunder GDPR, ePrivacy/markedsføring og konkurrence-/forbrugerhensyn.

**Gate-evidens:** Juridisk notat med afgrænset scope, antagelser, vurderet faktisk brugerrejse, selskabsdiagram, betalingsdiagram, datakort, godkendte/forbudte aktiviteter og eksplicitte betingelser. Generiske vilkår eller en selskabsregistrering er ikke tilstrækkelig evidens.

## 16. Beslutningsregister

| ID | Beslutning | Foreslået retning | Status |
|---|---|---|---|
| SRA-01 | Optatas rolle | Platform, ikke part i købsaftale, juridisk rådgiver eller købesumsmodtager | Stifterretning; juridisk review |
| SRA-02 | Advokatselskab | Selvstændigt klientforhold, konfliktkontrol, engagement og fakturering | Stifterretning; professions-/selskabsretligt review |
| SRA-03 | Serviceselskab | Behandles som separat juridisk enhed fra advokatselskab indtil andet er godkendt | Foreslået; stifterbeslutning |
| SRA-04 | DIRECT | Fuld servicevej med frivillige bestillinger og tydeligt leverandøransvar | Produktretning |
| SRA-05 | Fremvisning | Booking i Optata; fysisk adgang og sikkerhed hos sælger/udpeget udfører | Foreslået; operationel validering |
| SRA-06 | FulfillmentCase | Koordinerer status og handoffs, ejer ikke juridiske dokumenter eller midler | Foreslået; domæne-/arkitekturreview |
| SRA-07 | Platformindtægt | Abonnement, ikke closing-afhængig betaling | Stifterretning; juridisk review |
| SRA-08 | Servicebetaling | Direkte til leverandør eller godkendt PSP; ingen Optata-custody | Foreslået; betalingsreview |
| SRA-09 | B2B-købermuligheder | Aggregeret indsigt eller køberinitieret, konkret introduktion | Produktretning; privacy/juridisk review |
| SRA-10 | Kundeoplevelse | Én Optata-oversigt, adskilte leverandørsager og journaler | Foreslået |
| SRA-11 | Juridisk bindende accept | Platformstatus er ikke i sig selv juridisk konklusion | Åbent juridisk release gate |
| SRA-12 | Priser/pakker | Udskydes; arkitekturen skal understøtte flere niveauer | Stifterretning |
| SRA-13 | Pilot og markedsopstart | Udskydes til produkt- og juridisk readiness | Stifterretning |

## 17. Næste leverancer og rækkefølge

1. **Stifterbeslutninger:** Afklar om advokatselskabet og serviceselskabet er to juridiske enheder, og godkend de produktmæssige grænser i SRA-01–SRA-13.
2. **Juridisk vurdering:** Giv uafhængig rådgiver den faktiske service blueprint, RACI, selskabsdiagram, betalingsflow og dataflow – ikke kun en abstrakt beskrivelse.
3. **Skærm-for-skærm UX:** Omsæt køber, sælger, DIRECT, fremvisning og FulfillmentCase til skærme, fejltilstande, tomme tilstande og mobilflows.
4. **Domænekontrakter:** Specificér PropertyPresentation, ServiceOrder, Viewing og FulfillmentCase med states, events, commands, ownership og idempotency.
5. **Syntetisk prototype:** Test begge komplette rejser, herunder sameje, fuldmagt, dødsbo, andel, finansiering og afvigelser.
6. **Teknisk hardening:** Luk S0/S1-auditfund og Architecture Contracts før real-data transaktionsflow.
7. **Baselineopdatering:** Først efter eksplicit godkendelse indarbejdes accepterede beslutninger i v5.2, ADR'er, arkitektur, kontrakter og backlog.

### Definition of Ready for implementation

En funktion er først klar til implementering, når:
- Produktejer og ansvarlig leverandør er identificeret.
- Juridisk gate er enten lukket eller funktionen er tydeligt afgrænset til syntetisk/testbrug.
- State machine, authority, consent, datazone og audit er beskrevet.
- Fejl-, aflysning-, timeout-, genoptagelses- og klageforløb er defineret.
- Acceptance criteria og negative sikkerhedstests er skrevet.
- Kontrakter og module ownership er reviewet.

**Målet er ikke at skjule ansvaret bag én samlet platform. Målet er at gøre kundens rejse enkel, samtidig med at ansvar, data, penge og professionelle beslutninger forbliver hos den rigtige part.**
