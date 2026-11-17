# Optata — Agent Coordination

**Status:** Initial coordination protocol · 17 November 2026  
**Applies to:** All AI agents and human contributors working in this repository  
**Owner:** Product owner (human)

This directory is the durable coordination layer for parallel development. It does not replace the product baseline, architecture, ADRs, GitHub Issues, pull requests, CI, or human review.

## Start here — mandatory for every agent

Before doing any work:

1. Read this file and [AGENT-PROTOCOL.md](AGENT-PROTOCOL.md).
2. Read [PROJECT-STATE.md](PROJECT-STATE.md), [WORKSTREAMS.md](WORKSTREAMS.md), [DEPENDENCIES.md](DEPENDENCIES.md), and [DECISION-QUEUE.md](DECISION-QUEUE.md).
3. Inspect current GitHub Issues and open PRs, including comments and CI state. Do not rely on a previous chat or an old local checkout.
4. Identify the assigned issue, branch, file ownership, dependencies, and acceptance criteria.
5. Post a short **start-of-work sync** on the issue before editing.

Before each commit, after a meaningful change, and before handoff:

- Re-check the issue and relevant PRs for changes from other agents.
- Report changed files, contract/API/schema implications, tests, blockers, and next steps.
- Update the issue and the coordination documents when shared project state or dependencies change.

## Sources of truth

| Information | Canonical location |
|---|---|
| Product scope and approved product decisions | [Projectgrundlag v5.2](../Optata%20-%20Projektgrundlag%20v5.2.md) and accepted ADRs |
| Technical architecture and invariants | [ARCHITECTURE.md](../architecture/ARCHITECTURE.md), accepted ADRs and approved contracts |
| Proposed/unapproved design | Its own document, explicitly marked Proposed |
| Task ownership, status, discussion and handoff | GitHub Issue |
| Actual code change and review | Pull request and its commits |
| Quality evidence | CI run plus reproducible local test output |
| Cross-agent current snapshot | [PROJECT-STATE.md](PROJECT-STATE.md) and the registers in this directory |
| Unresolved decisions | [DECISION-QUEUE.md](DECISION-QUEUE.md) and linked Issues |

If sources conflict, do not silently choose one. Stop the affected work, record the conflict in the Issue and decision queue, and ask the product owner.

## Three-agent operating model

- **Agent 1 — Core & Data:** domain model, database, migrations, events, persistence, security-sensitive backend foundations.
- **Agent 2 — Product & API:** end-to-end journeys, application workflows, API contracts, integrations and user-facing behavior.
- **Agent 3 — Quality & Architecture:** independent review, tests, contract consistency, security/regression analysis and integration readiness.

Roles describe primary responsibility, not exclusive expertise. The product owner assigns actual agents and issues. Agent 3 participates continuously; it is not only a final test step.

## Git model

- `main` is the approved baseline.
- Each task gets its own branch from the latest `main`, unless the issue explicitly names another base.
- Pull requests target `main` and remain draft until implementation and self-checks are complete.
- Dependent work may proceed against an explicitly documented proposed contract, but must not be merged or represented as complete until its dependency is accepted.
- No agent merges to `main`, changes repository settings, or closes another agent's task without explicit human authorization.
- Avoid a permanent `develop` branch for now: the repository is small and its current work already uses PRs from task branches. Revisit only if integration volume makes it necessary.

## Important limitation: GitHub is shared, agent context is not

A GitHub Issue or commit does not automatically appear in another agent's active context. Agents must actively re-read Issues, PRs and this directory at the sync checkpoints. Notifications or polling can improve awareness, but this protocol does not claim instantaneous awareness.

## Required task records

Every implementation task must have a GitHub Issue with:
- objective and out-of-scope items;
- one accountable agent;
- branch and allowed file/module scope;
- dependencies and contracts touched;
- acceptance criteria and required tests;
- latest sync, blockers and handoff.

Use the repository's issue and PR templates. A task without a clear owner, scope and acceptance criteria is not ready for implementation.
