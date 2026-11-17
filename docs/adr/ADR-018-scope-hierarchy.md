# ADR-018 — Scope-hierarki

**Status:** Accepteret

**Beslutning:** `MUNICIPALITY ⊃ AREA ⊃ STREET ⊃ ADDRESS`. Match sker på det mest specifikke scope, køberen har valgt. Uden `address_id` kan gade/kommune-match stadig virke; **M1 (ejer-kontakt) kræver eksakt adresse**.

**Konsekvenser:** Købere kan udtrykke intention, som de faktisk tænker ("jeg vil bo i Gentofte"). Tæthed måles pr. `area_id`, men match kan være bredere. Dedup-index udvides til `(household_key, scope, scope_id)`.

**Verifikation:** `test_street_scope_not_zip_wide`, `test_municipality_hierarchy`, `test_m1_requires_exact_address`.
