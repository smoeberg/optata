# CI gates

The twelve gates from bilag 09 and what each one actually checks today. A gate
listed as "not built" does not protect anything yet.

Run everything locally with `make ci`. The same steps run in
`.github/workflows/ci.yml` on every pull request.

| # | Gate | Status | What runs |
|---|---|---|---|
| 1 | Contract first | Built for what exists | `tests/contract/`: routes and contract paths must match both ways; every response body is validated against its schema; events validate against `contracts/events/` |
| 2 | Lint and module boundaries | Built | `ruff check .` and `lint-imports`. No type checker yet |
| 3 | Unit and contract tests | Built | `pytest` |
| 4 | Guard tests | Built, draft | `tests/guards/`. Written by an AI assistant; needs human review before they count |
| 5 | Zone leakage | Built for the public API | Schemas must be closed at every depth, live responses are validated against them, and public requests run as `public_reader`, which cannot read zone B. No scan of rendered reports yet |
| 6 | k-anonymity | Not built | Zone C does not exist yet (S8) |
| 7 | SAST and secrets scan | Not built | |
| 8 | Dependency and licence scan | Not built | |
| 9 | Migration test | Partial | Migrations run from scratch in every test session. No check for destructive changes |
| 10 | Synthetic data check | Built, draft | `tests/guards/test_no_prod_like_data.py` |
| 11 | Human review | Not enforceable yet | `CODEOWNERS` exists. Branch protection on a private repository needs GitHub Pro or Team; until then a red run does not block a merge |
| 12 | End-to-end case flows | Not built | No flows exist yet |

## Database tests in CI

Tests that need Postgres are skipped locally when no database is reachable.
In CI (`CI=true`) a missing database fails the run. A guard that did not run
has not passed.

## What the guards cover today

| Guard | Invariant | File |
|---|---|---|
| Order events and audit log are append-only | 3 | `test_event_append_only.py` |
| Only `disclosure_service` reads the vault | 4 | `test_zone_separation.py` |
| Anonymous traffic cannot reach zone B | ADR-004 | `test_zone_separation.py` |
| A buyer sees only their own orders | ADR-004 | `test_zone_separation.py` |
| One active order per household and scope | 9 | `test_order_one_per_household.py` |
| Fixtures contain no real personal data | ADR-012 | `test_no_prod_like_data.py` |
| Register history is never overwritten | 2 | `test_property_history.py` |
| Property events are append-only | 3 | `test_property_history.py` |
| Raw density is not readable by application roles | 8 | `tests/unit/test_density.py` |

These were checked by breaking the rule on purpose in the migration and
confirming the tests failed: vault access, append-only order events, row level
security, the history trigger on `zone_a.property`, the one-open-version index,
distinct counting of households, address orders leaking to street level, and
read access to raw density.

Not checked that way: the household index on orders and the anonymous-access
guard. The data guard carries its own self-test of the detectors.
