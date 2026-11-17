# Optata — Architecture Contracts v1.0

**Status:** Proposed for technical review · Ikke godkendt eller implementeret
**Dato:** 17. november 2026
**Gælder for:** Arkitektur v2.1, Projektgrundlag v5.2 og S0/S1-hardening
**Ejer:** Stifter + teknisk reviewer

> **Vigtigt:** Dette dokument er en designkontrakt. Det lukker ikke auditfund, godkender ikke SQL-migrationer og udgør ikke en penetrationstest, juridisk vurdering eller produktionsgodkendelse. En kontrakt tæller først som implementeret, når kode, databasekontroller, negative tests og krævet menneskeligt review foreligger.

## 1. Normativ status og anvendelse

Dokumentet konkretiserer arkitekturens invarianter og auditfund A-01–A-12. Det supplerer, men erstatter ikke, Projektgrundlag v5.2, arkitektur v2.1, ADR'er eller juridiske release gates.

Kravord:
- **MUST / SKAL:** ufravigeligt krav.
- **MUST NOT / MÅ IKKE:** forbud.
- **SHOULD / BØR:** standardvalg; afvigelse kræver begrundelse og review.
- **MAY / KAN:** tilladt mulighed.

Ved konflikt gælder Projektgrundlag v5.2 for produkt- og juridiske beslutninger. En teknisk kontrakt må aldrig fortolkes som juridisk tilladelse.

### 1.1 Overordnet sikkerhedsregel

Zone B, rigtige persondata og transaktionsflows forbliver gated, indtil relevante S0/S1-kontroller er implementeret og reviewet. Syntetiske data og testmiljøer er fortsat tilladt inden for eksisterende guards.

### 1.2 Kontraktstatus

| Kontrakt | Hovedområde | Auditkobling | Status ved oprettelse |
|---|---|---|---|
| C-01 | Least privilege og zoneadgang | A-01, A-05 | Designkrav; implementering mangler |
| C-02 | Event-authoritative tilstand og atomiske writes | A-02, A-08, A-09 | Designkrav; implementering mangler |
| C-03 | Identitet, session og RLS-trusselsmodel | A-05 | Designkrav; review mangler |
| C-04 | Scope og adresseintegritet | A-03, A-07 | Designkrav; datamodelændring mangler |
| C-05 | Migration governance | A-06 | Proceskrav; menneskelig review mangler |
| C-06 | Workflow/saga og eksterne sideeffekter | A-08, A-09 | Designkrav |
| C-07 | Audit og transactional outbox | A-02, A-09 | Designkrav |
| C-08 | Zone C kontrolleret publicering | A-12 | Designkrav; pipeline mangler |
| C-09 | Samtykke og tilbagekaldelse | A-08 | Designkrav; propagation mangler |
| C-10 | Event, projection, replay og ingestion | A-02, A-08, A-09, A-10 | Designkrav; write path mangler |

A-04, A-11 og øvrige auditobservationer håndteres fortsat i audit/backlog. Dokumentet må ikke bruges til at markere dem som lukkede.

## 2. C-01 — Least privilege og zoneadgang

### Invariant
En databaseprincipal må kun læse de tabeller, kolonner og rækker, som dens eksplicitte formål kræver. API-filtrering er ikke en sikkerhedsgrænse.

### Krav
1. public_reader MUST NOT have generel SELECT på basistabeller med ejer-, identitets-, ordre-, attest-, samtykke- eller vaultdata.
2. app_role MUST NOT have bredere rettigheder end konkrete applikations-use cases kræver.
3. Public read models MUST være eksplicitte views/tabeller med allowlist af felter. Følsomme felter må ikke være tilgængelige via SELECT *.
4. Nye tabeller og kolonner MUST være lukket som standard. Default privileges må ikke utilsigtet åbne fremtidige objekter.
5. View-ejerskab, security_barrier, security_invoker/view-owner semantics og RLS-bypass MUST gennemgås bevidst. Et view er ikke automatisk sikkert, blot fordi det skjuler kolonner.
6. Direkte cross-module tabeladgang er forbudt, medmindre en dokumenteret read model har navngiven ejer og tests.

### Accepttests
- public_reader kan læse den godkendte public read model.
- Direkte SELECT af owner_cvr, vaultfelter og Zone B-tabeller fejler for public_reader.
- app_role kan ikke læse følsomme kolonner alene ved at kende tabelnavnet.
- Nye testtabeller får ikke utilsigtet adgang.
- Tests kontrollerer has_table_privilege, has_column_privilege og faktiske SELECT-forsøg under relevante roller.

**Audit:** A-01 kan først lukkes, når databaseprivilegier og negative tests er ændret og kørt mod en rigtig testdatabase.

## 3. C-02 — Event-authoritative tilstand og kontrollerede commands

### Invariant
Forretningsstatus for ordre, mandat, bud, listing og campaign er en projektion af append-only hændelseshistorik. En statuskolonne er aldrig en selvstændig autoritet.

### Krav
1. Domænet definerer en eksplicit state machine med tilladte tilstande, kommandoer og overgange.
2. Alle state-changing commands MUST autorisere actor, purpose, scope, aggregate, aktuel version og idempotency key.
3. Direkte UPDATE af statuskolonner fra almindelig app_role MUST være forbudt.
4. Event append og opdatering af en eventuel current-state projection MUST ske atomisk i samme lokale databasetransaktion.
5. En command MUST afvises, hvis forventet aggregate-version ikke matcher den aktuelle version (optimistic concurrency).
6. Ugyldige overgange, manglende actor/purpose/scope, genbrugte idempotency keys med andet payload og events med forkert aggregate-version MUST afvises.
7. Projektioner kan genopbygges fra den autoritative eventhistorik.

Den præcise ordre-state machine skal godkendes i domænespecifik kontrakt før implementering. QUALIFIED og VERIFIED er produktniveauer, ikke i sig selv en fuldstændig ordre-livscyklus.

### Accepttests
- Direkte statusændring uden event afvises af databasen.
- Ugyldig overgang afvises, også ved direkte adgang til command-laget.
- To samtidige commands med samme forventede version kan ikke begge vinde.
- Retry med samme idempotency key og samme request giver samme resultat uden dobbelt event.
- Retry med samme key og ændret request afvises.
- Projection rebuild giver samme aktuelle tilstand som den løbende projection.

**Audit:** A-02 lukkes ikke ved alene at tilføje event-tabeller; den direkte status-write path skal være lukket.

## 4. C-03 — Identitet, session og RLS-trusselsmodel

### Invariant
RLS er adgangskontrol på databaseniveau, men en værdi i en applikationsstyret sessionvariabel er ikke i sig selv bevis for brugerens identitet.

### Trusselsmodel
Modellen MUST behandle:
- Kompromitteret applikationsproces eller SQL-injection, der kører som app_role.
- En brugerdefineret GUC (app.identity_id) sat af samme databaseprincipal.
- Genbrug af pooled forbindelser, hvor session state kan lække mellem requests.
- Forveksling af service identity, human identity og acting-on-behalf-of.
- Stjålne, udløbne, replayede eller forkert audience-bundne tokens.
- Privilegerede roller, table owner, superuser og BYPASSRLS.
- Fejl i rollback/reset, transaction pooling og exception paths.

### Krav
1. current_setting('app.identity_id') MUST NOT alene betragtes som en autentificeret identitetsgrænse.
2. Identitetskontekst MUST stamme fra en betroet komponent, som har valideret identitetsbevisets audience, issuer, signatur, udløb, nonce/state og relevante assurance-krav.
3. En almindelig app_role MUST NOT kunne etablere eller ændre en vilkårlig brugers autoritative identitet.
4. En SECURITY DEFINER-funktion er ikke automatisk en løsning. Den er kun acceptabel, hvis kaldsadgang, ejer, search_path, inputvalidering og tillidskæden gør det umuligt for en lavere betroet principal at forfalske konteksten.
5. DB-identitetskontekst MUST være transaktionsbundet og ryddes/resettes ved alle afslutninger, også fejl og cancellation.
6. Connection pooling MUST testes for cross-request identity leakage. Pooling må først aktiveres, når reset- og isolationsegenskaberne er bevist.
7. Service identity og human identity MUST være separate felter/principals. En service må ikke automatisk arve brugerens rettigheder.
8. RLS-bypassroller, table owners og migrationsroller MUST være eksplicit dokumenteret og utilgængelige for almindelige runtime-komponenter.

### Designvalg før S3
Fastlæg og review en konkret tillidskæde:

MitID/OIDC → valideret identity assertion → applikationssession → betroet DB-kontekst → RLS.

Mulige DB-mønstre (separat gateway-loginrolle, signeret assertion verificeret af DB-laget eller isolerede kortlivede forbindelser) skal vurderes mod samme trusselsmodel. Ingen af mønstrene er godkendt alene ved at være nævnt her.

### Accepttests
- Som app_role kan en test angribe GUC og forsøge at læse en anden identitets rækker; forsøget skal fejle.
- Ugyldigt, udløbet, forkert audience-bundet eller replayet identity assertion afvises.
- To requests på samme genbrugte forbindelse kan ikke se hinandens identitetskontekst.
- Rollback, exception og timeout efter context setup efterlader ingen kontekst til næste request.
- Runtime-roller kan ikke aktivere BYPASSRLS, ændre policies eller antage migrations-/owner-roller.

**Gate:** Ingen rigtige Zone B-persondata eller S3-produktionsflow før threat model, designvalg, negative tests og uafhængigt sikkerhedsreview er godkendt.

## 5. C-04 — Kanonisk scope og adresseintegritet

### Invariant
Alle moduler bruger samme scope-vokabular, samme parent/child-regler og samme deduplogik. Scope er en forretningsidentitet, ikke en løs tekstværdi.

### Kanonisk model
Scope-typerne er MUNICIPALITY, ZIP, NEIGHBOURHOOD, STREET og ADDRESS.

ADDRESS er terminalt og refererer til en stabil address_id. De fire øvrige niveauer refererer til en versioneret geografisk area_id eller tilsvarende stabil scope-identitet. En adresse er ikke en femte area-række.

### Krav
1. API, event schemas, DB constraints, matching og fixtures MUST bruge samme enum og semantik.
2. ADDRESS MUST have address_id og MUST NOT have area_id.
3. Ikke-adresse scopes MUST have area_id og MUST NOT have address_id.
4. address_id MUST referere til en stabil registry identity/reference. Hvis den tidslige property-tabel ikke er egnet som FK-target, etableres en immutable identity/reference table; en løs UUID uden referentiel validering accepteres ikke.
5. Dedup-nøglen MUST være entydigt defineret som household + scope type + scope identity, med særskilt håndtering af gyldighed/aktiv status.
6. Unikke constraints skal håndhæve reglen transaktionelt; en applikationskontrol alene er utilstrækkelig.
7. Scope-ændringer i geografiske kilder må ikke stiltiende flytte en historisk ordre til en ny betydning. Den anvendte scope-version skal kunne rekonstrueres.
8. Ingen scope-model må genindføre uopfordret ejerkontakt; Projektgrundlag v5.2 har forrang.

### Accepttests
- Hver scope-type accepterer kun sin gyldige kombination af IDs.
- Ugyldige kombinationer af area_id og address_id afvises af DB.
- Ukendt adresse-reference afvises.
- Dubletordre for samme household + scope afvises også ved parallelle requests.
- Historiske ordre-scopes kan rekonstrueres efter ændring af geografi-/adressehierarki.

**Audit:** A-03 og A-07 kræver schemaændring, migration/review og negative tests.

## 6. C-05 — Migration governance og menneskelig godkendelse

### Invariant
En SQL-migration, der ændrer roller, privilegier, RLS, audit, append-only regler, persondata eller datamodel, er ikke godkendt driftsgrundlag, før en uafhængig menneskelig reviewer har godkendt den.

### Krav
1. AI-genererede migrationer er udkast, indtil review er dokumenteret. Review er obligatorisk uanset forfatter.
2. Forfatter og reviewer MUST være forskellige personer for sikkerhedsrelevante migrations.
3. Reviewregistrering MUST indeholde reviewer, dato, commit SHA, migrations-ID'er, scope, testbevis og eventuelle accepterede risici.
4. Review MUST omfatte roller, role membership, schema/table/column grants, default privileges, RLS, FORCE ROW LEVEL SECURITY, triggers, functions, SECURITY DEFINER, search path, indexes, constraints og data-retention-effekter.
5. CI MUST kunne migrere en tom database og opgradere fra den umiddelbart foregående baseline.
6. Destruktive ændringer kræver eksplicit review og dokumenteret expand/contract- eller tilsvarende sikker overgangsplan.
7. Backup/restore og rollback-/forward-recovery-procedure skal være afprøvet før produktionsbrug.
8. Migrationer MUST være deterministiske og må ikke afhænge af skjulte manuelle trin.

### Accepttests og reviewartefakter
- Clean install og upgrade tests er grønne.
- Privilege matrix er opdateret og testet.
- Backup kan gendannes i et isoleret miljø.
- Reviewsignatur peger på præcis commit og præcis migrationsmængde.
- En ændring efter review kræver nyt review.

**Audit:** A-06 lukkes først ved faktisk reviewbevis. Dokumentation af, at review er påkrævet, er ikke det samme som at review er udført.

## 7. C-06 — Cross-module workflows og sagaer

### Invariant
Et workflow på tværs af moduler er en eksplicit, sporbar proces med definerede lokale transaktioner og fejltilstande. Optata forsøger ikke at simulere én distribueret ACID-transaktion på tværs af moduler og eksterne systemer.

### Workflow-kontrakt
Hvert workflow MUST beskrive:
- Workflow ID og version.
- Startkommando og autoriseret actor/service.
- Deltagende moduler og ejerskab af data.
- Tilladte workflow- og deltilstande.
- Lokale transaktionsgrænser.
- Idempotency key og deduplication.
- Timeout, retry policy, backoff og dead-letter/manual review.
- Kompensation eller fremadrettet recovery.
- Audit- og correlation IDs.
- Håndtering af delvis succes, cancellation og genoptagelse.

### Saga-principper
1. Hvert modul ejer og committer sine egne data lokalt.
2. En saga step er idempotent og kan genkøres sikkert.
3. En step erklæres kun gennemført, når dens lokale transaktion er committed.
4. Fejl i en senere step må ikke skjule allerede gennemførte steps.
5. Kompensation er en ny forretningshændelse, ikke sletning af historik.
6. Eksterne, irreversible sideeffekter kan ikke antages at kunne rulles tilbage. Brug fremadrettet recovery, stop fremtidige handlinger og dokumentér resterende effekt.
7. Manuelle indgreb er synlige workflowtilstande med actor, begrundelse og audit.

### Accepttests
- Retry af hver step skaber ikke dobbelt effekt.
- Crash mellem to steps kan genoptages.
- Permanent fejl sætter workflow i eksplicit terminal eller manuel tilstand.
- Kompensation skaber ny historik og sletter ikke tidligere hændelser.
- Workflow kan spores via workflow/trace/correlation IDs.

## 8. C-07 — Audit før sideeffekt og transactional outbox

### Invariant
En følsom forretningsændring og dens obligatoriske auditregistrering er én atomisk lokal transaktion. Eksterne sideeffekter udføres først efter commit via en transactional outbox.

### Krav
1. En command må ikke returnere succes, hvis forretningsændringen eller obligatorisk auditrecord ikke er committed.
2. Business state, domain event, audit record og outbox record MUST skrives i samme DB-transaktion, hvor de tilhører samme lokale aggregate/transaction boundary.
3. Hvis audit-write fejler, rulles den tilhørende state change tilbage.
4. Workers læser kun committed outbox records.
5. Outbox delivery er at-least-once; consumers MUST være idempotente og deduplikere på stabil message/event ID.
6. Outbox status må ikke være eneste auditspor for, at forretningshandlingen fandt sted.
7. Retry, dead-letter og manuel replay skal være auditeret og adgangsbegrænset.
8. Ingen ekstern webhook, mail, partnerlevering eller anden irreversibel effekt må udføres før den lokale transaktion er committed.

### Fejlpolitik
- Audit eller outbox insert fejler: hele lokale transaktion rulles tilbage.
- Ekstern delivery fejler efter commit: forretningshændelsen forbliver committed; outbox retry/recovery håndterer leveringen.
- Ekstern delivery lykkes, men acknowledgement mistes: consumer idempotency forhindrer dobbelt domæneeffekt så vidt modtagerkontrakten tillader det; ellers kræves reconciliation.
- Audit pipeline/monitorering er utilgængelig: følsomme commands fail closed.

### Accepttests
- Simuleret auditfejl medfører rollback af business state.
- Simuleret outbox insert-fejl medfører rollback.
- Worker crash før/efter ekstern effekt giver sikker retry eller synlig reconciliation.
- Dobbelt delivery giver ikke dobbelt domæneeffekt.
- Manglende outbox delivery udløser alarm efter defineret SLA.

## 9. C-08 — Zone C som kontrolleret publiceringskanal

### Invariant
Zone C er ikke blot en anonymiseret SQL-view. Den er en kontrolleret publiceringsproces med dokumenteret dataset, formål, granularitet, risiko, godkendelse og versionsspor.

### Krav
1. Ingen Zone C-datasæt publiceres, før det har navngiven dataejer, formål, kilde-/licensgrundlag, population, tidsvindue og granularitet.
2. k ≥ 5 er et minimumskriterium i relevante sammenhænge, ikke en anonymiseringsgodkendelse.
3. Release review MUST vurdere små celler, suppression, komplementær suppression, differensangreb, overlappende geografier, tidsserieændringer, gentagne forespørgsler og eksterne hjælpedata.
4. Query-/releasekontroller skal begrænse, at successive forespørgsler kan isolere en enkelt person/husstand.
5. Rå Zone B-data og pseudonymer må ikke eksponeres til Zone C-forbrugere.
6. Hver publicering skal have dataset-version, query/version, release ID, godkender, tidspunkt og dokumenteret risikovurdering.
7. En publiceret release skal kunne stoppes/fjernes fra fremtidig adgang. Allerede downloadede kopier kan ikke garanteres tilbagekaldt.
8. Automatisk publicering uden godkendt release policy er forbudt.

### Accepttests
- Små celler under tærskel undertrykkes, også indirekte via totalsummer.
- Differens- og overlappende-område tests kan ikke isolere en skjult celle.
- Gentagne forespørgsler med ændrede filtre begrænses eller afvises.
- Tidsserieændringer og eksterne hjælpefelter indgår i release review.
- Ingen publicering uden gyldig, auditeret release approval.

**Gate:** Zone C forbliver ikke-publiceret, indtil pipeline og privacy review er godkendt.

## 10. C-09 — Samtykke og tilbagekaldelse

### Invariant
Samtykke er eksplicit, versioneret, formålsbundet og tilbagekaldeligt. Tilbagekaldelse skal stoppe fremtidig behandling/levering i alle kontrollerede Optata-flows inden for en defineret og målelig SLA.

### Krav
1. Samtykke-record MUST indeholde subject, purpose, scope, version af tekst/vilkår, tidspunkt, kilde, status og audit reference.
2. Hver kampagne-/partnerlevering MUST kontrollere aktuel consent state ved leveringstidspunktet, ikke kun ved audience-beregning.
3. Tilbagekaldelse MUST blokere queued og endnu ikke afsendte leveringer.
4. Tilbagekaldelse MUST propagere til interne workers, caches, materialiserede audiences og fremtidige partner-distributioner.
5. Partnerkontrakter og integrationer MUST definere modtagelse/acknowledgement af revocation, behandling af allerede modtagne data, retention/sletning og eskalation ved manglende svar.
6. Optata MUST registrere tidspunkt for anmodning, propagation, acknowledgement og eventuel fejl.
7. En allerede lovligt udført og modtaget ekstern disclosure kan ikke nødvendigvis tilbagekaldes teknisk. Systemet skal skelne mellem stop af fremtidig brug og håndtering af allerede disclosed kopier.
8. Mute, suppression, quiet hours og frequency caps er særskilte leveringskontroller og må ikke forveksles med samtykke.

### Accepttests
- Revocation før worker delivery stopper afsendelse.
- Revocation under workflow medfører re-check før ekstern effekt.
- Partner uden acknowledgement vises som uafklaret og udløser alarm/escalation.
- Cachede audiences kan ikke bruges efter revocation.
- Audit kan rekonstruere hele propagation-kæden.

## 11. C-10 — Eventkatalog, outbox/inbox og projektioner

### Invariant
Events er versionerede forretningsfakta. Projektioner er afledte og kan genopbygges. Eventvalidering alene er hverken autorisation, persistens eller atomisk state transition.

### Eventkontrakt
Alle domæneevents MUST have:
- event_id (globalt unik og stabil).
- event_type og schema_version.
- aggregate_type, aggregate_id og aggregate_version.
- occurred_at og recorded_at.
- actor og eventuel service_identity.
- purpose og scope, hvor relevant.
- trace_id, correlation_id og causation_id.
- Zone-/klassifikationsmetadata.
- Payload efter versioneret schema; ingen CPR eller hemmeligheder.

Eventkataloget skal udvides kontrolleret for ORDER, MANDATE, OFFER, LISTING, CAMPAIGN, CONSENT og PARTICIPATION før de tilsvarende moduler implementeres.

### Krav
1. Event schema validation MUST ske før persistens, men autorisation og state transition valideres separat.
2. Event persistence og aggregate version update MUST være atomisk.
3. Consumers MUST være idempotente og registrere behandlede message IDs (inbox/dedup).
4. Events med forkert version, manglende causation eller ulovlig transition afvises.
5. Upcasters er versionsstyrede, deterministiske og testede mod gemte historiske fixtures.
6. Projektioner MUST kunne genopbygges fra eventhistorikken uden at skabe eksterne sideeffekter.
7. Projektioner skal have mål for lag, monitorering og alarm ved overskridelse.
8. Replay må ikke sende e-mails, partnerkald, betalinger eller andre sideeffekter. Sideeffekter kræver separat eksplicit command/dispatch.
9. Event retention, persondata-minimering og slette-/begrænsningskrav skal afklares juridisk og teknisk før Zone B-produktion.

### Accepttests
- Samme event leveret flere gange ændrer projection kun én gang.
- Events i forkert aggregate-version afvises eller sættes i kontrolleret quarantine.
- Projection rebuild giver samme resultat som live processing.
- Rebuild udløser ingen eksterne sideeffekter.
- Upcasters kan læse alle understøttede eventversioner i testfixtures.
- Projection lag måles og udløser alarm.

## 12. Ingestion — single-writer og cursor-kontrakt (A-10)

### Invariant
For hver datakilde/checkpoint-strøm findes der højst én aktiv writer ad gangen, og checkpoint kan kun bevæge sig frem efter en fuldt committed batch.

### Krav
1. Runneren MUST validere cursorens monotonicitet og format; adapterens løfte er ikke tilstrækkeligt.
2. En source/checkpoint lock MUST håndhæves transaktionelt (fx row lock eller advisory lock med dokumenteret livscyklus).
3. Dataændringer, batchresultat og checkpoint advancement MUST have en defineret atomisk grænse.
4. Fejl midt i batch må ikke flytte checkpoint forbi ubehandlede records.
5. Retry skal være idempotent.
6. Out-of-order, gentagne, ugyldige og bagudgående cursors afvises eller sættes i quarantine efter en eksplicit regel.
7. Lock timeout og worker crash skal kunne håndteres uden permanent lås eller tab af batch.

### Accepttests
- To samtidige workers for samme source kan ikke committe konkurrerende checkpoints.
- To forskellige sources kan køre parallelt.
- Crash før commit efterlader checkpoint uændret.
- Retry af committed batch giver ingen dubletter.
- Cursor regression og out-of-order input opdages.
- Lock frigives ved exception, timeout og procesafslutning.

## 13. Fælles Definition of Done

Et fund eller en kontrakt kan kun markeres Lukket/Implemented når:
1. Kode/schema implementerer kontrollen.
2. Positive tests viser tilladt adfærd.
3. Negative tests forsøger aktivt at bryde grænsen.
4. Tests kører mod realistisk database-/runtime-konfiguration, ikke kun mocks.
5. CI kører testene på pull requests.
6. Migrationer er reviewet af en anden person end forfatteren.
7. Dokumentation, backlog og auditstatus er opdateret med konkrete links.
8. Ingen juridisk release gate er implicit lukket af teknisk implementering.
9. Resterende risici er navngivet, ejet og accepteret eksplicit.

Statusord:
- **Proposed:** designforslag, ikke godkendt.
- **Accepted:** beslutning godkendt af ansvarlig reviewer/ejer.
- **Implemented:** kode og tests findes.
- **Reviewed:** relevant uafhængigt review er dokumenteret.
- **Released:** relevante juridiske, sikkerhedsmæssige og driftsmæssige gates er lukket.

Disse statusser er uafhængige; et design kan fx være Accepted uden at være Implemented.

## 14. Mapping til auditfund og prioriteret hardening

| Auditfund | Kontrakt | Nødvendigt bevis før lukning |
|---|---|---|
| A-01 | C-01 | Least-privilege grants/views + direkte negative SELECT tests |
| A-02 | C-02, C-07, C-10 | Command/state machine + atomisk event/projection + race/replay tests |
| A-03 | C-04 | Kanonisk scope enum, constraints, dedup og historiske tests |
| A-04 | Dokumentationsgovernance | Unikke ADR-ID'er, statusoprydning, register og linkede konfliktrettelser |
| A-05 | C-03 | Threat model, ikke-spoofable trust chain, pool tests og uafhængigt security review |
| A-06 | C-05 | Reviewer-signatur, privilege matrix, migration/restore tests |
| A-07 | C-04 | Stabil address reference/FK og orphan tests |
| A-08 | C-02, C-06, C-10 | Eventkatalog og aggregate contracts før nye moduler |
| A-09 | C-02, C-07, C-10 | Autoriseret atomisk append boundary og negative tests |
| A-10 | §12 | Single-writer lock, cursor validation, concurrency/crash tests |
| A-11 | Data governance | Datadictionary, kilde/licensmatrix, quality/quarantine tests |
| A-12 | C-08 | Release pipeline, suppression/differencing/repeated-query tests og privacy approval |

### 14.1 Sprint A — anbefalet eksekveringsrækkefølge

1. **A-01 / C-01:** luk Zone A least privilege først; isoleret, målbar ændring med direkte DB-tests.
2. **A-06 / C-05:** etabler reviewproces og få alle eksisterende migrations gennemgået af et menneske. AI må ikke attestere egne migrations.
3. **A-02 / C-02 + C-07 + C-10:** beslut og implementér én kontrolleret ordre-write boundary; status uden event skal blive umulig.
4. **A-05 / C-03:** fastlæg threat model og trust chain før S3. Dette er et design-/review-gate, ikke en hurtig GUC-patch.
5. **A-03 + A-07 / C-04:** kanonisk scope, stabil adresse-reference, constraints og dedup.
6. **A-10 / §12:** single-writer ingestion og cursor/concurrency guards.
7. **A-04, A-11, A-12:** dokumentationsoprydning, datakildegovernance og Zone C release design.

Rækkefølgen er en anbefaling; afhængigheder kan kræve parallel dokumentationsarbejde. Den giver ikke tilladelse til at starte S3/S4/S5/S6.

## 15. Review- og ændringsregel

Før status ændres fra Proposed til Accepted, skal dokumentet reviewes af teknisk ejer/reviewer. C-03, C-05, C-08 og C-09 kræver særskilt sikkerheds-/privacy review før produktionsbrug.

Ændringer i kontrakterne skal:
1. Have begrundelse og konsekvensanalyse.
2. Opdatere arkitektur, relevante ADR'er og backlog.
3. Tilføje/ændre negative tests og CI-gates.
4. Angive hvilke auditfund der påvirkes.
5. Bevare historik; ingen kontrol må erklæres lukket alene ved at ændre dokumentstatus.

---

**Nuværende konklusion:** Optata har nu et samlet sæt foreslåede tværgående kontrakter, som kan styre hardening-arbejdet. Ingen af auditfundene A-01–A-12 erklæres lukket af dette dokument. Rigtige Zone B-persondata, transaktionsflows og Zone C-publicering forbliver gated.
