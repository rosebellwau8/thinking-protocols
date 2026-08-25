---
protocol_id: fact-checking
source_version: 0.1.0
source_digest: 440113d8de5ee41e749b2250f55511d9175ef42ca60db436079961c63e9e69d1
adapter: generic
---

# fact-checking

## Capability Contract

Required:

- web.search


Optional:

- files.read

- web.open


On missing required capability: `block`

## Interaction and State Contract

- Interaction mode: `one_shot`
- State required: `false`


## Stop Conditions


- Every factual claim has a scoped verdict or is explicitly unverified.

- Required web search capability is unavailable.

- Further searching is unlikely to change a verdict within the requested scope.


## Artifact Contract

Consumes:

- claim_set.v1


Produces:

- verified_claims.v1


## Canonical Procedure

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
