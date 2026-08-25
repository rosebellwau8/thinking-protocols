---
id: fact-checking
version: 0.1.0
lifecycle: draft
source_category: evidence_verification
epistemic_role:
  primary: verify
  secondary:
    - research
interaction:
  mode: one_shot
state:
  required: false
capabilities:
  required:
    - web.search
  optional:
    - web.open
    - files.read
  on_missing: block
inputs:
  required:
    - claims
  optional:
    - verification_scope
consumes:
  - claim_set.v1
produces:
  - verified_claims.v1
phases:
  - id: classify
    objective: Split the input into atomic factual claims, inferences, and value judgments.
  - id: source
    objective: Find dated primary evidence within the requested scope.
  - id: compare
    objective: Compare sources and record conflicts, context, and limitations.
  - id: report
    objective: Assign verdicts and preserve remaining uncertainty.
stop_conditions:
  - Every factual claim has a scoped verdict or is explicitly unverified.
  - Required web search capability is unavailable.
  - Further searching is unlikely to change a verdict within the requested scope.
use_when:
  - The user asks to verify externally checkable claims or requests evidence-backed fact checking.
avoid_when:
  - The request is purely interpretive, a value judgment, or answerable without claiming external verification.
safety:
  - Never substitute model memory for claimed external verification.
  - Keep facts, inferences, and value judgments visibly separate.
  - Record source date, context, conflict, scope, and uncertainty.
source:
  relationship: inspiration_for_independent_rewrite
  references:
    - kazike-12-prompts
---

# Fact Checking

## Purpose

Evaluate externally checkable claims against dated evidence while keeping inference and values distinct from facts.

## Preconditions

At least one claim and the `web.search` capability are required. A `claim_set.v1` Artifact may supply already-atomic claims. If required web search is unavailable, block external verification instead of answering from memory.

## Procedure

Classify each statement as a factual claim, inference, or value judgment. Verify only factual claims; explain that inferences need supporting premises and values cannot be proven as facts.

Search for the strongest available primary sources first. Use secondary sources only to locate, contextualize, or contrast primary evidence. For each factual claim, record the evidence, source date, applicable scope, relevant context, and any material conflict between sources. Assign a verdict of verified, refuted, mixed, or unverified, and state what uncertainty remains.

## Stop and Exit Behavior

Stop when every factual claim has a scoped verdict, when further search is unlikely to change the result, or immediately when required web search is unavailable. A blocked result must name `web.search` as missing.

## Artifact Contract

Produce `verified_claims.v1`. Each claim record includes its verdict, evidence, source date, scope, and remaining uncertainty. Preserve input Artifact and source provenance.

## Evidence Policy

Prefer primary, current, and scope-matched sources. Describe conflicts rather than averaging them away. Never label model memory as external verification.

## Safety Boundaries

Avoid overstating certainty, respect privacy and access restrictions, and do not turn value judgments into factual verdicts.
