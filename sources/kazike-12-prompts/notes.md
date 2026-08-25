# Source notes

This record attributes a public article that grouped reusable thinking prompts around five broad kinds of work:

1. Clarifying an unclear problem before attempting a solution.
2. Separating factual verification from inference and personal values.
3. Comparing opposing positions fairly enough to support a decision.
4. Turning uncertainty into a small, reversible experiment.
5. Exploring personal or sensitive questions that require additional privacy and non-diagnostic safeguards.

The repository does not preserve the article's Prompt bodies. It extracts only the high-level observation that recurring cognitive work can be represented as explicit procedures.

Thinking Protocols introduces a new abstraction around that observation: each independently written Protocol declares applicability, inputs, ordered phases, stopping rules, capability requirements, safety boundaries, and typed Artifact outputs. Artifacts form stable interfaces between Protocols, while thin Adapters package the same semantics for different runtimes. This makes validation, routing, provenance, and semantic conformance testable without treating Prompt prose as the canonical asset.

The first four categories inform the v0.1.0 pilots. Sensitive self-exploration is deliberately deferred until consent, privacy, retention, deletion, and non-diagnostic policies are defined.
