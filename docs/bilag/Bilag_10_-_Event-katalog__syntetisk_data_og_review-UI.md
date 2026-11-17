# OPTATA — (a) Event-katalog · (b) Syntetisk datagenerator · (c) Admin- & review-UI

De tre ting der gør systemet **målbart, udviklbart og driftbart** fra dag 1. Alt er repo-klar.

---

# DEL A — Event-katalog og versioneringsregler

## A1. Konvolut (alle events deler den)

```jsonc
// contracts/events/_envelope.v1.json
{
  "event_id":      "uuid",              // idempotens-nøgle
  "type":          "order.verified",    // domæne.handling, snake_case
  "schema_version":"1.0.0",             // semver pr. event-type
  "occurred_at":   "2026-11-16T09:14:22Z",  // forretningstid
  "recorded_at":   "2026-11-16T09:14:22Z",  // systemtid (bitemporal)
  "actor":         { "kind":"USER|STAFF|SYSTEM|PARTNER", "pseudonym":"K-7F3A" },
  "zone":          "A|B|C",
  "aggregate":     { "kind":"ORDER|DEAL|PROPERTY|IDENTITY", "id":"uuid" },
  "trace_id":      "…",                 // korrelation på tværs af services
  "causation_id":  "uuid",              // hvilket event udløste dette
  "payload":       { }                  // type-specifikt, ALDRIG CPR/rå kontakt
}
```

**Hårde regler:** `payload` må aldrig indeholde navn, CPR, e-mail, telefon eller dokumentindhold. Zone B-events bærer **kun pseudonym + reference-id**. Beskedindhold gemmes i `relay`-tabellen (redacted), ikke i event-loggen.

## A2. Katalog (uddrag — det komplette ligger i `contracts/events/`)

| Type | v | Zone | Nøglepayload | Konsument |
|---|---|---|---|---|
| `area.viewed` | 1.0 | A | area_id, source | funnel |
| `report.viewed` | 1.0 | A | area_id/address_id, profile_version | funnel |
| `order.created` | 1.1 | B | scope, area_id, level=CURIOS | orderbook, insights |
| `order.qualified` | 1.0 | B | criteria_hash | matching |
| `order.verified` | 1.0 | B | verification_id, expires_at | matching, agent-leads |
| `order.withdrawn` / `order.expired` | 1.0 | B | reason | insights, leads |
| `verification.submitted` | 1.0 | B | method, evidence_hash | review-UI |
| `verification.expired` | 1.0 | B | verification_id | leads (fjern), notify |
| `identity.linked` | 1.0 | B | from/to pseudonym | dedup |
| `identity.erased` | 1.0 | B | pseudonym, tombstone_ref | retention, insights |
| `owner.notified` | 1.0 | B | address_id, channel, legal_basis_ref | A2-måling |
| `owner.ownership_verified` | 1.0 | B | method, expires_at | disclosure |
| `interest.viewed` | 1.0 | B | order_pseudonym | A2 |
| `dialog.opened` | 1.0 | B | thread_id | A2, relay |
| `message.sent` | 1.0 | B | thread_id, redaction_flags[] | relay-metrics |
| `message.redacted` | 1.0 | B | rule, content_hash | sikkerhed |
| `deal.price_agreed` | 1.0 | B | thread_id, agreed_terms_hash | billing |
| `package.accepted` | 1.0 | B | package_id, payment_ref | fulfillment |
| `reveal.consent_given` | 1.0 | B | party, consent_ref | disclosure |
| `identity.revealed` | 1.0 | B | grant_id, audit_ref | audit, partner |
| `property.changed` | 1.0 | A | address_id, field, valid_from | overvågning, agent |
| `claims.extracted` | 1.0 | A | profile_id, count, model_version | review-UI |
| `profile.published` | 1.0 | A | profile_id, version, reviewed_by | reports |
| `subscription.started/expired` | 1.0 | B | product, scope_id, period | billing, RLS |
| `vault.accessed` | 1.0 | B | service, grant_id, reason | **P1-alarm hvis service≠disclosure** |

## A3. Versionering (semver + upcasting)

| Ændring | Version | Krav |
|---|---|---|
| Nyt valgfrit felt | MINOR | Ingen konsument-ændring |
| Nyt påkrævet felt | MAJOR | Upcaster + dobbeltskrivning i ≥1 release |
| Fjern/omdøb felt | MAJOR | Forbudt uden ADR + DK-review |
| Ny event-type | MINOR af katalog | Skema + konsument-test før merge |

```python
# events/upcast/order_created_1_0_to_1_1.py
def upcast(e):                       # gammel event → ny form, køres ved læsning
    e["payload"].setdefault("household_key", None)
    e["schema_version"] = "1.1.0"
    return e
```

**Regel:** gamle events **omskrives aldrig i store**. Upcasting sker ved læsning. Det er hele moatens integritet.

## A4. Levering, orden, idempotens

- **Transactional outbox:** domæneændring + event skrives i samme transaktion → worker publisher. Ingen dual-write.
- **Orden garanteres pr. aggregate** (`aggregate.id`), ikke globalt.
- **Konsumenter er idempotente** på `event_id`.
- Postgres-baseret bus i år 1; NATS/Kafka først ved målt behov.

## A5. Retention og sletning

| Lag | Indhold | Frist |
|---|---|---|
| Event-log | Pseudonym + metadata | 5 år (forretningshistorik) |
| Zone B-tabeller | Identitet, beviser, tråde | Formålsbestemt, slettes hårdt |
| Audit | Vault/reveal/samtykke | 5 år, uforanderlig |

`identity.erased` → **tombstone**: pseudonym beholdes i events (kan ikke re-identificeres), al zone B-indhold slettes, insights genberegnes. Det er foreneligt med "fuld historik" i §2.3.

---

# DEL B — Syntetisk datagenerator (UA-teamet kan arbejde dag 1)

## B1. Principper

1. **Deterministisk** — samme seed = samme data. Tests er reproducerbare.
2. **Vandmærket** — alle syntetiske poster bærer `_synthetic: true` + `seed`. Lækage kan detekteres automatisk.
3. **Aldrig rigtige persondata** — ingen CPR, ingen rigtige navne/telefoner.
4. **Ugyldige kontaktmønstre** — Danmark har intet officielt "fiktionelt" nummerinterval som US 555. Brug **ugyldige** numre (`+45 00 00 00 00`), e-mails på `example.invalid`, og CVR'er der er markeret syntetiske. Generatoren må aldrig emitte et gyldigt, potentielt rigtigt nummer.

## B2. CLI

```bash
optata-fixtures generate --seed 42 --area ZIP-2300 \
  --dwellings 10000 --orders 2500 --verified-ratio 0.10 \
  --include FX-01,FX-02,FX-03,FX-04,FX-05,FX-06,FX-07,FX-08 \
  --history-months 24 --out ./fixtures/generated/
```

## B3. Kerne (uddrag)

```python
def gen_area(seed, area_id, dwellings):
    rng = seeded(seed, area_id)
    # 1:mange er førsteklasses — andelsforeninger og udlejning findes altid
    yield andelsforening(bfe="BFE-1001", units=40)          # FX-01
    yield udlejning(bfe="BFE-2002", units=12, cvr=SYNTH_CVR) # FX-02
    for i in range(dwellings - 52):
        yield parcelhus(address_id=uuid5(seed, i), bfe=..., attrs=bbr_like(rng))

def gen_orders(area, n, verified_ratio):
    for i in range(n):
        lvl = "VERIFIED" if i < n*verified_ratio else pick(rng, ["CURIOS","QUALIFIED"])
        yield order(pseudonym=f"K-{hexid(seed,i)}", level=lvl,
                    household_key=household_of(i),          # FX-03 samboende
                    verification=attestation(expires_at=...)
                                 if lvl=="VERIFIED" else None)

def gen_redaction_corpus():                                  # FX-05
    return ["ring 00 00 00 00", "skriv til a@example.invalid",
            image_with_exif(gps=..., ocr_text="Navn: Testperson"),
            "ring nul nul nul nul …"]                        # stavevariant
```

## B4. Hvad generatoren skal producere ud over happy path

| Fixture | Genereres som |
|---|---|
| FX-01/02 | BFE med 40/12 adresse-id'er, korrekt `dwelling_count` |
| FX-03 | To identiteter, samme `household_key` |
| FX-04 | Attest `expires_at = i går`, status stadig VALID |
| FX-05 | Beskedkorpus incl. EXIF-billede og stavevarianter |
| FX-06 | Abonnement ZIP-2300 + ordrer i ZIP-2400 |
| FX-07 | Zone C-celle med 3 ordrer (k<5) |
| FX-08 | Identitet med `erased_at` + bevarede events |
| Bitemporal | 24 mdr. historik: BBR-arealændring, ejerskifte, ny lokalplan |
| Tæthed | Områder med 5 / 15 / 25 / 40 verificerede pr. 1.000 → KPI-grænser testes |

## B5. CI-integration (gate 10)

```python
def test_no_prod_like_data():
    for rec in fixtures.all():
        assert rec["_synthetic"] is True
        assert not looks_like_real_cpr(rec)
        assert not is_valid_dk_phone(rec)      # syntetiske numre SKAL være ugyldige
        assert rec.get("email","").endswith(".invalid") or "@" not in rec
```

**Kørbarhed:** generatoren er en del af `make dev` — UA-teamet får fuld, realistisk datamodel uden nogensinde at røre zone B i prod.

---

# DEL C — Admin- & review-UI (den flaskehals I får først)

## C1. Flader og roller

| Flade | Rolle | Zone | Formål |
|---|---|---|---|
| **Claim-review** | DK-analytiker | A | Godkend påstande før publicering |
| **Attest-review** | DK-stifter (senere UA-support m. begrænsning) | B | Godkend bankbevis → VERIFIED |
| **Support-konsol** | UA-support | B (pseudonym) | Sager uden vault-adgang |
| **Redaction-kø** | DK-sikkerhed | B | Gentagne omgåelsesforsøg |
| **Ops-dashboard** | Data-lead | A+C | Datakvalitet, expiry, tæthed |

## C2. Claim-review (C7)

**Layout:** kilde til venstre (artikel/plan, licenseret uddrag), claim til højre. Citatet **highlightes i kilden** via fuzzy-match — mismatch er synligt med det samme.

| Felt | Visning |
|---|---|
| subject / predicate / value | Redigerbart (med årsag) |
| status | VEDTAGET / FORESLÅET / UNDER_BYGNING / STOPPET / RYGTE |
| effective_date | Datovælger, påkrævet |
| kilde + dato + licens | Klikbar, altid synlig |
| confidence + model_version | Read-only |

**Handlinger:** `Approve` · `Reject(reason)` · `Edit+Approve` · `Merge duplicate` · `Escalate`.
**Genveje:** `A` approve, `R` reject, `E` edit, `J/K` næste/forrige. Mål: **< 20 sek. pr. claim.**

**Guard i UI:** `Publish` er deaktiveret indtil alle claims er APPROVED og profilen har `reviewed_by`. RYGTE-claims kan aldrig med i Bevægelse-laget.

## C3. Attest-review (C8) — den sikkerhedskritiske flade

**Sikker dokumentfremviser:** ingen download, ingen copy, vandmærke med reviewer-id, session bundet til sag, al adgang audit-logges (`vault.accessed`).

| Tjekliste (obligatorisk) | |
|---|---|
| Udsteder er genkendelig bank/realkredit | ☐ |
| Beløb aflæst og indtastet | ☐ |
| Udstedelsesdato + gyldighed | ☐ |
| Matcher købers MitID-identitet (navn vises transient, gemmes ikke) | ☐ |
| Dokument-hash beregnet | ☐ |

**Handlinger:** `Approve → VERIFIED (expires_at)` · `Reject(NO_ISSUER / UNREADABLE / MISMATCH / SUSPECTED_FORGERY)` · `Request new document`.

**Dual control:** beløb > 10 mio. kr. eller `SUSPECTED_FORGERY` kræver **anden godkender**. Fire-eyes er et salgsargument over for banken.

**Efter godkendelse:** kun attest-felterne (udsteder, beløbsinterval, dato, gyldighed) forlader vaulten. Dokumentet selv slettes efter fastsat frist.

## C4. Support-konsol (UA, uden vault)

Ser: pseudonym, ordrestatus, thread-status, redaction-flags, fejlkode, trace_id.
Ser **ikke**: navn, kontakt, dokument, beskedindhold i klartekst.
Kan: pause ordre, gensende notifikation, eskalere til DK, markere abuse. Kan **ikke**: reveal, ændre verifikation, eksportere.

## C5. Ops-dashboard

```
Datakvalitet:  dækning pr. register · quarantine-rate · dwelling_count-delta
Integritet:    udløbne VERIFIED i lead-lister (skal være 0) · pending attester > 24t
Tæthed:        verificerede/1.000 pr. område · P2-status
Sikkerhed:     vault.accessed{service≠disclosure} (skal være 0) · redaction-træff
Økonomi:       LLM-forbrug · cache-hit (alarm ved <70%)
```

## C6. Kapacitet og automatisering (den reelle flaskehals)

| Opgave | Volumen ved 250 verificerede | Tid | Hvem |
|---|---|---|---|
| Attest-review V1 | 250 + løbende fornyelser | ~10 min/stk → **~50 timer** | Stiftere |
| Claim-review | ~150 claims pr. profil × 3 profiler | ~20 sek/stk → **~2,5 timer** | Analytiker |
| Redaction-eskalering | ~2 % af beskeder | løbende | Sikkerhed |

**Automatiseringsvej:** V1 manuel → V2 bank-reference-validering (maskinel) → V3 bank-webhook (ingen review). Ved V3 falder attest-tiden til ~0. Det er den vigtigste driftsforbedring i år 2 — og den gør bank-partnerskabet til en **kapacitetsinvestering**, ikke kun et datasamarbejde.

## C7. Acceptkriterier for admin-UI

```
GIVEN claim uden kilde/dato     THEN kan ikke approves (guard, ikke kun UI)
GIVEN profil med PENDING claim  THEN Publish deaktiveret + 409 ved API-kald
GIVEN attest godkendt           THEN kun attest-felter eksponeres, dokument bliver i vault
GIVEN beløb > 10 mio.           THEN kræver anden godkender
GIVEN UA-support åbner sag      THEN ingen vault-felter i payload, vault.accessed ikke logget
GIVEN reviewer åbner dokument   THEN audit(zone=B, actor, sag, tid) skrives
GIVEN attest udløber i nat      THEN forsvinder fra lead-liste før kl. 06:00
```

---

## Tilsammen

- **(a)** gør historikken til et aktiv med integritet: append-only, versioneret, pseudonymt, sletnings-foreneligt.
- **(b)** fjerner den største praktiske blocker for UA+AI: realistiske data uden persondata, deterministisk og CI-håndhævet.
- **(c)** gør de to menneskelige gates (claims og bankbevis) til **hurtige, auditerede arbejdsgange** — og viser hvor automatisering betaler sig først.

*Næste skridt kan være (a) matching-algoritmen (score, reason_codes, tætheds-beregning og dedup i praksis), (b) notifikations- og samtykke-systemet (kanaler, jura-refs, afmelding, frekvensloft), eller (c) leverance- og fakturaflowet for områdeanalysen — den første krone i md. 4.*