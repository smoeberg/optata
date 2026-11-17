# Optata dokumentationsindeks

## Autoritative dokumenter
- `Optata - Projektgrundlag v5.2.md` — produkt, forretning, roller, faser og juridiske gates.
- `architecture/ARCHITECTURE.md` — moduler, datazoner, invariants, flows og systemgrænser.
- `architecture/ARCHITECTURE-CONTRACTS-v1.0.md` — foreslåede tværgående sikkerheds-, transaktions-, event- og workflowkontrakter. Status er Proposed indtil review.
- `security/ROLE-AUTHORITY-MODEL-v1.0.md` — fælles principals, relationer, organisationsroller, capabilities, rettighedsmatrix og negative tests. Status er Proposed.
- `adr/ADR-020-role-authority-model.md` — beslutningsforslag om fælles rolle- og autoritetsmodel.
- `adr/ADR-017-structure-c-supersession.md` — beslutningsretning for struktur C.
- `adr/ADR-019-relocation-case.md` — foreslået koordineret flytteforløb med separate salg- og købsspor.
- `backlog/S0-S1.md`, `S3.md`, `S4.md`, `S5.md`, `S6.md` — implementeringsplan.

## Produktlukning og udviklingsparathed
- `product/PRODUCT-CLOSURE-AND-DEVELOPMENT-READINESS-v1.0.md` — samlet audit af handelsrejsen, AI-agentinput, mangler, 20 %-mål og beslutninger før konceptlås. Status: audit/anbefaling, ikke godkendt baseline.

## Handelsmodel og service blueprint
- `product/TRANSACTION-MODEL-AND-SERVICE-BLUEPRINT-v0.1.md` — stifterretning for Optatas juridiske/platformsmæssige grænse, advokatselskab, DIRECT, komplette køber-/sælgerrejser, dødsbo, budmekanik, fulfillment og abonnementsmodel. Arbejdsgrundlag; ikke juridisk godkendt eller gældende baseline.

## Supplerende specifikationer
- `design/` — UI, produktdesign, listings, Campaign og markedsambition.
- `compliance/` — åbne juristspørgsmål og aftaleudkast.
- `security/` — guard-specifikationer.
- `ci-gates.md` — CI-kontrolplan.
- `bilag/` — historiske tekniske bilag, ikke selvstændig autoritet.

## Historik og konflikter
- Projektgrundlag v5.1 er historisk baseline og må ikke bruges som gældende krav, når det afviger fra v5.2.
- Tidligere S3–S6-planer og M3-flow er erstattet af de aktuelle backlogfiler.
- ADR'er med status Superseded/Retired er historik. Kun Accepted ADR'er er normative; Proposed kræver eksplicit godkendelse.
- Architecture Contracts v1.0 er et foreslået teknisk kontraktsæt og er ikke en implementerings- eller sikkerhedsgodkendelse.

## Ændringsregel
Alle ændringer i produktbeslutninger skal opdatere v5.2 og relevante ADR'er. Alle ændringer i systemadfærd skal også opdatere arkitektur, kontrakter, backlog og tests.
