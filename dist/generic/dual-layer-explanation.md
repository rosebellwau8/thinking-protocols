---
protocol_id: dual-layer-explanation
source_version: 0.1.0
source_digest: e4d27172d213a4c52b6bab6353ffb64b97f254c3f0424f7db67bdaf7219dcbb5
adapter: generic
---

# dual-layer-explanation

## Capability Contract

Required:

- None


Optional:

- files.read


On missing required capability: `degrade`

## Interaction and State Contract

- Interaction mode: `one_shot`
- State required: `false`


## Stop Conditions


- The topic is missing or too ambiguous to identify without one clarifying input.

- Both layers and their consistency check are complete.

- A factual foundation cannot be established, in which case uncertainty is stated instead of filled by invention.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Canonical Procedure

# Dual-Layer Explanation

## Purpose

Explain one topic at two compatible resolutions: a compact intuitive layer for orientation and a precise layer that exposes the real mechanism, terminology, conditions, and limits.

## Preconditions

A topic is required. Audience background and desired depth may be supplied but are not reasons to start an interview. If one ambiguity would materially change the subject being explained, request that input; otherwise state a narrow interpretation and proceed. External capabilities are not required.

## Procedure

Set a shared factual boundary before drafting. In the intuitive layer, name the central idea in plain language, minimize jargon, and use at most the analogies that preserve the causal structure. Mark each important simplification.

In the precise layer, explain the same claims with the relevant mechanism, vocabulary, assumptions, edge cases, and failure conditions. Do not silently replace the intuitive claim with a different technical claim. Finish with a short bridge that maps the simple concepts to the precise ones and names where any analogy breaks.

Prefer practical depth. Expand into a long tutorial only when the user or runtime requests it.

## Stop and Exit Behavior

Stop after both layers and the alignment check are complete. If the topic is absent, request it. If reliable factual grounding is unavailable, bound the explanation and label uncertainty rather than presenting recall as verified fact.

## Artifact Contract

This Protocol produces terminal reader-facing output, not a typed Artifact. A useful response contains an intuitive layer, a precise layer, and a consistency or analogy-limit note.

## Evidence Policy

Use supplied material when available and attribute it accurately. For current or externally checkable claims that require verification, state the evidence gap or hand off to an evidence-capable workflow; do not describe model memory as current research.

## Safety Boundaries

Accuracy has priority over elegance. Do not hide material exceptions, invent certainty, or reveal private reasoning traces.
