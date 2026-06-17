# WARRaNT Ontology — Module Integration Guide

**Project:** WARRaNT — Horizon Europe RIA 101202581  
**Scope:** Nine-module ontology stack for vessel dependability monitoring, assurance scoring, and Digital Twin decision support  
**Status:** Stable (PoC demonstrators active at LL1, LL2, LL4)

---

## Overview

The WARRaNT ontology is structured as a directed acyclic graph of nine modules. Each module has a precisely scoped responsibility; no module replicates concepts defined by another. Integration happens through **typed object properties** that cross module boundaries — a `Deviation` (CDM) is detected by a `DetectionEvent` (Observation), causes an `AssuranceDegradation` (CDM → Assurance), which updates an `AssuranceScore` (Assurance), which feeds a `DependabilityIndex` (DI), which the `DigitalTwin` (DT) visualises and responds to with a `MitigationRule` (Mitigation).

---

## Module Dependency Graph

```
warrant-core
    │
    ├──► warrant-davom
    │        │
    │        ├──► warrant-cdm
    │        │        │
    │        │        ├──► warrant-observation ──► warrant-assurance ──► warrant-di
    │        │        │                                                       │
    │        │        └──► warrant-assurance ─────────────────────────────────┤
    │        │                                                                 │
    │        ├──────────────────────────────────────────────────► warrant-di  │
    │        │                                                                 │
    │        ├──► warrant-scenario ─────────────────────────────────────────► │
    │        │                                                                 │
    │        └──► warrant-mitigation ──────────────────────────────────────── │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┼──► warrant-digital-twin
```

**Reading rule:** an arrow from A to B means A is imported by B (B depends on A).

| Module | Imports | Depended on by |
|---|---|---|
| `warrant-core` | *(none)* | all modules |
| `warrant-davom` | core | cdm, observation, di, scenario, mitigation, dt |
| `warrant-cdm` | core, davom | observation, assurance, di, scenario, mitigation |
| `warrant-observation` | core, davom, cdm | assurance, di |
| `warrant-assurance` | core, davom, cdm | di |
| `warrant-di` | core, davom, assurance | scenario, mitigation, dt |
| `warrant-scenario` | core, davom, cdm, di | mitigation, dt |
| `warrant-mitigation` | core, davom, cdm, di | dt |
| `warrant-digital-twin` | all modules | *(none)* |

---

## The Core Data Flow

The WARRaNT knowledge graph is driven by a single end-to-end data flow that runs continuously during vessel operation:

```
① Physical world
        │  sensor readings, operator reports
        ▼
② Observation (warrant-observation)
   Metric → Measurement → AnalyticalService
        │
        │  producesDetectionEvent
        ▼
③ Detection (warrant-observation)
   DetectionEvent
        │
        │  detectionEventDetects  [RED — critical path]
        ▼
④ Causal reasoning (warrant-cdm)
   Deviation → Hazard → Risk
        │
        │  causesAssuranceDegradation
        ▼
⑤ Assurance scoring (warrant-assurance)
   AssuranceDegradation → AssuranceScore (recomputed)
        │
        │  contributesTo
        ▼
⑥ Dependability indexing (warrant-di)
   DependabilityIndex (updated DI value + state)
        │
        ├──► DI state change triggers scenario
        │         warrant-scenario → ScenarioExecution → ScenarioResult
        │
        └──► DI state change matches mitigation rule
                  warrant-mitigation → AdvisoryAction → FailoverProcedure
                        │
                        ▼
⑦ Digital Twin (warrant-digital-twin)
   DigitalTwin visualises state, presents advisories, records results
```

---

## Cross-Module Integration Points

The following table identifies every inter-module property — the precise "stitches" that hold the ontology together.

### warrant-cdm ↔ warrant-observation

| Property | Direction | Semantics |
|---|---|---|
| `obs:detectionEventDetects` | Observation → CDM | A `DetectionEvent` grounds a `Deviation` |
| `obs:producesDetectionEvent` | Observation → CDM | A `DataSource` produces a `DetectionEvent` |

### warrant-cdm ↔ warrant-assurance

| Property | Direction | Semantics |
|---|---|---|
| `cdm:causesAssuranceDegradation` | CDM → Assurance | A `Deviation` / `UCA` triggers an `AssuranceDegradation` |
| `assurance:updatesAssuranceScore` | Assurance (internal) | `AssuranceDegradation` updates an `AssuranceScore` |

### warrant-assurance ↔ warrant-di

| Property | Direction | Semantics |
|---|---|---|
| `assurance:contributesTo` | Assurance → DI | `AssuranceScore` is an input to a `DependabilityIndex` |
| `di:appliesTo` | DI → DAVOM | `DependabilityIndex` applies to a `VesselFunction` / `System` |

### warrant-di ↔ warrant-scenario

| Property | Direction | Semantics |
|---|---|---|
| `scenario:hasProjectedDIState` | Scenario → DI | Scenario projects a future `DependabilityIndexState` |
| `scenario:hasTrigger` → `DeviationTrigger` | Scenario → CDM | Scenario initiated by a `Deviation` |

### warrant-di ↔ warrant-mitigation

| Property | Direction | Semantics |
|---|---|---|
| `mitigation:matchesDIState` | Mitigation → DI | Rule fires when a specific DI state is entered |
| `mitigation:hasRecoveryEffect` → `projectedDIGain` | Mitigation (internal) | Recovery effect projects DI improvement |

### warrant-scenario ↔ warrant-mitigation

| Property | Direction | Semantics |
|---|---|---|
| `scenario:involvesRisk` → `mitigation:matchesRisk` | Scenario ↔ Mitigation | Risk in a scenario is the same `Risk` matched by a mitigation rule |

### warrant-digital-twin ↔ all upstream modules

| Property | Domain | Range module | Semantics |
|---|---|---|---|
| `dt:representsStateOf` | DT | DAVOM | Twin mirrors a `Vessel` |
| `dt:monitors` | DT | Core | Twin monitors `OperationalEntity` |
| `dt:receivesUpdateFrom` | DT | Observation | Twin receives live data from `DataSource` |
| `dt:executes` | DT | Scenario | Twin executes a `Scenario` |
| `dt:storesResult` | DT | Scenario | Twin stores `ScenarioExecution` results |
| `dt:visualises` | DT | Core (VisualisableEntity) | Twin visualises any `VisualisableEntity` |

---

## Critical Design Constraints

These constraints are **non-negotiable** across all modules. Violation breaks the semantic integrity of the KG.

### 1. The Detection Event Rule
> A `Deviation` **must** be created via `detectionEventDetects` from a `DetectionEvent`. Direct assertion of `Deviation` individuals without a `DetectionEvent` is prohibited.

This ensures every deviation claim is auditable and traceable to a specific observation event.

### 2. DI States Are Closed
> `DependabilityIndexState` has exactly five named individuals. Subclassing it is prohibited. New states require formal ontology revision.

The five states (`NormalState`, `DegradedState`, `CriticalState`, `FailedState`, `UnsafeState`) form a complete severity ordering that the Digital Twin uses for colour coding and threshold triggering.

### 3. Deviation Types Are Vocabulary, Not Classes
> `Deviation` is never subclassed. Deviation types are expressed via `cdm:hasDeviationType` using the 10-value controlled vocabulary (NO, LESS, MORE, LATE, WRONG, UNAVAILABLE, UNTRUSTED, INCONSISTENT, NOISY, SPOOFED). Named subclasses of `Deviation` are deprecated.

This enables uniform SPARQL querying across all deviation types and avoids ontology proliferation.

### 4. HumanOperator Is AgentEntity, Not Component
> `HumanOperator` and `HumanOperatorRole` are subclasses of `AgentEntity` (from `warrant-core`), not of `OperationalEntity` or `Component`. Human operators are agents who supervise and act; they do not degrade like components.

### 5. VisualisableEntity Lives in Core
> `warrant:VisualisableEntity` is defined in `warrant-core`. No other module redefines it. Modules that want their classes to be visualisable declare `rdfs:subClassOf warrant:VisualisableEntity` and import only `warrant-core` — they do not import `warrant-digital-twin`.

### 6. Computation Is External
> Neither the assurance formula (A_v = Σβₖ·x_v^(k)) nor the DI formula (DI_i = A_i − β·R̃_i) is encoded in the ontology. Computation runs in external services (Python, SPARQL update). The KG stores inputs, weights, results, and audit events only.

---

## Module Responsibilities — Quick Reference

| Module | Owns | Does NOT own |
|---|---|---|
| `warrant-core` | Abstract superclasses, OperationalMode vocabulary, VisualisableEntity | Any domain-specific class |
| `warrant-davom` | Vessel decomposition, operator roles, dependencies, control actions | Observations, hazards, scores |
| `warrant-cdm` | Deviation, Hazard, Risk, Accident, Loss, STPA control loop, AssuranceDegradation | Metrics, scores, DI |
| `warrant-observation` | DetectionEvent, Metric, Measurement, DataSource, AnalyticalService | Causal chain, scoring |
| `warrant-assurance` | AssuranceScore, AssuranceAttribute (×6), weights, penalties | DI formula, causal chain |
| `warrant-di` | DependabilityIndex, SystemDI, DI states, RiskPropagationEdge | Assurance formula, detection |
| `warrant-scenario` | Scenario (×5 types), ScenarioExecution, ScenarioTrigger (×4) | Mitigation rules, DT visualisation |
| `warrant-mitigation` | MitigationRule, AdvisoryAction, FailoverProcedure, RecoveryEffect | Detection, scoring, DT |
| `warrant-digital-twin` | DigitalTwin, Views, Layers, ScenarioExecutionState | Domain knowledge |

---

## Living Lab Instantiation Pattern

Each WARRaNT living lab creates a set of named individuals that populate the full module stack:

```
Vessel individual (DAVOM)
  → VesselFunction individuals (DAVOM)
      → System / Component individuals (DAVOM)
          → Metric individuals (Observation)
              → Measurement individuals (Observation) [time-series anchors]
              → AnalyticalService individual (Observation)
                  → DetectionEvent individual (Observation)
                      → Deviation individual (CDM) [hasDeviationType: ...]
                          → Hazard individual (CDM)
                              → Risk individual (CDM) [likelihood, impact, severity]
                          → AssuranceDegradation individual (CDM)
                              → AssuranceScore individual (Assurance) [scoreValue, calculatedAt]
                                  → DependabilityIndex individual (DI) [DIValue, DIState, betaWeight]
                                      → MitigationRule individual (Mitigation)
                                          → AdvisoryAction individual (Mitigation)
                                              → FailoverProcedure individual (Mitigation)
  → DigitalTwin individual (DT)
      → visualises: DI, Hazard, Risk, MitigationAction, Scenario, ...
```

This pattern is instantiated in five validated examples:
- **GNSS Failover** (LL4 MAI-W) — UNAVAILABLE deviation, INS/AIS failover
- **Communication Degradation** (LL4 MAI-W) — MORE + LATE deviations, DI propagation
- **Smart Container Fire** (LL2 AELER) — UNAVAILABLE + LATE, CriticalState DI
- **ROC Handover** (LL4 MAI-W) — WRONG flaw + LATE deviation, human supervision dependency
- **ECDIS AIS Spoofing** (LL1 Danaos) — SPOOFED deviation, CyberattackScenario, UnsafeState DI

---

## Extension Points

The ontology is designed to be extended in the following ways without breaking existing deployments:

| Extension | Mechanism |
|---|---|
| New component type | Add `rdfs:subClassOf davom:Component` in a domain extension module |
| New assurance attribute | Requires ontology revision — the six attributes are closed |
| New DI state | Requires ontology revision — the five states are closed |
| New deviation type | Add value to `hasDeviationType` vocabulary (controlled string) |
| New scenario type | Add `rdfs:subClassOf scenario:Scenario` |
| New mitigation action | Add `rdfs:subClassOf mitigation:MitigationAction` |
| New visualisable entity | Declare `rdfs:subClassOf warrant:VisualisableEntity` in any module |
| New living lab | Instantiate the full individual pattern; no schema change needed |
