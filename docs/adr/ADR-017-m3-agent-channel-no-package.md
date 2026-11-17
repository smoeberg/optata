# ADR-017 — M3: køber→mægler, ingen salgspakke

**Status:** Accepteret · **Juridisk afklaring:** L34–L35

> **Status-opdatering (markedsambitionen, struktur C):** M3 som
> invitation/lead-kanal er **forkastet** — køberen får ikke mæglerens
> kontakt, køberen afgiver bud i Optata (OfferLedger). Se invariant 16 i
> `docs/architecture/ARCHITECTURE.md` og
> `docs/design/Optata - Efterspoergselsgravitation - struktur C v1.md`.
> Ikke-salgspakke-princippet gælder uændret.

**Kontekst:** Når en bolig allerede er til salg hos en mægler, er mægleren godkendt formidler. At tilbyde vores egen fulfillment-pakke ville være dobbelt formidling og dobbelt betaling.

**Beslutning:**
1. M3 matcher **udbud → ordre** og notificerer **køberen**.
2. Kontakt kræver **VERIFIED** køber; mægler skal **CVR-matche** udbuddets `agent_org` (MitID Erhverv).
3. **Gratis at svare** på den enkelte henvendelse — det er acquisition. Abonnement sælges bagefter.
4. **Ingen salgspakke, intet pakkegebyr** i M3. Indtægt = abonnement/lead.
5. Reveal i M3 har **4 guards** (gensidigt samtykke ∧ frisk step-up ∧ gyldig attest ∧ CVR-match) — ingen betalingsguard. Samme vault-indgang, samme audit, `channel=AGENT`.
6. Invitationer aggregeres pr. bolig (1 pr. 14 dage), suppression på mægler-org.

**Konsekvenser:** Renere formidlingsposition (L34 bliver lettere). Ny acquisition-kanal: hver invitation er en potentiel abonnent og en potentiel feed-leverandør. Reveal-protokollen får to dokumenterede varianter.

**Fravalgt:** Pakke i M3 (dobbelt formidling), betalt svar (dræber acquisition), direkte kontaktudlevering (bryder anonymitet).

**Verifikation:** `test_no_package_in_m3`, `test_m3_reveal_four_guards`, `test_agent_cvr_match_required`, `test_verified_gate_on_invitation`.
