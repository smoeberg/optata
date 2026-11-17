# OPTATA — Jurist-bilag: mandat, budbog og kampagner (L38–L48)

**Format:** Svar + handlingsregel + hjemmel + konsekvens for kode + blokerer deploy + dato/initialer.
*"Det afhænger af…"* accepteres ikke — skal udmøntes i en regel, vi kan implementere.

## C1 · Mandat, bud og positionering (🔴 før fase 4–5)

| # | Spørgsmål | Afgør |
|---|---|---|
| **L38** 🔴 | Kan Optata **eje sælgers mandat** (`SaleMandate`) og drive budbog, mens en licenseret partner er formel formidler of record? Hvor går grænsen for, hvad vi selv må gøre i processen (vise bolig, modtage bud, videregive accept, koordinere dokumenter)? | Hele struktur C. Afgør om vi skal søge egen mæglertilladelse før fase 4 |
| **L39** 🔴 | Er en **struktureret budplatform** med bud, modbud, accept og tidsstempler formidling i sig selv — eller markedsinfrastruktur? Betyder det noget, at buddene er strukturerede felter og ikke fri forhandling? | OfferLedger-design og vores rolle |
| **L40** 🔴 | Må vi markedsføre **"sælg uden mægler"** / **"bring din bolig i markedet"**, når partneren er formel formidler? Hvilken ordlyd er vildledende over for forbrugeren? | Hele positioneringen og forsiden |
| **L41** 🔴 | Krav til **mandatvilkår**: eksklusivitet, løbetid, tilbagekaldelse, prisvejledning (interval, ikke vurdering), sameje (alle ejere), andelsbolig (administrator-attest), gebyr ved tilbagekaldelse? | `sale_mandate` + vilkårstekst |
| **L42** | Mæglerens **deltagelsesvilkår**: scoped adgang (postnummer ∩ mandat), forbud mod eksport, tavshedspligt, sanktion ved omgåelse. Er "ingen eksport" håndhæveligt? | `participation_license` |

## C2 · Kampagner og målretning (🔴 før fase 3)

| # | Spørgsmål | Afgør |
|---|---|---|
| **L43** 🔴 | Hvilket **samtykke** kræves for at vise købere markedsføring fra tredjepart (mægler)? Er Optata **afsender på mæglerens vegne** eller formidler af indhold? Hvem er dataansvarlig for hvilken del? Skal der databehandleraftale mellem Optata og mægler? | Hele kampagne-modulet |
| **L44** 🔴 | Er målretning mod **købsintention + budget + geografi** profilering, der udløser særlige krav (art. 22, DPIA, information)? Er **audience ≥25 + k≥5** tilstrækkeligt til at undgå individuel målretning? | Targeting-model og gulve |
| **L45** | Er **kampagne → forespørgsel → bud** formidling, eller markedsføring af et eksisterende udbud? Vi tager intet honorar pr. handel, kun for rækkevidde | Juridisk position |
| **L46** | Krav til **indhold og attribution**: pris, status (solgt/tilbud), åbent hus, udsagn om boligen. Hvad er vildledende, og hvem har ansvaret for mæglerens fritekst? | Indholdsregler + scanning |
| **L47** | **P2B / platformforordningen**: krav til gennemsigtighed i rangering, omdømmescoring og kvotetildeling over for erhvervskunder? Skal vores relevans-model dokumenteres over for mægleren? | Omdømmemodel + vilkår |
| **L48** | Retention af **kampagne-interaktion** (leveret, åbnet, feedback, mute) — formål og frist? Er mute permanent af hensyn til køberen foreneligt med mæglerens indsigtsret? | Datamodel + retention-tabel |

## C3 · Svarskabelon

```markdown
### L__ — [titel]
Svar:            [ ] Ja  [ ] Nej  [ ] Ja, med ændringer:
Handlingsregel:  _________________________________________________
Hjemmel:         _________________________________________________
Konsekvens for kode/kontrakt: ____________________________________
Blokerer deploy: [ ] Ja  [ ] Nej
Dato / initialer: ____________________
```

**Leverance:** udfyldt L38–L48 + rettede vilkårstekster (L40, L41, L42) + samtykketekst (L43) + eventuel DPIA-vurdering (L44).

---

## Prioritet nu

| # | Handling | Blokerer |
|---|---|---|
| 1 | **L38–L40 til juristen** — mandat, budbog, positionering | Fase 4–5 (der hvor markedet vender) |
| 2 | **L43–L44** — kampagnesamtykke og profilering | Fase 3 (acquisition-motoren) |
| 3 | Datafordeler (EJF + **DAGI**) + MitID-broker | Fase 1–2 |
| 4 | **ADR-013** + branch protection + manglende CI-gates | Alt |

**Fase 1 og 2 kan bygges nu.** De er zone A og verificeret ordrebog — uændret af v5.1 bortset fra MitID fra start. Mandat og budbog er der, ambitionen realiseres, og de kræver juristens svar først.
