> **HISTORISK / SUPERSEDED:** Dette dokument beskriver den tidligere M3-invitations- og leadmodel. M3 som køber→mægler-invitation/reveal er forkastet. Brug S6-backloggen, arkitektur v2.1 og projektgrundlag v5.2. Dokumentet bevares kun som beslutningshistorik.

# M3-opdatering — events, sprint-renummerering og nye guards

Del af M3-opdateringen (udbudsmatch). Arkitektur-deltaet er indarbejdet i
`docs/architecture/ARCHITECTURE.md` (v1.1) og ADR-016–018 i `docs/adr/`.
Dette er de resterende dele: nye events, sprint-renummerering og listen over
nye guard-tests.

## Nye events

| Event | Zone | Payload |
|---|---|---|
| `listing.imported` | A | source, source_ref, area_id, license_ref, resolution_confidence |
| `listing.price_changed` | A | source_ref, old_band, new_band, changed_at |
| `listing.status_changed` | A | source_ref, from, to |
| `listing.matched` | B | order_pseudonym, listing_id, score, reason_codes[] |
| `agent.invited` | B | agent_org_cvr, listing_id, aggregated_count, legal_basis_ref |
| `agent.onboarded` | B | cvr, source=INVITATION, listing_id |
| `identity.revealed` | B | **+ channel: OWNER \| AGENT**, guards_variant |

## Sprint-renummerering

| Før | Nu | Indhold |
|---|---|---|
| S6 | **S6** | **Udbudsmatch (M3): listing-model, feed-adapter, invitation** |
| — | **S7** | Mægler-abonnement, eksklusivitet, lead-liste (var S6) |
| S7 | **S8** | Withdraw/expire/afmeld/slet |
| S8 | **S9** | Insights zone C, Demand Pro |

**Begrundelse:** M3 skal før abonnementet — det er M3, der *skaber* mæglerrelationen og feed-leverancen. Abonnementet sælges til en mægler, der allerede har oplevet værdien.

## Nye guards i `tests/guards/`

```
test_no_license_no_import.py
test_attribution_present.py
test_sold_removes_match.py
test_stale_not_sold.py
test_verified_gate_on_invitation.py
test_agent_cvr_match_required.py
test_no_package_in_m3.py
test_m3_reveal_four_guards.py
test_street_scope_not_zip_wide.py
test_m1_requires_exact_address.py
test_invitation_aggregation_and_suppression.py
```
