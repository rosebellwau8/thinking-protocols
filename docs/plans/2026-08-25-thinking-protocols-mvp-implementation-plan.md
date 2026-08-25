# Thinking Protocols MVP Implementation Plan

> For Claude: REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

Goal: Build a validated, Artifact-driven cognitive Protocol library with four pilot Protocols, a conservative Router, and deterministic Generic and Codex Adapter output.

Architecture: Protocol semantics live only in protocols/<id>/PROTOCOL.md. Versioned JSON Schema Artifacts are Protocol interfaces. Adapters compile Protocols into runtime-specific packages while conformance checks protect semantic invariants. The Router prefers direct answers and escalates only for an explicit request or a justified Artifact gap.

Tech Stack: Python 3.12, argparse, hashlib, PyYAML, jsonschema, Jinja2, pytest, GitHub Actions.

---

## Ground rules

- Initialize the empty directory as a Git repository and work on branch feat/mvp.
- Follow TDD: failing test, minimal implementation, passing test, commit.
- Do not copy third-party Prompt bodies into the repository.
- Do not edit generated/ or dist/ manually.
- Keep v0.1.0 to four Protocols and two Adapters.
- Do not add an LLM API, web crawler, database, UI, plugin system, or persistent runtime.
- Use python -m pytest for consistent test invocation.

### Task 1: Initialize the repository and Python project

Files:

- Create: .gitignore
- Create: pyproject.toml
- Create: src/thinking_protocols/__init__.py
- Create: tests/__init__.py
- Test: tests/test_package.py

Step 1: Initialize Git and create the branch.

    git init
    git switch -c feat/mvp

Expected: an empty repository on feat/mvp.

Step 2: Write tests/test_package.py.

    import thinking_protocols

    def test_package_exposes_version() -> None:
        assert thinking_protocols.__version__ == "0.1.0"

Step 3: Run the test and verify import failure.

    python -m pytest tests/test_package.py

Expected: FAIL because the package is absent.

Step 4: Create pyproject.toml with:

- hatchling build backend;
- package name thinking-protocols;
- Python >=3.12;
- runtime dependencies Jinja2 >=3.1,<4, jsonschema >=4.23,<5, PyYAML >=6,<7;
- dev dependencies pytest >=8.3,<9 and pytest-cov >=6,<7;
- CLI entry point thinking-protocols = thinking_protocols.cli:main;
- src package layout.

Step 5: Create src/thinking_protocols/__init__.py.

    __version__ = "0.1.0"

Create an empty tests/__init__.py.

Step 6: Add .gitignore entries for .venv, caches, bytecode, build metadata, coverage, generated output, and dist output. Retain .gitkeep files in generated/ and dist/.

Step 7: Install and run the smoke test.

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
    .\.venv\Scripts\python.exe -m pytest tests/test_package.py

Expected: 1 passed.

Step 8: Commit.

    git add .gitignore pyproject.toml src tests
    git commit -m "build: initialize thinking protocols package"

### Task 2: Add governance and provenance boundaries

Files:

- Create: README.md
- Create: NOTICE.md
- Create: docs/architecture.md
- Create: docs/versioning.md
- Create: sources/kazike-12-prompts/source.yaml
- Create: sources/kazike-12-prompts/notes.md
- Test: tests/test_governance.py

Step 1: Write tests asserting every governance file exists and sources/kazike-12-prompts/original.md does not exist.

Step 2: Run the test.

    .\.venv\Scripts\python.exe -m pytest tests/test_governance.py

Expected: FAIL because the files are absent.

Step 3: Copy the approved design into docs/architecture.md.

Step 4: Write docs/versioning.md. State that Protocols use SemVer, Artifact schema versions evolve independently, and breaking Artifact changes require a new major schema filename.

Step 5: Write NOTICE.md with this minimum boundary:

    This repository contains independently authored Protocol definitions inspired
    by publicly described cognitive methods. Third-party articles and Prompt
    texts are not included in the repository license. Source records exist for
    attribution and provenance only.

Step 6: Write sources/kazike-12-prompts/source.yaml.

    id: kazike-12-prompts
    title: 都Agent时代了，我还是想分享给你这12个我最常用的Prompt
    author: 数字生命卡兹克
    published: 2026-08-21
    url: https://mp.weixin.qq.com/s/NAdhdFrUq9-BKelqzqpwBQ
    relationship: inspiration_for_independent_rewrite
    rights_status: third_party_not_licensed_by_this_repository
    full_text_stored: false

Step 7: Write notes.md as an original summary of the five source categories and the new abstraction. Do not reproduce Prompt bodies.

Step 8: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_governance.py
    git add README.md NOTICE.md docs sources tests/test_governance.py
    git commit -m "docs: define architecture and provenance boundaries"

Expected: governance tests pass.

### Task 3: Define the canonical Protocol Schema

Files:

- Create: schemas/protocol.schema.json
- Create: schemas/capability.schema.json
- Create: protocols/_template/PROTOCOL.md
- Create: tests/schemas/test_protocol_schema.py
- Create: tests/fixtures/protocols/valid.md
- Create: tests/fixtures/protocols/invalid_iterative.md

Step 1: Write a test that validates valid.md and rejects invalid_iterative.md.

The invalid fixture must declare interaction.mode as iterative while leaving stop_conditions empty.

Step 2: Run the test.

    .\.venv\Scripts\python.exe -m pytest tests/schemas/test_protocol_schema.py

Expected: FAIL because schemas and fixtures are absent.

Step 3: Implement capability.schema.json. Capability identifiers must match:

    ^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$

Document the initial vocabulary: web.search, web.open, files.read, code.execute.

Step 4: Implement protocol.schema.json. Require:

- id, SemVer version, and lifecycle status;
- source_category;
- epistemic_role.primary and unique secondary roles;
- interaction.mode and optional positive max_turns;
- state.required and conditional lifetime;
- required and optional capabilities plus on_missing;
- required and optional inputs;
- consumes and produces;
- ordered phases and stop_conditions;
- use_when, avoid_when, safety, and source.

Use JSON Schema conditionals so iterative Protocols require non-empty stop_conditions and stateful Protocols require a lifetime.

Step 5: Create protocols/_template/PROTOCOL.md with valid frontmatter and these sections:

- Purpose
- Preconditions
- Procedure
- Stop and Exit Behavior
- Artifact Contract
- Evidence Policy
- Safety Boundaries

Step 6: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/schemas/test_protocol_schema.py
    git add schemas protocols/_template tests/schemas tests/fixtures
    git commit -m "feat: define canonical protocol schema"

Expected: 2 passing tests.

### Task 4: Implement the Protocol loader

Files:

- Create: src/thinking_protocols/errors.py
- Create: src/thinking_protocols/protocols.py
- Test: tests/test_protocols.py

Step 1: Write tests for valid frontmatter, non-empty body, a 64-character SHA-256 digest, missing frontmatter, invalid YAML, and empty body.

Step 2: Run tests.

    .\.venv\Scripts\python.exe -m pytest tests/test_protocols.py

Expected: FAIL because the loader is absent.

Step 3: Implement immutable Protocol data:

    @dataclass(frozen=True)
    class Protocol:
        path: Path
        metadata: dict[str, Any]
        body: str
        digest: str

Step 4: Implement load_protocol(path). It must:

- read UTF-8;
- require a leading YAML frontmatter delimiter;
- parse YAML into a mapping;
- require a non-empty Markdown body;
- calculate SHA-256 over the complete source;
- raise ProtocolParseError with the file path on failure.

Step 5: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_protocols.py
    git add src/thinking_protocols tests/test_protocols.py
    git commit -m "feat: load protocol definitions"

### Task 5: Define the Artifact envelope and schemas

Files:

- Create: schemas/artifacts/envelope.v1.schema.json
- Create: schemas/artifacts/clarified_problem.v1.schema.json
- Create: schemas/artifacts/claim_set.v1.schema.json
- Create: schemas/artifacts/verified_claims.v1.schema.json
- Create: schemas/artifacts/option_set.v1.schema.json
- Create: schemas/artifacts/decision_context.v1.schema.json
- Create: schemas/artifacts/decision_memo.v1.schema.json
- Create: schemas/artifacts/experiment_plan.v1.schema.json
- Create: tests/fixtures/artifacts/*.v1.json
- Test: tests/schemas/test_artifact_schemas.py

Step 1: Write a parametrized test that loads every schema and matching fixture and calls jsonschema.validate.

Step 2: Run it.

    .\.venv\Scripts\python.exe -m pytest tests/schemas/test_artifact_schemas.py

Expected: seven missing-file failures.

Step 3: Define the common envelope fields:

- type;
- schema_version;
- produced_by.protocol;
- produced_by.protocol_version;
- provenance.input_artifacts;
- provenance.sources;
- uncertainty.level;
- uncertainty.unresolved;
- payload.

Do not require timestamps or random IDs in v1 because they reduce determinism without helping routing.

Step 4: Define minimum payloads:

- clarified_problem: original, reframed, confirmed facts, unverified assumptions, key variables, next actionable question.
- claim_set: atomic claims tagged factual_claim, inference, or value_judgment.
- verified_claims: verdict, evidence, source date, scope, and remaining uncertainty.
- option_set: at least two distinct options.
- decision_context: goal, constraints, preferences, reversibility.
- decision_memo: strongest cases, decisive variables, recommendation, conditions, uncertainty.
- experiment_plan: hypothesis, action, budget, duration, metrics, continue threshold, stop threshold, information gain.

Reject unknown top-level properties.

Step 5: Add concise fictional fixtures and run tests.

    .\.venv\Scripts\python.exe -m pytest tests/schemas/test_artifact_schemas.py

Expected: 7 passed.

Step 6: Commit.

    git add schemas/artifacts tests/schemas tests/fixtures/artifacts
    git commit -m "feat: add versioned artifact contracts"

### Task 6: Implement repository validation

Files:

- Create: src/thinking_protocols/validation.py
- Test: tests/test_validation.py

Step 1: Write failing tests for:

- valid Protocol;
- Protocol schema error with stable path;
- unknown consumed Artifact;
- unknown produced Artifact;
- unknown capability;
- duplicate Protocol ID;
- duplicate producer ambiguity without an explicit priority.

Step 2: Run tests and verify import failure.

Step 3: Implement immutable ValidationIssue and ValidationResult objects. Every issue has code, path, and message. Tests assert error codes rather than complete prose.

Step 4: Implement schema validation followed by cross-reference validation over all Protocols and Artifact schema filenames.

Step 5: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_validation.py
    git add src/thinking_protocols/validation.py tests/test_validation.py
    git commit -m "feat: validate protocol repository contracts"

### Task 7: Author the four pilot Protocols independently

Files:

- Create: protocols/socratic-questioning/PROTOCOL.md
- Create: protocols/socratic-questioning/examples/clarified-problem.json
- Create: protocols/socratic-questioning/evals.yaml
- Create corresponding PROTOCOL.md, examples, and evals.yaml under:
  - protocols/fact-checking/
  - protocols/steelman-both-sides/
  - protocols/minimum-experiment/
- Test: tests/test_pilot_protocols.py

Step 1: Write a test requiring exactly the four pilot IDs and validating the repository.

Step 2: Run it and verify failure because the pilots are absent.

Step 3: Author Socratic Questioning:

- primary role clarify;
- iterative conversation state;
- maximum six substantive questions;
- one question per turn;
- early exit when another answer is unlikely to change the reframing;
- produces clarified_problem.v1;
- no solution until the user confirms the reframing;
- no request for hidden chain-of-thought.

Step 4: Author Fact Checking:

- primary role verify, secondary role research;
- requires web.search, optionally web.open and files.read;
- missing required web capability blocks external fact verification;
- consumes claim_set.v1 when available;
- produces verified_claims.v1;
- separates facts, inferences, and values;
- prefers primary sources and records date, context, conflict, scope, and uncertainty;
- never substitutes model memory for claimed external verification.

Step 5: Author Steelman Both Sides:

- primary role decide, secondary roles clarify and reason;
- consumes option_set.v1 and decision_context.v1 when available;
- asks no more than one decisive follow-up question;
- produces decision_memo.v1;
- rejects falsely binary or indistinct options.

Step 6: Author Minimum Experiment:

- primary role experiment;
- one-shot and turn-scoped in v0.1.0;
- consumes decision_memo.v1 when available;
- produces experiment_plan.v1;
- requires reversible bounded action, metrics, continue and stop thresholds, resource budget, and expected information gain;
- excludes persistent tracking.

Step 7: Add evals for should_trigger, should_not_trigger, missing_input, early_stop, and unsafe_or_sensitive. Fact Checking also requires missing_required_capability.

Step 8: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_pilot_protocols.py tests/schemas
    git add protocols tests/test_pilot_protocols.py
    git commit -m "feat: add four pilot cognitive protocols"

### Task 8: Generate the deterministic registry

Files:

- Create: src/thinking_protocols/registry.py
- Create: generated/.gitkeep
- Test: tests/test_registry.py

Step 1: Write tests for ID ordering, one canonical metadata record per Protocol, source digest, byte determinism, and stale generated output.

Step 2: Run tests and verify failure.

Step 3: Implement registry records containing:

- id and version;
- lifecycle status;
- primary and secondary epistemic roles;
- interaction mode;
- required capabilities;
- consumes and produces;
- source digest.

Sort Protocols and all set-like arrays. Serialize UTF-8 with LF newlines and deterministic PyYAML settings.

Step 4: Generate twice and compare bytes.

    .\.venv\Scripts\python.exe -m thinking_protocols.cli build-registry
    .\.venv\Scripts\python.exe -m pytest tests/test_registry.py

Expected: generated/registry.yaml exists and tests pass.

Step 5: Commit.

    git add src/thinking_protocols/registry.py generated tests/test_registry.py
    git commit -m "feat: generate deterministic protocol registry"

### Task 9: Implement the conservative Router

Files:

- Create: src/thinking_protocols/router.py
- Test: tests/test_router.py

Step 1: Write failing tests:

- simple question returns direct_answer;
- explicit Protocol request is honored;
- desired Artifact selects its smallest producer;
- existing Artifact is not reproduced;
- only one prerequisite may be added;
- missing required capability blocks;
- iterative Protocol requires user consent;
- no decision returns more than two Protocol IDs.

Step 2: Define immutable RoutingRequest and RoutingDecision objects. RoutingRequest contains explicit_protocol, desired_artifact, primary_role, available_artifacts, available_capabilities, allow_iterative, and complexity.

Step 3: Implement fixed precedence:

1. explicit Protocol;
2. direct answer for simple requests without a desired Artifact;
3. exact Artifact producer;
4. primary-role match;
5. at most one missing Artifact producer;
6. capability and consent checks.

Do not call an LLM. Break ties lexicographically in v1 and report a tie reason code.

Step 4: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_router.py
    git add src/thinking_protocols/router.py tests/test_router.py
    git commit -m "feat: add conservative artifact-aware router"

### Task 10: Implement the Generic Adapter

Files:

- Create: adapters/generic/adapter.yaml
- Create: adapters/generic/templates/prompt.md.j2
- Create: src/thinking_protocols/adapters.py
- Create: dist/.gitkeep
- Test: tests/test_generic_adapter.py

Step 1: Write tests requiring one Markdown file per pilot, complete canonical body, version and digest metadata, preserved capability and stop contracts, and byte-identical repeat builds.

Step 2: Define adapter.yaml:

    id: generic
    output: dist/generic
    supports:
      commands: false
      skills: false
      persistent_state: false
      tool_binding: false
    template: templates/prompt.md.j2

Step 3: Implement rendering with Jinja2 StrictUndefined, LF normalization, deterministic ordering, and write-only-when-changed behavior.

Step 4: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_generic_adapter.py
    git add adapters/generic src/thinking_protocols/adapters.py dist tests/test_generic_adapter.py
    git commit -m "feat: compile generic protocol prompts"

### Task 11: Implement the Codex Adapter and conformance checks

Files:

- Create: adapters/codex/adapter.yaml
- Create: adapters/codex/templates/SKILL.md.j2
- Create: src/thinking_protocols/conformance.py
- Test: tests/test_codex_adapter.py
- Test: tests/test_conformance.py

Step 1: Write tests requiring output at dist/codex/skills/<protocol-id>/SKILL.md with valid discovery frontmatter, source version, digest, capabilities, procedure, stop conditions, and Artifact contract.

Step 2: Write conformance tests over these invariant fields:

- id and version;
- interaction and state;
- capabilities;
- consumes and produces;
- phases and stop_conditions;
- safety.

Step 3: Implement the Codex manifest and template. Codex-specific discovery and tool mappings are allowed; semantic defaults are not.

Step 4: Implement conformance comparison by parsing a generated machine-readable invariant block. Compare normalized structures, not Markdown wording. Report the exact semantic path on drift.

Step 5: Run tests and commit.

    .\.venv\Scripts\python.exe -m pytest tests/test_codex_adapter.py tests/test_conformance.py
    git add adapters/codex src/thinking_protocols/conformance.py tests
    git commit -m "feat: compile conformant Codex skills"

### Task 12: Add CLI, end-to-end tests, and CI

Files:

- Create: src/thinking_protocols/cli.py
- Create: tests/test_cli.py
- Create: tests/e2e/test_decision_chain.py
- Create: tests/e2e/test_direct_answer_policy.py
- Create: tests/e2e/test_missing_web_capability.py
- Create: .github/workflows/ci.yml
- Create: CONTRIBUTING.md

Step 1: Write CLI tests for:

- thinking-protocols validate;
- thinking-protocols build-registry;
- thinking-protocols build --adapter generic;
- thinking-protocols build --adapter codex;
- thinking-protocols check-generated.

Success exits 0; validation or stale-output failure exits 1.

Step 2: Implement argparse commands as thin calls into existing modules. check-generated builds into a temporary directory and compares bytes without overwriting tracked files.

Step 3: Write an end-to-end fixture chain:

    clarified_problem.v1
      -> verified_claims.v1
      -> decision_memo.v1
      -> experiment_plan.v1

At every stage, assert that the Router chooses only the next smallest producer.

Step 4: Add at least ten simple requests spanning facts, formatting, translation, and arithmetic. Every one must return direct_answer with no Protocol.

Step 5: Request verified_claims.v1 without web.search. Assert blocked, name the missing capability, and do not substitute another Protocol.

Step 6: Configure GitHub Actions on Windows and Ubuntu with Python 3.12. Install .[dev], run tests, validate Protocols, and check generated output.

Step 7: Write CONTRIBUTING.md with this order:

1. Copy protocols/_template/PROTOCOL.md.
2. Write trigger and non-trigger evals first.
3. Add or reuse Artifact schemas.
4. Run validation.
5. Regenerate registry and distributions.
6. Run conformance and full tests.
7. Never paste third-party Prompt bodies.

Step 8: Run all checks.

    .\.venv\Scripts\python.exe -m pytest
    .\.venv\Scripts\thinking-protocols.exe validate
    .\.venv\Scripts\thinking-protocols.exe build-registry
    .\.venv\Scripts\thinking-protocols.exe build --adapter generic
    .\.venv\Scripts\thinking-protocols.exe build --adapter codex
    .\.venv\Scripts\thinking-protocols.exe check-generated

Expected: all commands exit 0.

Step 9: Commit.

    git add src tests .github CONTRIBUTING.md generated dist
    git commit -m "ci: verify protocol builds and routing behavior"

### Task 13: Perform the v0.1.0 release audit

Files:

- Modify: README.md
- Create: CHANGELOG.md
- Create only after owner decision: LICENSE or separate code/content license files

Step 1: Run the release audit.

    .\.venv\Scripts\python.exe -m pytest --cov=thinking_protocols --cov-report=term-missing
    .\.venv\Scripts\thinking-protocols.exe validate
    .\.venv\Scripts\thinking-protocols.exe check-generated
    git status --short

Expected: tests and checks pass; only intentional release-document changes remain.

Step 2: Audit third-party text.

    rg -n "原文|prompt 原文|CC BY-NC|完整转载" .

Expected: matches occur only in provenance, boundary tests, or independent notes. No third-party Prompt corpus exists.

Step 3: Complete README.md with installation, validation, builds, pilot Protocols, direct-answer default, Adapter invariants, generated-file policy, and non-goals.

Step 4: Add CHANGELOG.md for 0.1.0.

Step 5: Make licensing an explicit owner decision before public release. Do not inherit CC BY-NC 4.0 from the referenced repository. Whichever license is selected must exclude third-party source material identified in NOTICE.md.

Step 6: Run final verification and commit.

    .\.venv\Scripts\python.exe -m pytest
    .\.venv\Scripts\thinking-protocols.exe validate
    .\.venv\Scripts\thinking-protocols.exe check-generated
    git add README.md CHANGELOG.md NOTICE.md LICENSE*
    git commit -m "docs: prepare thinking protocols v0.1.0"

## Deferred until after v0.1.0

- Migrate the remaining eight independently rewritten Protocols.
- Add Horizontal-Vertical Analysis as a full Research Workflow.
- Add Claude and WorkBuddy Adapters after verifying their current formats.
- Add persistent state and experiment tracking.
- Add sensitive self-exploration only after privacy and non-diagnostic safeguards.
- Add semantic or LLM-assisted routing only if deterministic routing measurements justify it.
- Add an interactive UI or hosted service.

## Definition of done

- Four pilot Protocols validate against the canonical Schema.
- Seven versioned Artifact schemas validate representative instances.
- generated/registry.yaml is deterministic and source-derived.
- Generic and Codex builds are deterministic and semantically conformant.
- Router defaults to direct answers and returns no more than two Protocols.
- Missing required capabilities produce an explicit blocked result.
- End-to-end Artifact-driven routing succeeds without a super-pipeline.
- CI passes on Windows and Ubuntu.
- No complete third-party Prompt text is stored.
- Licensing boundaries are documented before public release.
