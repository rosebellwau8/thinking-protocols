---
protocol_id: life-design
source_version: 0.1.0
source_digest: 42325a946a73014603d6e8de06a5e8a339400250ec8f46cafb17a99489e6512a
adapter: generic
---

# life-design

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


- The user asks to stop, skips the workflow, or withdraws consent.

- Eight substantive questions have been asked.

- Several feasible hypotheses and bounded next experiments are ready and another question has low information value.

- A high-stakes medical, mental-health, legal, or financial issue requires qualified professional advice.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Canonical Procedure

# Life Design

## Purpose

Turn the user's current reality into several feasible life-design hypotheses and small experiments, rather than a sweeping declaration about identity or destiny.

## Preconditions

The user must provide at least a current-situation sketch and consent to an iterative process. Explain the eight-question maximum, skip rights, conversation-only state, non-diagnostic scope, and professional-advice limits before asking sensitive questions.

## Procedure

Ask one decision-relevant question per turn. Start with reality: roles and responsibilities, fixed commitments, health or energy constraints the user chooses to disclose, resources, deadlines, financial or geographic bounds, current sources of energy and depletion, and prior attempts. Do not assume every constraint is permanent, but do not wish it away.

Clarify value trade-offs through concrete choices rather than abstract labels. Separate immediate stabilization, one-year direction, and longer-horizon possibility. Identify which decisions are reversible, costly to reverse, or effectively irreversible and how uncertainty changes the appropriate commitment.

Generate two to four materially different hypotheses, including a conservative option when appropriate. For each, show fit with values and energy, responsibilities honored, resources needed, opportunity cost, risks, unknowns, reversibility, and evidence that would change the option. Avoid treating a small answer set as a lifetime verdict.

Convert the strongest options into small tests: a conversation, sample project, schedule trial, course, shadowing period, budget rehearsal, or other bounded action. Define duration, cost, learning question, stop signal, and review date. Prefer useful information over symbolic ambition.

## Stop and Exit Behavior

Stop on withdrawal, after eight substantive questions, or early when feasible hypotheses and experiments are ready. If the issue turns on medical, mental-health, legal, or financial advice, bound the planning support and direct the user to a qualified professional for that decision.

## Artifact Contract

This Protocol produces terminal output and no persistent personal Artifact. The output contains current-reality constraints, value trade-offs, multiple hypotheses, reversibility analysis, next experiments, review criteria, and uncertainty.

## Evidence Policy

Attribute personal facts to the user and mark interpretations as hypotheses. Use concrete behavior and outcomes where possible. Do not elevate a preference stated once into a stable identity claim.

## Safety Boundaries

Do not diagnose, pressure disclosure, persist a personal dossier, make irreversible choices for the user, or present this workflow as therapy or professional medical, legal, or financial advice.
