---
name: steelman-both-sides
description: >-
  Apply the steelman-both-sides cognitive Protocol when The user faces a consequential choice between at least two credible options.
metadata:
  source_version: "0.1.0"
  source_digest: "e8f04165e64683067ef4db22b521304a61752ccd2e2c2a07d7f0f853e345605f"
  required_capabilities: []
---

# steelman-both-sides

## Capability Contract

Required:

- None


Optional:

- `files.read`


If a required capability is missing, apply `degrade`.

## Stop Conditions


- The options are falsely binary, indistinct, or missing.

- One decisive missing fact requires a single follow-up question.

- The strongest cases and conditional recommendation are complete.


## Artifact Contract

Consumes:

- `decision_context.v1`

- `option_set.v1`


Produces:

- `decision_memo.v1`


## Procedure

# Steelman Both Sides

## Purpose

Produce a fair decision memo by expressing the strongest credible case for each real option and identifying what should decide between them.

## Preconditions

At least two distinct options are required. An `option_set.v1` and `decision_context.v1` may provide structured inputs. Reject a framing that is falsely binary or whose options are materially indistinct.

## Procedure

Inspect the option set before comparing it. Add an obviously omitted option only when its absence makes the framing false; otherwise stay within scope. State the shared goal, constraints, preferences, and reversibility.

Construct the strongest evidence-compatible case for each option using comparable criteria. Do not manufacture balance when evidence quality differs. Identify the smallest set of variables that could change the choice. If one missing answer is genuinely decisive, ask one follow-up question and exit; do not begin an open-ended interview.

Recommend an option, deferral, or bounded test. State the conditions under which the recommendation changes and the uncertainty that remains.

## Stop and Exit Behavior

Stop on invalid option framing, after one decisive question, or when the strongest cases and conditional recommendation are complete.

## Artifact Contract

Produce `decision_memo.v1` containing the strongest cases, decisive variables, recommendation, conditions, and uncertainty, with available Artifact provenance.

## Evidence Policy

Use the same evidentiary standard for each option. Label preferences and value judgments rather than presenting them as facts.

## Safety Boundaries

Do not create false equivalence, conceal decisive uncertainty, or make irreversible high-stakes choices on the user's behalf.

<!-- thinking-protocols-invariants
{"capabilities":{"on_missing":"degrade","optional":["files.read"],"required":[]},"consumes":["decision_context.v1","option_set.v1"],"id":"steelman-both-sides","interaction":{"mode":"one_shot"},"phases":[{"id":"inspect","objective":"Check that the options are distinct, credible, and not falsely binary."},{"id":"steelman","objective":"Build the strongest fair case for each option under shared evidence."},{"id":"decide","objective":"Identify decisive variables and make a conditional recommendation."}],"produces":["decision_memo.v1"],"safety":["Do not invent symmetry between positions with materially different evidence.","Ask no more than one decisive follow-up question.","Distinguish evidence, inference, preference, and recommendation."],"state":{"required":false},"stop_conditions":["The options are falsely binary, indistinct, or missing.","One decisive missing fact requires a single follow-up question.","The strongest cases and conditional recommendation are complete."],"version":"0.1.0"}
thinking-protocols-invariants -->
