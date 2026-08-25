---
name: minimum-experiment
description: >-
  Apply the minimum-experiment cognitive Protocol when The user can reduce a decision uncertainty through a small reversible action.
metadata:
  source_version: "0.1.0"
  source_digest: "b84f893ede4c01fe60036013f42a2212e64c816e7aef923deaefdc5b30eb9d36"
  required_capabilities: []
---

# minimum-experiment

## Capability Contract

Required:

- None


Optional:

- `code.execute`

- `files.read`


If a required capability is missing, apply `degrade`.

## Stop Conditions


- The action is not reversible or cannot be bounded safely.

- Metrics or explicit thresholds cannot be defined.

- A complete one-shot experiment plan has been produced.


## Artifact Contract

Consumes:

- `decision_memo.v1`


Produces:

- `experiment_plan.v1`


## Procedure

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

<!-- thinking-protocols-invariants
{"capabilities":{"on_missing":"degrade","optional":["code.execute","files.read"],"required":[]},"consumes":["decision_memo.v1"],"id":"minimum-experiment","interaction":{"mode":"one_shot"},"phases":[{"id":"hypothesize","objective":"Convert the decision uncertainty into a falsifiable hypothesis."},{"id":"bound","objective":"Define the smallest reversible action, duration, and resource budget."},{"id":"measure","objective":"Define metrics, continue and stop thresholds, and expected information gain."}],"produces":["experiment_plan.v1"],"safety":["Keep the action reversible, resource-bounded, and time-bounded.","Define both continue and stop thresholds before action begins.","Do not create persistent tracking or monitoring in v0.1.0."],"state":{"required":false},"stop_conditions":["The action is not reversible or cannot be bounded safely.","Metrics or explicit thresholds cannot be defined.","A complete one-shot experiment plan has been produced."],"version":"0.1.0"}
thinking-protocols-invariants -->
