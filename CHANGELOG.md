# Changelog

All notable changes to this project are documented in this file.

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
