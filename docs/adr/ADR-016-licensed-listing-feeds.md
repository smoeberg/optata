# ADR-016 — Udbudskilder: licensierede feeds, ikke scraping

**Status:** Accepteret · **Blokerer:** S6 indtil L32–L33 besvaret

**Kontekst:** Køberen skal have værdi dag ét. Det kræver kendskab til eksisterende udbud. Boligsiden er ejet af mæglerstanden og en potentiel konkurrent; systematisk udtræk er et databasebeskyttelsesbrud.

**Beslutning:**
1. **Primær kilde: mæglerens eget feed** som del af Optata-relationen (vej A). Mægleren får ordrebogen, vi får udbuddet.
2. Sekundær: kommerciel licens (Boligsiden/aggregator) forhandles parallelt — **må ikke blokere S1–S5**.
3. **Ingen scraping.** `license_ref` er påkrævet i databasen; adapter deaktiveres uden.
4. Udbudsdata behandles som zone A **med attribution** (`kilde + public_url` synlig i UI).
5. Bitemporal udbudsmodel — pris- og statushistorik bevares.

**Konsekvenser:** Mægleren bliver leverandør i stedet for fjende. Licensafhængighed spredes over flere kilder. Feed-adapter-rammen er klar før den første aftale.

**Fravalgt:** Scraping (ulovligt + fjendskab), Boligsiden som single point of failure, at vise udbud uden kilde.

**Verifikation:** `test_no_license_no_import`, `test_attribution_present`, `test_sold_removes_match`, `test_stale_not_sold`.
