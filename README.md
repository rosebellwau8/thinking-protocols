# Thinking Protocols

Thinking Protocols is an Artifact-driven library of machine-readable cognitive workflows. Canonical Protocol semantics live in `protocols/<id>/PROTOCOL.md`; registries and runtime packages are generated from those sources.

The v0.1.0 MVP contains four independently authored Protocols:

| Protocol | Primary role | Output |
| --- | --- | --- |
| Socratic Questioning | Clarify | `clarified_problem.v1` |
| Fact Checking | Verify | `verified_claims.v1` |
| Steelman Both Sides | Decide | `decision_memo.v1` |
| Minimum Experiment | Experiment | `experiment_plan.v1` |

See [the architecture](docs/architecture.md) for the domain model and routing contract.

## Requirements and installation

Python 3.11 or newer is supported.

```console
python -m venv .venv
python -m pip install -e ".[dev]"
```

Activate the virtual environment using the command appropriate for your shell, or invoke its Python and console script directly.

## Validate and build

```console
thinking-protocols validate
thinking-protocols build-registry
thinking-protocols build --adapter generic
thinking-protocols build --adapter codex
thinking-protocols check-generated
python -m pytest
```

`validate` checks Protocol schemas, Artifact schemas and examples, evaluation structure, cross-references, capability identifiers, and repository policy. `check-generated` rebuilds all generated targets in a temporary directory and fails if tracked output is stale.

## Routing behavior

The Router defaults to a direct answer for simple, bounded requests. An explicit Protocol request has precedence when its requirements can be met. For inferred routing, the Router selects the smallest suitable Protocol and adds at most one prerequisite to fill a required Artifact gap.

`routing_priority` is a non-negative integer used only to break ties among otherwise suitable producers: larger values win and omission means zero. It cannot override explicit Protocol selection, the direct-answer default, capability blocking, consent requirements, or safety constraints.

## Adapter invariants

Adapters may change packaging, filenames, metadata syntax, invocation commands, capability bindings, and presentation. They must preserve applicability, required inputs, phase order, stopping conditions, Artifact contracts, evidence rules, safety constraints, Protocol version, and the LF-normalized source digest. Conformance checks compare these invariant fields with the canonical Protocol.

The Generic adapter emits standalone Markdown prompts under `dist/generic/`. The Codex adapter emits skill packages under `dist/codex/skills/`.

## Generated files

`generated/registry.yaml` and all files under `dist/` are deterministic build output. Do not edit them by hand. Change canonical Protocols, schemas, or adapter templates, then run the corresponding build commands and commit the regenerated files. Authored and generated text uses UTF-8 with LF newlines.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required contribution order.

## MVP boundaries

The MVP intentionally excludes hosted services, LLM API integration, persistent runtimes, databases, user interfaces, plugin systems, semantic or LLM-assisted routing, and the eight deferred Protocol migrations. Sensitive self-exploration workflows remain out of scope until privacy, deletion, consent, and non-diagnostic safeguards are defined.

Original repository material is licensed under the Apache License 2.0. Third-party articles and Prompt bodies are not part of this repository or its license. Provenance records attribute inspiration without importing third-party text or licensing terms. See [NOTICE.md](NOTICE.md).
