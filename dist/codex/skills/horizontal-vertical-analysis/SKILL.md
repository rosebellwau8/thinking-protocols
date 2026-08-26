---
name: horizontal-vertical-analysis
description: >-
  Apply the horizontal-vertical-analysis cognitive Protocol when The user explicitly requests evidence-backed research that combines historical evolution with comparison to peers, alternatives, or contemporaries.
metadata:
  source_version: "0.1.0"
  source_digest: "8b0abca5f6ff4ab21b4ce1aea2c30fd685b9f08821a3ffed3c761936d0c62b5b"
  required_capabilities: ["web.search"]
---

# horizontal-vertical-analysis

## Capability Contract

Required:

- `web.search`


Optional:

- `files.read`

- `web.open`


If a required capability is missing, apply `block`.

## Stop Conditions


- The research subject or a usable scope is missing.

- Required web search is unavailable.

- The declared cutoff or research budget is reached and material gaps are disclosed.

- Both axes cover the decision-relevant evidence and further searching is unlikely to change the conclusions.


## Artifact Contract

Consumes:

- None


Produces:

- None


## Procedure

# Horizontal-Vertical Analysis

## Purpose

Research a subject on two connected axes: its development through time and its position among comparable or substitutable cases at a declared research cutoff.

## Preconditions

A research subject and `web.search` are required. Before searching, state the research question, cutoff date, time range, comparison logic, context or jurisdiction, and practical depth. If the user omits the cutoff, use the current runtime date and say so. A deep report is an explicit runtime or user preference, not the default.

## Procedure

Build an evidence ledger with title or publisher, source date, publication context, applicable scope, source type, and the claim supported. Search primary records first: official documentation, filings, standards, data, original research, or first-party statements. Use secondary sources for discovery, critique, or context, not as silent replacements for available primary evidence.

On the vertical axis, trace origins, prerequisites, turning points, causal claims, continuities, reversals, and path dependence. Do not turn chronology into causality without support. On the horizontal axis, choose peers, alternatives, substitutes, or contemporaries by an explicit rule and compare them on shared dimensions. Do not cherry-pick only favorable comparators.

Label each substantive statement as fact, inference, or viewpoint. When sources conflict, compare their dates, definitions, methods, incentives, samples, and scopes. Resolve only when evidence warrants it; otherwise retain the conflict and show how conclusions change under each account.

Synthesize where history explains current differences and where current comparison challenges the historical story. Link conclusions to evidence and state confidence, limitations, and applicability.

## Stop and Exit Behavior

Block if `web.search` is unavailable. Otherwise stop at evidence saturation, the declared cutoff, or the research budget. Missing or inaccessible evidence remains an explicit gap and never becomes a model-memory substitute.

## Artifact Contract

This Protocol produces a terminal research report rather than a typed Artifact. It includes scope and cutoff, source ledger, vertical narrative, horizontal comparison, conflict register, synthesis, citations, uncertainty, and limitations.

## Evidence Policy

Time-sensitive claims require evidence available within the declared cutoff. Cite sources near supported conclusions and preserve dates and scopes. Clearly identify inference from multiple sources.

## Safety Boundaries

Respect privacy, access controls, research ethics, and source terms. Do not fabricate citations, flatten disputed evidence into consensus, or extend conclusions beyond their supported population, period, or context.

<!-- thinking-protocols-invariants
{"capabilities":{"on_missing":"block","optional":["files.read","web.open"],"required":["web.search"]},"consumes":[],"id":"horizontal-vertical-analysis","interaction":{"mode":"one_shot"},"phases":[{"id":"scope","objective":"Fix the research question, comparison frame, time and context scope, cutoff, and practical output depth."},{"id":"source","objective":"Collect dated, scope-matched evidence with primary sources first."},{"id":"vertical","objective":"Trace historical evolution, causes, turning points, path dependence, and trend limits."},{"id":"horizontal","objective":"Compare contemporaries, alternatives, substitutes, and relevant peer cases on shared dimensions."},{"id":"reconcile","objective":"Separate facts, inferences, and viewpoints and explicitly resolve or preserve source conflicts."},{"id":"synthesize","objective":"Cross the two axes into evidence-linked conclusions with uncertainty and applicability limits."}],"produces":[],"safety":["Declare a research cutoff before searching and never present model memory as current evidence.","Prefer primary sources and record source date, context, scope, and applicability.","Keep facts, inferences, and viewpoints visibly distinct.","Preserve material source conflicts and explain their effect on conclusions.","Attach evidence and uncertainty to consequential conclusions."],"state":{"required":false},"stop_conditions":["The research subject or a usable scope is missing.","Required web search is unavailable.","The declared cutoff or research budget is reached and material gaps are disclosed.","Both axes cover the decision-relevant evidence and further searching is unlikely to change the conclusions."],"version":"0.1.0"}
thinking-protocols-invariants -->
