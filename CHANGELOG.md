# Changelog — WARRaNT KG Ontology

All notable changes to this repository are documented here.

---

## [0.10-poc] — 2026-09-06 — Methodology Alignment (framework paper v0409)

Aligns the ontology with the WARRaNT framework paper *A Knowledge-Graph and
Digital-Twin Framework for Continuous Dependability Assurance of Waterborne
Cyber-Physical Systems* (draft v0409, 3 September 2026): health-event
generation and node health monitoring, attribute-wise operational state,
typed per-hazard-class risk propagation, hierarchical DI aggregation,
resilience triggers and forecasts, the REDS/IRDS decision layer, and the
Living Dependability Case. Branch `feature/methodology-alignment-2026-09-06`.
Inventory: 200 classes · 194 object properties · 128 datatype properties ·
70 named individuals · 3,094 module triples (was 159 · 99 · 39 · 21 · 1,598).
All five examples (2,577 triples) pass syntax, namespace, domain and range,
and SHACL validation, and all ten competency queries return rows.

### Added
- `warrant-core.ttl`: `warrant:CalculationMethod`; `warrant:appliesUnder` (context scoping of weights, thresholds, floors, requirements); `warrant:derivedFrom` (lineage); `warrant:approvedBy`, `warrant:hasApprovalStatus` (configuration governance).
- `warrant-davom.ttl`: `davom:DependencyType` vocabulary (FUNCTIONAL, DATA, CONTROL, PHYSICAL, CYBER) and `davom:hasDependencyType`; `davom:isBidirectional`; `davom:SecurityZone`, `davom:Conduit`, `davom:belongsToZone`, `davom:connectsZone` (IEC 62443-3-2); `davom:AssetRole` vocabulary, `davom:hasAssetRole`, `davom:supportsAsset`; `davom:isCriticalNode`.
- `warrant-observation.ttl`: `obs:HealthEvent` (superclass of `obs:DetectionEvent`) with the full health-event record (`affectsAsset`, `indicatesCondition`, `hasRootCause`, `hasMissionContext`, `hasSeverityLevel`, `hasDuration`, `isPersistent`, `hasOperationalImpact`, `hasControlStatus`, `hasTrendIndicator`); `obs:PredictedConditionEvent`; `obs:NodeHealthMonitor`, `obs:MonitoringLevel` vocabulary, `obs:monitorsNode`, `obs:hasMonitoringLevel`, `obs:exchangesHealthEventWith`; `obs:producesHealthEvent` (super-property of `producesDetectionEvent`); `obs:substitutesFor`.
- `warrant-cdm.ttl`: `cdm:Control` with `cdm:mitigates` and `cdm:hasResidualRisk`; `cdm:HazardClass` vocabulary (CYBER_THREAT, PHYSICAL_FAILURE, DATA_LOSS) with `cdm:propagatesOverDependencyType` and `cdm:hasHazardClass`; `cdm:ThreatScenario`, `cdm:Vulnerability`, `cdm:exploits`; impact triple `cdm:hasSafetyImpact`, `cdm:hasEnvironmentalImpact`, `cdm:hasFinancialImpact`; FMEA ratings `cdm:hasSeverityScore`, `cdm:hasOccurrenceScore`, `cdm:hasDetectionScore`, `cdm:hasRiskPriorityNumber`.
- `warrant-assurance.ttl`: attribute-value provenance `assr:hasValueSource`, `assr:hasSourceConfidence`, `assr:assessedAt`; Living Dependability Case core — `assr:Requirement`, `assr:AssuranceClaim`, `assr:ClaimStatus` vocabulary, `assr:Assumption`, `assr:EvidenceObligation`, `assr:ObligationStatus` vocabulary, `assr:Nonconformity`, `assr:AssuranceLevel`, `assr:AssuranceLevelWeightSet`, `assr:CertificationReadiness`, `assr:LivingDependabilityCase`, and their properties (`supportsClaim`, `challengesClaim`, `addressesRequirement`, `claimAppliesTo`, `hasClaimStatus`, `expectsEvidence`, `isFulfilledBy`, `hasEvidenceSource`, `isChallengedBy`, `includes*`, EC/EF/EQ/MC/TC components and weights, RC/NC inputs, …).
- `warrant-di.ttl`: `di:DependabilitySupervisor`; `di:hasAttributeState`; per-attribute thresholds `di:thresholdAppliesToAttribute`, `di:thresholdAppliesToNode`, `di:hasNormalMinimum`, `di:hasCriticalThreshold`, `di:hasFailedThreshold`, `di:hasUnsafeThreshold`; `di:forHazardClass`, `di:hasLocalRiskValue`, `di:hasAggregatedRiskValue`, `di:mirrorsDependency`, `di:RiskPropagationParameter` (`hasDampingFactor`, `hasConvergenceTolerance`); `di:aggregatesInto`, `di:weightParent`, `di:weightChild`, `di:hasAggregationWeightValue`; `di:DIForecast` and its properties; `di:SupervisionConfiguration` (`hasTrendWindow`, `hasTrendSlopeThreshold`, `hasPredictionHorizon`, `hasManagementFloor`); `di:ResilienceTrigger`, `di:ResilienceTriggerType` vocabulary, `triggeredBy*`; `di:hasResilienceMargin`, `di:hasTrendSlope`, `di:isReportedWith`, `di:isRecordedIn`; `di:DIUpdateEvent` properties; `di:hasAggregationOperator`.
- `warrant-scenario.ttl`: `scen:ScenarioExecutionState` with PENDING/RUNNING/COMPLETED/FAILED; `scen:hasProjectedState`; `scen:producesForecast`.
- `warrant-mitigation.ttl`: `mit:DecisionSupportService` (REDS), `mit:ResilienceSupervisor` (IRDS); `mit:ResponseStrategyType` (the paper's seven strategies plus LOGICAL_ISOLATION and ENHANCED_MONITORING from §3.6 and the IRDS patent figure), `mit:ResiliencePosture`, `mit:AuthorisationStatus` vocabularies; `mit:ResponseEvaluation`, `mit:DecisionConfiguration`, `mit:ResponseExecution` and their properties; `mit:hasStrategyType`, `mit:hasDefaultPosture`, `mit:implementsControl`, `mit:requiresAuthorisationFrom`; `mit:RecoveryEffect` properties.
- `warrant-digital-twin.ttl`: `dt:producesForecast`, `dt:providesVirtualSensor`.
- `shapes/warrant-core-shapes.ttl`: shapes for `obs:HealthEvent`, `assr:AssuranceClaim`, `assr:Evidence`, `di:DIThreshold` (ordered thresholds), `di:ResilienceTrigger`, `mit:ResponseEvaluation`, `mit:ResponseExecution`.
- `queries/competency-queries.sparql`: Q7 evidence→claim→requirement traceability, Q8 trigger→evaluation→execution→outcome, Q9 attribute-wise state vs DI, Q10 forecasts against the management floor.
- `scripts/validate_turtle.py --shacl`; `scripts/generate_module_docs.py` (generated `docs/modules/*.md`, `--check` in CI).
- `scripts/validate_turtle.py`: domain and range check on every example assertion, following `rdfs:subClassOf` and `owl:unionOf`. SHACL constrains the shapes it targets, not every property use, so these errors passed validation silently; an audit found 62 across the five examples.
- `examples/example-gnss-failover.ttl`: extended to instantiate every layer of the framework, and now the reference for how each Section 6 quantity is derived.
- `examples/example-ecdis-spoofing.ttl`: a second STPA path for AIS target spoofing (`WrongTrafficPictureProcessModelFlaw`, `WrongCollisionAvoidanceUCA`), a course-alteration `ControlAction` and an explicit officer `ProcessModel`, and detection events for the eight deviations that had none.

### Changed
- **Operational state is attribute-wise.** `di:DependabilityIndexState` keeps its IRI and five individuals but is labelled "Operational State"; state is assigned per attribute from `di:DIThreshold`s and reported with the index; the DI value never determines it. `di:hasDIState` domain widened to `di:SystemDependabilityIndex`.
- `assr:AssuranceScore` relabelled "Node Dependability Score (ND)" (`skos:altLabel "Assurance Score"`); attribute weights documented as α; β is the risk sensitivity (`di:hasBetaWeight`).
- `di:appliesTo` range widened to `warrant:OperationalEntity`; `di:calculatedAt` domain widened to `assr:AssuranceLevel`, `assr:CertificationReadiness`, `di:PropagatedRisk`, `di:DIUpdateEvent`; `di:usesCalculationMethod` domain widened; `di:DICalculationMethod` is a `warrant:CalculationMethod`.
- `dt:DigitalTwin` is now an `obs:DataSource`; the Digital Twin → Supervisor/REDS direction is realised through `di:DIForecast` (owned by warrant-di) without any module importing warrant-digital-twin.
- Dependency direction made explicit: `davom:dependencySource` = upstream provider, `davom:dependencyTarget` = downstream consumer; the nine `Dependency` subclasses note their canonical type.
- `cdm:hasDeviationType` domain widened to `cdm:ProcessModelFlaw`; `cdm:isEvaluatedAs`, `cdm:affectsComponent`, `cdm:degrades` domains/ranges widened for threat scenarios, vulnerabilities, links and zones; `cdm:mayCause` range no longer includes `assr:AssuranceDegradation` (use `assr:causesAssuranceDegradation`).
- `mit:matchesRule` and `mit:isTriggeredBy` accept `di:ResilienceTrigger` (and `obs:HealthEvent`); `mit:addresses` and `mit:hasExpectedEffect` domains widened.
- `scen:hasExecutionState` now ranges over `scen:ScenarioExecutionState` (was `di:DependabilityIndexState`).
- Module imports repaired: observation imports cdm; assurance imports observation; di imports observation and cdm; scenario imports di; mitigation imports davom, observation, scenario; digital-twin imports di and mitigation. `warrant-assurance` no longer declares `di:calculatedAt`.
- `shapes/warrant-core-shapes.ttl`: shapes prefix declared (the file previously did not parse); `VesselFunctionShape` accepts metrics on supporting entities; `DependabilityIndexShape` targets `warrant:OperationalEntity`.
- `queries/competency-queries.sparql`: Q2 repaired (property path to supporting entities); Q3 keyed on resilience triggers as well as states; Q5 returns hazard class and mirrored dependency.
- `scripts/validate_turtle.py` parses `shapes/`; SHACL runs with the modules merged into the data graph and inference off.
- `examples/example-roc-handover.ttl`: added a handover-completion metric so the function is monitored; `examples/example-smart-container-fire.ttl`: the fire event is an `obs:HealthEvent` (it identifies no deviation).
- Documentation regenerated/rewritten: `docs/modules/*.md` (generated), `docs/modules/warrant-integration.md`, `docs/modelling-conventions.md`, `docs/kg-boundary.md`, `docs/external-ontology-alignment.md`, `docs/namespace-policy.md`, `docs/stack-overview.md`, `README.md`, `CONTRIBUTING.md`.
- Version strings in all module and example headers set to `0.10-poc` (were inconsistently `1.0.0`).

### Fixed
- Five domains and ranges were narrower than the modelling they are meant to support, which accounted for 51 of the 62 violations found by the new check: `davom:hasComponent` domain (a System may hold components directly), `davom:dependencySource`/`dependencyTarget` range (AgentEntity, without which `HumanSupervisionDependency` between two operator roles is unusable), `cdm:mayCause` range (ProcessModelFlaw, the STPA path by which a falsified input corrupts the controller's model), `cdm:affectsComponent` range (System, Subsystem), `mit:recommends` range (FailoverProcedure).
- `examples/example-gnss-failover.ttl`: propagated risk did not satisfy the documented recurrence; a trend slope breached its threshold with no trigger recorded; the post-response state had no attribute values to derive it from; two indices had no node score; and the response completed 68 s after detection against a 60 s requirement it claimed to satisfy. Every stated value now follows from the formulas.
- `examples/example-gnss-failover.ttl`: three maritime errors. AIS was used as an independent position source although own-ship AIS position is GNSS-derived; "INS" was used for inertial navigation although IMO and IEC use it for an Integrated Navigation System and no inertial unit is fitted; and the carrier-to-noise threshold (10 dB-Hz against a tracking floor around 25 to 30) was below the level at which a receiver has already lost lock and could not detect the spoofing scenario linked to it. The failover is now dead reckoning cross-checked against radar and AIS cooperative context, and detection uses both C/N0 and a RAIM protection level.
- `examples/example-ecdis-spoofing.ttl`: AIS spoofing was asserted to put a false own-ship position on the ECDIS. ECDIS takes own-ship position from the GNSS receiver over IEC 61162; AIS carries target data. The causal chain is split so that AIS spoofing leads to a wrong traffic picture and a wrong collision-avoidance manoeuvre, while GNSS spoofing and ECDIS compromise keep the wrong own-ship position and the wrong course alteration.
- Index-to-index aggregation used `di:contributesTo`, which carries a node score into an index, in LL1 and LL2; it now uses `di:aggregatesInto` and `di:contributesToSystem`, and the LL1 vessel index is a `SystemDependabilityIndex`. Also fixed: the LL1 STPA loop skipped the control action, the LL1 VDR was typed as a system but used as a component, and the ROC handover process model updated itself.

### Deprecated
- `di:hasThreshold`, `di:hasLowerThreshold`, `di:hasUpperThreshold` — DI-value bounds attached to a state implied that the state is derived from the DI; use the per-attribute thresholds. Will be removed in the next minor release.
- `di:hasSystemWeight` — flat aggregation weight; use a reified `di:DIWeight`. Will be removed in the next minor release.
- `dt:ScenarioExecutionState` — moved to `scen:ScenarioExecutionState`. Will be removed in the next minor release.
- The ten `cdm:*Deviation` subclasses remain deprecated (since 0.9-poc).

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
