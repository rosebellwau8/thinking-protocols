# Complete 12-Protocol Library Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add the eight deferred independently authored Protocols and release the complete 12-Protocol library without redesigning the v0.1.0 architecture.

**Architecture:** Keep `protocols/<id>/PROTOCOL.md` as the sole semantic source and reuse the seven existing Artifact contracts. The eight additions produce terminal reader-facing output, so they do not add sensitive or single-consumer Artifact schemas. Extend evaluation validation only for source-conflict coverage, and make ambiguous role-only routing conservatively prefer a direct answer while preserving explicit, Artifact, capability, consent, and priority precedence.

**Tech Stack:** Python 3.11+, Markdown/YAML canonical Protocols, JSON Schema 2020-12, Jinja2 adapters, pytest/pytest-cov.

---

### Task 1: Lock the 12-Protocol and evaluation contracts

**Files:**
- Modify: `tests/test_pilot_protocols.py`
- Modify: `tests/test_validation.py`
- Modify: `schemas/evals.schema.json`
- Modify: `src/thinking_protocols/validation.py`

**Steps:**
1. Write failing tests for the exact 12 IDs, required examples, base eval categories, capability failure cases, and research evidence-conflict cases.
2. Run the focused tests and confirm they fail against the four-Protocol baseline.
3. Add the backward-compatible `evidence_conflict` eval category and generic repository checks for required categories.
4. Re-run focused validation tests and retain failures only for Protocols not yet authored.

### Task 2: Author the six bounded/one-shot Protocols

**Files:**
- Create: `protocols/dual-layer-explanation/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Create: `protocols/reverse-engineering/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Create: `protocols/horizontal-vertical-analysis/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Create: `protocols/expert-panel/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Create: `protocols/first-principles/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Create: `protocols/cross-domain-transfer/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Modify: `protocols/fact-checking/evals.yaml`

**Steps:**
1. Independently write applicability, capability, evidence, phase, stop, output, and safety contracts from the supplied method descriptions.
2. Keep all results terminal and all state turn-scoped; require `web.search` only for the two research-dependent Protocols.
3. Add structured trigger, non-trigger, missing-input, stop, sensitive, capability, and source-conflict evals as applicable.
4. Run repository validation and protocol contract tests.

### Task 3: Author the two consent-gated self-exploration Protocols

**Files:**
- Create: `protocols/talent-discovery/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`
- Create: `protocols/life-design/{PROTOCOL.md,evals.yaml,examples/terminal-output.md}`

**Steps:**
1. Define bounded iterative workflows with explicit maximum turns and early stopping.
2. Require only conversation-lifetime state, allow skipped questions, forbid diagnosis, and declare default non-persistence.
3. Make conclusions provisional, counterexample-aware, and action/test oriented.
4. Verify schema, consent metadata, eval coverage, and absence of persistent state.

### Task 4: Harden Router behavior against over-routing

**Files:**
- Modify: `src/thinking_protocols/router.py`
- Modify: `tests/test_router.py`
- Modify: `tests/e2e/test_direct_answer_policy.py`
- Create: `tests/e2e/test_complete_library_routing.py`

**Steps:**
1. Write failing cases for all eight explicit Protocols, required capabilities, both iterative consent gates, and ambiguous role-only requests.
2. Replace lexical selection among multiple primary-role matches with conservative direct-answer behavior.
3. Prove simple factual, translation, formatting, ordinary explanation, generic analysis, generic complexity, and research-without-intent requests stay direct.
4. Prove explicit selection still precedes direct answer and cannot bypass capability or consent gates.

### Task 5: Update package, governance, version, and provenance

**Files:**
- Modify: `pyproject.toml`
- Modify: `src/thinking_protocols/__init__.py`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `NOTICE.md`
- Modify: `sources/kazike-12-prompts/source.yaml`
- Modify: `sources/kazike-12-prompts/notes.md`
- Modify: `tests/test_package.py`
- Modify: `tests/test_governance.py`

**Steps:**
1. Set the backward-compatible feature release version to 0.2.0.
2. Document all 12 use cases, research and consent boundaries, and removal of the MVP deferrals.
3. Record the one-to-one source-note mapping and independent-rewrite boundary without storing third-party Prompt text.
4. Test version consistency, provenance mapping, and absence of a copied source corpus.

### Task 6: Generate and audit the release

**Files:**
- Regenerate: `generated/registry.yaml`
- Regenerate: `dist/generic/*.md`
- Regenerate: `dist/codex/skills/*/SKILL.md`
- Modify: adapter/registry/conformance tests only if a generic gap is exposed

**Steps:**
1. Run repository validation and require `valid: True`, zero issues.
2. Build the deterministic Registry, Generic distribution, and Codex distribution.
3. Run semantic conformance and stale-output checks.
4. Run the full suite with at least 90% coverage.
5. Run packaging checks and inspect CI parity for Windows and Ubuntu commands.
6. Inspect licensing/provenance and repository diffs, then create focused commits.
7. Confirm tracked generated output is current and the final worktree is clean.
