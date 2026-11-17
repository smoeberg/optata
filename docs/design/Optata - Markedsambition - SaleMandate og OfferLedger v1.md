# Du har ret — jeg satte ambitionsniveauet forkert

M3-lite gør Optata til en lead-kanal for mæglerstanden. Det er den modsatte bevægelse af inverteringen: vi ville give dem origination *og* kontakten, og beholde en abonnementsindtægt. Det er at sælge dem det, de mangler, i stedet for at tage det, de lever af.

Lad mig korrigere — og gøre ambitionen konkret i stedet for bare at være enig.

---

## 1. Hvad "at tage markedet" betyder arkitektonisk

At ændre markedet er ikke et spørgsmål om markedsføring. Det er et spørgsmål om **hvilke objekter vi ejer**. En mægler ejer i dag fire ting. Vi skal tage dem én ad gangen:

| Kontrolpunkt | Mægleren i dag | Optata skal eje |
|---|---|---|
| **Origination** | Finder køberen | **Ordrebogen** — køberen starter her |
| **Mandat** | Får sælgers underskrift | **Sælgerens mandat til at bringe boligen i markedet** |
| **Proces** | Ejer dialog, bud, forhandling | **Budbogen** — strukturerede bud gennem os |
| **Gennemførelse** | Ejer sagen og papiret | **Sagsmappen** — dokumenter, tinglysning, refusion |

Mit M3-lite-forslag gav os kun det første. **Det andet og tredje er der, markedet vendes.** Og det er dem, vi ikke har specificeret endnu.

---

## 2. De to manglende primitiver

Vi har `order` (efterspørgsel) og `listing` (udbud). Vi mangler de objekter, der gør Optata til et **marked** og ikke en søgemaskine:

### A. SaleMandate — sælgerens autorisation til Optata

```
SaleMandate
  address_id, owner_identity (MitID + ejerskabsbevis)
  type: EXCLUSIVE | OPEN
  scope: BRING_TO_MARKET | ACCEPT_OFFERS | FULL_PROCESS
  price_guidance (interval — ikke en vurdering)
  agent_org_id? (valgt udfører, kan være tom)
  valid_from / valid_to
  status: DRAFT | ACTIVE | SUSPENDED | REVOKED
```

**Det er aktivet.** En mægler kan ikke tage en bolig, hvis mandatet ligger hos os og er eksklusivt. Og sælgeren får noget, de ikke får i dag: *en vej i markedet uden at afgive kontrollen til en mægler først.*

### B. OfferLedger — strukturerede bud, ikke fri chat

```
Offer
  mandate_id | listing_id
  buyer_pseudonym (VERIFIED, gyldig attest)
  price, takeover_date, conditions[]
  financing_status: VERIFIED_FUNDS | CONDITIONAL
  expires_at
  status: SUBMITTED | ACKNOWLEDGED | COUNTERED | ACCEPTED | DECLINED | EXPIRED
  append-only, tidsstemplet, uforanderlig
```

**Hvorfor budbog i stedet for relay-chat:**

- Det er en **markedsmekanisme**, ikke en beskedtjeneste
- Prisdannelsen bliver **data** — det er moat'en, der compounder
- Redaction-problemet krymper: strukturerede felter, få fritekstfelter
- Juridisk står vi stærkere: vi driver en budplatform, ikke en forhandling
- **Mægleren kan ikke tage samtalen ud** — der er ingen samtale at tage

Det sidste er afgørende. Fri chat kan kopieres til en indbakke. En budbog med verificerede købere, tidsstempler og modbud kan ikke.

---

## 3. Mæglerens rolle: fra kunde til deltager

| | Mit tidligere forslag | Den ambitiøse model |
|---|---|---|
| Mægleren er | Abonnent med leads | **Udfører med scoped adgang** |
| Får | Køberens kontaktinfo | **Ret til at svare/byde inde i platformen** |
| Kan eksportere | Ja | **Nej** |
| Betaler for | Data | **Adgang til mandat + budproces** |
| Mister | Ingenting | **Origination og kundeejerskab** |

**Mekanismen der tvinger dem ind:** køberen er allerede MitID-verificeret, bankattesteret og har afgivet et bud. En mægler, der ikke er på platformen, kan ikke se buddet, kan ikke svare og mister en handel, der allerede er i gang. Det er ikke et værktøj, de kan vælge fra — det er en markedsplads, de må deltage i.

**Og det løser v5.1-problemet med ejersiden:** ejeren har nu en **grund** til at komme. Ikke "se om nogen vil købe" (passiv indsigt), men **"bring din bolig i markedet uden mægler"** (handling). Det er derfor, de betaler.

---

## 4. Den juridiske pris — og den skal betales, ikke omgås

At eje mandat, budbog og proces **er** tæt på kerneformidling. Vi kan ikke både tage markedet og hævde, at vi blot er data.

| Struktur | Beskrivelse | Konsekvens |
|---|---|---|
| **A — Eget mæglerselskab** | Optata bliver godkendt ejendomsmægler | Fuld kontrol og indtægt. Kræver godkendelse, forsikring, AML, god skik |
| **B — Partner-of-record** | Licenseret partner er formel formidler; **vi ejer brand, UX, mandat, budbog og kunde** | Hurtigere. Partneren har vetoret og kan blive flaskehals |
| **C — Hybrid** | Start B, byg A parallelt; flyt mandatet til eget selskab ved godkendelse | **Anbefalet** — bevarer ambitionen, fjerner blocker |

**Juristens første spørgsmål er ikke længere "er vi formidling?"** Det er: *Kan Optata eje mandat og budbog, mens en licenseret partner er formel formidler — og hvor går grænsen for, hvad vi selv må gøre i processen?* Det afgør A vs. B vs. C.

---

## 5. Sekvens med ambitionen intact

| Fase | Leverance | Kontrolpunkt vundet |
|---|---|---|
| 1 | Register + analyse (zone A) | Cash. Ingen jura-blokering |
| 2 | Verificeret ordrebog (MitID + attest) | **Origination** |
| 3 | **SaleMandate + OfferLedger** | **Mandat + proces** |
| 4 | Udfører-adgang (MitID Erhverv, scoped, ingen eksport) | Mægleren kommer til os |
| 5 | Licenseret fulfillment (B → A) | **Sagsmappen + gebyret** |

**Fase 3 er der, markedet vender.** Ikke fase 5. Vi kan eje mandat og budbog, før vi ejer gennemførelsen — og det er nok til at gøre mægleren afhængig.

---

## 6. Hvad jeg retter i specifikationen nu

1. **M3-lite forkastes.** Køberen får ikke mæglerens kontakt. Køberen afgiver bud inde i Optata.
2. **S5 ændres:** fra fri relay-chat til **OfferLedger + begrænset beskedfelt**. Mindre redaction, mere marked.
3. **Nye moduler:** `mandates` og `offers`.
4. **Ny invariant:** *Intet bud, ingen accept og ingen identitetsudveksling sker uden for Optatas rails.*
5. **Ejersiden bliver mandat-indgangen** — ikke et passivt indsigtsprodukt.
6. **Mæglerabonnementet omdefineres:** adgang til at deltage, ikke adgang til data.

---

**Én ting skal jeg have bekræftet, før jeg skriver det om:** Med *"markedet skal vende sig mod mæglerne"* — mener du, at **mæglerne skal komme til Optata, fordi efterspørgslen er her** (min læsning ovenfor), eller at **Optata skal presse mæglerne helt ud af transaktionen**?

Svaret afgør, om vi bygger mod struktur **C** (mægleren som udfører i vores rails) eller **A** (vi erstatter dem fuldt ud). Det er den eneste beslutning, der ændrer arkitekturen fundamentalt — resten kan jeg skrive om med det samme.
