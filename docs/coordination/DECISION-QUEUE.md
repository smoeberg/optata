# Decision Queue

**Status:** Initial queue · 17 November 2026  
**Decision owner:** Product owner (human)

This is a register of decisions that affect multiple workstreams. A proposal is not a decision until the product owner explicitly accepts it and the relevant normative document/ADR is updated.

| ID | Decision needed | Current evidence / source | Owner | Blocks | Status |
|---|---|---|---|---|---|
| DQ-001 | Review and decide PR #17: three-company operating model alignment | [PR #17](https://github.com/smoeberg/optata/pull/17) is open draft; its body explicitly lists unresolved legal/privacy/commercial questions | Product owner | Company boundaries, services, roles, future contracts | Pending human review |
| DQ-002 | Confirm which product-closure recommendations become approved product scope | [Product closure audit](../product/PRODUCT-CLOSURE-AND-DEVELOPMENT-READINESS-v1.0.md) is not normative | Product owner | End-to-end product backlog and sequencing | Open |
| DQ-003 | Review and accept/reject Architecture Contracts v1.0 and its individual contracts | [Architecture Contracts v1.0](../architecture/ARCHITECTURE-CONTRACTS-v1.0.md) is Proposed | Product owner + independent technical reviewer | Cross-cutting implementation and security gates | Open |
| DQ-004 | Decide first development increment and explicitly bound its scope | S0/S1 backlog, CI gates and product readiness audit | Product owner | Assignment of the three agents | Open |
| DQ-005 | Determine whether to introduce a shared integration branch or GitHub Project automation | Current repository has a small set of task branches and PR-based flow | Product owner | Workflow tooling only | Deferred; start with Issues + PRs |

## Decision record format

For each decision, add:
- decision ID and date;
- exact question;
- options considered;
- decision and rationale;
- affected product/architecture/ADR/backlog documents;
- consequences and follow-up Issues;
- human decision owner.

Do not change Proposed to Accepted based on agent consensus alone.
