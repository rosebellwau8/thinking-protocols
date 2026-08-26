---
id: expert-panel
version: 0.1.0
lifecycle: draft
source_category: multi_perspective_analysis
epistemic_role:
  primary: reason
  secondary:
    - decide
interaction:
  mode: one_shot
state:
  required: false
capabilities:
  required: []
  optional:
    - web.search
    - web.open
    - files.read
  on_missing: degrade
inputs:
  required:
    - issue
  optional:
    - evidence
    - decision_criteria
    - requested_roles
consumes: []
produces: []
phases:
  - id: ground
    objective: Establish the issue, shared evidence, assumptions, constraints, and decision criteria.
  - id: compose
    objective: Select distinct analytical roles and declare the variables each role is responsible for examining.
  - id: deliberate
    objective: Let each role interpret the common evidence and state genuine agreements and disagreements.
  - id: audit
    objective: Identify unsupported claims, shared blind spots, missing roles, and evidence gaps.
  - id: synthesize
    objective: Integrate consensus, conflicts, omissions, and a conditional overall judgment.
stop_conditions:
  - The issue is missing or no distinct analytical perspectives are relevant.
  - A real-world factual dispute lacks evidence, in which case the gap is stated before role analysis.
  - Consensus, conflicts, omissions, and the integrated judgment are complete.
use_when:
  - The user explicitly asks for several professional or analytical perspectives whose variables and disagreements should be compared and synthesized.
avoid_when:
  - A direct answer or single-domain analysis is sufficient, or the request asks what named real experts actually said without supplying evidence.
safety:
  - Present roles as simulated analytical lenses, never as claims that real experts expressed generated opinions.
  - Use one shared evidence base and do not let role-play substitute for factual evidence.
  - Permit material disagreement instead of forcing theatrical consensus.
  - Mark assumptions, evidence gaps, and omitted perspectives.
source:
  relationship: inspiration_for_independent_rewrite
  references:
    - kazike-12-prompts
---

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
