# Jev for coding agents and agent harnesses

Jev is not a coding agent and does not generate patches. It can make the small,
high-frequency judgments around an agent that are useful for routing, safety,
retrieval, and verification.

Pair it with a coding model that can inspect and edit a repository. Use Jev as
the typed decision layer; keep file access, command authorization, approvals,
and the final diff review in the harness.

## Best-fit workflows

| Workflow | Jev’s role | Suggested output |
|---|---|---|
| Skill selection | Decide whether a turn needs a skill and which one | Closed-set skill choice + confidence |
| Tool routing | Select a safe tool family or deterministic handler | Function name / route choice |
| Command risk | Detect destructive or credential-sensitive intent | Noul probabilities + severity score |
| Retrieval filtering | Rank repository files, docs, or memories against a task | Relevance scores and review flags |
| Patch verification | Check whether a diff touches risky areas or violates a policy | Score, violations, and a human-review branch |
| CI semantic linting | Evaluate team-specific conventions | One Noul per convention |
| Model cascade | Decide whether a task needs a larger reasoning model | Difficulty/risk score + route |

## The harness boundary

```text
user turn ──► Jev: route / risk / retrieval / verify ──► code policy
                                                        │
                       ┌────────────────────────────────┼──────────────┐
                       ▼                                ▼              ▼
                 deterministic tool                coding model       human
```

Jev should not be the component that grants a capability. A high-confidence
answer may allow the harness to present an option, but the harness still checks
the user, repository, path, command, network policy, and approval state.

## 1. Skill and tool selection

### State

```python
state = {
    "user_request": "Review the payments migration and suggest tests.",
    "available_skills": [
        {"name": "repository-review", "description": "Inspect code and report file-backed findings."},
        {"name": "database-migrations", "description": "Review schema changes and migration safety."},
        {"name": "browser-qa", "description": "Run a bounded UI flow in a disposable environment."},
    ],
    "repository": {"language": "TypeScript", "changed_files": ["db/migrations/0042.sql"]},
}
```

### Questions

```python
from typesafe_sdk import Choice, Noul, Score

questions = {
    "needs_skill": Noul(
        instructions="Does `user_request` require one of the listed skills rather than a short direct answer?",
    ),
    "skill": Choice(
        instructions="Which available skill best matches `user_request` and the repository context?",
        criteria={
            "repository-review": "Inspect code and report file-backed findings.",
            "database-migrations": "Review schema changes and migration safety.",
            "browser-qa": "Run a bounded UI flow in a disposable environment.",
            "none": "No listed skill is a clear fit.",
        },
    ),
    "risk": Score(
        instructions="How risky would it be for an agent to make changes for `user_request`?",
        criteria=[
            "Read-only or easily reversible",
            "Changes application behavior but is testable",
            "Touches credentials, production data, permissions, or irreversible side effects",
        ],
    ),
}
```

### Code-owned policy

```python
def choose_agent_path(response) -> str:
    if response.answers["needs_skill"].noul < 0.5:
        return "direct_answer"

    skill = response.answers["skill"]
    if skill.choice == "none" or skill.confidence < 0.65:
        return "ask_for_clarification"

    if response.answers["risk"].score >= 1.5:
        return f"skill_with_approval:{skill.choice}"
    return f"skill:{skill.choice}"
```

If the selected skill changes the state or the available choices, make a second
Jev call after the harness loads that skill. Otherwise, ask all relevant
questions in one request and let code ignore unused answers.

Source: [Agent skill](https://docs.typesafe.ai/agent-skill),
[skill suggestion cookbook](https://docs.typesafe.ai/cookbooks/skill_suggestion),
and [speculative fan-out](https://docs.typesafe.ai/patterns/fan-out).

## 2. Command and tool-call safety

Before an agent executes a command or tool call, evaluate the proposed action
and its context. This is a semantic signal for policy code, not a replacement
for an allowlist or sandbox.

```python
questions = {
    "is_destructive": Noul(
        instructions="Does `proposed_call` delete, overwrite, publish, send, purchase, or otherwise create an irreversible side effect?",
    ),
    "touches_credentials": Noul(
        instructions="Does `proposed_call` read, enter, print, or transmit a credential, token, or secret?",
    ),
    "scope_matches": Noul(
        instructions="Is `proposed_call` limited to the repository, account, and files authorized in `policy`?",
    ),
    "impact": Score(
        instructions="How serious would the consequence be if `proposed_call` were wrong?",
        criteria=["Low and reversible", "Material but recoverable", "High impact or difficult to reverse"],
    ),
}
```

Example policy:

```python
def authorize_tool(response) -> str:
    destructive = response.answers["is_destructive"].noul
    credentials = response.answers["touches_credentials"].noul
    scope = response.answers["scope_matches"].noul
    impact = response.answers["impact"].score

    if credentials >= 0.30 or scope < 0.80:
        return "block"
    if destructive >= 0.70 or impact >= 1.5:
        return "require_human_approval"
    return "allow_only_after_deterministic_validation"
```

The harness must still parse the tool call, resolve paths, enforce a sandbox,
and keep a kill switch. Never allow a model-generated string to expand the
authorization boundary by itself.

## 3. Repository retrieval and context selection

Use a fast file search to build a shortlist, then use Jev to score whether each
file or excerpt is useful for the current task. Add questions for stale API,
security-sensitive code, and test coverage when those signals affect the
downstream coding model.

```python
state = {
    "task": "Add idempotency to the Stripe webhook handler.",
    "candidate_file": {
        "path": "src/webhooks/stripe.ts",
        "excerpt": "export async function handleStripeEvent(event) { ... }",
    },
}

questions = {
    "relevant": Noul(instructions="Does `candidate_file.excerpt` contain implementation details needed for `task`?"),
    "security_sensitive": Noul(instructions="Does `candidate_file.excerpt` handle authentication, payments, secrets, or authorization?"),
    "test_relevant": Noul(instructions="Would a test for `task` likely need to inspect or change this file?"),
    "context_value": Score(
        instructions="How valuable is `candidate_file` as context for the coding model?",
        criteria=["Not useful", "Possibly useful", "Directly useful"],
    ),
}
```

Include the top passages that clear the relevance threshold. Always preserve
file paths and line numbers in the handoff so the coding model can verify the
context against the repository instead of treating retrieved text as truth.

Source: [Re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe) and
[classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages).

## 4. Diff verification and semantic CI

After an agent proposes a patch, use Jev to classify the diff against explicit
team conventions. Keep compiler, test, security, and dependency checks as
deterministic CI steps.

```python
questions = {
    "has_unreviewed_auth_change": Noul(
        instructions="Does `diff` change authentication, authorization, or permission behavior without an explicit test or review note?",
    ),
    "violates_api_boundary": Noul(
        instructions="Does `diff` bypass the repository's documented API or service boundary?",
    ),
    "missing_regression_test": Noul(
        instructions="Does `diff` change behavior without adding or updating a relevant regression test?",
    ),
    "review_risk": Score(
        instructions="How much review attention does this diff require?",
        criteria=["Routine", "Focused review", "Senior or security review"],
    ),
}
```

A safe CI policy might annotate a pull request for routine issues, require a
reviewer for the middle band, and block merge for a high-confidence policy
violation. Do not use one Jev score as a substitute for tests or code review.

Source: [Semantic code linting](https://docs.typesafe.ai/concepts/use-case-map).

## 5. Model cascade for coding work

Jev can classify difficulty, risk, and need for current repository context. The
harness can then choose a small model, a larger reasoning model, or a human.

```python
questions = {
    "task_kind": Choice(
        instructions="What kind of coding task is this?",
        criteria={
            "formatting": "Mechanical formatting or a trivial rename.",
            "localized_fix": "A bounded change with a clear local test.",
            "cross_cutting": "A change spanning modules, interfaces, or data contracts.",
            "security_or_data": "A security, privacy, migration, or production-data change.",
            "other": "None of the categories clearly fits.",
        },
    ),
    "reasoning_depth": Score(
        instructions="How much architectural reasoning and verification does this task need?",
        criteria=["Shallow", "Moderate", "Deep"],
    ),
}
```

The output should select a workflow, not a model name embedded in a prompt:

```python
def choose_execution_mode(response) -> str:
    kind = response.answers["task_kind"]
    depth = response.answers["reasoning_depth"]
    if kind.confidence < 0.6 or depth.confidence < 0.6:
        return "human_scoping"
    if kind.choice == "security_or_data" or depth.score >= 1.5:
        return "large_reasoning_model_with_review"
    if kind.choice == "formatting":
        return "deterministic_tool"
    return "bounded_coding_model"
```

Use your own rework, latency, and defect data to tune this cascade. The point
is to make routing explicit and observable.

## 6. Agent output and citation checks

If a coding agent reports that a file, API, test, or documentation page supports
its conclusion, compare the claim with the cited excerpt. A `Choice` such as
`supports`, `insufficient`, `contradicts`, and `unrelated` gives the harness a
branchable result.

This is especially useful for repository review reports and generated release
notes. Keep the original evidence in the report; Jev’s result should identify a
review path, not erase uncertainty.

Source: [Double-checking citations](https://docs.typesafe.ai/cookbooks/citation_check).

## Prompting a coding agent around Jev

Give the coding model an explicit contract for the decisions it receives:

```text
You are the implementation model inside a reviewed software workflow.

The harness has already supplied typed routing and risk signals. Treat them as
inputs, not authorization. Inspect the repository and all applicable instruction
files before editing. Keep the change bounded to the approved scope. Run the
focused tests and report file-backed evidence. Stop before an irreversible
external side effect or a permission change.
```

Jev can improve routing and verification, but it does not remove the need for
repository inspection, tests, approvals, or human judgement.

## Evaluation checklist

- Freeze representative turns, repository states, diffs, and tool calls.
- Track the versioned model returned by the API, not only `jev-latest`.
- Measure false allows, false blocks, unnecessary escalations, latency, and cost.
- Include out-of-domain, ambiguous, adversarial, and missing-context cases.
- Test the policy code independently with simulated Jev answers.
- Require a human for high-impact, destructive, credential-sensitive, or
  permission-changing actions.
- Re-evaluate thresholds when question criteria, state shape, policy, or model
  version changes.

## Related reading

- [Awesome GPT-6 Astra](https://github.com/Anil-matcha/awesome-gpt-6-astra) — a sibling collection for a general-purpose reasoning model.
- [Awesome Agent APIs](https://github.com/Anil-matcha/awesome-agent-apis) — a catalog of APIs and tools an agent may route to.
- [Open Business Agents](https://github.com/Anil-matcha/open-business-agents) — a catalog of specialized agents for business workflows.
- [LLM Wiki Agent](https://github.com/SamurAIGPT/llm-wiki-agent) — a persistent, interlinked knowledge workflow that can benefit from typed retrieval and verification.
