# Optata

**Verificeret efterspørgsel og markedsinfrastruktur til boligmarkedet.**

Optata udvikles som en platform, der forbinder ejendomsregisterdata, verificeret købsintention, sælgermandater, strukturerede bud og afgrænset partnerudførelse. Platformens langsigtede differentiering er at eje proces- og efterspørgselslaget — ikke blot vise boliger.

## Dokumentation — start her

| Dokument | Autoritet |
|---|---|
| [Projektgrundlag v5.2](docs/Optata%20-%20Projektgrundlag%20v5.2.md) | **Autoritativ produkt- og beslutningsbaseline** |
| [Arkitektur v2.1](docs/architecture/ARCHITECTURE.md) | Teknisk målarkitektur og invarianter |
| [ADR-017-SC](docs/adr/ADR-017-structure-c-supersession.md) | Struktur C og afløst M3-model |
| [S0–S1 backlog](docs/backlog/S0-S1.md) | Fundament og register/API |
| [S3 backlog](docs/backlog/S3.md) | MitID, ordre og verifikation |
| [S4 backlog](docs/backlog/S4.md) | SaleMandate |
| [S5 backlog](docs/backlog/S5.md) | OfferLedger |
| [S6 backlog](docs/backlog/S6.md) | Listings, Campaign og scoped deltagelse |
| [Campaign – fuld design-spec](docs/design/Optata%20-%20Campaign-modul%20-%20fuld%20spec%20v1.md) | Supplerende detaljespecifikation; underordnet v5.2/arkitektur |
| [Juridiske spørgsmål L1–L37](docs/compliance/legal-questions-week6.md) | Åbne juridiske spørgsmål |
| [Juridiske spørgsmål L38–L48](docs/compliance/legal-questions-mandate-and-campaigns.md) | Mandat, budbog og Campaign |
| [CI-gates](docs/ci-gates.md) | Kontroller og implementeringsstatus |

## Dokumentationsregler

1. v5.2 er produktbaseline; ARCHITECTURE.md er teknisk baseline.
2. Gamle designoplæg, bilag og sprinttekster er historik, medmindre de er udtrykkeligt refereret af gældende baseline.
3. En juridisk problemstilling er ikke godkendt, blot fordi den er beskrevet. Se release gates i v5.2 §10.
4. Opdater kontrakter, ADR, backlog og tests sammen, når en beslutning ændres.
5. Dokumentationsændringer sker på branch og via PR. Ingen direkte ændringer på main.

## Implementeringsstatus

S0 og S1 er delvist/indledningsvist implementeret. Bitemporal registermodel, testadapter, density og zone A API findes i første version. MitID, attest/vault, SaleMandate, OfferLedger, Campaign, produktionsfeed, frontend og fulfillment er ikke færdigimplementeret. Se v5.2 §9 og S0–S1 backlog.

## Kode og lokal udvikling

Python 3.12 og Docker:

```bash
pip install -e ".[dev]"
make dev
make ci
```

Koden skal anvende syntetiske data, indtil de relevante juridiske, licensmæssige og sikkerhedsmæssige gates er lukket. Guards, RLS, vault, identitet, mandat, bud, samtykke og finansiel logik kræver dokumenteret menneskelig review.
