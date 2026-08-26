---
id: dual-layer-explanation
version: 0.1.0
lifecycle: draft
source_category: explanation
epistemic_role:
  primary: reason
  secondary:
    - clarify
interaction:
  mode: one_shot
state:
  required: false
capabilities:
  required: []
  optional:
    - files.read
  on_missing: degrade
inputs:
  required:
    - topic
  optional:
    - audience_background
    - desired_depth
    - source_material
consumes: []
produces: []
phases:
  - id: scope
    objective: Define the topic, audience, and factual boundaries shared by both layers.
  - id: intuitive
    objective: Explain the core idea plainly with a bounded and accurate mental model.
  - id: precise
    objective: Explain the same idea with mechanisms, terminology, conditions, and limitations.
  - id: align
    objective: Check that both layers make the same factual claims and expose analogy limits.
stop_conditions:
  - The topic is missing or too ambiguous to identify without one clarifying input.
  - Both layers and their consistency check are complete.
  - A factual foundation cannot be established, in which case uncertainty is stated instead of filled by invention.
use_when:
  - The user explicitly wants both an intuitive explanation and a more precise mechanism-level explanation of the same topic.
avoid_when:
  - A normal short answer, definition, translation, formatting change, or single requested depth is sufficient.
safety:
  - Keep factual claims consistent across both layers.
  - Never use a false analogy merely to make the simple layer memorable.
  - State where an analogy stops matching the mechanism.
  - Do not request or expose hidden chain-of-thought.
source:
  relationship: inspiration_for_independent_rewrite
  references:
    - kazike-12-prompts
---

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
