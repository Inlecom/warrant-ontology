# WARRaNT KG Ontology — Modelling Conventions

Version 0.10-poc | 2026-09-06

---

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Class | PascalCase, English, no abbreviations | `DetectionEvent`, `VesselFunction`, `ResponseEvaluation` |
| Object property | camelCase, starts with a verb | `producesDetectionEvent`, `hasDIState`, `aggregatesInto` |
| Datatype property | camelCase, starts with `has` or `is` (or a past participle for timestamps) | `hasScoreValue`, `hasTimestamp`, `assessedAt` |
| Named individual (controlled vocab) | UPPER_SNAKE_CASE for guidewords, types and statuses; PascalCase for the five operational states | `cdm:UNAVAILABLE`, `di:ATTRIBUTE_BREACH`, `mit:FAIL_SAFE`, `di:CriticalState` |
| Module namespace prefix | short, lowercase | `warrant:`, `davom:`, `obs:`, `cdm:`, `assr:`, `di:`, `scen:`, `mit:`, `dt:` |

---

## Instance Namespace Policy (MANDATORY)

Ontology terms (classes, properties, controlled individuals) use the module namespace:

```turtle
cdm:Hazard
di:CriticalState     # controlled vocabulary individual, lives in module
davom:hasFunction
```

Runtime data instances (individuals representing real or simulated entities) **MUST** use a separate data namespace:

```
https://warrant-project.eu/data/{context}#
```

where `{context}` identifies the Living Lab or use case:

| Context | Namespace |
|---------|-----------|
| `ll1` | `https://warrant-project.eu/data/ll1#` — LL1 Danaos containership |
| `ll2` | `https://warrant-project.eu/data/ll2#` — LL2 AELER smart container |
| `ll3` | `https://warrant-project.eu/data/ll3#` — LL3 DST NOVA vessel |
| `ll4` | `https://warrant-project.eu/data/ll4#` — LL4 Seafar MAI-W / ROC |

**Never** create data instances in `obs:`, `cdm:`, `davom:`, or any other module namespace.

Note that example files sharing a context (e.g. the three LL4 files) share individuals such as `ll4:MAI_W` and `ll4:RemoteNavigationFunction` on purpose; individuals that are specific to one scenario (indices, edges, events) must have scenario-specific local names so that files can be loaded together without collisions.

---

## When to Create a New Class

Create a new class when there is a clearly distinct real-world concept that needs to carry its own properties and appear as a type in SPARQL queries. Prefer subclassing an existing class. Do not create a class merely to group instances — use properties instead.

## When to Create an Individual

Create a named individual for controlled vocabulary entries and for runtime instance data (in `examples/` with the data namespace).

## When to Create a Controlled Vocabulary

Use a controlled vocabulary class when the set of values is small and stable, values are reused across many instances, and SPARQL filtering on specific values is required. Instances of the vocabulary class are named individuals in the module namespace. The current closed vocabularies are:

| Vocabulary | Values | Extension |
|---|---|---|
| `cdm:DeviationType` | NO, LESS, MORE, LATE, WRONG, UNAVAILABLE, UNTRUSTED, INCONSISTENT, NOISY, SPOOFED | ontology revision |
| `di:DependabilityIndexState` (operational state) | NormalState, DegradedState, CriticalState, FailedState, UnsafeState | **closed** — never extended |
| `warrant:OperationalMode` | RemoteOperation, Manual, Autonomous, Assisted, Degraded, Handover | ontology revision |
| `davom:DependencyType` | FUNCTIONAL, DATA, CONTROL, PHYSICAL, CYBER | ontology revision |
| `davom:AssetRole` | PRIMARY_ASSET, SUPPORTING_ASSET | closed |
| `davom:InterfaceType` | LAN, SERIAL, CONTACT, SERIAL_CONTACT, VIDEO, AUDIO, WIRELESS | ontology revision |
| `cdm:HazardClass` | CYBER_THREAT, PHYSICAL_FAILURE, DATA_LOSS | ontology revision (each new class must declare its admissible dependency types) |
| `obs:MonitoringLevel` | COMPONENT_LEVEL, FUNCTION_LEVEL, SYSTEM_LEVEL | closed |
| `di:ResilienceTriggerType` | ATTRIBUTE_BREACH, SUSTAINED_DECLINE, PREDICTED_FLOOR_CROSSING | closed (the three terms of the resilience criterion) |
| `mit:ResponseStrategyType` | RECONFIGURATION, LOGICAL_ISOLATION, REDUNDANCY_ACTIVATION, VIRTUAL_SENSOR_SUBSTITUTION, COMMUNICATION_REROUTING, SAFE_DEGRADED_MODE, RECOVERY, ENHANCED_MONITORING, OPERATOR_ESCALATION | ontology revision |
| `mit:ResiliencePosture` | FAIL_OPERATIONAL, FAIL_SAFE | closed |
| `mit:AuthorisationStatus` | AUTHORISATION_PENDING, AUTHORISED, REJECTED, OVERRIDDEN | ontology revision |
| `assr:ClaimStatus` | CLAIM_SUPPORTED, CLAIM_CHALLENGED, CLAIM_UNSUPPORTED | ontology revision |
| `assr:ObligationStatus` | PRESENT, MISSING, STALE, UNTRACEABLE | closed |
| `scen:ScenarioExecutionState` | PENDING, RUNNING, COMPLETED, FAILED | closed |

## Simple Object Property vs. Reified Relationship Node

Use a **simple object property** (`davom:dependsOn`) when the relationship is binary with no additional attributes.

Use a **reified relationship node** when the relationship has attributes that must be stored and queried: `davom:Dependency` (weight, criticality, canonical type, direction), `di:RiskPropagationEdge` (hazard class, weight, mirrored dependency), `di:DIWeight` (parent, child, γ, context), `mit:ResponseEvaluation` (action × trigger with rank, cost, expected effect).

---

## How to Model Metrics

```turtle
# Correct: operational entity HAS a metric
ll4:ROCToVesselCommandLink obs:hasDependabilityMetric ll4:CommandLatencyMetric .

# WRONG: do not say a component "generates" or "creates" a metric
```

Observers (Sensor, VirtualSensor, AnalyticalService, NodeHealthMonitor) **observe**, **measure**, **estimate** or **consume** metrics. They do not create them.

---

## How to Model Observations and Health Events

```
AnalyticalService / NodeHealthMonitor  →  obs:consumes                 →  Metric
DataSource                             →  obs:producesHealthEvent      →  HealthEvent
AnalyticalService / VirtualSensor      →  obs:producesDetectionEvent   →  DetectionEvent   (a HealthEvent)
DetectionEvent                         →  obs:detectionEventDetects    →  Deviation
```

A `HealthEvent` carries the methodology's named record. Populate what is known and enrich later:

```turtle
ll4:GNSSSignalLossDetectionEvent a obs:DetectionEvent ;
    warrant:hasIdentifier "HE-MAIW-20260517-0001" ;
    obs:hasTimestamp "2026-05-17T10:15:02Z"^^xsd:dateTime ;
    obs:hasSource ll4:GNSSMonitoringService ;
    obs:affectsAsset ll4:GNSSReceiverComponent ;
    obs:indicatesCondition ll4:PositionUncertaintyHazard ;
    obs:hasConfidenceValue "0.92"^^xsd:decimal ;
    obs:hasSeverityLevel "HIGH" ;
    obs:isPersistent true ;
    obs:hasRootCause ll4:FM_GNSSSignalOutage ;
    obs:hasMissionContext warrant:RemoteOperationMode ;
    obs:hasControlStatus "MITIGATION_PENDING_AUTHORISATION" .
```

Use `obs:PredictedConditionEvent` for a predicted failure (no deviation has occurred; the detection-event rule does not apply) and `di:DIForecast` for a quantitative DI prediction. Use `warrant:derivedFrom` for filtering/correlation/fusion lineage between events.

Use `obs:hasExternalRecordReference` on `obs:Measurement` to link to raw time-series stores. Do not persist high-frequency telemetry in the KG.

---

## How to Model Deviations (MANDATORY)

```turtle
# Correct: use hasDeviationType with a named individual
ll4:GNSSSignalLossDeviation a cdm:Deviation ;
    cdm:hasDeviationType cdm:UNAVAILABLE .

# WRONG: deviation subclasses are deprecated
ll4:GNSSSignalLossDeviation a cdm:UnavailableDeviation .  # DO NOT USE
```

`cdm:hasDeviationType` may also tag a `cdm:ProcessModelFlaw` (typically WRONG or LATE).

---

## How to Model Design-Time Knowledge

- A `cdm:Hazard`, `cdm:ThreatScenario`, `cdm:FailureMode` or `cdm:Risk` carries `cdm:hasHazardClass`; the class declares (in the ontology, not at runtime) the dependency types it propagates over.
- A `cdm:Risk` carries likelihood and the impact triple (`hasSafetyImpact`, `hasEnvironmentalImpact`, `hasFinancialImpact`); `hasImpact` is the governing maximum.
- A design-time safeguard is a `cdm:Control` that `mitigates` a hazard/threat/failure mode and `hasResidualRisk`. The runtime action that relies on it is a `mit:MitigationAction` with `mit:implementsControl`.
- Every `davom:Dependency` carries `davom:hasDependencyType`; `dependencySource` is the provider (upstream), `dependencyTarget` the consumer (downstream).
- Assumptions and scope statements are `assr:Assumption` individuals so that their invalidation can be monitored (`assr:isChallengedBy`).

---

## How to Model Attribute Values and Node Scores

```turtle
# Single-source estimate with confidence
ll4:RemoteNavSafetyValue_NHM a assr:AssuranceAttributeValue ;
    assr:hasAttributeValueNumber "0.15"^^xsd:decimal ;
    assr:hasSourceConfidence "0.90"^^xsd:decimal ;
    assr:hasValueSource ll4:RemoteNavigationNodeHealthMonitor ;
    assr:assessedAt "2026-05-17T10:15:04Z"^^xsd:dateTime .

# Fused value, state assigned from the attribute's thresholds
ll4:RemoteNavSafetyValue_Fused a assr:AssuranceAttributeValue ;
    assr:hasAttributeValueNumber "0.20"^^xsd:decimal ;
    warrant:derivedFrom ll4:RemoteNavSafetyValue_NHM , ll4:RemoteNavSafetyValue_DT ;
    di:hasAttributeState di:CriticalState .

# Node Dependability Score ND (class IRI retains its historical name)
ll4:NavigationAssuranceScore a assr:AssuranceScore ;
    assr:hasScoreValue "0.38"^^xsd:decimal ;
    di:calculatedAt    "2026-05-17T10:15:05Z"^^xsd:dateTime .
```

Weights (`assr:AssuranceWeight`, `di:DIWeight`), thresholds (`di:DIThreshold`), floors and damping (`di:SupervisionConfiguration`, `di:RiskPropagationParameter`) are governed configuration: give them `warrant:appliesUnder`, `warrant:hasVersion`, `warrant:approvedBy`.

---

## How to Model Operational State (MANDATORY)

State is **attribute-wise**. It is assigned by comparing each attribute value with the node's `di:DIThreshold` for that attribute (`hasNormalMinimum` > `hasCriticalThreshold` > `hasFailedThreshold` > `hasUnsafeThreshold`), recorded on the value with `di:hasAttributeState`, and reported on the node and system index with `di:hasDIState` as the most severe attribute state. **The DI value never determines the state.**

```turtle
# Correct: named individual, reported alongside the DI
ll4:RemoteNavigationDI di:hasDIValue "0.34"^^xsd:decimal ;
                       di:hasDIState di:CriticalState .

# WRONG: subclassing DependabilityIndexState is prohibited
# ll4:CriticalNavigationState a di:DependabilityIndexState .  # DO NOT USE

# WRONG: deriving the state from DI-value bounds (deprecated pattern)
# di:CriticalState di:hasThreshold [ di:hasLowerThreshold 0.3 ; di:hasUpperThreshold 0.5 ] .
```

Available named individuals: `di:NormalState`, `di:DegradedState`, `di:CriticalState`, `di:FailedState`, `di:UnsafeState`.

---

## How to Model Propagation, Aggregation, Triggers and Forecasts

- One `di:PropagatedRisk` per (node, hazard class) with local and propagated values; `di:hasAggregatedRiskValue` on the node index.
- One `di:RiskPropagationEdge` per admissible (dependency, hazard class) pair, with `di:mirrorsDependency` and `di:forHazardClass`.
- Hierarchy: `child di:aggregatesInto parent` (or `di:contributesToSystem`), with a `di:DIWeight` per parent–child pair. Never link indices with `di:contributesTo`; that property is for the node score only.
- Every firing of the resilience criterion is a `di:ResilienceTrigger` with one `di:hasTriggerType` and the attribute value, index or forecast that fired it.
- A DI prediction is a `di:DIForecast` with `di:forecastProducedBy` (the Digital Twin, a scenario execution, or a predictive service) and, when produced by the twin, `dt:producesForecast` from the twin.

---

## How to Model Responses

- Design-time library: `mit:MitigationRule` → `mit:recommends` → `mit:MitigationAction` (advisory in the PoC) with `mit:hasStrategyType`, `mit:hasDefaultPosture`, `mit:implementsControl`, `mit:requiresAuthorisationFrom`.
- REDS: one `mit:ResponseEvaluation` per alternative per trigger with `mit:hasExpectedIndex` (a `di:DIForecast`), cost, penalty, `mit:isAdmissible`, `mit:hasRank`, `mit:hasExplanation`.
- IRDS: one `mit:ResponseExecution` with `mit:selectedFrom`, `mit:hasAuthorisationStatus`, `mit:authorisedBy`, timing, `mit:hasResiliencePosture`, `mit:hasOutcome`, `mit:hasOutcomeIndex`, `mit:recordedOperatorInput`, `mit:isRecordedIn`.

---

## How to Model the Living Dependability Case

- Chain: `assr:Evidence` → `assr:supportsClaim` / `assr:challengesClaim` → `assr:AssuranceClaim` → `assr:addressesRequirement` → `assr:Requirement`.
- Evidence sources are observation-layer items (`assr:hasEvidenceSource` → health event, measurement, virtual-sensor output, operator input) so that every claim is traceable to what was observed or decided.
- Declare what evidence a claim or requirement expects as `assr:EvidenceObligation` with a validity period; evidence completeness is computed against these, and each obligation is PRESENT, MISSING, STALE or UNTRACEABLE.
- Health events and invalidated `assr:Assumption`s may `challengesClaim`; only the claim **status** changes at runtime, never the approved wording.
- Store `assr:AssuranceLevel` and `assr:CertificationReadiness` with their component values, weight set and method identity; report the Assurance Level together with the system DI (`di:isReportedWith`).
- Attach everything to the `assr:LivingDependabilityCase` (`assr:includes*`, `di:isRecordedIn`, `mit:isRecordedIn`).

---

## How to Model External Data References

```turtle
ll4:GNSSSignalQualityMetric obs:hasExternalTimeSeriesId "timeseries.gnss.signal_quality.MAI-W" .

ll4:GNSSSignalMeasurement_T1 obs:hasExternalRecordReference
    "timeseries.gnss.signal_quality.MAI-W::1747476900" .
```

---

## How to Model Example Scenarios

1. Place example files in `examples/`.
2. Use the data namespace (`https://warrant-project.eu/data/{context}#`).
3. Include the full chain: Vessel → Function → System → Component → Metric → Measurement → DetectionEvent (HealthEvent) → Deviation → Hazard → Risk → AssuranceDegradation → attribute values → AssuranceScore (ND) → DI with attribute-wise state.
4. Tag deviations with `cdm:hasDeviationType`; tag hazards with `cdm:hasHazardClass`; type dependencies with `davom:hasDependencyType`.
5. Set `di:hasDIState` to a named individual, assigned from attribute states, not from the DI value.
6. Include at least one `MitigationRule` with an `AdvisoryAction`; where the scenario reaches the decision layer, a `ResilienceTrigger`, `ResponseEvaluation`s and a `ResponseExecution`.
7. Include a `DigitalTwin` with `dt:visualises` assertions and, where used, `dt:producesForecast`.
8. Run `python scripts/validate_turtle.py --shacl` and `python scripts/run_queries.py`; the example must conform to the shapes.

`examples/example-gnss-failover.ttl` is the reference instantiation of every layer.

---

## Deprecation Rules

- Mark: `owl:deprecated true ; rdfs:comment "DEPRECATED. Use X instead. Will be removed in the next minor release."`.
- Deprecated terms remain for one full minor release before removal (see CONTRIBUTING.md). Currently deprecated: the ten `cdm:*Deviation` subclasses; `di:hasThreshold`, `di:hasLowerThreshold`, `di:hasUpperThreshold`, `di:hasSystemWeight`; `dt:ScenarioExecutionState`.
- `di:DependabilityIndexState` subclasses are prohibited outright (not deprecated: never allowed).

---

## Mandatory Principles Summary

| Principle | Rule |
|-----------|------|
| Human operators | Subclass `warrant:AgentEntity`, not `warrant:OperationalEntity` or `davom:Component` |
| Metrics | Operational entities have metrics; they do not generate them |
| Deviation typing | `cdm:hasDeviationType` + named individual only |
| Operational state | Named `di:DependabilityIndexState` individuals only; assigned attribute-wise; the DI value never determines it |
| Detection chain | `AnalyticalService → producesDetectionEvent → DetectionEvent → detectionEventDetects → Deviation` |
| `obs:produces` range | `obs:Status \| obs:VirtualSensorOutput` only; never `cdm:Deviation` |
| Dependency direction | `dependencySource` = provider (upstream), `dependencyTarget` = consumer (downstream); every Dependency has a canonical `hasDependencyType` |
| Computation | No Section-6 formula is encoded; the KG stores inputs, governed parameters, results with timestamp and method identity, and audit events |
| Forecasts | `di:DIForecast` lives in warrant-di; the Digital Twin produces it; no module imports warrant-digital-twin |
| VisualisableEntity | Defined in `warrant-core.ttl`; do not redefine |
| VoyageSegment, OperationalMode | Core/context module, not CDM |
| Raw telemetry | Outside KG; use external reference properties |
| Example individuals | `https://warrant-project.eu/data/{context}#` namespace |
| Controlled vocabulary | Ontology module namespace |
