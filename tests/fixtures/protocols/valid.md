---
id: example-protocol
version: 1.2.3
lifecycle: draft
source_category: decision_support
epistemic_role:
  primary: decide
  secondary:
    - clarify
    - reason
interaction:
  mode: iterative
  max_turns: 3
state:
  required: true
  lifetime: conversation
capabilities:
  required:
    - web.search
  optional:
    - files.read
    - web.open
  on_missing: block
inputs:
  required:
    - user_question
  optional:
    - decision_constraints
consumes:
  - option_set.v1
produces:
  - decision_memo.v1
phases:
  - id: frame
    objective: Establish the decision frame.
  - id: compare
    objective: Compare the strongest cases.
stop_conditions:
  - The decisive variables are explicit.
use_when:
  - A consequential choice has multiple credible options.
avoid_when:
  - The user only needs a simple factual answer.
safety:
  - Keep factual claims distinct from value judgments.
source:
  relationship: inspiration_for_independent_rewrite
  references:
    - kazike-12-prompts
---

# Example Protocol

This fixture has a non-empty canonical procedure body.

