# Thinking Protocols

Thinking Protocols is an Artifact-driven library of machine-readable cognitive workflows. Canonical semantics live only in `protocols/<id>/PROTOCOL.md`; registries and runtime packages are deterministic generated views.

Version 0.2.0 contains the complete twelve-Protocol library:

| Protocol | Primary role | Use it for | Output |
| --- | --- | --- | --- |
| `socratic-questioning` | Clarify | Reframing an ambiguous consequential problem with bounded questioning. | `clarified_problem.v1` |
| `fact-checking` | Verify | Checking externally verifiable claims against dated evidence. | `verified_claims.v1` |
| `steelman-both-sides` | Decide | Comparing the strongest credible cases for real options. | `decision_memo.v1` |
| `minimum-experiment` | Experiment | Designing the smallest safe, reversible test of a decision uncertainty. | `experiment_plan.v1` |
| `dual-layer-explanation` | Reason | Giving compatible intuitive and mechanism-level explanations. | Terminal output |
| `reverse-engineering` | Reason | Working backward from an existing outcome to mechanisms and a minimal reconstruction. | Terminal output |
| `horizontal-vertical-analysis` | Research | Crossing historical evolution with evidence-backed peer or alternative comparison. | Terminal output |
| `expert-panel` | Reason | Comparing explicitly defined analytical lenses without impersonating real experts. | Terminal output |
| `first-principles` | Reason | Re-deriving options from facts, hard constraints, goals, and stated assumptions. | Terminal output |
| `cross-domain-transfer` | Reason | Transferring an evidenced mechanism across domains through structural matching and tests. | Terminal output |
| `talent-discovery` | Clarify | Forming non-diagnostic, reality-testable talent hypotheses with consent. | Terminal output |
| `life-design` | Decide | Turning current reality and values into feasible options and reversible experiments. | Terminal output |

Terminal outputs are intentionally not typed Artifacts when no downstream Protocol consumes them. This keeps the seven v0.1 Artifact contracts unchanged and avoids persistent sensitive data.

See [the architecture](docs/architecture.md) for the frozen domain model and routing contract.

## Requirements and installation

Python 3.11 or newer is supported.

```console
python -m venv .venv
python -m pip install -e ".[dev]"
```

Activate the environment for your shell, or invoke its Python and console script directly.

## Validate and build

```console
thinking-protocols validate
thinking-protocols build-registry
thinking-protocols build --adapter generic
thinking-protocols build --adapter codex
thinking-protocols check-generated
python -m pytest --cov=thinking_protocols --cov-fail-under=90
```

`validate` checks Protocol schemas, evaluation structure and required categories, Artifact and capability cross-references, and producer priority. `check-generated` rebuilds every generated target in a temporary directory and fails on missing, extra, or stale output.

## Routing behavior

The Router prefers a direct answer for simple, bounded requests. Ordinary explanations, factual questions, translations, formatting, and generic analysis do not opt into specialized Protocols. An explicit Protocol request has precedence when its capability and consent requirements can be met.

For inferred routing, an exact desired Artifact selects its producer and may add at most one prerequisite for a real Artifact gap. `routing_priority` breaks Artifact-producer ties only; it cannot override an explicit request, direct-answer policy, missing capability, or consent gate. A primary-role request shared by multiple specialized Protocols stays a direct answer instead of choosing one by name order.

`horizontal-vertical-analysis` and `cross-domain-transfer` require `web.search`; missing search blocks rather than substituting model memory. `talent-discovery`, `life-design`, and all other iterative Protocols require user consent. Their state is conversation-scoped and never persistent by default.

## Adapter invariants

Adapters may change packaging, filenames, metadata syntax, invocation commands, capability bindings, and presentation. They must preserve interaction and state, capabilities, required inputs, phase order, stop conditions, Artifact contracts, evidence rules, safety boundaries, Protocol version, and the LF-normalized source digest.

The Generic adapter emits standalone Markdown under `dist/generic/`. The Codex adapter emits skill packages under `dist/codex/skills/`. Each generated file records its source Protocol version and digest.

## Generated files

`generated/registry.yaml` and all files under `dist/` are generated output. Do not edit them by hand. Change canonical Protocols, schemas, or adapter templates, then run the build commands and commit the regenerated files. Authored and generated text uses UTF-8 with LF newlines.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution order.

## Boundaries and provenance

This remains a workflow library and build system, not an autonomous agent, hosted LLM application, semantic router, database, persistent runtime, or universal reasoning pipeline. Self-exploration Protocols are non-diagnostic and do not replace medical, mental-health, legal, or financial professionals.

Original repository material is licensed under Apache-2.0. Third-party articles and Prompt bodies are not part of this repository or its license. Provenance records attribute inspiration and map each method to an independent rewrite without importing third-party text or licensing terms. See [NOTICE.md](NOTICE.md) and [source notes](sources/kazike-12-prompts/notes.md).
