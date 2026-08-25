# Thinking Protocols Architecture Design

Status: approved for implementation planning
Date: 2026-08-25

## Purpose

Thinking Protocols is a machine-readable cognitive workflow library. Prompt text is not the canonical asset. The repository preserves platform-neutral Protocols, typed Artifacts exchanged between Protocols, and thin Adapters that render those Protocols for concrete agent runtimes.

The MVP validates the architecture with four representative Protocols:

- socratic-questioning
- fact-checking
- steelman-both-sides
- minimum-experiment

Together they cover iterative interaction, conversation state, evidence-backed research, decision support, and Artifact composition. The MVP is a library and build system, not an autonomous reasoning engine, hosted service, or LLM application.

## Core domain model

The three authored core objects are:

- Protocol: applicability, inputs, phases, stopping rules, capability requirements, outputs, evidence rules, and safety boundaries.
- Artifact: the typed interface between Protocols. Protocols exchange validated Artifacts rather than depending on another Protocol's prose or hidden reasoning.
- Adapter: maps a valid Protocol to a target runtime's packaging and invocation format without changing protocol semantics.

Tools are runtime capabilities rather than peer domain objects. A Protocol requests abstract capabilities such as web.search, files.read, or code.execute. An Adapter maps these identifiers to runtime-specific tools. Missing required capabilities follow an explicit block, degrade, or ask_user policy.

The Router is an application service over the domain model. It receives a request, available Artifacts, capabilities, and user preferences, then returns direct_answer, run_protocol, request_input, or blocked.

## Canonical sources and dependency direction

protocols/<id>/PROTOCOL.md is the sole authored source of protocol semantics. YAML frontmatter is machine-readable; the Markdown body contains the human-readable procedure. The registry and platform distributions are generated and must never be edited manually.

    Protocol definitions ---> Registry
            |                    |
            +----> Adapters -----+----> dist/
            |
            +----> Artifact schemas

    Request + Artifacts + Capabilities ---> Router ---> Decision

Adapters may alter filenames, metadata syntax, invocation commands, capability bindings, and presentation. They may not alter applicability, required inputs, phase order, stop conditions, Artifact contracts, evidence rules, or safety constraints. Generated output records the source Protocol version and digest so conformance can be checked.

## Artifact model

Every Artifact instance uses a common envelope containing its type, schema version, producing Protocol, provenance, uncertainty, and payload. Type-specific JSON Schemas validate each payload.

Initial schemas:

- clarified_problem.v1
- claim_set.v1
- verified_claims.v1
- option_set.v1
- decision_context.v1
- decision_memo.v1
- experiment_plan.v1

Schema filenames end in .schema.json; example instances end in .json. Protocol and Artifact versions evolve independently. Breaking Artifact changes create a new major schema file rather than mutating an existing interface. Provenance distinguishes user statements, external evidence, and model inference. Uncertainty is explicit.

Sensitive self-exploration Artifacts are outside the MVP. Before adding them, define persistence, deletion, consent, and non-diagnostic boundaries.

## Routing policy

The Router is deliberately conservative:

    prefer_direct_answer: true
    default_protocol_count: 1
    max_protocol_count_per_stage: 2
    chain_only_on_artifact_gap: true

Routing precedence:

1. Honor an explicit Protocol request when requirements can be met.
2. Prefer a direct answer for simple bounded requests.
3. Infer the desired Artifact or primary epistemic role.
4. Select the smallest Protocol capable of producing it.
5. Add no more than one prerequisite Protocol for a missing required Artifact.
6. Refuse, degrade, or ask according to the missing-capability policy.
7. Require consent before long-running, iterative, persistent, or sensitive workflows.

Artifact gaps guide routing but do not override user intent, cost limits, safety constraints, or the direct-answer default. The Router never constructs a full multi-Protocol pipeline merely because a problem appears complex.

When multiple Protocols produce the same Artifact, `routing_priority` provides deterministic precedence. It is a non-negative integer; a larger integer wins and an omitted value has an effective priority of zero. Repository validation requires one unique highest effective priority; equal highest values, including multiple omitted values, are an ambiguity error. This priority is considered only after explicit Protocol selection and the direct-answer policy. It does not override capability, consent, or safety checks.

## Build and validation

Use Python 3.11 or newer, PyYAML, jsonschema, Jinja2, pytest, and a small argparse CLI.

Validation has four levels:

1. JSON Schema validation of Protocol frontmatter and Artifact instances.
2. Cross-reference validation of consumed and produced Artifacts and capability names.
3. Adapter conformance checks over invariant semantic fields.
4. Behavioral tests for positive and negative triggers, missing inputs, missing capabilities, early stopping, maximum turns, and over-routing.

Builds are deterministic: identical authored sources produce byte-identical registry and distribution output. Tests require no network access. Research Protocol tests simulate capability availability and evidence rather than browsing.

## Licensing and provenance

The repository does not store full third-party Prompt text. Source records contain attribution metadata, URLs, relationship statements, and independent notes. Protocol language is independently rewritten.

NOTICE.md distinguishes repository-authored material from third-party references. No content license is selected silently. Any later license applies only to rights controlled by the repository owner; third-party material is expressly excluded.

## MVP exit criteria

The architecture is validated when four pilot Protocols pass schema and behavioral validation; seven Artifact schemas validate representative instances; the registry is deterministic; Generic and Codex Adapters build without semantic drift; the Router passes direct-answer and anti-over-routing tests; at least one Artifact-driven chain succeeds; and the repository contains no copied third-party Prompt corpus.
