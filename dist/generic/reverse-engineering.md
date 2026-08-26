---
protocol_id: reverse-engineering
source_version: 0.1.0
source_digest: 28c0cf24dce796b47aa0e49ee9f22abaf14a615ef846b9301f48ef129e03e87c
adapter: generic
---

# reverse-engineering

## Capability Contract

Required:

- None


Optional:

- files.read

- web.open

- web.search


On missing required capability: `degrade`

## Interaction and State Contract

- Interaction mode: `one_shot`
- State required: `false`


## Stop Conditions


- No existing target or observable outcome has been supplied.

- Evidence cannot distinguish a key mechanism, in which case competing hypotheses and the gap are reported.

- A bounded reconstruction path with tests and failure signals is complete.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Canonical Procedure

# Reverse Engineering

## Purpose

Work backward from an existing outcome to the components, constraints, and candidate mechanisms that produced it, then propose the smallest reconstruction that can test those explanations.

## Preconditions

An inspectable target or observed outcome is required. The target may be described by the user or supported by accessible files and public evidence. For an external or changing system, use available evidence capabilities when needed; without them, narrow the analysis to supplied observations and state the limitation.

## Procedure

First freeze the object and outcome being explained: version, time, context, audience, and success measure. Decompose it into parts, interfaces, sequence, inputs, resources, feedback loops, and constraints. Record what is directly observed separately from what is merely a plausible explanation.

For each important outcome, propose the smallest set of candidate mechanisms and list predictions that would differ between them. Check alternative causes and interactions instead of assigning success to the most visible feature. Classify factors as replicable, adaptable only under stated conditions, or inseparable from context such as timing, reputation, proprietary assets, or luck.

End with a minimal reconstruction: the smallest lawful, safe implementation or experiment that tests the decisive mechanism, including inputs, success signal, failure signal, and what the test cannot establish.

## Stop and Exit Behavior

Stop when the reconstruction path is testable or when the evidence gap prevents choosing among mechanisms. In the latter case, report competing explanations and the next observation needed; do not manufacture a clean causal story.

## Artifact Contract

This Protocol produces terminal output. The report contains the observed target, decomposition, constraints, candidate mechanisms, transferability classification, uncertainties, and minimal reconstruction path.

## Evidence Policy

Prefer direct inspection and primary documentation for external objects. Record source date, version, context, and conflicts. If sources disagree, preserve each scoped claim and explain what evidence would resolve the difference.

## Safety Boundaries

Analyze only material the user is authorized to inspect. Do not facilitate credential theft, protection bypass, unauthorized copying, surveillance, or unsafe replication.
