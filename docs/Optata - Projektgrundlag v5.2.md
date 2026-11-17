# OPTATA — Samlet projektgrundlag

**Version 5.2 · 17. november 2026 · Status: beslutningsbaseline til stiftergodkendelse**

> **Autoritet:** Dette dokument erstatter v5.1 som gældende produkt- og beslutningsbaseline, når PR'en er godkendt. v5.1 bevares som historisk beslutningsgrundlag. Arkitekturen er specificeret i `docs/architecture/ARCHITECTURE.md`; implementeringsrækkefølgen i `docs/backlog/`. Juridiske spørgsmål er ikke juridiske svar.

## 0. Executive baseline

Optata er en efterspørgselsdrevet markedsplatform for boligmarkedet. Platformen samler verificeret købsintention, giver sælgeren mulighed for at give Optata et afgrænset salgsmandat, gennemfører budprocessen i en struktureret og auditerbar budbog og lader kvalificerede partnere udføre de opgaver, som kræver autorisation eller lokal faglighed.

Optata er ikke en boligportal, et leadbureau eller blot et analyseprodukt. Den langsigtede platformsværdi ligger i sammenhængen mellem:

1. **Registerlaget** — autoritative ejendoms- og geografidata med kilde, licens og bitemporal historik.
2. **Efterspørgselslaget** — købsintention med identitet, købeevne, samtykke og udløb.
3. **Mandatlaget** — sælgerens dokumenterede og tilbagekaldelige autorisation.
4. **Markeds-/budlaget** — strukturerede bud, modbud, accept og statusændringer.
5. **Udførelseslaget** — partner eller mægler med afgrænset adgang og ansvar.
6. **Distributionslaget** — analyser, licenserede udbud og samtykkebaserede kampagner.

**Strategisk tese:** Optata ejer platformens relation, proces og datahistorik. Det betyder ikke, at Optata automatisk har juridisk ret til at udføre alle aktiviteter. Produktansvar, dataansvar og lovregulerede formidleropgaver skal være eksplicit adskilt.

## 1. Beslutningshierarki

Ved uoverensstemmelse gælder følgende rækkefølge:

1. Lovgivning, myndighedskrav og skriftlige juridiske vurderinger for den konkrete aktivitet.
2. Dette projektgrundlag v5.2 for produkt- og forretningsbeslutninger.
3. `docs/architecture/ARCHITECTURE.md` for tekniske invariants og systemgrænser.
4. Accepterede ADR'er for afgrænsede arkitekturvalg.
5. Aktuelle sprintbacklogs for leverancer og acceptkriterier.
6. Designoplæg, gamle bilag og historiske backlogversioner som baggrund, ikke som aktuelle krav.

Ingen backlog eller designfil kan tilsidesætte en invariant eller et juridisk release gate.

## 2. Produktbeslutninger

| ID | Beslutning | Konsekvens |
|---|---|---|
| P-01 | Struktur C er valgt som målretning: Optata ejer origination, mandatoplevelse og budrails; partner/mægler kan udføre regulerede eller delegerede opgaver | Ingen implementering må antage, at Optata allerede har mæglertilladelse |
| P-02 | MitID fra første identitetsbærende flow | Ingen e-mail-ordre, magic-link-identitet eller CURIOS-niveau |
| P-03 | Ordreniveauer er QUALIFIED og VERIFIED | Kun VERIFIED tæller i verificeret efterspørgsel og kan afgive bud |
| P-04 | Ingen uopfordret ejerkontakt | Ejeren initierer kontakt ved selv at logge ind; notifikation er særskilt opt-in |
| P-05 | SaleMandate er et eksplicit, versionsbundet, tilbagekaldeligt mandat | Alle relevante ejere/parts skal være identificeret og godkende |
| P-06 | OfferLedger er den autoritative budhistorik | Bud og statusændringer er append-only; fri relay-chat er ikke transaktionsmotor |
| P-07 | DIRECT og AGENT_EXECUTED er to udførelsesveje | Begge bruger samme mandat- og budrails; kun udførelsen og vederlaget adskiller sig |
| P-08 | Mægler får kun scoped deltagelse | Ingen eksport af ordrebog, køberidentitet eller bud uden for udtrykkelig lovlig proces |
| P-09 | Campaign er et separat distributionsmodul | Kræver eget aktivt licenseret udbud, gyldigt samtykke og målretnings-/frekvensguards |
| P-10 | Modulær monolit er første implementeringsform | Ingen mikroserviceopdeling før målbar driftsmæssig begrundelse |
| P-11 | Optata, advokatselskabet og serviceselskabet er tre selvstændige juridiske selskaber | Egne aftaler, leverancer, beslutninger, fakturering, ansvar og adgangsgrænser; konkret juridisk/regulatorisk vurdering er fortsat påkrævet |
| P-12 | Area Intelligence er et selvstændigt produktområde, der sammen med Property Discovery bygger på én fælles geografisk rygrad | Områder profileres med dokumenterede faciliteter og tilgængelig statistik; geografiske niveauer og datakilders opløsning må ikke forveksles |

## 3. Produktets aktører og ansvar

| Aktør | Kan | Kan ikke uden særskilt grundlag |
|---|---|---|
| Køber | Oprette/vedligeholde ordre, dokumentere købeevne, se relevante udbud, afgive/tilbagetrække bud | Se andre køberes identitet eller kontakte sælger uden for processen |
| Sælger/ejer | Verificere ejerskab, læse aggregeret interesse, oprette/tilbagekalde mandat, vælge udfører, behandle bud | Give mandat på vegne af medejere uden gyldig fuldmagt |
| Optata-platformsselskabet | Drive platform, adgangskontrol, matching, mandat- og budworkflow, audit, rapportering og egne softwareprodukter | Udføre lovreguleret ejendomsformidling uden nødvendig tilladelse/partnerstruktur; automatisk optræde som advokat eller serviceleverandør |
| Advokatselskabet | Indgå eget klientforhold, udføre særskilt engageret juridisk rådgivning og juridiske/berigtigelsesopgaver | Få automatisk klientforhold eller adgang til Optatas/Serviceselskabets data; levere ikke-juridiske services på Serviceselskabets vegne uden særskilt aftale og juridisk afklaring |
| Serviceselskabet | Indgå egne serviceaftaler og levere/koordinere ikke-juridiske ydelser inden for godkendt forretningsområde | Yde juridisk rådgivning, optræde som advokat eller disponere over advokatselskabets klientforhold/journal |
| Mægler/øvrig leverandør | Udføre tildelte opgaver inden for egen aftale, autorisation/licens og konkret scope | Se andre mandater, eksportere ordrebog eller overtage relationen uden hjemmel |
| B2B-kunde | Købe licenserede analyser og aggregerede indsigter | Re-identificere, sammenkøre eller eksportere beskyttede data |

### 3.1 Fast selskabs- og ansvarsgrænse

Optata-platformsselskabet, advokatselskabet og serviceselskabet er tre selvstændige juridiske selskaber. Dette er en fastlagt stifterbeslutning og ikke en åben produktmulighed. Hvert selskab indgår egne aftaler, træffer egne beslutninger, fakturerer egne ydelser og bærer ansvaret for egne leverancer. Et login, mandat eller kundeforhold hos ét selskab opretter ikke automatisk et aftale-, klient- eller repræsentationsforhold hos et andet.

Advokatselskabet ejer klientaccept, konfliktkontrol, juridisk rådgivning, egen journal og professionelt ansvar. Serviceselskabet ejer egne ikke-juridiske serviceaftaler og leverancer, herunder klargøring, rengøring, styling, fotografering, fremvisning og praktisk koordinering. Optata ejer softwareplatformen og egne platformprodukter. Eksterne leverandører kan indgå særskilte aftaler med Serviceselskabet eller kunden; den konkrete kontraktpart skal altid fremgå.

Selskabsadskillelsen fastlægger ikke i sig selv dataansvarsroller, lovligheden af henvisninger, fælles markedsføring, fælles ejerskab/ledelse, delte IT-systemer eller betalingsflows. Disse forhold kræver konkret juridisk og databeskyttelsesretlig vurdering. Data må kun deles efter dokumenteret formål, behandlingsgrundlag, modtagerrolle og mindst mulige scope.

## 4. Markedsmodellen

### 4.1 Efterspørgsel
En ordre er en struktureret købsintention knyttet til geografi, boligtype, økonomisk interval og tidsramme. QUALIFIED betyder, at de krævede ordreoplysninger er udfyldt. VERIFIED betyder MitID-identitet og gyldig, godkendt købeevneattest efter den gældende verifikationspolitik. Attester udløber; udløb nedgraderer status og fjerner adgang til bud.

### 4.2 Mandat
SaleMandate er sælgerens tilladelse til, at Optata kan gennemføre præcist angivne platformshandlinger. Mandatet skal som minimum indeholde adresse/ejendom, samtlige mandatsgivende parter, mandatets omfang, valgt udførelsesvej, vilkårsversion, gyldighed, tilbagekaldelsesregler og auditspor. Mandatet er ikke i sig selv dokumentation for, at Optata må udføre lovreguleret formidling.

### 4.3 Bud
OfferLedger registrerer bud, modbud, vilkår, finansieringsstatus, frist og beslutninger som uforanderlige hændelser. Et accepteret bud starter fulfillment, men må ikke beskrives som en juridisk bindende købsaftale, før den relevante juridiske proces og dokumentation er fastlagt.

### 4.4 Udførelsesveje
- **DIRECT:** sælger vælger Optatas partner-/closingforløb uden at tilknytte en ejendomsmægler. Optata må kun levere de platformstjenester, som den juridiske model tillader. Fast gebyr på 10.000 kr. er en tidligere forretningsantagelse, ikke en juridisk undtagelse.
- **AGENT_EXECUTED:** sælger vælger en mægler/udfører. Udføreren får adgang til det konkrete mandat og tilknyttede opgaver. Optata beholder platformens proces- og auditspor.

Begge veje er produktmæssige målbilleder. Ingen af dem må lanceres, før L38–L42 og de relevante øvrige juridiske spørgsmål er besvaret skriftligt.


### 4.5 Koordineret flytning — RelocationCase

Optata skal understøtte en families koordinerede flytning, hvor salg af nuværende bolig og køb af ny bolig vurderes som ét samlet beslutningsforløb. Dette er en central tværgående use case og ikke en ny handelstype.

- **RelocationCase** er proces- og koordinationsobjektet for husstandens flyttemål, ønsket tidsvindue, boligbehov, økonomiske rammer, scenarier, afhængigheder og beslutningshistorik.
- Salg og køb forbliver separate domænespor. Salgssporet refererer til SaleMandate og eventuelle OfferLedger-objekter. Købssporet refererer til købsintention/ordre, relevante boligmuligheder og eventuelle bud som køber.
- RelocationCase ejer ikke mandatet, købsordren, boligen, buddet, finansieringsbeviset eller en købsaftale. Den koordinerer kun gennem versionsbundne referencer og domænekontrakter.
- Et spor kan eksistere, afvente eller afsluttes uafhængigt af det andet. Afslutning, afvisning eller tilbagekaldelse i ét spor må ikke automatisk ændre juridisk status i det andet.
- Deling mellem spor, med partner eller med andre personer kræver særskilt, formåls- og scopebestemt samtykke. Et generelt samtykke til flytteforløbet giver ikke automatisk adgang til identitet, økonomi, mandat eller bud.
- Optata kan vise scenarier som “salg først”, “køb først” og “finansieringsafklaring nødvendig”, men skal skelne mellem verificerede fakta, daterede estimater, mulige match og uafklarede forhold. Et match er ikke dokumentation for tilgængelighed, finansiering eller egnethed.
- Optata må ikke fremstille scenarier som finansiel, juridisk eller ejendomsmæssig rådgivning. Forhold, der kræver autoriseret eller individuel rådgivning, markeres og henvises til relevant fagperson.

RelocationCase er et koordinerende workflow under Architecture Contract C-06 (saga). Eksterne og irreversible handlinger kræver særskilt command, autorisation, samtykke og audit efter C-07. Det samlede forløb må aldrig behandles som én distribueret ACID-transaktion eller én uadskillelig bolighandel.

### 4.6 Area Intelligence og fælles geografisk rygrad

Area Intelligence er et selvstændigt produktområde ved siden af Property Discovery. De to produktområder deler geografisk identitet, geometri, kildeproveniens og område-/ejendomsrelationer:

- **Area Intelligence** beskriver et områdes faciliteter, services, demografi, økonomi, uddannelse, beskæftigelse, boligforhold og øvrige dokumenterede kvaliteter.
- **Property Discovery** beskriver den konkrete adresse og ejendom med registeroplysninger, ejendomsdata og rapporter.
- En bruger skal kunne navigere fra et bredt geografisk niveau til en konkret adresse og fra en ejendom tilbage til dens relevante områder.

Optatas geografiske navigation omfatter: **region → kommune → område → by → bydel → kvarter → gade → hus/adresse**. Dette er en bruger- og produktnavigation, ikke en påstand om ét strengt administrativt træ. Officielle geografier kan overlappe, have forskellige formål eller ændre grænser over tid. Optata skal derfor bevare geografitype, stabil kildeidentifikator, geometri, gyldighed og versionshistorik.

Officielle geografiske enheder (fx region, kommune, byområde, sogn og postnummer) skal holdes adskilt fra Optata-definerede områder, bydele og kvarterer. Optata-definerede områder skal have dokumenterede afgrænsningsregler, versionering og relationer til de officielle enheder. Gader og adresser knyttes til autoritative adresseidentiteter; en ejendom/BFE må ikke sidestilles med én adresse.

Hvert område skal kunne have en standardiseret profil. Produktretningen er at kortlægge **30 primære facilitets- og servicetyper** pr. område og gøre det muligt at åbne kategorien, se de konkrete steder og undersøge deres oplysninger. Den endelige taksonomi, underkategorier og kategorispecifikke kilder fastlægges i en særskilt specifikation/arbejdspakke; eksempler i dialog og prototyper er ikke en endeligt godkendt taksonomi.

Områdeprofiler kan desuden indeholde officielle statistiske indikatorer, herunder indkomst, disponibel indkomst, demografi, beskæftigelse, uddannelse og boligforhold. En indikator må kun vises på den geografiske opløsning, som kilden faktisk understøtter. Optata må ikke nedskalere kommunetal til bydele, kvarterer, gader eller adresser og præsentere dem som observerede lokale tal. Estimater skal være tydeligt mærket, metodebeskrevet og adskilt fra officiel statistik. Små grupper og følsomme statistiske udtræk skal følge kilde- og disclosurebegrænsninger.

Facility discovery kan bruge AI til at finde kandidater og foreslå ændringer, men AI-genererede udsagn er ikke registerfakta. Den tiltænkte kontrolmodel har tre adskilte roller: discovery, uafhængig verification og audit. Kontrollerne skal arbejde på dokumentation og kilder – ikke blot gentage hinandens konklusioner. Kun dokumenterede og godkendte faciliteter tælles som verificerede. Uafklarede, modstridende eller utilstrækkeligt dokumenterede kandidater sættes i karantæne/afventer og må ikke indgå i offentlige totaler. Der skal være sporbarhed til kilde, observationstid, kontrolresultat, geografisk placering, status og ændringshistorik.

Eksterne data må kun indsamles, lagres, sammenstilles og vises inden for dokumenterede licens- og brugsrettigheder. Ingen scraping eller antagelse om videredistributionsret. Realdata og offentlige produktionsprofiler kræver kilde-, licens-, privacy-, sikkerheds- og kvalitetsreview. Første udvikling kan anvende tydeligt mærkede syntetiske data.

Detaljeret produkt- og datakrav findes i [Area Intelligence v1.0](product/AREA-INTELLIGENCE.md). Denne produktretning godkender ikke i sig selv en bestemt dataleverandør, den endelige liste over 30 kategorier, konkrete API-/DB-kontrakter eller produktionsbrug af AI-agenter.

## 5. Campaign og udbudsdata

Campaign er ikke en genindførelse af M3-invitationer. Kampagner kan kun sendes gennem Optatas inbox til købere, som har givet særskilt, informeret, frivilligt og tilbagekaldeligt samtykke til det relevante formål. Mægleren må kun annoncere et udbud, som vedkommende har ret til at markedsføre, og som har gyldig licens-/kilde-reference.

Audience-gulve, k-anonymitet, relevans, mute, suppression og frekvenslofter er kumulative kontroller. En audience-estimering er ikke i sig selv bevis for lovlig målretning. L43–L48 er release gates.

## 6. Indtægtsmodel og økonomisk status

Indtægtsben, der fortsat kan undersøges:
- B2B områdeanalyse og områdeovervågning.
- Licenserede data-/analyseprodukter og Demand Pro.
- Mægler-/udførerabonnement for scoped deltagelse.
- Kampagnebetaling for lovlig, samtykkebaseret rækkevidde.
- Eventuelt ejerbetalt mandat-/fulfillment-produkt.

**Vigtigt:** Priserne i v5.1 (85.000 kr. analyse, 4.500 kr./md. overvågning, 9.500 kr./md. Demand Pro, 2.900/6.900 kr. mægler, 1.495 kr. ejerside og 10.000 kr. pakke) er historiske hypoteser. De er ikke godkendt som v5.2-prisliste. Enhedsøkonomien skal genberegnes ud fra struktur C, betalingsvillighed, juridisk rollefordeling og faktiske konverteringer. Ingen finansiel forecast må præsentere disse som validerede tal.

## 7. Datazoner og datakilder

- **Zone A — offentlige/licenserede virksomheds- og ejendomsdata:** registerdata, geometri, licenserede udbud og rapporteringsgrundlag. Kilde, licens, gyldighed og proveniens er obligatorisk.
- **Zone B — person- og transaktionsdata:** identitet, ordre, attest, samtykke, ejerskabsbevis, mandat, bud, kampagneinteraktion og audit. EU-prod, RLS, mindst privilegium, kryptering, retention og kontrolleret adgang.
- **Zone C — aggregerede produkter:** kun godkendte, tilstrækkeligt aggregerede datasæt. k≥5 er en minimumsregel, ikke et generelt bevis på anonymitet. Supplerende suppression, differensangreb, tidsserier og små geografier skal vurderes.

CPR må ikke lagres. Transient behandling må kun ske efter dokumenteret nødvendighed, leverandørvilkår og juridisk godkendelse. Datafordeler-, EJF-, DAGI-, medie- og udbudsrettigheder må ikke antages; de skal dokumenteres pr. kilde.

## 8. Arkitekturprincipper

1. Modulær monolit med klare domænegrænser.
2. PostgreSQL/PostGIS, separate zoner/roller og RLS som forsvar i dybden.
3. Bitemporal registerhistorik; forretningshændelser append-only.
4. Domæneevents med versionerede kontrakter og idempotente consumers.
5. Ingen service må omgå den autoritative domæne-API eller DB-guard.
6. Matching er forklarlig: score + reason codes + modelversion.
7. Ingen eksport af rå køber-/mandat-/buddata til mægler eller B2B-kunde.
8. Eksterne feeds er licensbundne og må aldrig screen-scrapes.
9. Alle følsomme handlinger er auditerede med actor, purpose, scope og correlation/trace id.
10. Feature flags kan begrænse funktionalitet, men må ikke bruges til at omgå juridiske eller sikkerhedsmæssige guards.

## 9. Faser og rækkefølge

| Fase | Indhold | Kan starte? | Gate |
|---|---|---|---|
| 0 | S0 fundament, CI, sikkerhedsbaseline | Ja, syntetiske data | menneskelig review af røde migrations/guards |
| 1 | S1 register, bitemporalitet, område-API | Ja, syntetiske data; rigtige kilder efter licens/adgang | datakilde- og geometri-afklaring |
| 2 | S2 analyser/agent/kommercielt bevis | Delvist | medielicens, datakvalitet og kundebetaling |
| 3 | S3 MitID, ordre, attest, vault | Kun test/syntetisk indtil juridisk gate | identitets-/persondatagrundlag |
| 4 | S4 SaleMandate | Specifikation nu; produktionskode gated | L38–L42, ejerskab/sameje, kontrakter |
| 5 | S5 OfferLedger | Specifikation nu; produktionskode gated | L38–L40, budretlige regler |
| 6 | S6 Campaign + mæglerdeltagelse | Kampagne-/feed-specifikation nu; produktion gated | L32–L37 og L43–L48 |
| 7 | S7 Fulfillment, partnerdrift og skalering | Senere | L1–L5, L21–L25, partneraftaler og forsikring |
| 8 | Zone C/Demand Pro og større partner-API | Senere | anonymitetsvurdering, licenser, kontrakter og driftskontroller |

Sprints er leveranceenheder, ikke juridiske tilladelser. S2 kan paralleliseres med S3-forberedelse. S4/S5/S6 kan designes og testes på syntetiske data, men må ikke kobles til rigtige personer eller handler før gates.

## 10. Juridiske release gates

| Gate | Spørgsmål | Stopper |
|---|---|---|
| LG-1 | L1–L5: samlet formidlerrolle, ansvar, forsikring, positionering | alle offentlige transaktions-/formidlerclaims |
| LG-2 | L11–L16: persondata, retention, CPR, DPIA | zone B-produktionsbehandling |
| LG-3 | L26–L31: datakilde-, medie-, tredjelands- og IP-rettigheder | relevante realdata-/mediemoduler |
| LG-4 | L32–L37: feed-licens, attribution, udbudsdata | listing/feed-produktion |
| LG-5 | L38–L42: mandat, budbog, rolle, deltagelsesvilkår | SaleMandate, OfferLedger og udføreradgang i produktion |
| LG-6 | L43–L48: marketing-samtykke, profilering, indhold, P2B og retention | Campaign i produktion |
| LG-7 | L21–L25: betaling, AML, forbrugerret | gebyr, pakke og betaling relateret til handel |

Et gate lukkes kun med skriftligt svar, hjemmel, handlingsregel, ansvarlig, dato, berørte dokumenter og accept af konsekvensen. “Afventer jurist” er ikke “godkendt”.

## 11. Definition of Ready og Definition of Done

En opgave er **Ready**, når:
- den har én entydig produktadfærd og ejer;
- afhængigheder, datazone, API/event og fejlsituationer er beskrevet;
- relevante ADR'er og juridiske gates er identificeret;
- sikkerhedskritiske guards og negative tests er navngivet;
- acceptkriterier kan testes uden fortolkning.

En opgave er **Done**, når:
- kontrakt og dokumentation er opdateret sammen med kode;
- tests dækker positive, negative, race-/replay- og adgangsgrænser efter risiko;
- audit, retention, observability og runbook er dækket;
- ingen persondata eller hemmeligheder findes i fixtures/logs;
- menneskelig review af røde felter er dokumenteret;
- CI-gates er håndhævet, ikke blot beskrevet.

## 12. Åbne beslutninger

1. Juridisk rollefordeling i struktur C og om egen tilladelse bliver nødvendig.
2. Mandatets præcise retlige karakter, parter, fuldmagt, sameje og andelsboliger.
3. Buds juridiske status, accept, tilbagekaldelse, frister og aftaleindgåelse.
4. Hvilket advokatselskab eller hvilken anden kvalificeret juridisk leverandør kunden kan engagere til DIRECT-vejens juridiske/berigtigelsesarbejde.
5. Pris-/indtægtsmodel og enhedsøkonomi efter ny produktstruktur.
6. Dataansvarsroller, behandlingsgrundlag og lovlig datadeling mellem de tre selskaber og øvrige partnere, herunder Campaign.
7. Licenser til Datafordeler/EJF, DAGI, medier og feeds.
8. Den præcise afgrænsningsmetode, versionering og vedligeholdelse af Optata-definerede områder, bydele og kvarterer; geografisk navigation og skellet mellem officielle og Optata-definerede geografier er fastlagt i P-12.
9. Hosting, observability, branch protection og uafhængig reviewkapacitet.
10. Om gamle M3- og e-mail-/brevflows skal bevares som historik alene (anbefaling: ja).
11. RelocationCase v1: præcis husstands-/deltagerrelation, samtykkegranularitet og scenariomodellens grænser.

## 13. Ændringslog

- **v5.2:** Struktur C fastlagt som produktmål; SaleMandate, OfferLedger og Campaign indarbejdet; M3 som lead-/invitationkanal og gamle e-mail-/brevflows markeret som forældede; juridiske gates, faseplan og governance samlet.
- **v5.2-addendum (Proposed):** RelocationCase som koordinerende flytteforløb; salg og køb forbliver separate domænespor.
- **v5.2 Area Intelligence direction:** Area Intelligence fastlagt som selvstændigt produktområde sammen med Property Discovery; fælles geografisk rygrad, 30 facilitetskategorier som produktmål, kildebaseret AI-verifikation og statistisk opløsning dokumenteret. Detaljer og implementering er fortsat under afklaring.
- **v5.2 company-boundary update:** Optata, advokatselskabet og serviceselskabet fastlagt som tre selvstændige juridiske selskaber; konkrete regulatoriske/dataretlige forhold forbliver åbne gates.
- **v5.1:** Historisk baseline fra 16. november 2026. Se `docs/historik/` eller git-historikken.
