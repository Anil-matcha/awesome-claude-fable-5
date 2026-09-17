# Claude Fable 5 Coding Agent Use Cases

Use Claude Fable 5 when the coding task benefits from long-context review, high-level planning, or hard-to-reproduce debugging. Route routine implementation and cheap iteration to lower-cost models when the plan is already stable.

## Best-fit workflows

| Workflow | Why Fable 5 fits | Suggested output |
|---|---|---|
| Architecture review | It can compare cross-module tradeoffs before code is written. | Decision-complete implementation plan |
| Large PR review | It can hold more context and focus on correctness risks. | Findings ordered by severity |
| Agent relay planning | It can define handoff boundaries for cheaper execution models. | Task graph plus acceptance criteria |
| Debugging triage | It can reason from logs, diffs, traces, and reproduction notes together. | Root-cause hypothesis and verification checklist |
| Migration planning | It can map compatibility, rollout, and test coverage before edits. | Stepwise migration plan |

## First prompt template

```text
You are reviewing a production codebase change.

Goal:
<what needs to ship>

Context:
<repo/module summary, constraints, interfaces, and known risks>

Artifacts:
<paste relevant diffs, logs, stack traces, or design notes>

Output:
1. Findings that could break production, ordered by severity.
2. The smallest implementation plan that resolves them.
3. Tests that prove the change works.
4. Any assumptions that must be verified before shipping.
```

## Conversion path

- Model page: https://muapi.ai/playground/claude-fable-5
- API key: https://muapi.ai
- Python example: ../api-examples/python/messages.py
- Node.js example: ../api-examples/node/messages.mjs
