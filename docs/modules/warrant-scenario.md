# `warrant-scenario` — Scenario

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/scenario#`  
**Prefix:** `scen:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/scenario`  
**Imports:** `warrant-cdm`, `warrant-core`, `warrant-di`  
**Version:** `1.0.0`

---

## Purpose

Scenario semantics for what-if cases: cyberattack, failure, degraded operation, environmental, and unsafe control scenarios, their executions (with a lifecycle state) and results. A scenario result may carry a projected operational state and produce di:DIForecast individuals, which is how Digital Twin what-if analysis feeds the Supervisor's predictive trigger and REDS's expected-effect estimates. The KG defines scenario semantics; the external scenario engine (typically hosted by the Digital Twin) executes them.

**Role:** what-if semantics. Scenario types (cyberattack, failure, degraded
operation, environmental, unsafe control), triggers, executions with a
lifecycle state, and results that carry a projected operational state and
produce DI forecasts.

**Design rules**

1. The graph defines scenario semantics; the external scenario engine (typically hosted by the Digital Twin) executes them and writes back `ScenarioResult`.
2. `ScenarioExecutionState` (PENDING, RUNNING, COMPLETED, FAILED) is an execution lifecycle; it is not a dependability state. The projected operational state is `hasProjectedState` on the result.
3. `producesForecast` is how a scenario execution feeds the Supervisor's predictive trigger and the REDS expected-effect estimate.

---

## Classes (14)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `scen:CyberattackScenario` | `scen:Scenario` | Cyberattack Scenario |  |
| `scen:DegradedOperationScenario` | `scen:Scenario` | Degraded Operation Scenario |  |
| `scen:DeviationTrigger` | `scen:ScenarioTrigger` | Deviation Trigger |  |
| `scen:EnvironmentalScenario` | `scen:Scenario` | Environmental Scenario |  |
| `scen:EventTrigger` | `scen:ScenarioTrigger` | Event Trigger |  |
| `scen:Failure` | `scen:ScenarioTrigger` | Failure |  |
| `scen:FailureScenario` | `scen:Scenario` | Failure Scenario |  |
| `scen:Scenario` | `warrant:VisualisableEntity` | Scenario | A simulated what-if case: cyberattack, failure, degraded operation, environmental, or unsafe control. The external scenario engine executes it. |
| `scen:ScenarioExecution` | `warrant:VisualisableEntity` | Scenario Execution | A specific execution instance of a Scenario, with state, timestamps, and result. |
| `scen:ScenarioExecutionState` | — | Scenario Execution State | Controlled vocabulary for the lifecycle of a ScenarioExecution: PENDING → RUNNING → COMPLETED \| FAILED. Named individuals only. This is an execution lifecycle, not a dependability state; it must not be confused with di:DependabilityIndexState. Moved here from warrant-digital-twin, where the class existed without individuals. |
| `scen:ScenarioResult` | — | Scenario Result | Stores the outcome of a ScenarioExecution: result summary, the projected operational state if the scenario plays out (scen:hasProjectedState), and the quantitative DI forecasts it produced (scen:producesForecast → di:DIForecast), e.g. the projected system DI unmitigated and under each candidate response. Owned by this module; the DT module references but does not redefine it. |
| `scen:ScenarioTrigger` | — | Scenario Trigger |  |
| `scen:Threat` | `scen:ScenarioTrigger` | Threat |  |
| `scen:UnsafeControlScenario` | `scen:Scenario` | Unsafe Control Scenario |  |

## Controlled vocabularies (named individuals)

### `scen:ScenarioExecutionState`

| Individual | Label | Description |
|---|---|---|
| `scen:COMPLETED` | COMPLETED | Execution finished; ScenarioResult available. |
| `scen:FAILED` | FAILED | Execution failed; partial results may be available. |
| `scen:PENDING` | PENDING | Scenario queued; trigger confirmed but execution not yet started. |
| `scen:RUNNING` | RUNNING | Execution in progress; projections being computed. |

## Object properties (9)

| Property | Domain | Range | Description |
|---|---|---|---|
| `scen:affects` | `scen:Scenario` ∪ `cdm:Deviation` ∪ `cdm:Hazard` | `davom:Component` ∪ `davom:System` ∪ `davom:VesselFunction` | affects |
| `scen:causes` | `scen:Scenario` | `cdm:Risk` ∪ `cdm:Hazard` | causes |
| `scen:hasExecutionState` | `scen:ScenarioExecution` | `scen:ScenarioExecutionState` | Lifecycle state of the execution (PENDING, RUNNING, COMPLETED, FAILED). Formerly ranged over di:DependabilityIndexState, which conflated the execution lifecycle with the operational state; the projected operational state is now scen:hasProjectedState on the result. |
| `scen:hasProjectedState` | `scen:ScenarioResult` | `di:DependabilityIndexState` | The operational state the scenario projects for the affected node or system if it plays out (unmitigated unless the result is for a specific response). |
| `scen:hasScenarioExecution` | `scen:Scenario` | `scen:ScenarioExecution` | has scenario execution |
| `scen:hasScenarioParameter` | `scen:Scenario` | `owl:Thing` | has scenario parameter |
| `scen:hasScenarioResult` | `scen:ScenarioExecution` | `scen:ScenarioResult` | has scenario result |
| `scen:hasTrigger` | `scen:Scenario` | `cdm:Deviation` ∪ `scen:Failure` ∪ `scen:Threat` ∪ `warrant:EnvironmentalCondition` ∪ `scen:EventTrigger` | has trigger |
| `scen:producesForecast` | `scen:ScenarioResult` | `di:DIForecast` | A DI forecast generated by this scenario execution: the projected node or system DI over the horizon, either unmitigated or conditional on a candidate response. Consumed by the Supervisor's predictive trigger (di:triggeredByForecast) and by REDS (mit:hasExpectedIndex). |

## Datatype properties (2)

| Property | Domain | Range | Description |
|---|---|---|---|
| `scen:hasExecutionTimestamp` | `scen:ScenarioExecution` | `xsd:dateTime` | has execution timestamp |
| `scen:hasResultSummary` | `scen:ScenarioResult` | `xsd:string` | Human-readable outcome description of the scenario execution. |

