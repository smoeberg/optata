# Optata

Verificeret efterspørgsel på boligmarkedet: købere registrerer, hvad de vil købe, og ejere kan logge ind og se interessen for deres område, gade og hus.

## Indhold

| Sti | Indhold |
|---|---|
| `docs/Optata - Projektgrundlag v5.1.md` | Masterdokumentet: forretning, koncept, data, mekanismer, sikkerhed, jura og leveranceplan |
| `docs/historik/Optata - Projektgrundlag v5.0.md` | Forrige version |

Ændringerne fra v5.0 til v5.1 står i §0.2 i masterdokumentet. De åbne beslutninger står i §0.3.

## Mangler i repoet

Disse filer er nævnt i masterdokumentets bilag B, men er endnu ikke lagt ind:

- Optata - Forretningsplan v4.2.md
- Optata - Arkitekturreview v4.2.md
- Optata - Finansiel Model 36 Mdr.xlsx
- De elleve tekniske bilag (`attachments/altf73/*.txt`)

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
