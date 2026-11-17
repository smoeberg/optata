# Jurist-spørgsmål — uge 6

---

# DEL A — `docs/compliance/legal-questions-week6.md`

**Formål:** Skriftlige svar der kan lægges til grund for kode, kontrakter og due diligence.
**Format pr. spørgsmål:** Svar + hjemmel + dato + juristens initialer. *"Det afhænger af…"* accepteres ikke som svar — det skal udmøntes i en handlingsregel.
**Frist:** Uge 6. Spørgsmål markeret 🔴 blokerer deploy af den tilhørende feature.

---

## A1 · Formidling og rolle (🔴 blokerer S5)

| # | Spørgsmål | Hvorfor det afgør | Hvis svaret er… |
|---|---|---|---|
| **L1** 🔴 | Er Optatas samlede aktivitet — match af verificeret køber med ejer, anonym relay-dialog om pris og betalt identitetsudveksling — **formidling** efter ejendomsmæglerloven? Vurder aktiviteten samlet, ikke pr. komponent. | Afgør om vi overhovedet må drive produktet uden godkendelse | **Ja:** Model A (advokat/godkendt mægler som formel formidler) eller B (eget mæglerselskab). **Nej:** dokumentér begrundelsen, den skal kunne vises en bank |
| **L2** 🔴 | Fritager **fast gebyr** (10.000 kr., uafhængigt af handelens gennemførelse og pris) os for formidlingsklassifikation? Eller er vederlagets form irrelevant, når aktiviteten er formidling? | Vi har antaget at fast gebyr er et værn. Antagelsen skal bekræftes eller forkastes | **Forkastet:** hele pakkestrukturen redesignes før S5 |
| **L3** 🔴 | Hvor går grænsen mellem **annoncering/dataformidling** og formidling, når vi hoster prisdialogen? Er relay mere end et teknisk rør? | Relay er den komponent, der flytter os tættest på formidling | **Mere end rør:** partner skal eje dialogen, eller vi skal fjerne prisforhandling fra relay |
| **L4** | Må vi kalde mægleren "partner" i markedsføring, når vi reelt overtager origination? Hvilke formuleringer er vildledende? | Markedsføringslov + interessekonflikt | Angiv tilladte og forbudte formuleringer |
| **L5** | Kræver vores rolle **ansvarsforsikring** ud over almindelig erhvervsansvar? Hvilken dækning og sum? | Fejl i dokumentflow kan give store krav | Angiv krav til police før første pakke sælges |

---

## A2 · Kontakt til ejere (🔴 blokerer S4)

| # | Spørgsmål | Hvorfor det afgør | Hvis svaret er… |
|---|---|---|---|
| **L6** 🔴 | Hvilket **behandlingsgrundlag og markedsføringsgrundlag** kan vi bruge til første henvendelse til en ejer, når EJF er offentligt, men offentlighed ikke er samtykke? Angiv præcist grundlag pr. kanal (e-mail, brev, Digital Post). | Det er hele ejersidens forretningsmodel | **Intet grundlag for e-mail:** kun brev/Digital Post, eller kun inbound (ejeren slår selv op) |
| **L7** 🔴 | Er vores skabelon (saglig, afgrænset, ingen køberdata, afmeld synlig, "derfor får du denne mail") tilstrækkelig? Hvad skal ændres ordret? | Skabelonen er allerede skrevet — den skal godkendes eller rettes | Lever rettet tekst med versionering |
| **L8** | Er **aggregering** (3 interesser → 1 mail) og **frekvensloft** (1 pr. 14 dage) tilstrækkeligt til at undgå "uønsket henvendelse"? Er der en absolut grænse? | Afgør notifikationsmotorens parametre | Angiv loft og evt. absolut grænse |
| **L9** | Gælder afmelding på **adressen** eller på **personen**? Hvis ejer skifter, må vi så kontakte den nye ejer? | Afgør suppression-nøgle i databasen | Angiv nøgle og regel ved ejerskifte |
| **L10** | Må vi kontakte ejere af **andelsboliger** via foreningen/administrator, og hvem er dataansvarlig i den kæde? | Andelsboliger er en stor del af pilotområdet | Angiv rollefordeling og grundlag |

---

## A3 · Persondata, retention og historik (🔴 blokerer S3/S7)

| # | Spørgsmål | Hvorfor det afgør | Hvis svaret er… |
|---|---|---|---|
| **L11** 🔴 | Er vores **to-lags sletning** lovlig? Zone B (identitet, bevis, tråde) slettes hårdt; pseudonym event-historik bevares 5 år. Er pseudonymet reelt anonymiseret, når vi ikke kan mappe det tilbage? | Det er konflikten mellem "fuld historik" (moat) og sletteret | **Ikke anonymiseret:** historikken skal også slettes eller aggregeres — moaten svækkes, men skal redesignes nu |
| **L12** 🔴 | Bekræft **retentionsfrister**: bankbevis 90 dage efter review · attest-felter til udløb + 12 mdr. · identitet aktiv + 12 mdr. · tråde 6 mdr. efter lukning · ejerrespons 12 mdr. · audit/reveal 5 år · bogføring 5 år fra regnskabsårets udløb. | Fristerne hardcodes i jobs | Ret tabellen med hjemmel pr. række |
| **L13** | Er **ejerrespons** (svar på "der er interesse på din adresse") et selvstændigt formål med eget grundlag og egen frist? | Vi har antaget ja — skal bekræftes | Angiv grundlag + frist |
| **L14** 🔴 | Er **CPR-minimering** korrekt implementeret: kun broker-pseudonym gemmes, CPR/navn passes transient ved match, logges aldrig? Er transient behandling i hukommelsen acceptabel? | Hele identitetsmodellen hviler på det | **Ikke acceptabel:** match skal ske hos broker eller helt undgås |
| **L15** | Er **DPIA påkrævet** for denne behandling (systematisk, ny teknologi, sårbare data om boligøkonomi)? | Afgør om vi skal lave den før lancering | Ja → DPIA skal foreligge før S3 i prod |
| **L16** | Hvilke **undtagelser** skal stå i privatlivspolitikken (bogføring, audit, retlige krav)? Formulér dem. | Vi må ikke love sletning vi ikke kan holde | Lever ordlyd |

---

## A4 · Anonymitet og B2B-data (🔴 blokerer S6/S8)

| # | Spørgsmål | Hvorfor det afgør | Hvis svaret er… |
|---|---|---|---|
| **L17** 🔴 | Er **k≥5 + afrunding til 5 + komplementær suppression + max 3 dimensioner + postnummer som mindste geo + kvartalsvindue** tilstrækkeligt til at zone C er anonymiseret og kan sælges uden samtykke? | Det er hele Demand Pro-produktet | **Utilstrækkeligt:** hæv k, grovere dimensioner, eller samtykke kræves |
| **L18** | Er **budgetintervaller** (ikke præcise beløb) tilstrækkeligt til at forhindre re-identifikation i små områder? | Lille postnummer + få ordrer = risiko | Angiv mindste intervalbredde |
| **L19** | Må en **mægler** få adgang til anonyme, verificerede købere i et eksklusivt postnummer uden køberens særskilte samtykke pr. mægler? | Afgør om lead-adgang kræver ekstra samtykke | **Ja kræves:** tilføj samtykketrin i ordre-flowet |
| **L20** | Er vores **kontraktforbud mod re-identifikation** hos B2B-kunden håndhæveligt, og hvad skal sanktionen være? | Beskytter moaten og anonymiteten | Lever klausul |

---

## A5 · Betaling, hvidvask og forbrugerret (🔴 blokerer S4/S5)

| # | Spørgsmål | Hvorfor det afgør | Hvis svaret er… |
|---|---|---|---|
| **L21** 🔴 | Bekræft at Optata **aldrig** må holde købesum i forvaring, og at kun pakkegebyret (10.000 kr.) må passere os. Hvor går grænsen til betalingstjenestelov og hvidvasklov? | Escrow ville udløse licenskrav | Angiv præcis grænse og forbudte flows |
| **L22** 🔴 | Hvem har **hvidvaskpligten** i vores model — advokatpartneren, mægleren eller os? Skal vi have KYC på køber ud over MitID + bankattest? | Afgør om vi skal bygge KYC | **Os:** KYC-flow skal i S3/S5, planen ændres |
| **L23** 🔴 | Er vores **fortrydelses-waiver** korrekt: "14 dages fortrydelsesret. Adgangen åbnes med det samme, hvis du accepterer" + checkbox med versioneret tekst? Gælder det både ejerside (1.495) og pakke (10.000)? | Hver eneste ejerside-salg er ellers en klagesag | Lever korrekt ordlyd + krav til dokumentation |
| **L24** | Ved fortrydelse efter delvis levering: hvordan beregnes **forholdsmæssig betaling** for pakken? | Skal implementeres i refusionslogik | Angiv beregningsmetode |
| **L25** | Er **eksklusivitet pr. postnummer** med 6 mdr. binding og automatisk fornyelse lovlig over for mindre mæglervirksomheder? Krav til varsling? | Afgør abonnementsvilkår | Angiv varslingsfrist og opsigelsesregler |

---

## A6 · Datakilder, medier og tredjeland (🔴 blokerer S1/S2)

| # | Spørgsmål | Hvorfor det afgør | Hvis svaret er… |
|---|---|---|---|
| **L26** 🔴 | Hvilke **Datafordeler-datasæt** må vi bruge kommercielt, herunder **EJF** (ejerfortegnelse)? Kræver EJF berettigelse, og har vi den? | EJF-adgang afgør ejerskabsverifikationens metode | **Afvist:** Tingbogen + manuel kø bliver primær (allerede designet) |
| **L27** 🔴 | Bekræft at **systematisk udtræk fra DinGeo, Boligsiden, OIS-front-ends eller mæglersystemer** er ulovligt uden aftale (databasebeskyttelse), og at kilde-adgang er lovlig. | Vi har bygget hele arkitekturen på kilde-adgang | Bekræft eller angiv begrænsninger |
| **L28** 🔴 | Hvad må vi **lagre og vise** fra licenserede medier: kort uddrag ≤200 tegn + metadata + link? Kræver videresalg i en betalt analyse særskilt licens? | Agentens claim-pipeline og PDF-leverancen | Angiv tegn-grænse og licenskrav |
| **L29** 🔴 | Er **Ukraine-udvikling på syntetiske data** tilstrækkeligt til at undgå tredjelandsoverførsel af persondata? Kræves SCC + TIA alligevel (adgang til systemer, support, logs)? | Det er bankens due-diligence-spørgsmål | Angiv krav til SCC/TIA og adgangskontrol |
| **L30** | Er **EU-LLM-endpoint** tilstrækkeligt, når input er zone A-dokumenter? Skal vi have databehandleraftale med LLM-udbyderen, og må de træne på input? | Agenten og redaction-supplement | Angiv krav: ingen træning, DPA, EU-region |
| **L31** | Krav til **IP-overdragelse** fra UA-teamet (FOP/agentur): hvad skal stå i kontrakten for at selskabet ejer al kode og kan sælges? | Uden det er selskabet ikke salgbart | Lever klausul |

---

## A7 · Svarskabelon

```markdown
### L__ — [kort titel]
Svar:            [ ] Ja  [ ] Nej  [ ] Ja, med følgende ændringer:
Handlingsregel:  _________________________________________________
Hjemmel:         _________________________________________________
Konsekvens for kode/kontrakt: ____________________________________
Blokerer deploy: [ ] Ja  [ ] Nej
Dato / initialer: ____________________
```

**Leverance fra juristen:** udfyldt skabelon for L1–L31 + rettede skabelontekster (L7, L16, L23) + klausuler (L20, L25, L31) + eventuel DPIA-vurdering (L15).

---

---

# Tilføjelse — udbudsmatch (M3): L32–L37

## Spørgsmål (samme format som L1–L31)

| # | Spørgsmål | Blokerer |
|---|---|---|
| **L32** 🔴 | Må vi importere, indeksere, matche og vise udbud fra **mæglerens eget feed** med den vedlagte licens (bilag A2)? Er parterne korrekt selvstændigt dataansvarlige? Kræves databehandleraftale nogen steder i kæden? | S6-01/04 |
| **L33** 🔴 | Er en **Boligsiden-licens** nødvendig, når vi kun bruger mæglerens egne udbud? Hvad er vores rettigheder ved **aggregeret videresalg** i analyser (k≥5)? Skal attribution suppleres? | S6 + Demand Pro |
| **L34** 🔴 | Er **køber→mægler-invitation + anonym relay-dialog** formidling efter ejendomsmæglerloven, når mægleren allerede er godkendt formidler for boligen? Vi tager **intet gebyr** i dette flow og tilbyder **ingen** fulfillment-pakke. | S6-10/11 |
| **L35** 🔴 | Må vi sende en **konkret køberhenvendelse** til en uregistreret mægler på deres offentlige forretnings-e-mail? Hvilket grundlag, og hvilke krav til indhold, afmelding og frekvens (vores forslag: 1 pr. bolig pr. 14 dage, aggregeret)? | S6-08/10 |
| **L36** | Kræver visning af **pris, status og udbudsdata** attribution eller andre vilkår? Er "Kilde: [Mægler] · Se annonce ↗" tilstrækkeligt? Må vi vise prisændringshistorik? | S6-09 |
| **L37** | Må udbudsdata indgå i **Demand Pro/gap-analyse** som aggregeret statistik, eller kræver licensen særskilt vederlag? Hvad ved ophør af feed-aftale? | S9 |

**Svarskabelon:** udfyld `Svar / Handlingsregel / Hjemmel / Konsekvens for kode / Blokerer deploy / Dato+initialer` som i `legal-questions-week6.md`.

Se også `docs/compliance/pilot-feed-aftale.md` (licensvilkårene, bilag A2) og `docs/design/Optata - Udbudsmatch M3 v1.md`.

---

# Tilføjelse — struktur C (mandat + budbog): L38–L42

| # | Spørgsmål | Afgør |
|---|---|---|
| **L38** 🔴 | Kan Optata **eje sælgers mandat** og drive budbog, mens en licenseret partner er formel formidler? Hvor går grænsen for, hvad vi selv må gøre? | Hele struktur C |
| **L39** 🔴 | Er en **struktureret budplatform** med accept/modbud formidling i sig selv — eller markedsinfrastruktur? | OfferLedger-design |
| **L40** 🔴 | Må vi markedsføre **"sælg uden mægler"** når partneren er formel formidler? Hvilken ordlyd er vildledende? | Hele positioneringen |
| **L41** | Krav til **mandatvilkår**: eksklusivitet, løbetid, tilbagekaldelse, sameje, andel | SaleMandate |
| **L42** | Mæglerens **deltagelsesvilkår**: scoped adgang, ingen eksport, tavshedspligt, sanktion | participation_license |

**L38–L40 skal besvares før fase 3 bygges.** Fase 1 (register/analyse) og fase 2 (verificeret ordrebog) kan bygges nu.

Se `docs/design/Optata - Efterspoergselsgravitation - struktur C v1.md`.

---

# Tilføjelse — målrettet rækkevidde (kampagner): L43–L48

| # | Spørgsmål | Afgør |
|---|---|---|
| **L43** 🔴 | Hvilket **samtykke** kræves for at vise købere markedsføring fra tredjepart (mægler)? Er Optata afsender på mæglerens vegne, eller formidler af indhold? Hvem er dataansvarlig? | Hele produktet |
| **L44** 🔴 | Er målretning mod **købsintention + budget** profilering der udløser særlige krav? Er audience ≥25 + k≥5 tilstrækkeligt til at undgå individuel målretning? | Targeting-model |
| **L45** | Er kampagne→forespørgsel→bud **formidling**, eller markedsføring af et udbud? Vi tager intet honorar pr. handel | Positionering |
| **L46** | Krav til **indhold og attribution**: pris, "solgt"-status, åbent hus, vildledende udsagn | Indholdsregler |
| **L47** | **P2B / platform-forordningen**: krav til gennemsigtighed i rangering, omdømmescoring og kvotetildeling over for erhvervskunder | Omdømmemodel |
| **L48** | Retention af **kampagne-interaktion** (åbnet, feedback, mute) — formål og frist | Datamodel |

**L43 og L44 skal besvares før kampagne-modulet bygges.** Resten kan afklares parallelt.

Se `docs/design/Optata - Maalrettet raekkevidde - Campaign v1.md`.
