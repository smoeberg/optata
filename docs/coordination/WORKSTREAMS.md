# Workstreams and Agent Ownership

**Status:** Initial assignment model · 17 November 2026  
**Assignments:** Product owner assigns the actual agent instance to each role and Issue.

## Agent 1 — Core & Data

**Primary responsibility**
- Domain entities and invariants.
- PostgreSQL schema, migrations, constraints and indexes.
- Event model, persistence and projections.
- Backend foundations and data ingestion.
- Database permissions and security-sensitive implementation (with mandatory independent review).

**Typical owned areas**
- `app/db/`, `app/domain/`, `migrations/`, `contracts/events/`, and narrowly assigned backend modules.

**Must coordinate with**
- Agent 2 before changing API-visible behavior, commands, event payloads or lifecycle states.
- Agent 3 before changing guards, tests, security controls or shared contracts.

## Agent 2 — Product & API

**Primary responsibility**
- Buyer/seller journeys and product workflows.
- API endpoints, request/response contracts and integration adapters.
- User-visible states, validation, errors and recovery behavior.
- Product acceptance criteria translated into testable behavior.

**Typical owned areas**
- `app/api/`, `app/services/`, API schemas and product workflow modules, only as assigned.

**Must coordinate with**
- Agent 1 before changing persistence, event shape, aggregate identity or lifecycle transitions.
- Agent 3 before changing contracts, test fixtures or acceptance behavior.

## Agent 3 — Quality & Architecture

**Primary responsibility**
- Continuous integration awareness and regression analysis.
- Independent review of work from Agents 1 and 2.
- Contract consistency across code, OpenAPI, events, ADRs and tests.
- Negative tests, boundary tests, security review preparation and release evidence.
- Identify integration conflicts early; maintain dependency visibility.

**Typical owned areas**
- Tests, quality tooling and architecture/coordination documentation, only as assigned.

**Independence rule**
Agent 3 should not be the sole author and approver of the same security-critical implementation. For sensitive changes, a human reviewer remains required.

## Ownership is explicit per Issue

The role above does not grant blanket write access to every path in a workstream. Each Issue MUST include an explicit allowed-file list or module boundary. If the task crosses boundaries, split it or name the coordinated changes and reviewers before coding.

## Parallelism policy

Safe parallel work is work with separate files and stable interfaces. Work that shares a migration, event schema, API contract, state machine, permission model or product decision is sequential or contract-first.

Do not maximize the number of simultaneous tasks. Maximize independently mergeable work with clear integration points.
