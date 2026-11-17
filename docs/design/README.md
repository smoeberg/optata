# Design

Designleverancerne fra designfasen, lagt ind uændrede. Læs i denne rækkefølge:

1. `Optata - Designoplaeg v1.md` — brandidé, visuel identitet, forside, komponentbibliotek og designbrief
2. `Optata - Tekstdeck, maerkespecifikation og ejer-mail v1.md` — alle skærmtekster, wordmark og parcel-mærket, ejer-mailen
3. `Optata - Systemmails, PDF-leverance og da.json v1.md` — systemmails, områdeanalysen som PDF og `da.json`
4. `Optata - Sidste skaerme og designpakke v1.md` — de sidste skærme og den foreslåede `docs/design/`-struktur
5. `Optata - Udbudsmatch M3 v1.md` — udbudsmatch: ny match-retning, listing-model, mægler-invitation
6. `Optata - Feed-adapter, invitation og M3-tekster v1.md` — AGENT_FEED-adapteren, køber-notifikation, invitationsmailen og gratis-svar-flowet
7. `Optata - Markedsambition - SaleMandate og OfferLedger v1.md` — ambitionskorrektion: M3 som lead-kanal forkastes; SaleMandate, OfferLedger og mægleren som udfører
8. `Optata - Efterspoergselsgravitation - struktur C v1.md` — retningen låst: struktur C, `sale_mandate` + `offer`-modellerne, invarianter 14–17, L38–L42 og fasesekvensen
9. `Optata - Maalrettet raekkevidde - Campaign v1.md` — mægleren betaler for rækkevidde: `campaign`-modellen, invarianter 18–20, L43–L48 og kill-kriterier

Punkt 8 låser strukturen: ARCHITECTURE.md er opdateret til v2.0 (20 invarianter, modulerne `mandates`, `offers`, `campaigns`), og S4/S5/S6-backloggene bærer rettelses-noter.

Sprintbackloggen for S3 ligger i `docs/backlog/S3.md`, og guard-tests til S3 ligger som specifikation i `docs/security/guards-s3.md`. Udbudsmatch (S6) ligger i `docs/backlog/S6.md`.
