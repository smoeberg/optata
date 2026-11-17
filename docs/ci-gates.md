# CI gates

The twelve gates from bilag 09 and what each one actually checks today. A gate
listed as "not built" does not protect anything yet.

Run everything locally with `make ci`. The same steps run in
`.github/workflows/ci.yml` on every pull request.

| # | Gate | Status | What runs |
|---|---|---|---|
| 1 | Contract first | Partial | `tests/contract/`: every route in the app exists in `contracts/openapi.yaml`; events validate against `contracts/events/` |
| 2 | Lint and module boundaries | Built | `ruff check .` and `lint-imports`. No type checker yet |
| 3 | Unit and contract tests | Built | `pytest` |
| 4 | Guard tests | Built, draft | `tests/guards/`. Written by an AI assistant; needs human review before they count |
| 5 | Zone leakage | Partial | Response schemas must set `additionalProperties: false`. No scan of live payloads yet |
| 6 | k-anonymity | Not built | Zone C does not exist yet (S8) |
| 7 | SAST and secrets scan | Not built | |
| 8 | Dependency and licence scan | Not built | |
| 9 | Migration test | Partial | Migrations run from scratch in every test session. No check for destructive changes |
| 10 | Synthetic data check | Built, draft | `tests/guards/test_no_prod_like_data.py` |
| 11 | Human review | Needs GitHub setting | `CODEOWNERS` exists. Branch protection on `main` must be switched on |
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

Each of these was checked once by breaking the rule on purpose and confirming
the guard failed.
