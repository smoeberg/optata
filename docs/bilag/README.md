# Tekniske bilag 06–16

De elleve bilag er de oprindelige specifikationer, som projektgrundlaget konsoliderer. De ligger her uændrede.

**Ved uenighed gælder `docs/Optata - Projektgrundlag v5.1.md`.** Bilagene er skrevet før beslutningerne i v5.1 og er ikke opdateret.

| Bilag | Indhold |
|---|---|
| 06 | Systemarkitektur udledt af ni cases (C1–C9) og brugerflows |
| 07 | Arkitekturspecifikation S1–S5: database, API, relay og reveal, skærme |
| 08 | Test-fixtures, ingestion-adapters og agentens claim-kontrakt |
| 09 | Repo-struktur, CI-gates 1–12, OpenAPI-uddrag, drift og observability |
| 10 | Event-katalog, syntetisk datagenerator, admin- og review-UI |
| 11 | Matching, notifikation og samtykke, leverance og faktura |
| 12 | Ejerskabsverifikation, betaling og abonnement, trusselsmodel (STRIDE) |
| 13 | Leveranceplan S1–S7, retention og sletning, Demand Pro |
| 14 | Gap-analyse, onboarding til 250 verificerede, arkitekturdokument v1 |
| 15 | ADR 001–015, backlog for S0 og S1, kravspecifikation til UA-teamet |
| 16 | Backlog for S2, kontraktfiler i fuld tekst, DK-reviewerens checkliste |

## Hvad v5.1 har ændret i forhold til bilagene

Disse dele af bilagene må ikke bygges, som de står:

| Bilag | Afsnit | Forældet | Gælder nu (v5.1) |
|---|---|---|---|
| 06 | C1, C2, C3 | E-mail-ordre med magic link; notifikation til ejer, der ikke er logget ind | Login med MitID; ingen uopfordret kontakt (§4.3) |
| 06 | C4 | Ejerside med 12 ugers adgang til én adresse | Betalt adgang på fem niveauer, antaget 12 mdr. (§1.3, §4.3) |
| 07 | A1 | `provider = EMAIL`, dedup-index på `buyer_id`, k-anonymitet i materialized view, `EJF_MATCH` | MitID-login, dedup på `household_key`, fast kvartalsudtræk, adressekode (§4.2, §4.4, §4.8) |
| 07 | C1, C2 | Skærmene K4 og E1 (e-mail-ordre, notifikation pr. mail eller brev) | Udgår |
| 08 | A1 | Acceptkriterier for e-mail-ordre og CURIOS | CURIOS er udgået (§2.3) |
| 08 | B2 | EBR som kilde til koordinat og geometri | EBR er ejendomsbeliggenhed; se kildetabellen (§3.1) |
| 09 | B | `emailSession` og `POST /orders` som CURIOS | MitID-session (bilag A i v5.1) |
| 10 | A2, B3 | `level=CURIOS`, `identity.linked` fra e-mail | Udgår |
| 11 | A1 | »M2 må aldrig udløse kontakt til en ejer« | M2 må vises til og notificere ejere, der selv har slået det til (§4.1) |
| 11 | DEL B | Kanaler (e-mail, brev), `legal_basis_ref`, frekvensloft, afmelding permanent på adressen | Digital postkasse som tilvalg; fravalg følger ejerperioden (§4.3) |
| 12 | A3 | EJF-match som første metode | Adressekode plus navnematch som standard (§4.4) |
| 12 | B3 | Eksklusivitet via overlap-check og advisory lock | Én række pr. postnummer (§4.7) |
| 13 | A2, A3 | Lineær rækkefølge S1–S7; MitID-broker som kritisk vej for alt | A før B; broker er kritisk vej for B1 (§6.2, §6.4) |
| 13 | C2 | k-anonymitet håndhævet i forespørgslen | Fast kvartalsudtræk (§4.8) |
| 14 | B4 | Aktiveringsstige med e-mail-trin og påmindelse efter 48 timer | Stigen starter med MitID; ingen påmindelser (§4.9) |
| 15 | ADR-005, 006, 009, 010 | Ingen CPR lagret; progressiv identitet via e-mail; EJF først; regler i forespørgslen | Se ADR-registret i §7.3 |
| 15 | S1-13 | Ordre CURIOS med magic link | Køberordre er flyttet til S3 |
| 16 | B1 | `emailSession`, `level: CURIOS` i OpenAPI | Kontrakten skal skrives om, før den lægges i `contracts/` |

Listen dækker de steder, hvor v5.1 siger noget andet. Alt andet i bilagene står ved magt.
