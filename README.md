# Optata

Verificeret efterspørgsel på boligmarkedet: købere registrerer, hvad de vil købe, og ejere kan logge ind og se interessen for deres område, gade og hus.

## Indhold

| Sti | Indhold |
|---|---|
| `docs/Optata - Projektgrundlag v5.1.md` | Masterdokumentet: forretning, koncept, data, mekanismer, sikkerhed, jura og leveranceplan |
| `docs/historik/Optata - Projektgrundlag v5.0.md` | Forrige version |
| `docs/bilag/` | De elleve tekniske bilag (06–16), uændrede, med en oversigt over hvad v5.1 har ændret |
| `docs/design/` | Designleverancer: brandidé, visuel identitet, tekstdeck, mærke, mails, PDF, skærme, udbudsmatch (M3), markedsambitionen (SaleMandate + OfferLedger) og målrettet rækkevidde (Campaign) |
| `docs/architecture/ARCHITECTURE.md` | Arkitekturen: formål, zoner, moduler og de 20 invarianter |
| `docs/architecture/M3-opdatering.md` | M3-events, sprint-renummerering og nye guard-tests |
| `docs/backlog/S3.md`, `S4.md`, `S5.md` og `S6.md` | Sprintbacklogs for S3–S6 (S0 og S1 ligger i `docs/backlog/S0-S1.md`) |
| `docs/security/guards-s3.md` | Guard-tests til S3 som specifikation (udkast, afventer DK-review) |
| `docs/compliance/legal-questions-week6.md` | Spørgsmål, juristen skal besvare skriftligt (L1–L37) |
| `docs/compliance/pilot-feed-aftale.md` | Pilot-aftale: mægler-feed mod gratis adgang (M3) |
| `docs/adr/` | ADR-016–018: udbudskilder, M3 uden salgspakke, scope-hierarki |
| `contracts/feeds/agent-feed.v1.json` | Feed-kontrakt for mæglerens udbudsfeed (JSON Schema) |
| `docs/backlog/docs-struktur.md` | Foreslået samlet `docs/`-struktur og commit-plan |

Ændringerne fra v5.0 til v5.1 står i §0.2 i masterdokumentet. De åbne beslutninger står i §0.3.

## Mangler i repoet

Disse filer er nævnt i masterdokumentets bilag B, men er endnu ikke lagt ind:

- Optata - Forretningsplan v4.2.md
- Optata - Arkitekturreview v4.2.md
- Optata - Finansiel Model 36 Mdr.xlsx

## Kode

S0 (fundamentet) er påbegyndt. Status og næste skridt står i `docs/backlog/S0-S1.md`.

```
apps/api/        HTTP-transport, ingen forretningsregler
core/            domænet: ét modul pr. ansvar, events deles via core/events
workers/         baggrundsjobs
contracts/       OpenAPI og event-skemaer, skrives før koden
migrations/      zoner, roller, RLS og append-only tabeller
tools/           migrationer og syntetisk datagenerator
tests/guards/    de regler, der aldrig må brydes
```

Kom i gang (kræver Python 3.12 og Docker):

```
pip install -e ".[dev]"
make dev      # lokal database med syntetiske data
make ci       # lint, modulgrænser og alle tests
```

## Regler for koden

Reglerne står i masterdokumentets §7:

- Udvikling sker kun på syntetiske data. Ingen persondata i repoet.
- Guards, RLS, vault, reveal, finansiel logik og sletning skrives og godkendes af et menneske. Det, der ligger i `migrations/` og `tests/guards/` nu, er udkast og er markeret sådan.
- En rød guard-test blokerer merge. Det kræver, at branch protection er slået til på `main`.
- Kode, kommentarer og commits er på engelsk. Forretningsdokumenter og brugervendt tekst er på dansk.
