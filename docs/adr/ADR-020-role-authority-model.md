# ADR-020 — Fælles Role & Authority Model

**Status:** Proposed · kræver produkt-, arkitektur-, sikkerheds- og juridisk review  
**Dato:** 17. november 2026  
**Beslutningsejer:** Stifter  
**Relaterer til:** Projektgrundlag v5.2, Architecture v2.1, Architecture Contracts C-01–C-10, ADR-019, LG-1/LG-2/LG-5/LG-6

## Kontekst

Optata har allerede domænespecifikke relationer og adgangsprincipper for købere, medkøbere, sælgere, medejere, mæglere, udførende partnere og RelocationCase-deltagere. De er ikke samlet i én autoritativ model. Samtidig skelner C-03 mellem human identity og service identity, og arkitekturens invariant 19 begrænser partneradgang til organisationens scope, aktiv participation license og konkret mandat/opgave.

Uden en fælles model risikerer hvert modul at implementere egne globale roller, uens samtykkekrav og utilsigtet adgang på tværs af husstande, organisationer og sager.

## Beslutning — foreslået

Indfør en fælles Role & Authority Model med fem adskilte lag:
1. Principal (human, service, organization, system operator).
2. Objekt- og tidsbundet domænerelation.
3. Verificeret organisationsmedlemskab.
4. Eksplicit capability-/authority grant.
5. Kontekst (purpose, scope, legal basis/consent, validity, assurance og domain state).

Adgang afgøres fail-closed af den samlede kontekst. En global rolle giver ikke i sig selv adgang. RBAC bruges til at beskrive funktion/capability-katalog; ABAC og objektbundne relationer/grants afgrænser den konkrete adgang.

Samtykke og retsgrundlag er ikke roller. Serviceidentiteter arver ikke menneskers rettigheder. RelocationCase koordinerer separate spor, men giver ikke automatisk adgang til dem.

## Konsekvenser

- Ét fælles autorisationssprog for S3, S4, S5, S6 og RelocationCase.
- Mere præcis organisations-, fuldmagts- og revocation-model.
- Kræver policy contract, datamodel, audit og negative tests før Zone B-produktionsbrug.
- A-05 (trusted identity/session boundary) forbliver release blocker, indtil C-03 er implementeret og testet.
- Ingen juridisk godkendelse eller implementering følger af ADR'en.

## Reviewpunkter

1. Godkend principal-, relation-, organisations- og servicekatalog.
2. Gennemgå permission matrix og capabilities.
3. Gennemgå delegation, fuldmagt, mindreårige og juridiske personer.
4. Gennemgå RelocationCase-deltagernes adgang og individuel godkendelse.
5. Afklar professionel rolle-/ansvarsfordeling under LG-1/LG-5/LG-6.
6. Godkend negative sikkerhedstests og implementeringsrækkefølge.

Se [Role & Authority Model v1.0](../security/ROLE-AUTHORITY-MODEL-v1.0.md) for den detaljerede specifikation.
