---
protocol_id: expert-panel
source_version: 0.1.0
source_digest: 2313ebb2ef188fc0582a0da472419b5a8812d45c7a03755b9e6a021a54600fc6
adapter: generic
---

# expert-panel

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


- The issue is missing or no distinct analytical perspectives are relevant.

- A real-world factual dispute lacks evidence, in which case the gap is stated before role analysis.

- Consensus, conflicts, omissions, and the integrated judgment are complete.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Canonical Procedure

# Expert Panel

## Purpose

Analyze one issue through several explicitly defined professional lenses, preserving real disagreement and then forming an integrated judgment without impersonating real people.

## Preconditions

An issue is required. Begin from a shared set of user-supplied or externally verified facts. When current or real-world facts are decisive, obtain evidence before convening roles or label the evidence gap; agreement among generated roles is not verification.

## Procedure

Choose the smallest useful panel, normally three to five roles. Define each role by responsibility and variables, such as safety and failure modes, economics and incentives, operations and constraints, user impact, or governance and externalities. Do not use a famous person's name as a shortcut for a perspective.

Give every role the same facts, scope, and decision criteria. For each, state its interpretation, key concern, preferred action, confidence, and what evidence would change its view. Allow direct disagreement about weights, mechanisms, or acceptable risk.

Audit the panel for correlated assumptions, missing stakeholders, unsupported factual claims, and perspectives excluded by the chosen roles. Synthesize the strongest consensus, unresolved conflicts, overlooked variables, and a conditional overall judgment. Do not decide by vote count.

## Stop and Exit Behavior

Stop when additional roles would repeat existing variables and the synthesis covers consensus, conflict, omissions, and conditions. If the issue is factual rather than interpretive and evidence is absent, state that block instead of simulating certainty.

## Artifact Contract

This Protocol produces terminal output: panel charter, shared evidence, role analyses, disagreement map, blind-spot audit, and integrated judgment.

## Evidence Policy

Roles interpret evidence; they do not create it. Attribute sourced facts outside the role voices, label assumptions, and keep confidence tied to evidence quality.

## Safety Boundaries

Do not fabricate quotations, endorsements, credentials, consensus, or testimony. Do not disguise a generated perspective as medical, legal, financial, or other professional advice from a real practitioner.
