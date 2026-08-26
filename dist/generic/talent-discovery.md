---
protocol_id: talent-discovery
source_version: 0.1.0
source_digest: 1b89d8869111eb0b05987721acad0f8385d0fd829d0e59d691a00ca4ddd40855
adapter: generic
---

# talent-discovery

## Capability Contract

Required:

- None


Optional:

- files.read


On missing required capability: `degrade`

## Interaction and State Contract

- Interaction mode: `iterative`
- State required: `true`

- State lifetime: `conversation`


## Stop Conditions


- The user asks to stop, skip the workflow, or withdraws consent.

- Eight substantive questions have been asked.

- Additional questions are unlikely to change the evidence-weighted hypotheses materially.

- The request becomes clinical diagnosis or disclosure would exceed the user's stated boundaries.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Canonical Procedure

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
