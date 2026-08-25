---
id: invalid-iterative
version: 0.1.0
lifecycle: draft
source_category: clarification
epistemic_role:
  primary: clarify
  secondary: []
interaction:
  mode: iterative
  max_turns: 2
state:
  required: true
  lifetime: conversation
capabilities:
  required: []
  optional: []
  on_missing: block
inputs:
  required:
    - user_question
  optional: []
consumes: []
produces:
  - clarified_problem.v1
phases:
  - id: question
    objective: Ask one clarifying question.
stop_conditions: []
use_when:
  - The problem statement is ambiguous.
avoid_when:
  - The request is already precise.
safety:
  - Do not request hidden chain-of-thought.
source:
  relationship: original
  references: []
---

# Invalid Iterative Protocol

This fixture is invalid because no stop condition bounds the interaction.

