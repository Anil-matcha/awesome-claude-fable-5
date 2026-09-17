<div align="center">

<a href="https://docs.typesafe.ai/introduction"><img src="images/banner.svg" alt="Awesome Jev by TypeSafe: typed decisions for software" width="760"></a>

[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)
[![Jev](https://img.shields.io/badge/TypeSafe-Jev-0d9488)](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
[![API docs](https://img.shields.io/badge/API-Docs-0f766e)](https://docs.typesafe.ai/api)
[![Python SDK](https://img.shields.io/badge/Python-SDK-3776ab)](https://github.com/typesafe-ai/typesafe-sdk-python)
[![JavaScript SDK](https://img.shields.io/badge/JavaScript-SDK-f7df1e?logo=javascript&logoColor=111827)](https://github.com/typesafe-ai/typesafe-sdk-js)

</div>

# Awesome Jev by TypeSafe

An evidence-backed, practical collection of use cases, patterns, prompts, and starter code for **Jev**, TypeSafe AI’s first **System One Model**.

Jev is built for software that needs a judgment, not a paragraph:

```text
text or JSON state + typed questions → constrained answers + probabilities → your code
```

Use it to classify, route, score, detect, rank, extract, verify, and gate automation. Keep the final control flow, thresholds, and side effects in code.

> This is an independent community collection. It is not an official TypeSafe AI repository. Product behavior, prices, limits, and model aliases can change.
>
> Snapshot reviewed: **September 18, 2026.**

## Related Projects

- [awesome-gpt-6-astra](https://github.com/Anil-matcha/awesome-gpt-6-astra) — sibling evidence-backed use-case collection for a general-purpose reasoning model.
- [awesome-agent-apis](https://github.com/Anil-matcha/awesome-agent-apis) — catalog of APIs and tools that typed decisions can route to.
- [open-business-agents](https://github.com/Anil-matcha/open-business-agents) — specialized business agents that can use Jev as a decision and safety layer.
- [awesome-generative-ai-apps](https://github.com/Anil-matcha/awesome-generative-ai-apps) — production-oriented AI app templates where Jev can help with routing, guardrails, and verification.
- [llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) — persistent, interlinked knowledge workflow that pairs naturally with semantic retrieval and citation checks.

## The short version

Most LLMs produce strings for people. Jev evaluates a state against questions whose answer spaces you define in advance. It returns typed values and probability distributions that ordinary software can branch on.

That makes Jev a good fit for the fuzzy middle between brittle rules and expensive generative workflows:

| If your application needs to… | Reach for… |
|---|---|
| Pick one value from a known set | `Choice` |
| Measure a position on an ordered rubric | `Score` |
| Estimate whether a condition is true | `Noul` |
| Decide whether to act, review, or fall back | probabilities + confidence + code |
| Write an explanation, code, or a reply | an LLM, optionally after Jev routes or verifies it |

## Quick facts

| Item | Current detail | Source |
|---|---|---|
| Model | **Jev**, TypeSafe’s flagship and first System One model | [Introduction](https://docs.typesafe.ai/introduction) |
| API model alias | `jev-latest` | [Models](https://docs.typesafe.ai/models) |
| Current version listed by TypeSafe | `jev-1.13.0` | [Models](https://docs.typesafe.ai/models) |
| Endpoint | `POST https://api.typesafe.ai/v1/systemone` | [API reference](https://docs.typesafe.ai/api) |
| Input | A string, JSON object, or array of text values | [State](https://docs.typesafe.ai/concepts/state) |
| Output | `Choice`, `Score`, and `Noul` answers with typed fields; Choice and Score also include probabilities and confidence | [Primitives](https://docs.typesafe.ai/primitives) |
| Current listed price | `$0.042 / 1M` input tokens; output tokens listed as free | [Models](https://docs.typesafe.ai/models) |
| Current listed limits | `250,000` tokens/second and `1,200` requests/minute; TypeSafe says limits can change dynamically | [Models](https://docs.typesafe.ai/models) |
| Modalities | Text only for now; images, audio, and video are not supported | [System One](https://docs.typesafe.ai/concepts/system-one) |
| Availability | Early access at launch; check the [TypeSafe console](https://console.typesafe.ai/) | [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev) |

TypeSafe’s launch materials report **70–500 ms** end-to-end response times for TypeSafe and describe Jev as roughly two orders of magnitude faster and more efficient for System One-shaped tasks. Treat those as vendor-reported, workload-dependent results; benchmark your own state, question design, network path, and concurrency.

## Read first

1. [Introduction](https://docs.typesafe.ai/introduction) — the core mental model.
2. [State](https://docs.typesafe.ai/concepts/state) — how to package messages, records, policies, and application context.
3. [Primitives](https://docs.typesafe.ai/primitives) — when to use `Choice`, `Score`, or `Noul`.
4. [Confidence](https://docs.typesafe.ai/confidence) — how to turn uncertainty into safe routing.
5. [Patterns](https://docs.typesafe.ai/patterns) — fan-out, confidence gates, composite scoring, and intent routing.
6. [API reference](https://docs.typesafe.ai/api) — the request and response contract.

## Quick start

### Python

The official Python SDK reads `TYPESAFE_API_KEY` from the environment and defaults to `jev-latest`.

```bash
python -m pip install typesafe-sdk
export TYPESAFE_API_KEY="your-key"
python examples/python/quickstart.py
```

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

state = {
    "ticket": "I was charged twice and need the duplicate refunded today.",
    "account_tier": "business",
}

with TypeSafeClient() as client:
    response = client.system_one(
        state=state,
        questions={
            "intent": Choice(
                instructions="What is the customer's main request?",
                criteria={
                    "refund": "The customer wants money returned.",
                    "technical_help": "The customer needs a bug or integration fixed.",
                    "information": "The customer is asking for information only.",
                    "other": "None of the other options clearly fits.",
                },
            ),
            "is_urgent": Noul(
                instructions="Does the ticket explicitly communicate time pressure?",
            ),
            "frustration": Score(
                instructions="How frustrated does the customer appear?",
                criteria=[
                    "Calm and neutral",
                    "Concerned but civil",
                    "Very angry or using strong language",
                ],
            ),
        },
    )

print(response.answers["intent"].choice)
print(response.answers["intent"].probabilities)
print(response.answers["is_urgent"].noul)
print(response.answers["frustration"].score)
```

### JavaScript / TypeScript

```bash
npm install @typesafe-ai/sdk
export TYPESAFE_API_KEY="your-key"
npx tsx examples/typescript/quickstart.ts
```

```ts
import { choice, noul, score, TypeSafeClient } from "@typesafe-ai/sdk";

const client = new TypeSafeClient();
const result = await client.systemOne({
  state: {
    ticket: "I was charged twice and need the duplicate refunded today.",
  },
  questions: {
    intent: choice("What is the customer's main request?", {
      refund: "The customer wants money returned.",
      technical_help: "The customer needs a bug or integration fixed.",
      information: "The customer is asking for information only.",
      other: "None of the other options clearly fits.",
    }),
    isUrgent: noul("Does the ticket explicitly communicate time pressure?"),
    frustration: score("How frustrated does the customer appear?", [
      "Calm and neutral",
      "Concerned but civil",
      "Very angry or using strong language",
    ]),
  },
});

console.log(result.answers.intent.choice);
console.log(result.answers.isUrgent.noul);
console.log(result.answers.frustration.score);
```

See the [official Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python), [official JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js), and [Quick start](https://docs.typesafe.ai/introduction/quickstart) for the supported client options.

## The three primitives

Each question should ask for one focused judgment about the same state. Several questions can be sent in one request and are evaluated independently.

### `Choice`: one known option

Use it for intent, department, document type, tool name, risk category, or any other unordered finite set. Include `other` or `none_of_the_above` when your options may not cover reality.

```python
"department": Choice(
    instructions="Which team should own this ticket?",
    criteria={
        "billing": "Payments, invoices, refunds, or charges.",
        "technical": "Bugs, outages, or integrations.",
        "account": "Access, profile, or account administration.",
        "other": "None of the teams above clearly fits.",
    },
)
```

Returns the selected `choice`, a probability for every option, and `confidence`.

### `Score`: a position on an ordered rubric

Use it for severity, relevance, frustration, quality, suitability, or complexity. Define what each level means. The returned `score` is probability-weighted and may land between levels.

```python
"severity": Score(
    instructions="How severe is the customer-facing impact of this incident?",
    criteria=[
        "Minor inconvenience; workaround available",
        "Material degradation; some users affected",
        "Critical outage; core workflow blocked",
    ],
)
```

Returns `score`, `legend`, `probabilities`, and `confidence`.

### `Noul`: probability that a statement is true

Use it when the probability itself is useful: “Does this request ask for a refund?”, “Does this passage answer the question?”, or “Is this prompt a jailbreak attempt?”

```python
"contains_prompt_injection": Noul(
    instructions="Does the user-provided text attempt to override the application's instructions?",
)
```

Returns `noul` from `0` to `1`. Near `0.5` means the question is uncertain; it is not a medium score.

## Core patterns

| Pattern | Shape | Where it shines |
|---|---|---|
| Atomic questions | One narrow question per judgment | Reliable, inspectable workflow logic |
| Speculative fan-out | Ask every likely-needed question in one call; ignore irrelevant answers in code | Support triage, smart-home commands, agent routing |
| Confidence-gated routing | Treat answer and confidence as separate axes | Automation with human fallback |
| Composite scoring | Normalize several Scores and combine with explicit weights | Candidate, lead, vendor, and risk ranking |
| Intent routing | Choose deterministic code, specialist LLM, or human | Cost and latency control |
| Two-stage dependency | Make a second call only when the first answer changes the next state or options | Hierarchical classification, structure recovery |

The important design rule is: **questions describe judgments; code owns composition, thresholds, and side effects.**

## Use-case map

The following cases are practical starting points, not promises that Jev will be correct for every domain. Each one is a small decision system with a clear output contract.

### Workflow control

#### 1. Support inbox triage

Classify the request, detect urgency and refund intent, score frustration, then route with ordinary code. Ask all dimensions together—even bug severity that matters only for bug reports—using [speculative fan-out](https://docs.typesafe.ai/patterns/fan-out).

```python
if result.answers["intent"].choice == "technical_help":
    if result.answers["severity"].score >= 1.5:
        escalate_to_engineering()
    else:
        add_to_bug_backlog()
elif result.answers["intent"].choice == "refund":
    route_to_billing()
```

Evidence: [TypeSafe’s support fan-out pattern](https://docs.typesafe.ai/patterns/fan-out) and [customer-support use cases](https://docs.typesafe.ai/concepts/use-case-map).

#### 2. Intent and model routing

Put a cheap, fast decision layer in front of deterministic handlers, specialist LLMs, and human agents. Let confidence decide when a category is safe to trust.

Evidence: [Intent routing](https://docs.typesafe.ai/patterns/intent-routing).

#### 3. Confidence-gated actions

Use lower thresholds for reversible read-only actions and higher thresholds for risky operations. For example, show a balance at one threshold, ask for confirmation before a transfer at another, and send ambiguous commands to a human.

Evidence: [Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing).

#### 4. Typed function and tool dispatch

Map a natural-language command to a function name and closed-set arguments. Jev chooses only from the values your function accepts; code still validates authorization, required fields, and side effects before execution.

Evidence: [Function-calling cookbook](https://docs.typesafe.ai/cookbooks/function_calling).

### Retrieval and knowledge

#### 5. RAG passage filtering

Score relevance, answer support, contradiction, and prompt-injection risk for each retrieved passage. Pass only evidence that clears your application’s thresholds to the answering model.

Evidence: [Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages).

#### 6. Semantic search and re-ranking

Use BM25 or embeddings to create a shortlist, then score each query–candidate pair with a `Noul` and sort by the returned value. This gives the semantic stage a numeric signal without asking a generative model to invent a scale.

Evidence: [Re-ranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe) and [line-by-line search](https://docs.typesafe.ai/cookbooks/semantic_find).

#### 7. Citation and claim verification

Compare a claim, its cited passage, and the source document. Ask whether the passage supports, contradicts, or fails to establish the claim, and route low-confidence results to review.

Evidence: [Double-checking citations](https://docs.typesafe.ai/cookbooks/citation_check).

#### 8. Knowledge-graph entity alignment

For each candidate pair, choose `merge`, `leave_unlinked`, or `curator_review`, or score how likely the records refer to the same entity. Keep the final merge policy deterministic and auditable.

Evidence: [Knowledge-graph entity alignment](https://docs.typesafe.ai/cookbooks/entity_alignment).

### Safety and quality

#### 9. LLM input/output guardrails

Screen prompts, generated replies, and tool calls with hazard `Noul`s and a harm `Score`. Your policy can pass, review, block, or route instead of relying only on a system prompt.

Evidence: [Guardrails for LLMs](https://docs.typesafe.ai/cookbooks/llm_guardrails).

#### 10. Semantic code and writing linting

Turn team conventions into narrow yes/no checks and run them in CI. Use the result to annotate a pull request or request review; do not silently rewrite code or policy text.

Evidence: [Semantic code linting in the TypeSafe use-case map](https://docs.typesafe.ai/concepts/use-case-map).

#### 11. Policy, compliance, and document verification

Check contracts, filings, marketing claims, or support replies against explicit requirements. Return structured findings and escalate high-impact or ambiguous cases to a named reviewer.

Evidence: [Legal and compliance use cases](https://docs.typesafe.ai/concepts/use-case-map).

#### 12. Self-consistency and uncertain labels

Add an explicit uncertain option to a moderation or classification space, or compare repeated decisions on high-risk inputs. Use disagreement as a review signal, not as a reason to blindly majority-vote.

Evidence: [TypeSafe’s self-consistency cookbooks](https://docs.typesafe.ai/llms.txt).

### Data and operations

#### 13. Structured extraction with validation

Recover known fields from messy text by first finding candidate spans with deterministic code, then using Jev to choose the requested span or label. Normalize dates, amounts, and identifiers in code and validate them before storage.

Evidence: [Pre-parsed value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) and [date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook).

#### 14. Composite candidate, lead, or vendor scoring

Score independent dimensions—such as role evidence, technical depth, and communication—then combine normalized values with weights you own. The same design works for lead fit, vendor risk, ad suitability, and claim complexity.

Evidence: [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring).

#### 15. Feature extraction for classical ML

Convert language into probabilistic features such as purchase intent, churn signals, competitive pressure, or complaint severity, then feed them into a supervised model alongside structured features.

Evidence: [Feature extraction use cases](https://docs.typesafe.ai/concepts/use-case-map).

#### 16. High-cardinality and hierarchical classification

For large taxonomies, use staged choices or a probability-aware beam. Let the first decision choose a branch and ask a second question only when the next option set depends on that branch.

Evidence: [Hierarchical classification](https://docs.typesafe.ai/cookbooks/hierarchical_classification).

### Real-time and agentic systems

#### 17. Smart-home and UI command control

Fan out across command category, domain, device type, and action in one request. Use deterministic code for permissions and execution, and hand general conversation to a generative model when the request is outside the closed command space.

Evidence: [Smart-home demo](https://docs.typesafe.ai/demos/smart-home).

#### 18. Agent harness routing and skill suggestion

Use Jev to decide whether a turn needs a skill, tool, retrieval step, or expensive reasoning model. Keep tool descriptions, authorization, and stop conditions outside the model’s answer space.

Evidence: [Agent skill](https://docs.typesafe.ai/agent-skill) and [skill-suggestion cookbook](https://docs.typesafe.ai/cookbooks/skill_suggestion).

## A production-shaped decision loop

```text
      ┌────────────┐
      │ state      │  text / JSON records / policy / history
      └─────┬──────┘
            │
            ▼
      ┌────────────┐      typed questions
      │ Jev        │  ──────────────────────┐
      └─────┬──────┘                         │
            │ answers + distributions       │
            ▼                                │
      ┌────────────┐  high confidence       ▼
      │ code       │ ───────────────────► act / route / rank
      │ thresholds │
      └─────┬──────┘  uncertain or risky
            └───────────────────────────► review / confirm / fallback
```

A useful implementation boundary is:

1. **Inspect** the state and decide which judgments the workflow needs.
2. **Evaluate** atomic questions together where they share the same state.
3. **Compose** answers, probabilities, and business rules in code.
4. **Gate** side effects by risk-specific thresholds.
5. **Record** the version, question definitions, distributions, chosen path, and reviewer outcome.
6. **Calibrate** thresholds on representative labeled data and revisit them after model or policy changes.

## What Jev is not

- It is not a chatbot, copywriter, code generator, or explanation engine.
- It does not return arbitrary strings. The answer space comes from the question you define.
- It is not a guarantee that a semantic judgment is correct. Calibration describes groups of predictions, not any individual answer.
- It is not a replacement for authorization, deterministic validation, policy enforcement, or human review in high-impact workflows.
- It does not currently accept images, audio, or video.

When you need a free-form answer, pair Jev with a generative model: let Jev route, retrieve, verify, or guard the call, then let the LLM write within the boundaries your application enforces.

## Safety and reliability checklist

- Keep API keys server-side and restrict which services may call the endpoint.
- Include an `other`, `unknown`, or `review` option whenever the option list can be incomplete.
- Set thresholds per action and risk level; do not copy one global threshold across the system.
- Treat low confidence as a first-class branch: ask for clarification, use a fallback, or involve a person.
- Version state schemas, question instructions, criteria, and policy code together.
- Log the versioned model returned in the response, not only the alias sent in the request.
- Store probability distributions for audit and calibration, not just the winning label.
- Use the SDK’s default retry behavior for `429` and `529`, or implement exponential backoff for direct HTTP calls.
- Make side effects an explicit second step after inspection and approval.
- Evaluate with your own representative cases, including ambiguity, adversarial text, missing fields, and out-of-domain inputs.

## Included examples

| Path | What it demonstrates |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | One request mixing Choice, Noul, and Score |
| [`examples/python/workflows.py`](examples/python/workflows.py) | Support triage, guardrail questions, semantic re-ranking, and composite scoring |
| [`examples/python/decision_policies.py`](examples/python/decision_policies.py) | Pure policy code for confidence gates and weighted scores |
| [`examples/typescript/quickstart.ts`](examples/typescript/quickstart.ts) | TypeScript SDK usage |
| [`tests/test_decision_policies.py`](tests/test_decision_policies.py) | Offline tests that need no API key |
| [`docs/jev-use-case-playbook.md`](docs/jev-use-case-playbook.md) | Detailed, implementation-oriented case studies |
| [`docs/coding-agent-use-cases.md`](docs/coding-agent-use-cases.md) | Agent harness and coding-agent patterns |

Run the offline checks:

```bash
python -m unittest discover -s tests -v
```

Run a live example only after setting `TYPESAFE_API_KEY`:

```bash
python examples/python/quickstart.py
```

## Repository metadata

The intended GitHub description and topic set are recorded in [`docs/repository-metadata.md`](docs/repository-metadata.md). The topic list is capped at **20**.

## Official references

- [TypeSafe AI](https://typesafe.ai/)
- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [TypeSafe documentation](https://docs.typesafe.ai/introduction)
- [API reference](https://docs.typesafe.ai/api)
- [Models, aliases, prices, and limits](https://docs.typesafe.ai/models)
- [State](https://docs.typesafe.ai/concepts/state)
- [Primitives](https://docs.typesafe.ai/primitives)
- [Confidence](https://docs.typesafe.ai/confidence)
- [Patterns](https://docs.typesafe.ai/patterns)
- [Example use cases](https://docs.typesafe.ai/concepts/use-case-map)
- [Quick start](https://docs.typesafe.ai/introduction/quickstart)
- [Official Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python)
- [Official JavaScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js)
- [TypeSafe console](https://console.typesafe.ai/)

## Contributing

Useful contributions are small, reproducible, and honest about uncertainty:

- add a use case with a clear state, question contract, code-owned policy, and source;
- include a fixture or offline test when behavior can be checked without an API key;
- report model version, date, thresholds, and evaluation set for performance claims;
- separate TypeSafe-reported results from your own measurements;
- avoid putting credentials, private customer data, or irreversible actions in examples.

## License

MIT — see [LICENSE](LICENSE).
