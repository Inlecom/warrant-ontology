# Changelog — WARRaNT KG Ontology

All notable changes to this repository are documented here.

---

## [0.9-poc] — 2026-06-05 — Pre-release (Repository Refactoring)

### Added
- Modular repository structure: monolithic `warrant_ontology.ttl` refactored into 9 modules.
- `warrant-core.ttl`: shared superclasses including `warrant:AgentEntity` (new) and `warrant:VisualisableEntity` (relocated from DT module).
- `warrant-core.ttl`: `warrant:OperationalMode` controlled vocabulary with 6 named individuals (RemoteOperationMode, ManualOperationMode, AutonomousOperationMode, AssistedOperationMode, DegradedOperationMode, HandoverMode).
- `warrant-di.ttl`: risk-propagation DI model — `PropagatedRisk`, `RiskPropagationEdge`, `SystemDependabilityIndex` with all supporting properties.
- `warrant-digital-twin.ttl`: `DigitalTwinView`, `VisualisationLayer`, `DecisionSupportView`, `dt:receivesUpdateFrom`.
- `examples/example-gnss-failover.ttl`: updated PoC with ll4 data namespace, PropagatedRisk, hasBetaWeight.
- `examples/example-communication-degradation.ttl`: LL4 packet loss / latency degradation.
- `examples/example-smart-container-fire.ttl`: LL2 container fire detection.
- `examples/example-roc-handover.ttl`: LL4 Use Case 2 ROC–boatmaster handover.
- `examples/example-ecdis-spoofing.ttl`: LL1 AIS spoofing cyberattack.
- `shapes/warrant-core-shapes.ttl`: SHACL starter set (6 shapes).
- `queries/competency-queries.sparql`: 6 competency queries.
- `scripts/validate_turtle.py`: Turtle syntax validator with namespace policy check.
- `scripts/merge_ontology.py`: module merge script writing to `dist/`.
- `.github/workflows/validate-ontology.yml`: CI validation workflow.
- `docs/modelling-conventions.md`, `docs/namespace-policy.md`, `docs/kg-boundary.md`, `docs/external-ontology-alignment.md`.
- `CONTRIBUTING.md`, `CODEOWNERS`, `README.md`.

### Changed
- `davom:HumanOperator` and `davom:HumanOperatorRole` now subclass `warrant:AgentEntity` (not `warrant:OperationalEntity`).
- `warrant:VisualisableEntity` moved from `dt:` namespace to `warrant:` (core module).
- `obs:produces` range: removed `cdm:Deviation`; range is now `obs:Status | obs:VirtualSensorOutput` only.
- All example instance IRIs migrated to `https://warrant-project.eu/data/{context}#` namespaces.
- Version comment aligned to `0.9-poc` (was inconsistently `0.8` in header, `0.9-poc` in versionInfo).

### Deprecated
- `cdm:UnavailableDeviation`, `cdm:LessDeviation`, `cdm:MoreDeviation`, `cdm:LateDeviation`, `cdm:WrongDeviation`, `cdm:UntrustedDeviation`, `cdm:InconsistentDeviation`, `cdm:NoisyDeviation`, `cdm:SpoofedDeviation`, `cdm:NoDeviation` — all marked `owl:deprecated true`. Use `cdm:Deviation` with `cdm:hasDeviationType` and named individuals instead. Will be removed in v0.2.0.

---

## [0.8] — 2026-05-17 — Monolithic Proof of Concept

Initial monolithic Turtle ontology with GNSS failover example (MAI-W, LL4).
Applied corrections C1–C9 from review pass 1.
