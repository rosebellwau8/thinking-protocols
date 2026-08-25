---
id: protocol-template
version: 0.1.0
lifecycle: draft
source_category: template
epistemic_role:
  primary: clarify
  secondary: []
interaction:
  mode: one_shot
state:
  required: false
capabilities:
  required: []
  optional: []
  on_missing: block
inputs:
  required:
    - user_request
  optional: []
consumes: []
produces: []
phases:
  - id: assess
    objective: Assess the request against the Protocol contract.
  - id: execute
    objective: Execute the smallest sufficient procedure.
stop_conditions:
  - The declared output contract is satisfied.
use_when:
  - Replace with a specific positive trigger.
avoid_when:
  - Replace with a specific negative trigger.
safety:
  - Stop when a required safety boundary cannot be maintained.
source:
  relationship: original
  references: []
---

# Protocol Template

## Purpose

State the outcome this Protocol is designed to produce.

## Preconditions

List required inputs, capabilities, consent, and any assumptions that must hold.

## Procedure

Describe the ordered phases without relying on hidden reasoning.

## Stop and Exit Behavior

Define success, early-exit, blocking, and maximum-effort conditions.

## Artifact Contract

Describe consumed and produced Artifact types and the obligations for each field.

## Evidence Policy

Explain what evidence is required, how sources are prioritized, and how uncertainty is recorded.

## Safety Boundaries

State prohibited behavior, escalation conditions, and privacy or sensitivity constraints.
