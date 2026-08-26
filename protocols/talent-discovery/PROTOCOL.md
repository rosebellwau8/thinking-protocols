---
id: talent-discovery
version: 0.1.0
lifecycle: draft
source_category: self_exploration
epistemic_role:
  primary: clarify
  secondary:
    - reason
    - experiment
interaction:
  mode: iterative
  max_turns: 8
state:
  required: true
  lifetime: conversation
capabilities:
  required: []
  optional:
    - files.read
  on_missing: degrade
inputs:
  required:
    - exploration_goal
  optional:
    - disclosure_boundaries
    - behavior_examples
    - external_feedback
consumes: []
produces: []
phases:
  - id: consent
    objective: Confirm the exploration goal, optional boundaries, skip rights, question limit, and non-diagnostic scope.
  - id: observe
    objective: Gather concrete evidence from repeated behavior, long-term interest, learning speed, voluntary effort, feedback, and outcomes.
  - id: distinguish
    objective: Separate liking, familiarity, forced practice, access advantage, and demonstrated capability.
  - id: challenge
    objective: Seek counterexamples and summarize the strength and limits of each emerging pattern.
  - id: synthesize
    objective: Form provisional capability, interest, and behavior-pattern hypotheses without personality labels.
  - id: test
    objective: Propose small real-world tests that could confirm, refine, or reject the hypotheses.
stop_conditions:
  - The user asks to stop, skip the workflow, or withdraws consent.
  - Eight substantive questions have been asked.
  - Additional questions are unlikely to change the evidence-weighted hypotheses materially.
  - The request becomes clinical diagnosis or disclosure would exceed the user's stated boundaries.
use_when:
  - The user explicitly consents to a bounded exploration of possible talents using real behavior, feedback, outcomes, and counterexamples.
avoid_when:
  - The user wants a personality or clinical diagnosis, a deterministic career label, or a direct answer that does not require sensitive iterative exploration.
safety:
  - Present outputs as hypotheses for real-world validation, never as diagnosis or fixed identity.
  - Allow any question to be skipped without pressure or penalty.
  - Ask at most one substantive question per turn and never exceed eight.
  - Do not request hidden chain-of-thought or unnecessary sensitive details.
  - Keep state conversation-scoped and do not persist the exploration by default.
  - Summarize evidence strength, gaps, and counterexamples before conclusions.
source:
  relationship: inspiration_for_independent_rewrite
  references:
    - kazike-12-prompts
---

# Talent Discovery

## Purpose

Develop provisional, reality-testable hypotheses about capability, interest, and recurring behavior patterns from concrete evidence, without diagnosing or assigning a fixed identity.

## Preconditions

The user must state an exploration goal and consent to an iterative workflow. Explain that any question may be skipped, the workflow asks at most eight substantive questions, state lasts only for the conversation, and the result is not psychological or clinical assessment.

## Procedure

Ask one high-information question per turn. Prefer concrete episodes over self-ratings: activities resumed voluntarily over time, unusually fast learning, tasks that sustain energy, repeated deliberate effort, problems others seek the user out to solve, credible feedback, and observable outcomes. Ask only for detail needed to distinguish hypotheses.

Keep separate ledgers for interest, familiarity, forced practice, demonstrated skill, learning rate, voluntary persistence, access or privilege, feedback, and results. A frequently practiced activity is not automatically liked or talented; enjoyment is not automatically skill; success may reflect opportunity or team contribution.

Periodically summarize candidate patterns with supporting evidence, contradictory evidence, alternatives, and confidence. Invite correction. Stop early when another answer has low expected information value. Before synthesis, actively seek at least one counterexample to each strong hypothesis.

Return a small set of provisional hypotheses, evidence-strength notes, counterexamples, environments where each pattern may or may not appear, and low-risk real-world tests. Do not convert sparse answers into a permanent vocation or identity.

## Stop and Exit Behavior

Stop immediately on withdrawal or after eight substantive questions. On early exit, provide only a bounded evidence summary if useful. If the user requests diagnosis, decline that part and offer non-diagnostic behavior exploration.

## Artifact Contract

This Protocol produces terminal output and no persistent sensitive Artifact. The conversation summary includes hypotheses, evidence strength, counterexamples, uncertainty, and optional experiments.

## Evidence Policy

Treat recollections and external feedback as evidence with provenance and limits. Favor repeated behavior and observable outcomes over flattering labels. Reality tests are for learning, not proof of personal worth.

## Safety Boundaries

Do not diagnose mental illness, personality disorders, or clinical traits. Do not pressure disclosure, retain sensitive profiles, claim destiny, or imply that a short conversation establishes stable identity.
