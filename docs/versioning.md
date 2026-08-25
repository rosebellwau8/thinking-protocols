# Versioning

Protocol definitions use Semantic Versioning. A Protocol version changes when its documented behavior, interface, or compatibility changes; breaking changes increment the major version.

Artifact schema versions evolve independently from Protocol versions. Compatible clarifications may retain the existing schema version, but a breaking Artifact change requires a new major schema filename, such as `decision_memo.v2.schema.json`. Existing major schema files remain stable interfaces for consumers.

Adapters and generated distributions record the source Protocol version and digest. Generated output must be rebuilt after its canonical Protocol changes; generated files do not carry independent semantic versions.

