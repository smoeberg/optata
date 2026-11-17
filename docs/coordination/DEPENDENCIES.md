# Cross-Agent Dependency Register

**Status:** Initial register · 17 November 2026

Keep this file short and current. The GitHub Issue remains the detailed task record. Every dependency row must link to its Issue/PR once created.

## Dependency rules

- A dependency is **blocking** if a task cannot be safely completed or merged until another task is accepted.
- A dependency is **soft** if work can proceed against a documented assumption but integration must wait.
- No agent may silently change a shared contract to unblock itself.
- When a dependency changes, update both linked Issues and this register.

## Initial dependency map

| Producer | Contract / output | Consumer | Dependency | Status |
|---|---|---|---|---|
| Product owner + Agent 2 | Approved end-to-end product scope and acceptance journeys | Agents 1, 2, 3 | Blocking for full product workflow implementation | Open |
| Agent 1 | Approved domain aggregates, state transitions, event schemas and persistence rules | Agent 2 | Blocking for integrated API/workflow implementation | Not yet assigned |
| Agent 2 | API/OpenAPI contracts and user-visible workflow behavior | Agent 1 and Agent 3 | Soft during contract-first design; blocking for final integration | Not yet assigned |
| Agent 3 | Contract tests, negative tests, regression evidence and review findings | Agents 1 and 2 | Required before PR readiness where relevant | Continuous |
| Product owner + human reviewer | Legal/privacy/security decisions and acceptance of high-risk design | All agents | Blocking wherever a release gate applies | Open |

## Active conflict watch

- PR #17 changes product/company-model documentation. Do not independently edit the same normative documents until PR #17 is reviewed or its ownership/scope is explicitly coordinated.
- Proposed ADRs and Architecture Contracts are not approved merely because related code exists or a PR has merged.
- Database migrations and shared event/API schemas are single-owner at a time. Reserve the migration/schema scope in the Issue before work starts.

## Task dependency entry template

| Issue | Depends on | Produces | Consumers | Blocking / soft | State | Last checked |
|---|---|---|---|---|---|---|
| # | # | Contract/file | # | Blocking | Open | YYYY-MM-DD |
