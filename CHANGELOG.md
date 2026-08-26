# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 - 2026-08-26

### Added

- Eight independently authored Protocols: Dual-Layer Explanation, Reverse Engineering, Horizontal-Vertical Analysis, Expert Panel, First Principles, Cross-Domain Transfer, Talent Discovery, and Life Design.
- Structured examples and complete trigger, non-trigger, missing-input, stop, sensitive, capability, and evidence-conflict eval coverage as applicable for all twelve Protocols.
- Tool-aware research contracts with required web search, dated evidence, explicit research cutoffs, source conflict handling, and uncertainty reporting.
- Consent-gated, conversation-scoped self-exploration with question limits, skip rights, non-diagnostic boundaries, counterexamples, and non-persistent terminal output.
- Full Registry, Generic, and Codex generated distributions for all twelve Protocols.

### Changed

- Repository validation now requires the five base eval categories for every Protocol, a missing-capability case for capability-bound Protocols, and an evidence-conflict case for research-role Protocols.
- Ambiguous primary-role-only routing now conservatively returns a direct answer instead of selecting a specialized Protocol lexicographically.
- README, NOTICE, and source notes now describe the complete twelve-Protocol library and its one-to-one independent rewrite provenance.

### Compatibility

- The seven v0.1 Artifact schemas, Protocol schema, capability vocabulary, Adapter contracts, and routing precedence remain unchanged.
- The eight new terminal-output Protocols add no Artifact schemas and no persistent sensitive state.

## 0.1.0 - 2026-08-25

### Added

- Four canonical pilot Protocols: Socratic Questioning, Fact Checking, Steelman Both Sides, and Minimum Experiment.
- Seven versioned Artifact schemas with positive and negative validation coverage.
- Deterministic Protocol registry generation with LF-normalized source digests.
- Conservative routing with direct-answer defaults, explicit-request precedence, capability blocking, consent checks, and bounded Artifact-driven chaining.
- Generic Markdown and Codex skill adapters with semantic conformance checks.
- Repository validation, build, and generated-file freshness commands.
- Cross-platform CI for Python 3.11 and 3.12 on Windows and Ubuntu.
- Apache License 2.0 coverage for original repository material, with third-party source material explicitly excluded.

### Boundaries

- Third-party Prompt bodies and source corpora are excluded.
- Hosted services, persistent state, user interfaces, plugin systems, and semantic routing are deferred beyond the MVP.
