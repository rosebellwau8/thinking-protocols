---
protocol_id: cross-domain-transfer
source_version: 0.1.0
source_digest: 0744aff5a3e0a69533e5dc500448053f8057dd301adfcb472ad5d267cedfba0c
adapter: generic
---

# cross-domain-transfer

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


- The target problem or desired outcome is missing.

- Required web search is unavailable.

- No candidate has sufficient structural similarity, in which case no transfer is recommended.

- A bounded, evidence-linked, testable transfer hypothesis and its failure conditions are complete.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Canonical Procedure

# Cross-Domain Transfer

## Purpose

Find an evidence-backed mechanism in another domain whose causal structure may address a target problem, then translate it into a bounded hypothesis rather than a persuasive but superficial analogy.

## Preconditions

A target problem is required. `web.search` is required because candidate domains and external cases must be grounded rather than recalled vaguely. Declare a research cutoff, scope, and target constraints before selecting cases.

## Procedure

Describe the target in mechanism-neutral terms: desired outcome, actors, resources, information flow, incentives, feedback, delays, scale, environment, and known failure modes. Identify which mechanism must change, not merely which result is attractive.

Search for candidate mechanisms in at least two plausible source domains when scope permits. For every candidate, capture primary or authoritative evidence, date, context, actual mechanism, observed outcome, and alternative explanations. Reject candidates selected only because they share words, shapes, or narratives with the target.

Compare structural correspondence: entities, relationships, causal direction, feedback loops, constraints, scale, timescale, and environmental assumptions. Map what transfers, what must be translated, and what does not correspond. Preserve source conflicts and lower confidence when the mechanism itself is disputed.

Return one or more testable transfer hypotheses in the form: under stated target conditions, adapting this mechanism should change this observable outcome because of this mapped causal link. Include a smallest safe test, disconfirmation signal, and boundary conditions.

## Stop and Exit Behavior

Block without `web.search`. Recommend no transfer when candidates are only superficially similar or their mechanism lacks reliable support. Stop when the hypothesis is falsifiable and all important correspondence and failure conditions are explicit.

## Artifact Contract

This Protocol produces terminal output: target mechanism, sourced candidate set, structural comparison, boundary map, selected or rejected transfers, uncertainty, and testable hypotheses.

## Evidence Policy

Use current, scope-matched evidence and prefer primary sources. Record dates, context, and conflicting accounts. Never invent a historical, scientific, or business example to improve the narrative.

## Safety Boundaries

Do not transfer practices that depend on coercion, deception, unsafe experimentation, or incompatible legal and ethical conditions. Analogy never replaces domain-specific professional evidence.
