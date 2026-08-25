---
name: socratic-questioning
description: >-
  Apply the socratic-questioning cognitive Protocol when The problem is consequential but ambiguous, underspecified, or framed around an unverified assumption.
metadata:
  source_version: "0.1.0"
  source_digest: "31186063f64df46f74de3af3a5653b6d5fa75b049bee6fd80e18ebec05e80524"
  required_capabilities: []
---

# socratic-questioning

## Capability Contract

Required:

- None


Optional:

- None


If a required capability is missing, apply `block`.

## Stop Conditions


- The user confirms the reframing.

- Another answer is unlikely to change the reframing materially.

- Six substantive questions have been asked.

- The user asks to stop or requests a direct answer.


## Artifact Contract

Consumes:

- None


Produces:

- `clarified_problem.v1`


## Procedure

# Socratic Questioning

## Purpose

Turn an ambiguous problem into a user-confirmed statement that distinguishes facts, assumptions, variables, and the next actionable question.

## Preconditions

The user must provide a problem they are willing to clarify. No external capability is required. Treat user statements as claims, not automatically as verified facts.

## Procedure

First summarize the apparent problem in neutral language and label confirmed facts separately from unverified assumptions. Then select the one question whose answer is most likely to change the framing and ask only that question in the current turn. Do not ask for a hidden reasoning trace.

After each answer, update the working reframing. Stop asking questions early when another answer is unlikely to change it materially. Never exceed six substantive questions. Present the reframed problem, key variables, remaining assumptions, and next actionable question, then ask the user to confirm or correct that reframing.

Do not move into solution generation before confirmation. If the user requests a direct answer or asks to stop, exit immediately with the best bounded summary available.

## Stop and Exit Behavior

Stop on confirmation, diminishing information value, six substantive questions, or an explicit user exit. On an early exit, clearly mark what remains unconfirmed.

## Artifact Contract

Produce `clarified_problem.v1` only after presenting the reframing. Preserve the original problem, confirmed facts, unverified assumptions, key variables, next actionable question, provenance, and unresolved uncertainty.

## Evidence Policy

Attribute facts to the user unless external verification has occurred elsewhere. Never convert a plausible assumption into a confirmed fact.

## Safety Boundaries

Do not solicit hidden chain-of-thought, diagnose the user, pressure disclosure, or continue questioning after consent is withdrawn.

<!-- thinking-protocols-invariants
{"capabilities":{"on_missing":"block","optional":[],"required":[]},"consumes":[],"id":"socratic-questioning","interaction":{"max_turns":6,"mode":"iterative"},"phases":[{"id":"establish","objective":"Restate the problem and separate stated facts from assumptions."},{"id":"question","objective":"Ask the single question most likely to change the framing."},{"id":"reframe","objective":"Propose a concise reframing with key variables and uncertainty."},{"id":"confirm","objective":"Obtain user confirmation before offering any solution direction."}],"produces":["clarified_problem.v1"],"safety":["Ask only one substantive question per turn.","Do not request hidden chain-of-thought or private internal reasoning.","Do not provide a solution until the user confirms the reframing."],"state":{"lifetime":"conversation","required":true},"stop_conditions":["The user confirms the reframing.","Another answer is unlikely to change the reframing materially.","Six substantive questions have been asked.","The user asks to stop or requests a direct answer."],"version":"0.1.0"}
thinking-protocols-invariants -->
