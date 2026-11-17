# OPTATA — Efterspørgselsgravitation: mægleren kommer til os

Så er retningen låst. Vi erstatter ikke mægleren — **vi flytter markedets tyngdepunkt**, så mægleren må møde op dér, hvor efterspørgslen og mandatet ligger. Det er struktur **C**, og det er den stærkeste position: vi ejer relationen, processen og dataene; mægleren udfører arbejde, vi definerer.

---

## 1. Tyngdepunktet: tre trin der låser markedet

```
1. Efterspørgslen samles hos os
   MitID-verificerede købere med bankattest. Ingen andre har det.
        ↓
2. Sælgeren giver mandatet til os
   "Bring min bolig i markedet" — uden at afgive kontrollen til en mægler først.
        ↓
3. Mægleren må deltage i vores rails
   Buddene ligger her. Mandatet ligger her. Køberen er her.
   Vil du byde eller vejlede din kunde, sker det inde i Optata.
```

**Hvorfor mægleren kommer:** ikke fordi vi har et godt værktøj, men fordi **en handel allerede er i gang**, og de ikke kan se eller påvirke den udefra. Det er ikke et valg om software — det er et valg om at miste omsætning.

**Hvorfor sælgeren kommer (og det løser v5.1-problemet):** ejersiden er ikke længere "se om nogen vil købe" (passiv indsigt, ingen akut grund). Den er **"bring din bolig i markedet — du bestemmer hvem der arbejder for dig"** (handling). Det er en grund til at logge ind i dag.

---

## 2. Kontrolpunkterne — hvad vi ejer, hvad de udfører

| Kontrolpunkt | Ejer | Mæglerens rolle |
|---|---|---|
| **Efterspørgsel / ordrebog** | **Optata** | Ingen adgang til rådata |
| **Mandat** | **Optata** (sælgers autorisation) | Kan inviteres som udfører |
| **Budproces** | **Optata** (OfferLedger) | Kan vejlede, ikke eksportere |
| **Prisdannelse** | **Optata** (bud er data) | Ser bud i eget scope |
| **Køberrelation** | **Optata** | Får kontakt ved gensidig enighed |
| **Gennemførelse** | Partner eller mægler | Udfører papirarbejdet |
| **Sagsmappe + historik** | **Optata** | Bidrager, ejer ikke |

Vi tager de fem første. Gennemførelsen kan ligge hos dem — **det er arbejde, ikke ejerskab.**

---

## 3. To nye primitiver

### A. `SaleMandate` — sælgers autorisation til Optata

```sql
CREATE TABLE sale_mandate (
  mandate_id      uuid PRIMARY KEY,
  address_id      text NOT NULL,
  owner_identity  uuid NOT NULL,        -- MitID + ejerskabsbevis
  mandate_type    text NOT NULL,        -- EXCLUSIVE | OPEN
  scope           text NOT NULL,        -- BRING_TO_MARKET | ACCEPT_OFFERS | FULL_PROCESS
  price_guidance  int8range,            -- interval, IKKE en vurdering
  executor_mode   text NOT NULL,        -- DIRECT (partner) | AGENT_EXECUTED
  agent_org_id    uuid,                 -- valgt udfører, kan være NULL
  status          text NOT NULL,        -- DRAFT|ACTIVE|SUSPENDED|REVOKED|EXPIRED
  valid_from      date NOT NULL,
  valid_to        date NOT NULL,
  terms_version   text NOT NULL,        -- hvad sælger faktisk accepterede
  created_at      timestamptz NOT NULL
);
CREATE UNIQUE INDEX one_active_mandate
  ON sale_mandate(address_id) WHERE status='ACTIVE';
```

**Sameje:** alle nødvendige ejere er separate rækker i `mandate_party` og skal godkende samme vilkårsversion. **Andelsbolig:** andelshaver + relevant administrator-/foreningsdokumentation; EJF må ikke antages at dække andelsretten. Fuldmagt, dødsbo og tvister går i manuel review.

**Det er aktivet.** Et eksklusivt mandat hos Optata kan en mægler ikke tage. Og sælgeren kan tilbagekalde det — det er deres kontrol, ikke vores lås.

### B. `OfferLedger` — strukturerede bud, ikke fri chat

```sql
CREATE TABLE offer (
  offer_id         uuid PRIMARY KEY,
  mandate_id       uuid NOT NULL,
  buyer_identity   uuid NOT NULL,       -- VERIFIED + gyldig attest
  price_dkk        bigint NOT NULL,
  takeover_date    date NOT NULL,
  conditions       jsonb NOT NULL,      -- strukturerede vilkår, ikke fritekst
  financing_status text NOT NULL,       -- VERIFIED_FUNDS | CONDITIONAL
  expires_at       timestamptz NOT NULL,
  parent_offer_id  uuid,                -- modbud-kæde
  status           text NOT NULL,       -- SUBMITTED|ACKNOWLEDGED|COUNTERED
                                        -- |ACCEPTED|DECLINED|EXPIRED|WITHDRAWN
  submitted_at     timestamptz NOT NULL
);
-- append-only: statusændringer er nye events, aldrig UPDATE af buddet
```

**Hvorfor budbog i stedet for relay-chat — fire gevinster på én gang:**

1. **Det er en markedsmekanisme**, ikke en beskedtjeneste. Vi driver et marked.
2. **Prisdannelsen bliver data.** Bud, modbud, accept, tid — det er den mest værdifulde historik i boligmarkedet, og ingen andre har den.
3. **Redaction-problemet krymper.** Strukturerede felter + ét begrænset beskedfelt. Ikke fri tekst hvor kontaktinfo skal filtreres.
4. **Mægleren kan ikke tage samtalen ud** — der er ingen samtale at tage. Et bud med tidsstempel, finansieringsstatus og modbud-kæde kan ikke kopieres til en indbakke.

**Bud-state:**
```
SUBMITTED → ACKNOWLEDGED → COUNTERED → (nyt bud fra køber)
                        └→ ACCEPTED → FULFILLMENT → COMPLETED
                        └→ DECLINED | EXPIRED
```

---

## 4. Mæglerens deltagelse: scoped, ikke eksportérbar

| Mægleren får | Mægleren får ikke |
|---|---|
| Se anonyme, verificerede købere i eget postnummer | Navn, kontakt, præcise budgetter |
| Se bud på boliger hvor de er **inviteret udfører** | Bud på andres mandater |
| Vejlede egen kunde inde i platformen | Eksport af ordrebog eller bud |
| Byde/counter på vegne af sælger (mandat-scoped) | Tage dialogen ud af systemet |
| Bidrage til sagsmappen | Eje kundereationen eller historikken |

**Adgang:** MitID Erhverv → CVR → `participation_license` med område-scope + mandat-scope. Håndhæves i RLS.

**Pris:** deltagelsesabonnement pr. postnummer (2.900 / 6.900 bydel). **Ikke** betaling pr. lead, **ikke** kommission, **ikke** andel af salær. Vi sælger adgang til at deltage i et marked — ikke data de kan tage med hjem.

---

## 5. To veje gennem handlen — sælger vælger

| | **DIRECT** | **AGENT_EXECUTED** |
|---|---|---|
| Mandat hos | Optata | Optata |
| Budproces | Optata | Optata |
| Gennemførelse | **Advokatpartner** | Mægler (udfører) |
| Sælger betaler | **10.000 kr. fast gebyr** til Optata | Mæglerens salær |
| Optata tjener | Gebyr + deltagelse | Deltagelsesabonnement |
| Mægler involved | Nej (valgfrit senere) | Ja, som udfører |

**Default er DIRECT.** Det er hele pointen: sælgeren kan gennemføre en handel uden mægler, men *med* fuld tryghed via partner. Mægleren er et tilvalg, sælgeren kan købe sig til — ikke en port de skal igennem.

**Og derfor kommer mægleren:** de vil være den valgte udfører på mandater, der ellers går uden om dem.

---

## 6. Fire nye invarianter (14–17)

```
14. Ethvert mandat kræver MitID + ejerskabsbevis for ALLE ejere.
    Ét aktivt mandat pr. adresse. Tilbagekaldelse er øjeblikkelig.

15. Ethvert bud kræver VERIFIED køber med gyldig attest.
    Bud er append-only; statusændringer er events, aldrig overskrivning.

16. Intet bud, ingen accept og ingen identitetsudveksling sker
    uden for Optatas rails. Ingen eksport af ordrebog, bud eller kontakt.

17. Mægleradgang er scoped til (postnummer ∩ mandat hvor de er udfører).
    Ingen mægler ser bud på mandater, de ikke udfører.
```

**Guards der skal skrives af mennesker:**
`mandate_requires_all_owners` · `one_active_mandate_per_address` · `offer_requires_verified` · `offer_append_only` · `agent_scope_intersection` · `no_export_of_offers` · `reveal_requires_accepted_offer`

---

## 7. Juridisk struktur C — og hvad juristen skal svare på først

Vi ejer mandat, budbog og proces. **Det er tæt på kerneformidling** — det skal betales, ikke omgås.

**Struktur C:** Licenseret partner er *formel formidler of record*; Optata ejer brand, UX, mandat, budbog, kunde og data. Byg mod eget mæglerselskab (A) parallelt, flyt mandatet når godkendelsen foreligger.

**Juristens første spørgsmål er ændret.** Ikke længere *"er vi formidling?"* men:

| # | Spørgsmål | Afgør |
|---|---|---|
| **L38** 🔴 | Kan Optata **eje sælgers mandat** og drive budbog, mens en licenseret partner er formel formidler? Hvor går grænsen for, hvad vi selv må gøre? | Hele struktur C |
| **L39** 🔴 | Er en **struktureret budplatform** med accept/modbud formidling i sig selv — eller markedsinfrastruktur? | OfferLedger-design |
| **L40** 🔴 | Må vi markedsføre **"sælg uden mægler"** når partneren er formel formidler? Hvilken ordlyd er vildledende? | Hele positioneringen |
| **L41** | Krav til **mandatvilkår**: eksklusivitet, løbetid, tilbagekaldelse, sameje, andel | SaleMandate |
| **L42** | Mæglerens **deltagelsesvilkår**: scoped adgang, ingen eksport, tavshedspligt, sanktion | participation_license |

**L38–L42 skal besvares før SaleMandate, OfferLedger eller executor access aktiveres i produktion.** Men fase 1 (register/analyse) og fase 2 (verificeret ordrebog) kan bygges nu — de er uændrede.

---

## 8. Sekvens — hvor markedet vender

| Fase | Leverance | Kontrolpunkt vundet | Jura-blokering |
|---|---|---|---|
| **1** | S0 færdig · S1 rigtige data · S2 analyse/agent | Cash + troværdighed | Ingen (zone A) |
| **2** | S3: MitID, ordre, bankattest, vault | **Origination** | Kun persondata |
| **3** | **S4: SaleMandate** (inbound, ejer logger ind) | **Mandat** | L38, L41 |
| **4** | **S5: OfferLedger** + begrænset beskedfelt | **Budproces + prisdannelse** | L38–L39 |
| **5** | S6: Listings + Campaign + scoped deltagelse | Mægleren kommer til os | L42 |
| **6** | S7: Fulfillment via partner (DIRECT) | **Gebyret + sagsmappen** | L1–L3, L21–L24 |
| **7** | Demand Pro + egen mæglertilladelse (A) | Fuld kontrol | Godkendelse |

**Fase 3+4 er der, markedet vender.** Ikke fase 6. Vi kan eje mandat og budbog, før vi ejer gennemførelsen — og det er nok til at gøre mægleren afhængig.

---

## 9. Hvad der rettes i den eksisterende spec

| Dokument | Rettelse |
|---|---|
| `ARCHITECTURE.md` | 17 invarianter · nye moduler `mandates`, `offers` · relay erstattes af OfferLedger + begrænset besked |
| ADR-006 | MitID fra start (v5.1) — e-mail-identitet udgår |
| ADR-007 | Anonymitet bevares, men **bud er strukturerede**, ikke fri chat |
| ADR-008 | Reveal kræver **accepteret bud** + samtykke + step-up. To varianter: DIRECT (med gebyr) / AGENT_EXECUTED (uden) |
| ADR-016/017 | M3-lite **forkastes**. Køberen får ikke mæglerens kontakt — køberen afgiver bud i Optata |
| S4-backlog | Ejerside = **mandat-indgang**, ikke passivt indsigtsprodukt. 12 mdr. løbetid |
| S5-backlog | OfferLedger i stedet for relay-chat. Mindre redaction, mere marked |
| S6-backlog | Mægler = **deltager med scoped adgang**, ikke abonnent med leads |
| Forretningsplan | Ejersidens økonomi genberegnes (inbound). Nyt ben: mandat-baseret fulfillment |

---

## 10. Det første bevis — og det er ikke en analyse

Med denne model er det første bevis, der betyder noget:

> **Kan vi få én sælger til at give Optata et mandat — og én verificeret køber til at afgive et bud på det?**

Ét mandat + ét bud i ét postnummer beviser hele tesen: at efterspørgslen kan samle sig, at sælgeren vil bruge den, og at handlen kan ske i vores rails. Det er et mindre bevis end 250 verificerede købere — og det er **meget stærkere**.

Alt andet (tæthed, abonnementer, analyser) er skalering af noget, der allerede virker.

---

## Konklusion

Ambitionen er nu korrekt placeret: **vi tager origination, mandat, budproces og prisdannelse.** Mægleren beholder udførelsen — og kommer til os, fordi de ikke kan være andre steder.

Det kræver to nye primitiver (`SaleMandate`, `OfferLedger`), fire nye invarianter, og at juristen besvarer L38–L40 før fase 3. Til gengæld får vi den mest værdifulde datahistorik i boligmarkedet: **hvem bød hvad, hvornår, med hvilken finansiering — og hvad der blev accepteret.**

*Vil du have, at jeg skriver (a) `SaleMandate` + `OfferLedger` som fuld spec med API, states og guards, (b) den korrigerede ARCHITECTURE.md v2.0 med 17 invarianter og de nye moduler, eller (c) L38–L42 som jurist-bilag med de præcise spørgsmål der afgør struktur C?*
