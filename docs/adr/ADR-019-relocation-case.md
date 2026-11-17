# ADR-019 — Koordineret flytning med RelocationCase

**Status:** Proposed · kræver produkt-, arkitektur- og juridisk review  
**Dato:** 17. november 2026  
**Beslutningsejer:** Stifter  
**Relaterer til:** Projektgrundlag v5.2 §4.5, Architecture v2.1, Contracts C-06/C-07, S3/S4/S5

## Kontekst

En husstand kan skulle sælge sin nuværende bolig og købe en ny i en anden by som én sammenhængende livsbeslutning. Hvis Optata kun modellerer salg og boligjagt hver for sig, mangler familien overblik over timing, afhængigheder og scenarier. Hvis Optata derimod samler begge handler i ét aggregate, bliver juridisk status, samtykke, fejlhåndtering og ejerskab uhensigtsmæssigt koblet.

Eksempel: Familie Nielsen undersøger, om de kan sælge i Holbæk og købe passende bolig i Aarhus inden for et ønsket tidsvindue og økonomisk råderum.

## Beslutning — foreslået

Indfør RelocationCase som et selvstændigt koordinerende domæneobjekt og workflow. Det samler familiens flyttemål og viser status på separate salg- og købsspor.

RelocationCase ejer:
- case-id, oprettende actor og autoriserede deltagere;
- fra-/til-geografi, ønsket flyttevindue, boligbehov og brugeroplyste økonomiske rammer;
- versionsbundne referencer til salgsspor og et eller flere købsspor;
- milepæle, afhængigheder, scenarieversioner, beslutninger og audit/correlation IDs;
- referencer til særskilte samtykker og godkendelser — ikke selve samtykkeregisteret.

RelocationCase ejer ikke:
- SaleMandate eller dets parter/vilkår;
- købsordre/købsinteresse eller VERIFIED-status;
- OfferLedger, bud, accept eller aftale;
- ejendoms-/listingdata, identitetsvault, attest eller finansieringsbeslutning.

## Domænegrænser og relationer

- mandates ejer salgssporet og mandatets state machine.
- orderbook ejer købsintention, husstandens ordre og matchberettigelse.
- offers ejer bud og budhistorik.
- listings ejer licenserede udbud og tilgængelighedsstatus fra kilden.
- identity, verification og consent ejer henholdsvis identitet, attest og samtykke.
- relocation koordinerer gennem typed aggregate references, events og eksplicitte read contracts. Ingen direkte cross-module writes.

Et case kan have ét salgsspor og flere købsspor/områdesøgninger. Det konkrete cardinality-design fastlægges i domænemodellen, men må ikke skabe ejerskab af de underliggende aggregates.

## Proces og scenarier

Minimumsforløb:
1. Familien opretter et flyttemål med fra-/til-geografi, tid, boligbehov og økonomiske rammer.
2. Salgssporet kan undersøge registerfakta og efterspørgsel. Oprettelse/aktivering af SaleMandate kræver særskilt flow og godkendelse fra alle nødvendige parter.
3. Købssporet kan undersøge listings og mulige matches. Et match er ikke bevis på, at boligen fortsat er tilgængelig, egnet eller økonomisk mulig.
4. Case viser scenarier, fx salg først, køb først eller finansieringsafklaring, med forudsætninger, usikkerhed og afhængigheder.
5. Familien vælger næste handling. Hver handling kræver sin egen autorisation, samtykke og audit.

Scenarier er beslutningsstøtte, ikke løfter eller rådgivning. Verificerede register-/kildeoplysninger, brugeroplyste data, estimater, mulige matches og uafklarede forhold skal være visuelt og maskinelt adskilt med provenance og tidsstempler.

## Samtykke og adgang

- Case-deltagelse giver ikke automatisk adgang til alle data for alle husstandsmedlemmer.
- Deling af oplysninger mellem salgsspor, købsspor og tredjepart kræver særskilt formål, modtager, datakategori, scope og varighed.
- En samtykke-tilbagekaldelse stopper fremtidig deling/levering efter consent-kontrakten; allerede lovligt videregivne kopier kan ikke nødvendigvis kaldes tilbage.
- Uopfordret ejerkontakt er fortsat forbudt. Flytteforløbet må ikke bruges som lead-/kontaktmekanisme.

## Workflow, fejlhåndtering og audit

RelocationCase følger saga-principperne i C-06. Hvert domæne udfører egne lokale transaktioner. Retry er idempotent; delvis succes er synlig; fejl kan kræve manuel afklaring. En handling i ét spor må ikke implicit gennemføre eller tilbagerulle en handling i det andet. Eksterne sideeffekter følger C-07 transactional outbox og audit-before-side-effect.

Mulige case-statusser (foreløbige): DRAFT, PLANNING, ACTIVE, PAUSED, COMPLETED, CANCELLED, EXPIRED. Statusser for salg og køb vises separat og er ikke afledt alene af case-status.

## Konsekvenser

**Fordele**
- Optata kan hjælpe familien med den reelle beslutning: om og hvordan flytningen kan gennemføres.
- Samlet tidslinje uden at sammenblande mandat, ordre og bud.
- Klart ejerskab, særskilte samtykker og kontrolleret deling.
- Understøtter delvise forløb og genoptagelse efter fejl eller ændrede planer.

**Omkostninger/risici**
- Nyt domæne, API/events, read models og UI.
- Komplekse husstands-/deltagerrettigheder og consent propagation.
- Scenariemodellen kræver datakvalitet, provenance og tydelig usikkerhedsformidling.
- Juridiske/finansielle afklaringer kan ikke automatiseres væk.

## Release gates og åbne spørgsmål

- S3/LG-2 for identitet, deltagere, persondata, retention og DPIA.
- S4/S5/LG-1/LG-5 for mandat, bud og udførerroller.
- LG-7 før betaling eller transaktionsrelaterede gebyrer.
- Afklar om RelocationCase har én primær household owner eller flere ligeværdige initiativtagere.
- Afklar præcis granularitet for deling af økonomiske rammer, dokumenter og bud mellem deltagere.
- Definér scenariometodik og hvad der kan vises som verificeret kontra estimat.

## Implementeringsregel

Denne ADR er Proposed og giver ikke tilladelse til produktionskode eller behandling af rigtige persondata. Før implementering skal ADR'en godkendes, Relocation-modulets kontrakter og event schemas specificeres, backlog afhængigheder opdateres, og negative adgangs-/samtykke-/race-/replay-tests defineres.
