# Example terminal output

Problem: reduce a fictional support queue.

- Objective: lower median resolution time without increasing reopened cases.
- Fact: 40% of tickets await one missing field. Assumption: users can provide it at submission.
- Removed convention: every ticket must enter the same queue.
- Derivation: validate that field before intake, then route only complete tickets.
- Failure condition: abandon the change if completion rate falls or reopened cases rise.
