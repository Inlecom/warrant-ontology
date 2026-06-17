# `warrant-scenario` — Scenario Module

**Namespace:** `https://w3id.org/warrant/scenario#`  
**Prefix:** `scenario:`  
**Status:** Stable  
**Role:** Simulation layer — defines the vocabulary for representing, triggering, executing, and recording the outcomes of operational and risk scenarios within the WARRaNT Digital Twin.

---

## Purpose

`warrant-scenario` enables the Digital Twin to move beyond passive monitoring into **active "what-if" reasoning**. A scenario is a structured description of a potential operational situation — a failure mode, a cyber attack, a weather degradation event — that can be executed in the Digital Twin to project its effects on the DI, assurance scores, and required mitigations.

Scenarios are both *descriptive* (documenting known risk scenarios from safety analyses) and *executable* (the Digital Twin can run them to project DI evolution and mitigation effectiveness).

---

## Class Hierarchy

```
Scenario
├── FailureScenario          (component or system failure)
├── DegradationScenario      (gradual performance reduction)
├── CyberattackScenario      (adversarial cyber intervention)
├── WeatherScenario          (environmental condition change)
└── HumanErrorScenario       (operator error or procedure violation)

ScenarioExecution            (a specific run of a Scenario in the Digital Twin)
ScenarioResult               (the recorded outcome of a ScenarioExecution)

ScenarioTrigger              (what initiates a scenario)
├── FailureTrigger           (triggered by component failure)
├── ThreatTrigger            (triggered by a detected threat)
├── EventTrigger             (triggered by a DetectionEvent)
└── DeviationTrigger         (triggered by a specific Deviation)
```

---

## Scenario Lifecycle

A scenario follows a defined lifecycle when executed in the Digital Twin:

```
Scenario
  → scenario:hasTrigger → ScenarioTrigger
      [trigger conditions met]
  → scenario:executes → ScenarioExecution
      [lifecycle: PENDING → RUNNING → COMPLETED | FAILED]
  → scenario:hasResult → ScenarioResult
      [DI projection, assurance impact, recommended mitigations]
```

The lifecycle state of a `ScenarioExecution` is tracked by `warrant-digital-twin` as a `ScenarioExecutionState` — the scenario module defines the semantic content; the digital-twin module manages the execution state.

---

## Trigger Types

| Class | Trigger condition |
|---|---|
| `FailureTrigger` | A `Component` or `System` transitions to a failed state |
| `ThreatTrigger` | A security threat is identified (e.g., cyber attack detected by IDS) |
| `EventTrigger` | A `DetectionEvent` with a specified type is produced |
| `DeviationTrigger` | A `Deviation` of a specified `hasDeviationType` is recorded |

Triggers connect the passive observation layer (`warrant-observation`) to the active scenario layer — a `DetectionEvent` or `Deviation` can automatically initiate a scenario execution in the Digital Twin.

---

## Scenario Content

Each `Scenario` individual specifies:

- **`hasTrigger`** → the condition that initiates it
- **`involvesDeviation`** → the deviation(s) it models
- **`involvesHazard`** → the hazard(s) it addresses
- **`involvesRisk`** → the risk(s) it evaluates
- **`affectsComponent`** / **`affectsSystem`** / **`affectsVesselFunction`** → the structural scope
- **`underCondition`** → the `EnvironmentalCondition` context
- **`hasProjectedDIState`** → the DI state projected if the scenario plays out unmitigated

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `scenario:hasTrigger` | `Scenario` | `ScenarioTrigger` | What initiates this scenario |
| `scenario:involvesDeviation` | `Scenario` | `Deviation` | Deviation(s) central to this scenario |
| `scenario:involvesHazard` | `Scenario` | `Hazard` | Hazard(s) this scenario models |
| `scenario:involvesRisk` | `Scenario` | `Risk` | Risk(s) assessed in this scenario |
| `scenario:affectsComponent` | `Scenario` | `Component` | Component(s) in scope |
| `scenario:affectsSystem` | `Scenario` | `System` | System(s) in scope |
| `scenario:affectsVesselFunction` | `Scenario` | `VesselFunction` | Function(s) in scope |
| `scenario:underCondition` | `Scenario` | `EnvironmentalCondition` | Environmental context |
| `scenario:hasProjectedDIState` | `Scenario` | `DependabilityIndexState` | Projected DI outcome |
| `scenario:executes` | `DigitalTwin` | `ScenarioExecution` | DT runs this scenario |
| `scenario:hasResult` | `ScenarioExecution` | `ScenarioResult` | Recorded execution outcome |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `scenario:scenarioId` | `Scenario` | `xsd:string` | Unique scenario identifier |
| `scenario:description` | `Scenario` | `xsd:string` | Human-readable description |
| `scenario:executionStatus` | `ScenarioExecution` | `xsd:string` | PENDING / RUNNING / COMPLETED / FAILED |
| `scenario:startedAt` | `ScenarioExecution` | `xsd:dateTime` | Execution start timestamp |
| `scenario:completedAt` | `ScenarioExecution` | `xsd:dateTime` | Execution completion timestamp |
| `scenario:projectedDIValue` | `ScenarioResult` | `xsd:decimal` | Projected DI if scenario plays out |
| `scenario:mitigationEffectiveness` | `ScenarioResult` | `xsd:decimal` | Projected DI if mitigations applied |

---

## Relationship to Other Modules

| Module | Relationship |
|---|---|
| `warrant-cdm` | Scenarios involve `Deviation`, `Hazard`, `Risk` from CDM |
| `warrant-davom` | Scenarios affect `Component`, `System`, `VesselFunction` from DAVOM |
| `warrant-observation` | `EventTrigger` / `DeviationTrigger` respond to `DetectionEvent` / `Deviation` |
| `warrant-di` | `hasProjectedDIState` references DI state named individuals; `ScenarioResult` carries projected DI values |
| `warrant-mitigation` | Scenario results inform mitigation selection; mitigations reference scenarios they address |
| `warrant-digital-twin` | `DigitalTwin` executes scenarios and stores `ScenarioExecution` results |

---

## Design Principles

1. **Scenarios are both documentation and execution.** A `Scenario` individual can exist as a documented risk scenario (linked to safety analysis artefacts) and be activated for execution in the DT — they are the same individual.
2. **Triggers are typed.** The four trigger types enable the DT to automatically initiate the right scenario when specific detection events or deviations are observed.
3. **Results are first-class.** `ScenarioResult` individuals carry projected DI values and mitigation effectiveness scores, making scenario outcomes queryable and comparable across runs.

---

## Imports

- `warrant-core`
- `warrant-davom`
- `warrant-cdm`
- `warrant-di`

---

## Downstream Dependents

`warrant-mitigation` · `warrant-digital-twin`
