# ADR-017-SC — Struktur C: SaleMandate, OfferLedger og scoped udførere

**Status:** Proposed baseline — stiftergodkendelse og juridisk afklaring kræves  
**Dato:** 17. november 2026  
**Erstatter/afklarer:** Den tidligere ADR-017 om M3 uden salgspakke skal læses som historisk beslutning om det daværende M3-flow. Denne ADR fastlægger den nye produktretning; den gør ikke M3-flowet gældende igen.

## Kontekst
Den tidligere M3-model byggede på køber→mægler-invitation, anonym relay-dialog og lead-/abonnementsrelation. Den passer ikke til den vedtagne struktur C, hvor Optata samler efterspørgslen, registrerer sælgermandat og driver en struktureret budproces. Campaign og licenserede listings er selvstændige distributionsmoduler; de er ikke en lead-invitation til at afsløre køberen.

## Beslutning
1. Optata udvikler SaleMandate som versionsbundet, tilbagekaldeligt mandatobjekt.
2. Optata udvikler OfferLedger som append-only bud- og modbudshistorik.
3. DIRECT og AGENT_EXECUTED er to udførelsesveje gennem samme mandat- og budrails.
4. Mægler/partner får scoped adgang via aktiv participation license; adgang er skæringsmængden af organisation, geografi, mandat og opgave.
5. M3 som invitation-/lead-/reveal-kanal er forkastet.
6. Campaign er et separat opt-in distributionsmodul med licenserede listings og egne guards.
7. Produktretningen er ikke juridisk godkendelse af Optatas rolle. Produktion er gated af L38–L48 og øvrige relevante spørgsmål.

## Konsekvenser
- S4 bliver SaleMandate, S5 bliver OfferLedger, S6 bliver Listings/Campaign/scoped participation.
- Gamle S3–S6-backlogs må ikke bruges som implementeringsspecifikation.
- `owner_identity` alene er utilstrækkelig til sameje; `mandate_party` er nødvendig.
- Fri relay-chat, reveal og lead-export er ikke transaktionsmekanismer.
- En platformaccept må ikke markedsføres som endelig købsaftale uden juridisk godkendelse.
- Forretningsplan og unit economics skal genberegnes; v5.1-priser er historiske hypoteser.

## Åbne forhold
- Juridisk formidlerrolle, mandatets gyldighed, bud/accept, markedsføringsordlyd, mæglerens ansvar.
- Dataansvar og samtykke ved Campaign.
- Licenser til listing feeds og tredjepartsdata.
- DIRECT-partnerens rolle og ansvar.
- Endelig prismodel.

## Implementeringsregel
Indtil alle relevante gates er lukket, må udvikling kun ske på syntetiske data, testmiljø og feature-disabled flows. Ingen rigtig ejer, køber, mægler eller budproces må onboardes på grundlag af denne ADR alene.
