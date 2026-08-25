---
id: minimum-experiment
version: 0.1.0
lifecycle: draft
source_category: experiment_design
epistemic_role:
  primary: experiment
  secondary:
    - decide
interaction:
  mode: one_shot
state:
  required: false
capabilities:
  required: []
  optional:
    - files.read
    - code.execute
  on_missing: degrade
inputs:
  required:
    - candidate_action
  optional:
    - constraints
consumes:
  - decision_memo.v1
produces:
  - experiment_plan.v1
phases:
  - id: hypothesize
    objective: Convert the decision uncertainty into a falsifiable hypothesis.
  - id: bound
    objective: Define the smallest reversible action, duration, and resource budget.
  - id: measure
    objective: Define metrics, continue and stop thresholds, and expected information gain.
stop_conditions:
  - The action is not reversible or cannot be bounded safely.
  - Metrics or explicit thresholds cannot be defined.
  - A complete one-shot experiment plan has been produced.
use_when:
  - The user can reduce a decision uncertainty through a small reversible action.
avoid_when:
  - The proposed action is irreversible, unsafe, unbounded, or requires persistent tracking.
safety:
  - Keep the action reversible, resource-bounded, and time-bounded.
  - Define both continue and stop thresholds before action begins.
  - Do not create persistent tracking or monitoring in v0.1.0.
source:
  relationship: inspiration_for_independent_rewrite
  references:
    - kazike-12-prompts
---

# Minimum Experiment

## Purpose

Convert decision uncertainty into the smallest safe, reversible action that yields decision-relevant information.

## Preconditions

A candidate action or `decision_memo.v1` is required. The action must be reversible and capable of fitting within a stated time and resource budget. This Protocol is one-shot and turn-scoped.

## Procedure

State one falsifiable hypothesis tied to the unresolved decision variable. Select the smallest action that can produce useful evidence without creating an irreversible commitment. Bound the duration, money, effort, access, and exposure.

Choose observable metrics. Define a continue threshold and a stop threshold before execution, ensuring they do not overlap. State the expected information gain: what decision would become easier after the result and which uncertainty may remain.

Return the plan only. Do not start persistent tracking, schedule monitoring, or imply that future results will be collected automatically.

## Stop and Exit Behavior

Block when the action is unsafe, irreversible, or unbounded, or when meaningful metrics and thresholds cannot be defined. Otherwise stop after one complete experiment plan.

## Artifact Contract

Produce `experiment_plan.v1` with hypothesis, bounded action, budget, duration, metrics, continue threshold, stop threshold, and expected information gain.

## Evidence Policy

Use available decision evidence to set realistic thresholds. Label estimates and avoid claiming that the experiment proves more than its scope permits.

## Safety Boundaries

Do not prescribe harmful tests, bypass consent, create persistent surveillance, or exceed the declared budget and duration.
