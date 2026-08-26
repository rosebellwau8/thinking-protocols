# Source notes

This record attributes a public article that grouped twelve reusable thinking prompts. The repository does not preserve the article's Prompt bodies, excerpts, or corpus. The URL and bibliographic metadata exist for attribution and research traceability only; the linked material remains outside this repository and its Apache-2.0 license.

Each canonical Protocol is an independent rewrite from the high-level method, intended outcome, and safety requirements. The one-to-one mapping is:

| Source-method label | Canonical Protocol | Independent abstraction |
| --- | --- | --- |
| Socratic questioning | `socratic-questioning` | Bounded clarification ending in a user-confirmed problem statement. |
| Fact checking | `fact-checking` | Dated evidence verification that separates facts, inference, and values. |
| Steelman both sides | `steelman-both-sides` | Fair comparison of credible options and a conditional decision memo. |
| Minimum experiment | `minimum-experiment` | Small reversible tests with thresholds and information value. |
| Dual-layer explanation | `dual-layer-explanation` | Fact-consistent intuitive and mechanism-level explanations of one topic. |
| Reverse engineering | `reverse-engineering` | Backward analysis of an existing outcome into mechanisms and a minimal reconstruction. |
| Horizontal-vertical analysis | `horizontal-vertical-analysis` | Tool-aware research crossing historical evolution with current peer comparison. |
| Expert panel | `expert-panel` | Simulated analytical roles that interpret shared evidence without impersonating real experts. |
| First principles | `first-principles` | Derivation from evidence-backed facts, hard constraints, goals, and explicit assumptions. |
| Cross-domain transfer | `cross-domain-transfer` | Evidence-backed mechanism transfer with structural matching and falsifiable tests. |
| Talent discovery | `talent-discovery` | Consent-gated, non-diagnostic hypotheses from behavior, feedback, outcomes, and counterexamples. |
| Life design | `life-design` | Consent-gated planning from present constraints toward reversible life-design experiments. |

Thinking Protocols adds the repository's own machine-readable abstraction: every Protocol declares applicability, inputs, ordered phases, stopping rules, capability requirements, safety boundaries, and Artifact interfaces. Thin Adapters package those semantics for runtimes without becoming a second semantic source.

No third-party wording is required to build, test, route, or use these Protocols. The two self-exploration Protocols intentionally produce terminal, conversation-scoped output rather than persistent sensitive Artifacts. The two research-dependent additions require `web.search` so externally checkable examples are not invented from model memory.
