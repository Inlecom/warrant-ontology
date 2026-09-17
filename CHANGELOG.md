# Changelog — WARRaNT KG Ontology

All notable changes to this repository are documented here.

---

## [Unreleased] — LL1 reworked around area-wide GNSS spoofing

Renames `examples/example-ecdis-spoofing.ttl` to `examples/example-gnss-spoofing.ttl`
and makes one primary business use case of it: area-wide GNSS spoofing degrading
the bridge's navigation situational awareness. 2,450 → 2,902 triples.

### Changed — scenario
- The primary scenario is `AreaWideGNSSSpoofingScenario`, triggered by `DevGPSSpoofed`. It replaces `AISECDISSpoofingScenario`, which mixed AIS spoofing, GNSS spoofing and VDR erasure as concurrent triggers.
- Direct AIS spoofing is kept as a separate secondary scenario, `DirectAISSpoofingScenario`, in which own-ship position stays correct.
- ECDIS is modelled as the consumer and presentation layer of the wrong position. ECDIS compromise remains a separate, alternative cause of a wrong own-ship position.
- VDR tampering, AMS corruption and the other FMEA entries remain as design-time knowledge. Their detection events are dated on earlier legs and take no part in the GNSS chain.

### Added — design-time layer
- Position data flows: `OwnShipPositionData`, `OwnShipAISBroadcast`, `SurroundingVesselGNSSPositionData` and `SurroundingTrafficAISReports`, plus the external `Link_AIS_VHFDataLink`. Surrounding vessels are modelled at data-flow level, not as vessel models.
- Dependencies that make the propagation traceable: GPS → position data → ECDIS, radar geo-referencing, AIS, autopilot track control and the navigation function; our AIS → our broadcast; surrounding vessels' GNSS → their AIS reports → our AIS; ECDIS and radar → navigation officer. `Dep_GPS_to_ECDIS` and `Dep_GPS_to_Radar` now take the position data flow as their source.
- Deviations `DevOwnShipAISBroadcastWrong` and `DevSurroundingTrafficAISPositionsWrong` (type WRONG, not SPOOFED): genuine AIS carrying positions that were wrong at their GNSS source.
- Detection event `SurroundingTrafficGNSSCorruptionEvent`: coherent AIS-to-radar divergence across targets. `GPSSpoofingDetectionEvent` is rewritten around the radar fix on charted features, depth and dead reckoning.
- `RadarFeedback` as a second, independent STPA feedback channel. The two process-model flaws are now the officer's own-ship position understanding and surrounding-traffic understanding.
- Integrity metrics: GNSS against radar fix, GNSS against dead reckoning, depth consistency, coherent AIS divergence fraction and fused position confidence. Availability metrics are described as saying nothing about correctness.

### Fixed — conceptual errors
- The header described spoofed AIS as moving own ship on the ECDIS.
- `DevGPSSpoofed` cited the "settings modified" FMEA row. The Danaos FMEA has no spoofing entry; this is now stated.
- `DevGPSSpoofed` matched the jamming rule. It now matches a new `RuleGNSSSpoofing`.
- `ActionDualGPSCrossCheck` implemented the independent cross-check control, which its own description said it is not. The link is removed.
- `Threat_GNSSSpoofing` credited RAIM and constellation disagreement with detection. Detection now rests on independent evidence, and signal strength, GPS No1 against No2 and own-ship GNSS against own-ship AIS are explicitly excluded.
- `DevECDISInterfaceModified` no longer causes the wrong-position flaw: lost feeds produce an alarmed, missing position, not a silently wrong one.
- Obsolete version-history comments and the stale FLAG-03 and FLAG-04 notes are removed.

### Added — documentation
- A modelling assumptions block (A1–A20) in the file header, covering technical, modelling, numeric and governance assumptions.

### Changed — runtime layer and Living Dependability Case
- New position-data node index `DI_OwnShipPosition` (availability 0.95 Normal, integrity 0.05 Unsafe) propagates CYBER_THREAT risk into `DI_Navigation`. It is used for propagation only, not aggregated into the system index.
- The navigation availability attribute stays Normal (0.90) while integrity, reliability and safety collapse.
- The other three functions are at baseline (DI 0.80, Normal). DI_sys is 0.56: above the 0.55 floor, but in the Unsafe state.
- `Trigger_SystemDecline` is replaced by `Trigger_PredictedFloorCrossing`, raised by the unmitigated forecast (0.50). The sudden drop is correctly not a sustained decline (slope −0.036 per hour).
- REDS ranks three responses: revert to independent navigation (0.565, executed), reduce speed (0.43), and switch to GPS No2 / ECDIS No2 (0.425, inadmissible because its forecast stays below the floor). The previous AIS-overlay evaluations, forecasts and execution are removed.
- The case's evidence, assumptions, obligations and nonconformities are rebuilt for the GNSS scenario. The AL is 0.66 and readiness is 0.43, with the readiness mapping now defined.

### Changed — approval
- All 51 governed artefacts (attribute weights, thresholds, aggregation weights, supervision, propagation and decision configuration, claims, evidence obligations and the AL weight set), the company position-fixing requirement and the readiness mapping are `APPROVED` by "WARRaNT LL1 use-case team". Nothing is left `PROPOSED`, and the Danaos approval dependency is removed.

---

## [Unreleased] — LL1 modernisation to the 0.10 vocabulary

Rewrites `examples/example-ecdis-spoofing.ttl` (LL1, Danaos CATHERINE C) to use
the 0.10 vocabulary. In 0.10-poc the file validated and its causal model was
correct, but it exercised none of the new terms, so its indices carried states
that were not attribute-derived and it appeared in none of the four new
competency queries. Branch `feature/ll1-modernisation-2026-09-16`; 778 → 2,450
triples. Two commits: the design-time layer, which is derived from the Danaos
source documents, and the runtime layer, which is not.

### Added — design-time layer (derived from the Danaos FMEA and equipment inventory)
- Hazard classes and the safety, environmental and financial impact triple on every risk.
- `CoastalApproachSegment`, `HighTrafficDensityCondition` and `GNSSInterferenceAreaCondition`, with `isCriticalUnder`, `modifiesLikelihoodOf` and `modifiesImpactOf`.
- Asset roles and critical-node flags across the equipment inventory.
- Four IEC 62443-3-2 security zones, with the satellite-to-LAN and BNWAS-to-AMS links as conduits.
- Nine typed dependencies between functions and systems.
- Twenty-one failure modes carrying their FMEA severity, occurrence, detection and RPN as typed values rather than free text, closing FLAG-04 in the file header.
- Five vulnerabilities, six threat scenarios and eight controls with two residual risks, linked to the advisory and failover actions through `implementsControl`.
- Strategy types and resilience postures on the ten pre-existing response actions.

### Added — runtime layer (PROPOSED policy values, not Danaos policy)
- Six node health monitors across the component, function and system levels, with peer exchange.
- The full health-event record on the four principal detection events.
- Sixteen attribute values with mode-scoped weights and per-node, per-attribute thresholds, and the operational state each yields.
- Typed CYBER_THREAT propagation: a damping parameter, a propagation edge mirroring a function-level cyber dependency, and four propagated-risk individuals.
- Reified hierarchical aggregation weights, a supervision configuration, a DI update audit record and two resilience triggers.
- Three REDS response evaluations ranked by the paper's objective, and one authorised IRDS execution with its post-response index.
- A Living Dependability Case: four requirements, three claims, two assumptions, six evidence items, four evidence obligations, three unresolved nonconformities, an Assurance Level and a Certification Readiness.
- Digital Twin forecasts for the unmitigated case and for each evaluated response.

Every index in the file is derivable by hand from the Section 6 formulas: node
scores from the weighted attribute values, node indices from the node score and
the propagated risk, the system index from the aggregation weights, the margin
from the management floor, the Assurance Level from its weight set and the
response ranking from the decision weights. The forty-eight artefacts that carry
a policy value are marked `warrant:hasApprovalStatus "PROPOSED"` and are for
Danaos to replace; the file header sets out which content is derived and which
is proposed.

### Changed
- Consolidated the two overlapping node scores on the navigation function into one, so that each node index has exactly one node score behind it. `ll1:NavCyberAssuranceScore` is now `ll1:NavigationNodeScore`; `ll1:SensorAssuranceScore` is removed.
- The five indices now carry attribute-derived states, aggregated and propagated risk values, a calculation method, the supervisor that produced them and the case that records them.

### Fixed
- `mit:hasStrategyType`, `mit:hasDefaultPosture` and `mit:requiresAuthorisationFrom` had `mit:ResponseAction` as their domain, which excluded `mit:FailoverProcedure`. A failover is a response strategy and needs all three.

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
