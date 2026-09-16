# WARRaNT Ontology — Module Integration Guide

**Project:** WARRaNT — Horizon Europe RIA 101202581  
**Scope:** Nine-module ontology stack for continuous dependability assurance of waterborne digital systems: design-time hazard knowledge, health events and node health monitoring, attribute-wise supervision and the Dependability Index, resilience decision and response, and the Living Dependability Case, with the Digital Twin as both consumer and producer  
**Status:** Aligned with the WARRaNT framework paper (v0409, September 2026); PoC demonstrators active at LL1, LL2, LL4  
**Version:** 0.10-poc

---

## Overview

The WARRaNT ontology is structured as a directed acyclic graph of nine modules. Each module has a scoped responsibility; no module replicates concepts defined by another. Integration happens through **typed object properties** that cross module boundaries. The central loop of the methodology maps onto the modules as follows: design-time knowledge (CDM) is attached to the vessel structure (DAVOM); runtime observations become health events interpreted by Node Health Monitors (Observation); monitors produce attribute assessments that the Dependability Supervisor fuses into node scores (Assurance), propagates as typed risk, aggregates into indices, and turns into attribute-wise operational states and resilience triggers (DI); a trigger initiates graph diagnosis and REDS ranking of response alternatives, and IRDS coordinates the authorised response (Mitigation); everything is recorded in the Living Dependability Case as evidence traceable to claims and requirements (Assurance); the Digital Twin visualises the state of the loop and feeds it with virtual sensing and forecasts (Digital Twin, Scenario).

---

## Module Dependency Graph

Derived from the `owl:imports` in the Turtle sources.

```
warrant-core
   │
   ├──► warrant-davom
   │       │
   │       ├──► warrant-cdm
   │       │       │
   │       │       ├──► warrant-observation ─────────┐
   │       │       │                                 ▼
   │       │       └──────────────────────► warrant-assurance
   │       │                                         │
   │       ├──────────────────────────────────► warrant-di ◄── (also imports observation, cdm)
   │       │                                         │
   │       │                                         ├──► warrant-scenario
   │       │                                         │         │
   │       └──────────────────────────────► warrant-mitigation ◄┘  (also imports cdm, observation)
   │                                                 │
   └──────────────────────────────────────► warrant-digital-twin  (also imports observation, di, scenario)
```

**Reading rule:** an arrow from A to B means A is imported by B (B depends on A). Transitive imports are not repeated.

| Module | Direct imports | Depended on by |
|---|---|---|
| `warrant-core` | *(none)* | all modules |
| `warrant-davom` | core | cdm, observation, di, mitigation, digital-twin |
| `warrant-cdm` | core, davom | observation, assurance, di, scenario, mitigation |
| `warrant-observation` | core, davom, cdm | assurance, di, mitigation, digital-twin |
| `warrant-assurance` | core, cdm, observation | di |
| `warrant-di` | core, davom, observation, cdm, assurance | scenario, mitigation, digital-twin |
| `warrant-scenario` | core, cdm, di | mitigation, digital-twin |
| `warrant-mitigation` | core, davom, cdm, observation, di, scenario | digital-twin |
| `warrant-digital-twin` | core, davom, observation, di, scenario, mitigation | *(none)* |

**No module imports `warrant-digital-twin`.** The twin's outputs enter the loop through classes owned upstream: it is an `obs:DataSource`, and the forecast it produces is a `di:DIForecast`.

---

## The Core Data Flow

The knowledge graph is driven by the framework's closed loop. Arrows show the direction of information; module names in brackets.

```
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ ⓪ Design-time knowledge [cdm on davom]                                    │
 │    HAZOP / FMEA / STPA / cyber assessment → Hazard, FailureMode,          │
 │    ThreatScenario, Control (+ residual Risk), HazardClass with admissible │
 │    DependencyTypes; Requirement, AssuranceClaim, Assumption [assr]        │
 └───────────────────────────────────────────────────────────────────────────┘
        │ classify against                                        ▲ challenge / support
        ▼                                                         │
 ① Physical world ─ sensors, virtual sensors, cyber monitors, operators,
                    Digital Twin state estimates [dt as obs:DataSource]
        │  Metric → Measurement
        ▼
 ② Health events [obs]
    HealthEvent {id, time, source, affectedAsset, condition, confidence,
                 severity, duration, impact, rootCause, missionContext,
                 controlStatus} — DetectionEvent → detectionEventDetects →
                 Deviation [cdm]; PredictedConditionEvent (no deviation yet)
        │  NodeHealthMonitor exchanges along dependency paths
        ▼
 ③ Attribute assessment [assr]
    AssuranceAttributeValue per (node, attribute, source) with confidence
    → fused value (derivedFrom) → AssuranceScore = Node Dependability Score ND
        │  contributesTo
        ▼
 ④ Supervision [di]  (DependabilitySupervisor)
    PropagatedRisk per HazardClass over RiskPropagationEdges that mirror
    typed Dependencies → DependabilityIndex = clip(ND − β·R)
    → aggregatesInto (DIWeight) → SystemDependabilityIndex
    hasAttributeState from DIThreshold → hasDIState (attribute-wise; never from DI)
    ResilienceTrigger: ATTRIBUTE_BREACH | SUSTAINED_DECLINE | PREDICTED_FLOOR_CROSSING
        │                                     ▲ DIForecast (T_pred)
        │ respondsToTrigger                   │
        ▼                                     │
 ⑤ Decision [mit]  (DecisionSupportService = REDS)                 Digital Twin [dt]
    ResponseEvaluation per alternative: hasExpectedIndex ◄──────── producesForecast
    (DIForecast), cost, penalty, admissibility, rank, explanation    providesVirtualSensor
        │ selectedFrom                                              executes Scenario [scen]
        ▼                                                             └ ScenarioResult
 ⑥ Response [mit]  (ResilienceSupervisor = IRDS)                         producesForecast
    ResponseExecution: AuthorisationStatus, authorisedBy (role),
    ResiliencePosture FAIL_OPERATIONAL | FAIL_SAFE, outcome,
    hasOutcomeIndex, recordedOperatorInput
        │ re-enters at ① (virtual-sensor substitution, reconfiguration, ...)
        ▼
 ⑦ Living Dependability Case [assr]
    Evidence (from health events, outputs, operator inputs) supportsClaim /
    challengesClaim → AssuranceClaim → addressesRequirement → Requirement;
    EvidenceObligation PRESENT | MISSING | STALE | UNTRACEABLE;
    di:isRecordedIn, mit:isRecordedIn; AssuranceLevel (isReportedWith DI_sys);
    CertificationReadiness
        │
        ▼
 ⑧ Digital Twin [dt] visualises indices, states, triggers, evaluations,
    executions, claims, AL and the case; presents decisions; records operator input
```

Two timescales: operational data (①–⑧) updates continuously; ontology, hazard models, weights, thresholds, floors and approved controls change only through the governed, versioned process recorded with `warrant:hasVersion`, `warrant:approvedBy`, `warrant:hasApprovalStatus`.

---

## Cross-Module Integration Points

Every object property or subclass axiom in the Turtle sources whose domain or range lies in a different module (core excluded). Derived from the `.ttl` files; the declaring module is the one that imports the other.

### Declared in warrant-observation

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `obs:detectionEventDetects` | `obs:DetectionEvent` → `cdm:Deviation` | **The detection-event rule.** Only path to a Deviation |
| `obs:detects` | `obs:DetectionEvent` → `cdm:Deviation` | SPARQL shortcut only |
| `obs:indicatesCondition` | `obs:HealthEvent` → `cdm:Hazard ∪ cdm:FailureMode ∪ cdm:Deviation ∪ cdm:ThreatScenario` | Health event classified against design-time knowledge |
| `obs:hasRootCause` | `obs:HealthEvent` → `cdm:CausalEntity ∪ obs:HealthEvent ∪ warrant:OperationalEntity` | Diagnosed root cause |
| `obs:captures`, `obs:presents` | `davom:OperatorInterface` → observation items | HMI in/out |
| `davom:HumanOperatorRole ⊑ obs:DataSource` | | Operator roles are data sources |

### Declared in warrant-cdm

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `cdm:propagatesOverDependencyType` | `cdm:HazardClass` → `davom:DependencyType` | Admissible propagation types per hazard class |
| `cdm:affectsComponent` | `cdm:FailureMode ∪ cdm:Vulnerability` → `davom:Component` | FMEA / vulnerability anchoring |
| `cdm:degrades` | hazard / deviation / threat / vulnerability → components, systems, functions, data flows, links, zones | Affected assets |
| `cdm:issues`, `cdm:actsOn`, `cdm:isPerformedUnder` | STPA loop over `davom:ControlAction` and `warrant:OperationalMode` | Control structure |

### Declared in warrant-assurance

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `assr:causesAssuranceDegradation` | `cdm:Deviation ∪ cdm:Hazard ∪ cdm:UnsafeControlAction` → `assr:AssuranceDegradation` | CDM → scoring bridge |
| `assr:wasTriggeredBy` | `assr:AssuranceDegradation` → CDM entities | Traceability back |
| `assr:hasValueSource` | `assr:AssuranceAttributeValue` → `obs:DataSource` | Which source (NHM, sensor, twin, operator) supplied the estimate |
| `assr:hasEvidenceSource` | `assr:Evidence` → `obs:EvidenceEntity ∪ obs:DataSource` | Evidence grounded in observation-layer items |
| `assr:challengesClaim` | `assr:Evidence ∪ obs:HealthEvent ∪ assr:Assumption` → `assr:AssuranceClaim` | Events and invalidated assumptions challenge claims |
| `assr:isChallengedBy` | `assr:Assumption` → `obs:HealthEvent ∪ assr:Evidence` | Assumption invalidation is a monitored condition |
| `assr:claimAppliesTo` | `assr:AssuranceClaim` → `warrant:OperationalEntity ∪ cdm:Control` | Claim scope |
| `assr:assumptionAppliesTo` | `assr:Assumption` → operational entity, causal entity, claim, context | Assumption scope |

### Declared in warrant-di

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `di:contributesTo` | `assr:AssuranceScore` → `di:DependabilityIndex` | Node score ND is the intrinsic input to the node DI |
| `di:hasAttributeState` | `assr:AssuranceAttributeValue` → `di:DependabilityIndexState` | **Attribute-wise state** |
| `di:thresholdAppliesToAttribute` | `di:DIThreshold` → `assr:AssuranceAttribute` | Per-attribute thresholds |
| `di:forHazardClass` | propagated risk / edge / parameter → `cdm:HazardClass` | Typed propagation |
| `di:mirrorsDependency` | `di:RiskPropagationEdge` → `davom:Dependency` | Edge derived from a structural dependency |
| `di:forecastProducedBy` | `di:DIForecast` → `obs:DataSource` | Forecast provenance (the twin is a DataSource) |
| `di:triggeredByAttributeValue` | `di:ResilienceTrigger` → `assr:AssuranceAttributeValue` | T_attr |
| `di:updateTriggeredBy` | `di:DIUpdateEvent` → `obs:HealthEvent ∪ assr:AssuranceDegradation ∪ assr:AssuranceAttributeValue` | Audit |
| `di:isReportedWith` | `di:SystemDependabilityIndex` → `assr:AssuranceLevel` | (DI_sys, AL) reported together |
| `di:isRecordedIn` | indices, triggers, updates → `assr:LivingDependabilityCase` | LDC record |
| `di:DependabilitySupervisor ⊑ obs:AnalyticalService` | | Supervisor is an analytical agent |

### Declared in warrant-scenario

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `scen:hasTrigger` | `scen:Scenario` → `cdm:Deviation ∪ triggers ∪ warrant:EnvironmentalCondition` | Scenario initiation |
| `scen:affects`, `scen:causes` | scenario → DAVOM assets / CDM hazard, risk | Scenario scope |
| `scen:hasProjectedState` | `scen:ScenarioResult` → `di:DependabilityIndexState` | Projected operational state |
| `scen:producesForecast` | `scen:ScenarioResult` → `di:DIForecast` | What-if result as forecast |

### Declared in warrant-mitigation

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `mit:matchesRule` | `cdm:Deviation ∪ cdm:Hazard ∪ di:DependabilityIndexState ∪ di:ResilienceTrigger` → `mit:MitigationRule` | Rule library keyed on trigger (preferred) or state |
| `mit:isTriggeredBy` | `mit:MitigationAction` → deviation, hazard, state, `di:ResilienceTrigger`, `obs:HealthEvent` | What invoked the action |
| `mit:respondsToTrigger` | `mit:ResponseEvaluation` → `di:ResilienceTrigger` | REDS invoked by the resilience criterion |
| `mit:hasExpectedIndex` | `mit:ResponseEvaluation` → `di:DIForecast` | E[DI_sys \| u] from the twin or a scenario |
| `mit:evaluatedWithScenario` | `mit:ResponseEvaluation` → `scen:Scenario` | What-if used for the estimate |
| `mit:violatesConstraint` | `mit:ResponseEvaluation` → `cdm:SafetyConstraint ∪ assr:Requirement` | Exclusion from U_safe |
| `mit:implementsControl` | action / procedure → `cdm:Control` | Runtime response ↔ design-time control |
| `mit:requiresAuthorisationFrom`, `mit:authorisedBy`, `mit:performsMitigation` | ↔ `davom:HumanOperatorRole` (and `obs:AnalyticalService` for automated authority) | Authority allocation |
| `mit:recordedOperatorInput` | `mit:ResponseExecution` → `obs:OperatorInput` | Approval / override as evidence |
| `mit:hasOutcomeIndex` | `mit:ResponseExecution` → `di:DependabilityIndex ∪ di:SystemDependabilityIndex` | Loop closure |
| `mit:isRecordedIn` | evaluation / execution → `assr:LivingDependabilityCase` | LDC record |
| `mit:addresses` | action / procedure → DAVOM assets | Target of the response |
| `mit:DecisionSupportService ⊑ obs:AnalyticalService`, `mit:ResilienceSupervisor ⊑ obs:AnalyticalService` | | REDS and IRDS are analytical agents |

### Declared in warrant-digital-twin

| Axiom | Domain → Range | Semantics |
|---|---|---|
| `dt:DigitalTwin ⊑ obs:DataSource` | | **Producer role:** twin outputs are observation sources |
| `dt:producesForecast` | `dt:DigitalTwin` → `di:DIForecast` | **DT → Supervisor / REDS direction** |
| `dt:providesVirtualSensor` | `dt:DigitalTwin` → `obs:VirtualSensor` | Virtual sensing |
| `dt:receivesUpdateFrom` | `dt:DigitalTwin` → `obs:DataSource` | Live updates |
| `dt:executes`, `dt:storesResult` | `dt:DigitalTwin` → `scen:Scenario`, `scen:ScenarioExecution` | What-if execution |
| `dt:representsStateOf`, `dt:monitors`, `dt:visualises` | twin → `davom:Vessel`, `warrant:OperationalEntity`, `warrant:VisualisableEntity` | Consumer role |
| `X ⊑ warrant:VisualisableEntity` for `warrant:OperationalEntity`, `warrant:AgentEntity`, `di:DependabilityIndex`, `di:SystemDependabilityIndex`, `scen:Scenario`, `scen:ScenarioExecution` | | Visualisable declarations made here; other modules declare their own |

---

## Critical Design Constraints

These constraints are **non-negotiable** across all modules. Violation breaks the semantic integrity of the KG.

### 1. The Detection Event Rule
> A `Deviation` **must** be created via `detectionEventDetects` from a `DetectionEvent`. Direct assertion of `Deviation` individuals without a `DetectionEvent` is prohibited. `DetectionEvent` is the `HealthEvent` that identifies a deviation; a `PredictedConditionEvent` anticipates a condition and is not subject to this rule.

### 2. Operational States Are Closed
> `DependabilityIndexState` (label "Operational State") has exactly five named individuals: `NormalState`, `DegradedState`, `CriticalState`, `FailedState`, `UnsafeState`, totally ordered by severity. Subclassing it is prohibited. New states require formal ontology revision.

### 3. Deviation Types Are Vocabulary, Not Classes
> `Deviation` is never subclassed. Deviation types are expressed via `cdm:hasDeviationType` using the 10-value controlled vocabulary (NO, LESS, MORE, LATE, WRONG, UNAVAILABLE, UNTRUSTED, INCONSISTENT, NOISY, SPOOFED). Named subclasses of `Deviation` are deprecated.

### 4. HumanOperator Is AgentEntity, Not Component
> `HumanOperator` and `HumanOperatorRole` are subclasses of `AgentEntity` (from `warrant-core`), not of `OperationalEntity` or `Component`. Human operators are agents who supervise, authorise and act; their decisions enter the assurance record as evidence, not as equipment state.

### 5. VisualisableEntity Lives in Core
> `warrant:VisualisableEntity` is defined in `warrant-core`. No other module redefines it. Modules that want their classes to be visualisable declare `rdfs:subClassOf warrant:VisualisableEntity` and import only `warrant-core` — they do not import `warrant-digital-twin`.

### 6. Computation Is External
> No computation defined by the methodology is encoded in the ontology: not the confidence-aware fusion of attribute values, the node dependability score, typed risk propagation and its damping/convergence, hierarchical DI aggregation, attribute-wise state assignment, the resilience criterion and margin, REDS response ranking, the Assurance Level, nor Certification Readiness. Formulas appear in module headers as documentation only. The KG stores **inputs**, **governed configuration** (weights, thresholds, floors, windows, horizons, damping factors, decision weights — versioned and approved), **results** with timestamp and `CalculationMethod` identity, and **audit events**. Computation runs in external services and writes back.

### 7. State Is Attribute-Wise; the DI Never Determines It
> Operational state is assigned per attribute from `DIThreshold`s (`hasAttributeState`), and the node or system state is the most severe attribute state across the (critical) nodes (`hasDIState`). The Dependability Index is reported alongside the state as a management composite; it is not a state classifier, not a diagnosis, and not comparable across vessels or modes. Responses are invoked by a `ResilienceTrigger` (attribute breach, sustained decline, predicted floor crossing), not by a DI value. The deprecated DI-value bounds (`hasThreshold`, `hasLowerThreshold`, `hasUpperThreshold`) must not be used.

### 8. Forecasts Live in warrant-di; the Digital Twin Produces Them
> `di:DIForecast` is owned by `warrant-di` and produced by the Digital Twin (`dt:producesForecast`, `di:forecastProducedBy`) or a scenario execution (`scen:producesForecast`). This is how Digital Twin predictions reach the Supervisor's predictive trigger and REDS's expected-effect term without any module importing `warrant-digital-twin`.

### 9. Dependency Direction and Typing
> `davom:dependencySource` is the upstream provider and `davom:dependencyTarget` the downstream consumer; effects flow source → target, matching `di:propagationSource → di:propagationTarget`. Every `Dependency` carries a canonical `hasDependencyType`; a `HazardClass` propagates only over its declared admissible types.

---

## Module Responsibilities — Quick Reference

| Module | Owns | Does NOT own |
|---|---|---|
| `warrant-core` | Abstract superclasses, OperationalMode vocabulary, VisualisableEntity, CalculationMethod, `appliesUnder`, `derivedFrom`, identity/version/validity/approval properties | Any domain-specific class |
| `warrant-davom` | Vessel decomposition, data flows, links, zones and conduits, asset roles, operator roles, control actions, procedures, typed dependencies, DependencyType vocabulary, critical-node flag | Observations, hazards, scores |
| `warrant-cdm` | Deviation (+ DeviationType), Hazard, Risk (+ impact triple), Accident, Loss, STPA loop, FailureMode (+ FMEA ratings), ThreatScenario, Vulnerability, Control (+ residual risk), HazardClass (+ admissible types) | Metrics, scores, DI, runtime responses |
| `warrant-observation` | Metric, Measurement, DataSource, Observer / VirtualSensor, AnalyticalService, NodeHealthMonitor (+ MonitoringLevel), HealthEvent / DetectionEvent / PredictedConditionEvent with the full record, operator inputs | Causal chain, scoring |
| `warrant-assurance` | Six attributes, AssuranceAttributeValue (+ source, confidence, fusion), AssuranceWeight (α), AssuranceScore (= ND), AssuranceDegradation, Penalty; Requirement, AssuranceClaim (+ ClaimStatus), Assumption, Evidence, EvidenceObligation (+ ObligationStatus), Nonconformity, AssuranceLevel (+ weight set), CertificationReadiness, LivingDependabilityCase | DI formula, causal chain, response records |
| `warrant-di` | DependabilityIndex, SystemDependabilityIndex, operational states (closed), DIThreshold (per attribute), hasAttributeState, PropagatedRisk / RiskPropagationEdge / RiskPropagationParameter (typed by HazardClass), DIWeight and aggregatesInto, SupervisionConfiguration, ResilienceTrigger (+ types), DIForecast, DependabilitySupervisor, DICalculationMethod, DIUpdateEvent | Node-score formula, detection, response ranking |
| `warrant-scenario` | Scenario (×5 types), ScenarioTrigger (×4), ScenarioExecution (+ lifecycle states), ScenarioResult (+ projected state, forecasts) | Mitigation rules, DT visualisation |
| `warrant-mitigation` | MitigationRule, MitigationAction (Advisory / MachineActionable), FailoverProcedure, RedundantResource, RecoveryEffect, ResponseStrategyType, ResiliencePosture, AuthorisationStatus, DecisionSupportService (REDS), ResponseEvaluation, DecisionConfiguration, ResilienceSupervisor (IRDS), ResponseExecution | Detection, scoring, DT |
| `warrant-digital-twin` | DigitalTwin (as DataSource and forecast producer), Views, Layers, DecisionSupportView, producesForecast, providesVirtualSensor | Domain knowledge; forecasts (owned by di) |

---

## Living Lab Instantiation Pattern

Each WARRaNT living lab creates a set of named individuals that populate the full module stack. `examples/example-gnss-failover.ttl` instantiates every line below.

```
Vessel (DAVOM)
  → VesselFunction [hasAssetRole PRIMARY_ASSET, isCriticalNode] (DAVOM)
      → System / Subsystem / Component [SUPPORTING_ASSET, belongsToZone] (DAVOM)
      → CommunicationLink / Conduit [connectsZone] (DAVOM)
      → Dependency [hasDependencyType, weight, source=provider, target=consumer] (DAVOM)
  → Design-time knowledge (CDM)
      → FailureMode [FMEA ratings] → producesDeviation
      → Hazard [hasHazardClass] → isEvaluatedAs → Risk [likelihood, impact triple]
      → ThreatScenario → exploits → Vulnerability
      → Control [mitigates, hasResidualRisk]
      → Requirement ← addressesRequirement ← AssuranceClaim [hasClaimStatus]; Assumption (Assurance)
  → Observation
      → Metric → Measurement [external record reference]
      → Sensor / VirtualSensor [substitutesFor] / AnalyticalService / NodeHealthMonitor [monitorsNode, level]
          → DetectionEvent (HealthEvent record) → detectionEventDetects → Deviation [hasDeviationType]
          → PredictedConditionEvent (from the twin or a monitor)
  → Attribute assessment (Assurance)
      → AssuranceAttribute × k → AssuranceWeight [appliesUnder mode]
      → AssuranceAttributeValue [hasValueSource, hasSourceConfidence] → fused value [derivedFrom]
      → AssuranceDegradation → updatesAssuranceScore → AssuranceScore (ND) [scoreValue, calculatedAt]
  → Supervision (DI)
      → DIThreshold per (node, attribute) → hasAttributeState on each value
      → PropagatedRisk [forHazardClass, local, propagated] ; RiskPropagationEdge [mirrorsDependency]
      → DependabilityIndex [DIValue, betaWeight, aggregatedRisk, hasDIState, appliesTo]
      → DIWeight [parent, child, γ] → aggregatesInto → SystemDependabilityIndex [state, trend, margin]
      → SupervisionConfiguration [W, ε, T_p, φ] ; RiskPropagationParameter [ρ_h]
      → DIUpdateEvent ; DIForecast [forecastProducedBy twin] ; ResilienceTrigger [type, triggeredBy*]
  → Scenario: Scenario → ScenarioExecution [lifecycle] → ScenarioResult [projected state, producesForecast]
  → Decision and response (Mitigation)
      → MitigationRule → recommends → MitigationAction [strategy, posture, implementsControl, requiresAuthorisationFrom]
      → ResponseEvaluation × alternatives [respondsToTrigger, hasExpectedIndex, cost, penalty, rank, admissible]
      → ResponseExecution [selectedFrom, authorisation, authorisedBy, posture, outcome, hasOutcomeIndex, operator input]
  → Living Dependability Case (Assurance)
      → Evidence [hasEvidenceSource, supports/challengesClaim, quality, validity]
      → EvidenceObligation [status PRESENT | MISSING | STALE | UNTRACEABLE]
      → Nonconformity ; AssuranceLevel [EC, EF, EQ, MC, TC, weight set] ; CertificationReadiness [RC, NC]
      → LivingDependabilityCase [includes*, baseline version] ← isRecordedIn (indices, triggers, evaluations, executions)
  → DigitalTwin (DT) [DataSource]
      → producesForecast, providesVirtualSensor, executes, storesResult, receivesUpdateFrom
      → visualises: indices, states, triggers, hazards, evaluations, executions, claims, AL, the case
```

This pattern is instantiated in five validated examples:
- **GNSS Failover** (LL4 MAI-W) — the reference instantiation of every layer above; UNAVAILABLE deviation, INS/AIS virtual-sensor substitution, attribute breach and predicted-floor-crossing triggers, three ranked alternatives, authorised fail-operational execution, challenged navigation-integrity claim
- **Communication Degradation** (LL4 MAI-W) — MORE + LATE deviations, DI propagation
- **Smart Container Fire** (LL2 AELER) — UNAVAILABLE + LATE, FMEA failure modes, CriticalState
- **ROC Handover** (LL4 MAI-W) — WRONG process-model flaw + LATE deviation, human supervision dependency
- **ECDIS AIS Spoofing** (LL1 Danaos) — SPOOFED deviation, CyberattackScenario, UnsafeState

All five conform to `shapes/warrant-core-shapes.ttl` (`python scripts/validate_turtle.py --shacl`) and are exercised by `queries/competency-queries.sparql`.

---

## Extension Points

The ontology is designed to be extended in the following ways without breaking existing deployments:

| Extension | Mechanism |
|---|---|
| New component type | Add `rdfs:subClassOf davom:Component` in a domain extension module |
| New assurance attribute | Requires ontology revision — the six attributes are closed |
| New operational state | Prohibited — the five states are closed |
| New deviation type | Add a `cdm:DeviationType` individual (ontology revision) |
| New hazard class | Add a `cdm:HazardClass` individual **with** its `propagatesOverDependencyType` declaration (ontology revision) |
| New dependency type | Ontology revision — the five canonical types are the propagation basis |
| New response strategy or authorisation status | Add a vocabulary individual (ontology revision) |
| New trigger type, posture, obligation status | Prohibited — these vocabularies are defined by the methodology |
| New scenario type | Add `rdfs:subClassOf scen:Scenario` |
| New mitigation action | Add `rdfs:subClassOf mit:MitigationAction` |
| New visualisable entity | Declare `rdfs:subClassOf warrant:VisualisableEntity` in any module |
| New calculation | Add a `warrant:CalculationMethod` individual; never a formula |
| New living lab | Instantiate the full individual pattern; no schema change needed |
