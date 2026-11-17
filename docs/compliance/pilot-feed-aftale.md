# Pilot-aftale: mægler-feed mod gratis adgang

**Formål:** Én mægler, ét postnummer, ét feed. Nok til at bevise M3 uden Boligsiden-forhandling.
**Format:** 2 sider, kan underskrives uden indkøbsafdeling. Ingen kommission, ingen gebyrdeling.

## A1 · Kommercielle vilkår (term sheet)

| Punkt | Vilkår |
|---|---|
| **Parter** | Optata ApS (CVR) ↔ [Mægler] (CVR) |
| **Optata leverer** | Verificerede køberhenvendelser på mæglerens egne udbud i [postnummer] · anonym dialog · gratis svar på hver henvendelse |
| **Mægler leverer** | Feed af egne aktive udbud i [postnummer], opdateret min. hver 30. min |
| **Pris i pilot** | **0 kr. i 90 dage** fra første feed-leverance |
| **Efter pilot** | Postnummer-abonnement 2.900 kr./md., 6 mdr. binding — **kun hvis mægleren vælger at fortsætte**. Ingen automatisk overgang |
| **Eksklusivitet** | Ingen i pilotperioden. Ved fortsættelse: én mægler pr. postnummer |
| **Kommission** | **Ingen.** Ingen andel af mæglerens salær, intet gebyr pr. handel |
| **Salgspakke** | Tilbydes **ikke** på mæglerens udbud. Mægleren gennemfører handlen |
| **Opsigelse** | 14 dages varsel i pilot. Feed-adgang ophører ved ophør |
| **Data efter ophør** | Udbud skjules fra match efter 30 dage. Historik bevares jf. licens og lov |

**Hvorfor gratis i 90 dage:** vi køber en feed-leverance og et bevis, ikke en kunde. Konverteringen sker, når mægleren har svaret på en verificeret køber, de ikke selv havde.

## A2 · Data- og rettighedsvilkår

| Punkt | Vilkår |
|---|---|
| **Licens** | Mægleren giver Optata ikke-eksklusiv ret til at importere, indeksere, matche og vise udbudsdata (felter i bilag 1) med kildehenvisning og link til annonce |
| **Omfang** | Kun mæglerens egne udbud i aftalt postnummer. Ikke andre mægleres, ikke portaldata |
| **Attribution** | Mæglerens navn + link til annonce vises ved hvert udbud i UI |
| **Billeder** | **Ingen** download eller videresalg. Kun URL-reference hvis medietilladelse foreligger |
| **Videresalg** | Aggregeret, anonymiseret statistik (k≥5) må indgå i Optatas analyser. **Ingen** enkeltudbud videresælges som rådata |
| **Persondata** | Feedet indeholder **ingen** personoplysninger om sælger eller køber. Kun ejendoms- og udbudsdata |
| **Roller** | Parterne er selvstændigt dataansvarlige for egne behandlinger. Ingen fælles dataansvar |
| **Fortrolighed** | Gensidig NDA. Køberidentitet deles aldrig med mægleren uden gensidigt samtykke |
| **Anonymitet** | Al dialog via Optatas relay. Kontakt udveksles kun ved gensidig enighed |
| **IP** | Optata ejer ordrebog, match-model og platform. Mægleren ejer egne udbudsdata |
| **Ansvar** | Optata formidler ikke handel i dette flow. Mægleren er ansvarlig formidler for egne udbud |

## A3 · Bilag 1 — felter i feedet

```
Påkrævet:  source_ref, status, listed_at, changed_at,
           street, house_no, zip, municipality_code,
           property.type, living_area_m2, rooms, asking_price_dkk, public_url
Valgfrit:  floor, door, lot_area_m2, build_year, energy_label,
           monthly_owner_cost_dkk, open_house[], hero_image_url
Forbudt:   sælgernavn, sælgerkontakt, køberdata, interne notater,
           vurderingsfortroligheder, data fra andre mæglere/portaler
```

## A4 · Underskriftsblok

```
For Optata ApS:              For [Mægler]:
Navn / titel: ____________   Navn / titel: ____________
Dato: ____________________   Dato: ____________________

Bilag 1 (felter) vedlagt.    Licensvilkår accepteret: ☐
Postnummer: ______________   Feed-URL / metode: ______________
Pilotperiode: 90 dage fra første leverance
```

> **Jurist-note:** Aftalen skal have `license_ref` i Optatas database, før adapteren aktiveres. Ingen licens → ingen import (invariant 11).
