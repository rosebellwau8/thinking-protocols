# Example terminal output

Target: reduce congestion in a fictional review queue.

- Needed mechanism: smooth bursty arrivals without hiding priority.
- Candidate domain: network congestion control; similarity lies in feedback and delayed capacity signals, not in the word traffic.
- Boundary: human reviewers respond more slowly and strategically than packet senders.
- Hypothesis: visible queue-delay feedback plus bounded intake should reduce peak backlog.
- Test: one reversible team trial; reject if urgent-item latency or rework rises.
