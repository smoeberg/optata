# Optata — Role & Authority Model v1.0

**Status:** Proposed · kræver produkt-, sikkerheds-, arkitektur- og juridisk review  
**Dato:** 17. november 2026  
**Beslutningsejer:** Stifter  
**Autoritativt grundlag:** Projektgrundlag v5.2, Architecture v2.1, Architecture Contracts v1.0  
**Relaterer til:** ADR-020, ADR-019, C-01, C-02, C-03, C-05, C-06, C-07, LG-1, LG-2, LG-5, LG-6

## 1. Formål og normativ status

Dette dokument definerer den fælles rolle- og autoritetsmodel for Optata. Det skal forhindre, at hvert modul opfinder egne brugerroller eller giver adgang ud fra en global rolle som fx `buyer`, `broker` eller `admin`.

Modellen er et designgrundlag. Den er **ikke** en implementering, juridisk godkendelse eller tilladelse til at behandle rigtige persondata. Ingen produktionsadgang må tildeles alene med henvisning til dette dokument.

## 2. Grundregel: rolle er ikke adgang

Optata skal skelne mellem fem uafhængige begreber:

1. **Principal:** hvem eller hvad der foretager handlingen — en menneskelig identitet eller en teknisk serviceidentitet.
2. **Relation:** hvilken dokumenteret relation principalen har til et konkret objekt — fx køber på en ordre, medejer på et mandat eller deltager i en RelocationCase.
3. **Organisationsmedlemskab:** hvilken organisation personen arbejder for, og om medlemskabet er aktivt og verificeret.
4. **Authority grant:** en konkret, afgrænset bemyndigelse til at udføre bestemte handlinger på et bestemt objekt eller scope.
5. **Context:** formål, samtykke/retsgrundlag, scope, gyldighed, datakategori, zone, assurance-niveau og aktuel objektstatus.

En rolle beskriver en funktion. Den giver ikke i sig selv adgang til data eller ret til at handle.

**Adgangsbeslutning:** allow kræver en autentificeret principal, en relevant relation eller eksplicit authority grant, en tilladt capability, korrekt objekt-/organisationsscope, gyldig purpose og aktuelt retsgrundlag/samtykke, gyldighed og beståede domæneguards. Hvis et led mangler, er resultatet deny.

## 3. Identiteter og principals

| Principaltype | Eksempel | Regel |
|---|---|---|
| HUMAN | MitID-verificeret person | Individuel identitet; CPR må ikke bruges som intern nøgle |
| SERVICE | ingestion worker, disclosure service, notification worker | Egen teknisk identitet og egne minimale rettigheder; arver ikke automatisk menneskets rettigheder |
| ORGANIZATION | mæglerfirma, advokatfirma, finansiel partner | Organisationsidentitet; kan ikke logge ind eller handle som en person |
| SYSTEM_OPERATOR | drifts-/platformsoperatør | Teknisk driftsadgang; ingen implicit adgang til identitetsvault, dokumenter eller forretningsindhold |

En brugerhandling på vegne af en anden skal bevare begge identiteter: `actor` (den faktiske bruger) og `subject/on_behalf_of` (den person eller organisation, handlingen vedrører). Delegation skal kunne verificeres og auditeres. En service, der udfører en godkendt handling, registreres som service actor med oprindelig initiator og grant reference.

## 4. Relationer i domænet

Relationer er objekt- og tidsbundne. De må ikke implementeres som globale brugerflags.

| Relation | Objekt | Hvad relationen kan betyde | Hvad den ikke betyder |
|---|---|---|---|
| BUYER / CO_BUYER | Købsordre | Deltagelse i den konkrete købsordre efter individuel verifikation | Adgang til alle husstandens data eller andre ordrer |
| SELLER / CO_OWNER | SaleMandate / ejendom | Dokumenteret ejerskab eller anden relevant ret; individuel godkendelse | At én part kan godkende for alle øvrige parter |
| HOUSEHOLD_MEMBER | Husstand / RelocationCase | Deltagelse i det konkrete flytteforløb | Automatisk adgang til identitet, økonomi, bud eller dokumenter |
| CASE_INITIATOR | RelocationCase | Oprette og administrere planlægningsforløbet inden for egne rettigheder | Ret til at disponere over andre voksnes data eller aktiver |
| CASE_PARTICIPANT | RelocationCase | Se og udføre de handlinger, der er særskilt givet adgang til | Generel adgang til de tilknyttede salg-/købsspor |
| PROXY / REPRESENTATIVE | Konkret ordre, mandat eller sag | Handle inden for verificeret fuldmagt/delegation | Ubegrænset repræsentation eller adgang efter udløb/tilbagekaldelse |
| EXECUTOR | SaleMandate / opgave | Udføre den konkrete tildelte opgave via DIRECT eller AGENT_EXECUTED | Generel adgang til andre mandater eller kundedata |
| REVIEWER | Verification case | Vurdere tildelt dokumentation efter need-to-know | Adgang til alle identitetsdokumenter |
| PARTNER_ASSIGNEE | Konkret partneropgave | Udføre tildelt, tidsbegrænset opgave | Adgang til hele sagen eller organisationens øvrige sager |

Relationens status, kilde, verificeringsniveau, gyldighedsperiode og eventuelle begrænsninger skal registreres. En relation kan suspenderes eller tilbagekaldes uden at slette historikken.

## 5. Professionelle roller og organisationer

Professionel rolle og organisationsmedlemskab er separate fra den konkrete udpegning til en opgave.

| Professionel funktion | Mulige capabilities — kun efter konkret grant | Yderligere krav |
|---|---|---|
| BROKER | Læse mandatets tilladte oplysninger, opdatere tildelt salgsopgave, indsende tilladte hændelser | Aktiv organisationsmedlemskab, relevant licens/participation, aktivt mandat og scope |
| LAWYER | Læse og levere materiale til konkret juridisk opgave | Klient-/opgaveudpegning, fortrolighed og dataminimering |
| CLOSING_PARTNER | Udføre konkrete closing-/dokumentopgaver | Aktiv opgave, verificeret modtager og begrænset datagrundlag |
| FINANCING_PARTNER | Modtage særskilt godkendte finansieringsoplysninger | Separat formål, modtager, datakategori og tidsbegrænset samtykke/retsgrundlag |
| VALUATION_PARTNER | Modtage nødvendige ejendoms-/vurderingsdata | Konkret opgave, kilde-/licensvilkår og begrænset scope |
| DATA_PROVIDER | Levere data gennem godkendt adapter/kontrakt | Kildeidentitet, licens, schema, provenance og ingest-scope |

Organisationsmedlemskab giver aldrig automatisk adgang til organisationens sager. Organisationens godkendte scope, personens aktive medlemskab, konkret opgave/grant og gældende licens skal alle være opfyldt. Fjernelse af en medarbejder skal straks fjerne dennes fremtidige adgang uden at slette auditsporet.

## 6. Tekniske service- og driftsroller

Tekniske serviceidentiteter er ikke menneskelige roller.

| Serviceprincipal | Tilladt ansvarsområde | Forbud |
|---|---|---|
| DISCLOSURE_SERVICE | Kontrolleret, auditeret udlevering af identitetsoplysninger efter gyldig autorisation | Forretningsbeslutninger eller generel søgning i vault |
| IDENTITY_SERVICE | Identitetsassertion, pseudonym og sessionsbinding | Direkte mandat-/budbeslutninger |
| VERIFICATION_SERVICE | Modtage og route verifikationsresultater | At selv godkende ud over defineret policy |
| INGESTION_SERVICE | Skrive til tildelte kilde-/ingestion-tabeller | Læse Zone B eller ændre bruger-/mandatdata |
| PROJECTION_WORKER | Bygge afledte read models fra autoriserede events | At være autoritativ kilde eller omgå modulgrænser |
| NOTIFICATION_SERVICE | Levere godkendte meddelelser efter genkontrol af samtykke og suppression | At opfinde modtagere eller kontakte ejere uopfordret |
| BILLING_SERVICE | Håndtere platformproduktets betalingsstatus | Escrow, købesum eller frigivelse af handelsmidler |
| PLATFORM_OPERATOR | Drift, deployment, metrics og incident response | Standardadgang til identitetsvault, private dokumenter eller forretningsindhold |

Servicekonti skal have separate database-/runtime-identiteter, eksplicitte grants, secrets rotation, audit og dokumenteret ejer. Ingen generisk `admin`-service med fuld læse-/skriveret.

## 7. Capability-model

Autorisering skal baseres på capabilities, ikke kun CRUD eller en global rolle. Følgende capability-navne er foreslåede og skal versionsstyres:

- `resource.discover` — opdage at et objekt findes, uden nødvendigvis at se indhold.
- `resource.read` — læse tilladte felter.
- `resource.create` — oprette et objekt.
- `resource.update` — ændre tilladte felter via domænekommando.
- `resource.submit` — indsende en bindende eller workflow-udløsende handling.
- `resource.approve` — godkende en specifik handling eller version.
- `resource.revoke` — tilbagekalde eget samtykke/grant eller anmode om tilbagekaldelse efter policy.
- `resource.delegate` — udstede en begrænset delegation, hvis principalen har denne ret.
- `resource.disclose` — videregive bestemte data til navngiven modtager.
- `resource.export` — eksportere et godkendt datasæt.
- `resource.administer` — administrere teknisk konfiguration; aldrig synonymt med læseadgang til data.

Capabilities er kun tilladelser til at forsøge en handling. Domæneguards skal fortsat kontrollere state, version, frister, attest, licens, samtykke og lovlige forudsætninger.

## 8. Foreløbig rettighedsmatrix

Matrixen viser den maksimale designmæssige retning, ikke en aktuel produktionsadgang. `Own` betyder egne data/egne handlinger; `Scoped` betyder kun konkret grant + scope; `—` betyder ingen standardret.

| Aktør/relation | Egen profil/session | Købsordre | SaleMandate | Bud/OfferLedger | RelocationCase | Identitetsvault |
|---|---|---|---|---|---|---|
| Køber | Own | Own/Scoped | — | Own/Scoped | Own/Scoped | Via disclosure |
| Medkøber | Own | Scoped, individuel relation | — | Scoped efter mandat/ordre | Scoped | Via disclosure |
| Sælger/medejer | Own | — | Own, individuel partsret | Scoped som mandatpart | Scoped hvis deltager | Via disclosure |
| Fuldmægtig | Own | Scoped grant | Scoped grant | Scoped grant | Scoped grant | Kun hvis grant udtrykkeligt omfatter det |
| Mægler/udfører | Own | — | Scoped aktivt mandat | Scoped mandat og opgave | — som standard | Ingen direkte adgang |
| Advokat/closingpartner | Own | — | Scoped konkret opgave | Scoped konkret opgave | — som standard | Kun dataminimeret disclosure |
| Finansieringspartner | Own | — | — | — | Kun særskilt finansieringsscope | Ingen direkte adgang |
| Platform support/admin | Teknisk supportmetadata | — | — | — | — | Ingen |
| Disclosure service | — | — | — | — | — | Kun godkendt, konkret disclosure |
| Ingestion service | — | — | — | — | — | — |

Ingen celle i matrixen giver automatisk ret til at godkende en anden persons handling. Særlige rettigheder skal udtrykkes som grants og kontrolleres per command.

## 9. RelocationCase: konkret adgangsregel

RelocationCase binder et flyttemål sammen, men udvider ikke rettigheder på tværs af spor.

Eksempel: To voksne deltager i samme flytteforløb. Den ene har oprettet casen. Begge kan se fælles planlægningsoplysninger, hvis de hver især er tilføjet og har accepteret deltagelsen. Den ene kan ikke på den andens vegne:
- dele identitetsdokumenter eller finansielle oplysninger;
- oprette eller godkende en købsordre for den anden;
- underskrive eller aktivere et SaleMandate;
- indsende, ændre eller acceptere et bud;
- give en mægler, bank eller advokat adgang til den andens data.

En broker i Holbæk får kun adgang til den aktive salgsopgave og de felter, der er nødvendige for den. En partner i Aarhus får kun adgang til en særskilt godkendt købssøgnings-/opgavepakke. At begge opgaver refereres fra samme RelocationCase giver ikke adgang til hinandens data.

## 10. Delegation, fuldmagt og tilbagekaldelse

Enhver delegation skal mindst indeholde:
- grant-id og version;
- principal, grantor og eventuel repræsenteret subject;
- præcis capability-liste;
- resource/aggregate og scope;
- purpose og tilladte datakategorier;
- gyldighed fra/til og eventuelle anvendelsesgrænser;
- dokumentation/verifikationsstatus for fuldmagt eller andet mandat;
- mulighed for øjeblikkelig suspension/tilbagekaldelse;
- audit af oprettelse, brug, ændring og tilbagekaldelse.

Delegation kan aldrig give flere rettigheder end grantor selv har. Den kan ikke udvide scope, forlænge gyldighed eller overleve tilbagekaldelse af den underliggende autoritet. En almindelig case-deltager kan ikke udstede juridisk fuldmagt ved at invitere en anden person til casen.

## 11. Samtykke og retsgrundlag er ikke roller

Samtykke er ikke en rolle, capability eller generel adgangsbillet. Hver adgangsbeslutning skal skelne mellem:
- formål og behandlingsgrundlag;
- samtykkestatus, når samtykke er det relevante grundlag;
- modtager og modtagerorganisation;
- datakategori;
- konkret scope/objekt/spor;
- gyldighed og tilbagekaldelsesstatus.

Samtykke kan ikke skabe en ret, som personen ikke har, og kan ikke erstatte dokumenteret ejerskab, fuldmagt, professionel licens eller lovligt behandlingsgrundlag. Tilbagekaldelse skal propagere til fremtidige leveringer, køer, caches og partneradgange efter C-09. Allerede lovligt videregivne kopier kan ikke nødvendigvis tilbagekaldes.

## 12. Autorisationsbeslutning og audit

Hver følsom command skal evalueres mod en samlet, eksplicit kontekst:

`principal + actor + subject + relation/grant + capability + resource + scope + purpose + legal_basis/consent + validity + assurance + domain_state`

Beslutningen skal være fail-closed. Manglende, tvetydig, udløbet eller modstridende information giver deny eller manuel review — aldrig implicit allow.

Audit skal som minimum registrere actor, service principal hvis relevant, subject/on-behalf-of, action/capability, resource, scope, purpose, grant/consent reference, beslutningsresultat, policy version, tidspunkt, correlation/trace ID og reason code. Følsomme dokumenter og hemmeligheder må ikke kopieres ind i auditpayloads.

## 13. Obligatoriske negative sikkerhedstests

Før hver relevant modul-release skal der være tests, der beviser at:

1. En bruger ikke kan skifte identity context ved at ændre en sessionvariabel eller database-GUC.
2. Et organisationsmedlem ikke kan læse en anden organisations eller kollegas sager uden grant.
3. Et aktivt broker-medlemskab uden konkret mandat/opgave giver deny.
4. Et mandat uden gyldig executor/participation license giver deny.
5. En case-deltager ikke automatisk kan læse alle linkede ordre-, mandat-, bud- eller dokumentdata.
6. Én voksen ikke kan give samtykke eller godkende på vegne af en anden voksen uden verificeret authority.
7. En udløbet eller tilbagekaldt delegation ikke kan bruges — heller ikke via kø, cache eller replay.
8. En service principal ikke kan optræde som human principal eller arve brugerens rettigheder.
9. Support/admin ikke kan læse identitetsvault eller private dokumenter gennem API, DB, logs eller debugværktøjer.
10. Disclosure kun returnerer godkendte felter til den konkrete modtager og purpose.
11. Et samtykke til én datakategori, modtager eller spor ikke kan genbruges til et andet.
12. Manglende purpose, scope, actor, audit eller idempotency metadata giver deny.
13. Race conditions mellem revocation og sideeffekt ikke kan give efterfølgende uautoriseret levering.
14. Ingen rolle eller grant kan omgå Zone A/Zone B/Zone C-grænser eller modulernes dataejerskab.

## 14. Implementeringsrækkefølge

1. Godkend rollekatalog, relationstyper, capability vocabulary og permission matrix.
2. Afklar juridisk rolle-/ansvarsfordeling under LG-1, LG-2, LG-5 og LG-6.
3. Definér identity assertion og trusted context efter C-03; løs A-05 før Zone B.
4. Definér datamodel for organisation, medlemskab, relation, authority grant og revocation.
5. Definér policy evaluation contract og audit event schema.
6. Implementér negative tests og DB/RLS-grænser før UI-roller.
7. Integrér først derefter S3 (buyer/household/identity), S4 (seller/mandate), S5 (offers) og S6 (broker/partner/campaign).
8. Integrér RelocationCase som koordinator uden at sammenlægge underliggende rettigheder.

## 15. Åbne beslutninger før Accepted

- Hvilke professionelle funktioner kræver lovbestemt autorisation, og hvilke kan alene være platformspartnere?
- Hvilke former for fuldmagt kan verificeres digitalt, af hvem og med hvilken assurance?
- Hvilken person-/husstandsmodel kan anvendes uden at udlede relationer fra adresse eller fælles økonomi?
- Hvordan håndteres mindreårige, værger, dødsboer, selskaber og andre juridiske personer?
- Hvilke actions kræver step-up authentication eller særskilt MitID-confirmation?
- Hvilke grants kan udstedes af en person, en organisation eller kun Optatas policy engine?
- Hvilke datafelter må hver professionel rolle modtage under hvert lovligt formål?

## 16. Beslutningsregel

Dette dokument forbliver **Proposed**, indtil stifter, arkitektur-/sikkerhedsreviewer og relevant juridisk rådgiver har gennemgået rollefordeling, fuldmagt, partneradgang, persondata og release gates. Efter godkendelse skal ADR-020 markeres Accepted, og v5.2, Architecture, Contracts, backlog og tests opdateres samlet.

Der må ikke implementeres en generisk `admin`, `broker` eller `household`-rolle med bred dataadgang som genvej uden om denne model.
