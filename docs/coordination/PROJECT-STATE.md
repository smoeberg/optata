# Optata — Shared Project State

**Snapshot date:** 17 November 2026  
**Snapshot branch:** `main`  
**Snapshot commit:** `7a8f52ab5f01b652beceb9e40a611ec0f3f97f27`  
**Maintainer:** Product owner (human)

> This is a coordination snapshot, not a replacement for the normative documents. Update it when a material project state changes. Always verify GitHub before acting; this file can become stale.

## Current baseline

- Product baseline: `docs/Optata - Projektgrundlag v5.2.md`.
- Architecture baseline: `docs/architecture/ARCHITECTURE.md` (v2.1).
- ADRs: only Accepted ADRs are normative. Proposed ADRs and proposed contracts are not approved implementation authority.
- Architecture Contracts v1.0: **Proposed**, not approved or implemented as a whole.
- Product Closure and Development Readiness v1.0: audit/recommendations, not an approved product baseline.
- Synthetic data remains the default. Real personal data and production transaction flows remain gated by the relevant legal, privacy, security and human-review requirements.

## Repository and current activity

- Default branch: `main`.
- The repository is public and has Issues and PRs enabled.
- At this snapshot, open draft PR [#17 — three-company operating model](https://github.com/smoeberg/optata/pull/17) targets `main`. It must be reviewed and explicitly decided by the product owner; it is not merged or normative yet.
- Existing non-main branches at snapshot: `docs/product-closure-gap-analysis`, `docs/service-responsibility-architecture-v1`, `docs/three-company-model-alignment`. Check their current PR/Issue links and heads before using or deleting them.
- This coordination foundation is being introduced on its own branch and must be merged through a human-reviewed PR.

## Product / engineering readiness

The repository already contains a useful technical foundation: FastAPI application, public area/property APIs, Zone A registry and bitemporal history, ingestion adapter/runner foundations, synthetic fixtures, event envelope/schema validation, OpenAPI contract tests, unit/guard tests and CI.

This does **not** mean the full Optata product is implemented. Major product capabilities remain incomplete, including verified identity/session, buyer order lifecycle, SaleMandate, OfferLedger, campaign consent and execution, production listing ingestion, partner access controls, Zone C publication/anonymization, full buyer/seller journeys, post-acceptance fulfillment, reporting/front end, payments/billing and production operations.

The detailed gap analysis is [PRODUCT-CLOSURE-AND-DEVELOPMENT-READINESS-v1.0.md](../product/PRODUCT-CLOSURE-AND-DEVELOPMENT-READINESS-v1.0.md). Its own status is audit/recommendation, not approved baseline.

## Quality and release posture

See [CI gates](../ci-gates.md). The documented state is mixed: core lint/tests/contracts exist, while several planned controls are not built or only partial/draft (including SAST/secrets, dependency/license scanning, migration safety, enforceable human review, k-anonymity and end-to-end case flows).

A green CI run only proves the checks that actually ran. It does not close missing gates, legal questions, independent security review or production readiness.

## Coordination rules

- No agent begins implementation without a GitHub Issue and a named accountable agent.
- No agent assumes another agent has seen a branch, commit or chat message.
- No agent treats Proposed documents as approved contracts.
- Cross-workstream changes require an Issue comment and updated dependency register.
- Product owner controls prioritization, decisions and merges to `main`.

## Update log

| Date | Change |
|---|---|
| 2026-11-17 | Initial coordination snapshot based on main commit `7a8f52a`; PR #17 recorded as open draft. |
