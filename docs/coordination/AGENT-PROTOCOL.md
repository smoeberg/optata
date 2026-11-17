# Agent Protocol

**Status:** Mandatory working agreement · 17 November 2026

## 1. Before starting

Every agent MUST:

1. Read `docs/coordination/README.md` and all current coordination registers.
2. Fetch the latest `main`; do not assume the branch or commit in a prior session is current.
3. Review open Issues and PRs, including recent comments, changed files, review state and CI.
4. Read the authoritative documents relevant to the assigned task.
5. Confirm the assigned Issue, owner, allowed files, dependencies and acceptance criteria.
6. Comment on the Issue using the start-of-work format below.

**Start-of-work comment**

```text
SYNC — START
Agent:
Issue:
Base commit:
Branch:
Scope / allowed files:
Dependencies checked:
Relevant PRs checked:
Expected output:
Risks or conflicts:
```

## 2. While working

- Keep one accountable agent per Issue. Other agents may review or advise, but do not silently co-own edits.
- Do not edit outside the assigned scope. If scope must expand, explain why and get approval in the Issue first.
- Do not edit a file currently owned by another active task without coordination in the affected Issues.
- Before changing an API, event, schema, migration, shared enum, permission boundary or state machine, identify every consumer and update the relevant contract/tests.
- Treat migrations, RLS, grants, identity/session logic, audit, privacy boundaries, financial logic and legal gates as high-risk. Require independent human review where the repository documents it. AI review is not a substitute.
- Never invent that a test, CI job, review or external integration passed. State what actually ran and what did not.
- Use synthetic data unless the approved product/security/legal gates explicitly permit otherwise.
- Do not weaken, delete or bypass a test/guard to make a PR green without a documented root cause and human approval.
- If another agent's change affects your task, pause the conflicting part and coordinate in the Issues. Do not resolve conflicts by overwriting their branch.

## 3. Sync checkpoints

An agent MUST sync with GitHub:
- before starting;
- before its first edit to a shared contract or migration;
- before every commit that changes shared behavior;
- after each meaningful commit;
- when a blocker or cross-workstream dependency appears;
- before opening/updating a PR;
- before stopping or handing off.

A sync means checking the latest Issue and relevant PR comments/status, not merely posting a comment.

**Progress comment**

```text
SYNC — UPDATE
Commit:
Files changed:
Behavior / contract impact:
Tests run (exact command + result):
Tests not run:
Dependencies changed:
Other agents affected:
Blockers / decisions needed:
Next step:
```

## 4. Pull request rules

Every PR MUST state:
- linked Issue (`Closes #...` only if the PR fully completes it);
- what changed and why;
- files/modules touched;
- contract, migration, data, security and privacy implications;
- exact tests run and results;
- known limitations and follow-up work;
- dependency PRs and whether they are merged.

A PR is not ready merely because code is written. It must have:
1. self-review and scope check;
2. relevant tests and lint;
3. CI green (or explicit documented reason why a required check is unavailable);
4. independent review for cross-cutting/high-risk changes;
5. human approval before merge.

Agents MUST NOT merge PRs to `main`.

## 5. Handoff

Use [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md) in the Issue before stopping. A handoff must let another agent continue without reconstructing hidden chat context.

## 6. Conflict and stop-work rule

Stop the affected work and notify the product owner when:
- two tasks claim the same files or migration sequence;
- implementation requires an unapproved product or legal decision;
- the normative baseline conflicts with a proposed document;
- a security boundary or privacy assumption is unclear;
- a dependency changed after work began;
- a test failure may be pre-existing or caused by another branch and cannot be isolated.

Do not guess, silently redefine scope, or merge around the conflict.
