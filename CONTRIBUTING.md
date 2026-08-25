# Contributing

Keep Protocol semantics in canonical sources and preserve deterministic generated output. Use this contribution sequence:

1. Copy `protocols/_template/PROTOCOL.md` into a new Protocol directory.
2. Write positive trigger and non-trigger cases in `evals.yaml` first.
3. Add or reuse versioned Artifact schemas for every consumed or produced contract.
4. Run `thinking-protocols validate`.
5. Regenerate the registry and both distributions.
6. Run conformance checks and the complete test suite.
7. Never paste third-party Prompt bodies into the repository.

Generated files under `generated/` and `dist/` must be changed only by their build commands. Keep all authored and generated text in UTF-8 with LF newlines.
