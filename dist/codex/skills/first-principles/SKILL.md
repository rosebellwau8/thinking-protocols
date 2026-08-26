---
name: first-principles
description: >-
  Apply the first-principles cognitive Protocol when The user explicitly wants to discard inherited assumptions and derive a solution from irreducible facts, constraints, and goals.
metadata:
  source_version: "0.1.0"
  source_digest: "e765343dc7a76cb8e3248f4c75925a5610c5fd3d2616129355b4f6b2f93bfb70"
  required_capabilities: []
---

# first-principles

## Capability Contract

Required:

- None


Optional:

- `files.read`

- `web.open`

- `web.search`


If a required capability is missing, apply `degrade`.

## Stop Conditions


- The problem or objective is missing.

- A required factual foundation cannot be established, in which case assumptions or evidence requests replace derivation.

- At least one feasible derivation and its failure conditions are explicit.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Procedure

# First Principles

## Purpose

Remove unverified conventions and analogies from a problem, identify the smallest defensible set of facts, constraints, and goals, and derive feasible options from that set.

## Preconditions

A problem is required; an objective or success condition must be supplied or narrowly inferred and stated. User statements remain inputs, not automatically verified facts. When a factual premise is both external and decisive, use available evidence capabilities or mark it as an assumption before deriving from it.

## Procedure

Restate the problem without solution-shaped language. List inherited conventions, common analogies, bundled labels, and claims that merely describe how the problem is usually handled. Remove each unless it is a hard constraint or evidence-backed fact.

Build a foundation ledger with four columns: objective, irreducible facts, hard constraints, and explicit assumptions or unknowns. A fact must be supported by the input or evidence; a constraint must state who or what imposes it and whether it can change. Do not call an intuition fundamental because it sounds simple.

Derive candidate actions one link at a time from the ledger. For every link, name the premise it uses. Compare at least one materially different derivation when feasible. Challenge candidates with counterexamples, resource bounds, sensitivity to assumptions, and real implementation constraints. Return the smallest feasible next action and the conditions that would invalidate it.

## Stop and Exit Behavior

If the objective is absent, request it. If decisive foundations remain unknown, stop derivation and present the exact evidence need or explicit assumptions. Otherwise stop when feasible options, derivation links, and failure conditions are clear.

## Artifact Contract

This Protocol produces terminal output: reframed problem, stripped assumptions, foundation ledger, derivations, tests, and bounded next action.

## Evidence Policy

Evidence grounds facts; reasoning connects them. Never use confident prose, consensus, or a familiar analogy as evidence. Label estimates and explain sensitivity to them.

## Safety Boundaries

Do not use a first-principles label to launder speculation, erase legal or safety constraints, or make irreversible high-stakes choices for the user.

<!-- thinking-protocols-invariants
{"capabilities":{"on_missing":"degrade","optional":["files.read","web.open","web.search"],"required":[]},"consumes":[],"id":"first-principles","interaction":{"mode":"one_shot"},"phases":[{"id":"frame","objective":"Define the objective, boundary, success condition, and decision-relevant unknowns."},{"id":"strip","objective":"Remove inherited conventions, labels, analogies, and bundled assumptions from the framing."},{"id":"ground","objective":"Establish irreducible facts, hard constraints, explicit assumptions, and unresolved evidence needs."},{"id":"derive","objective":"Build candidate solutions step by step from the grounded set."},{"id":"challenge","objective":"Test derivations against constraints, counterexamples, sensitivity, and feasible alternatives."}],"produces":[],"safety":["Never relabel plausible guesses as fundamental facts.","Separate evidence, user constraints, assumptions, and derived conclusions.","Request or use evidence when factual foundations are not supplied.","Test each derivation against counterexamples and real constraints."],"state":{"required":false},"stop_conditions":["The problem or objective is missing.","A required factual foundation cannot be established, in which case assumptions or evidence requests replace derivation.","At least one feasible derivation and its failure conditions are explicit."],"version":"0.1.0"}
thinking-protocols-invariants -->
