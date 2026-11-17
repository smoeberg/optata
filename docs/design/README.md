> **VIGTIGT — status:** Punkterne 5–6 beskriver den tidligere M3-invitations-/leadmodel og er historiske. M3 som køber→mægler-invitation/reveal er forkastet. Brug `docs/backlog/S6.md` og projektgrundlag v5.2. Punkt 7–10 er designmateriale underordnet projektgrundlag v5.2 og arkitektur v2.1.\n\n# Design

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
10. `Optata - Campaign-modul - fuld spec v1.md` — kampagne-modulet som fuld spec: datamodel, tilstandsmaskine, leverings-pipeline, API, samtykketekst og guards

Punkt 8 beskriver struktur C. Den aktuelle tekniske baseline er ARCHITECTURE.md v2.1, og de aktuelle sprintkrav står i S4/S5/S6-backloggene. Jurist-spørgsmålene L38–L48 ligger i `docs/compliance/legal-questions-mandate-and-campaigns.md`.

Sprintbackloggen for S3 ligger i `docs/backlog/S3.md`, og guard-tests til S3 ligger som specifikation i `docs/security/guards-s3.md`. Udbudsmatch (S6) ligger i `docs/backlog/S6.md`.
