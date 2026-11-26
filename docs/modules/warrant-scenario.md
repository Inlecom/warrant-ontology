# `warrant-scenario` — Scenario

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/scenario#`  
**Prefix:** `scen:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/scenario`  
**Imports:** `warrant-cdm`, `warrant-core`, `warrant-di`  
**Version:** `0.11-poc`

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

## Classes (17)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `scen:CyberattackScenario` | `scen:Scenario` | Cyberattack Scenario |  |
| `scen:DegradedOperationScenario` | `scen:Scenario` | Degraded Operation Scenario |  |
| `scen:DeviationTrigger` | `scen:ScenarioTrigger` | Deviation Trigger |  |
| `scen:EnvironmentalScenario` | `scen:Scenario` | Environmental Scenario |  |
| `scen:EventTrigger` | `scen:ScenarioTrigger` | Event Trigger |  |
| `scen:ExecutionMode` | — | Execution Mode | Controlled vocabulary for how a scenario execution was run. Named individuals only. |
| `scen:Failure` | `scen:ScenarioTrigger` | Failure |  |
| `scen:FailureScenario` | `scen:Scenario` | Failure Scenario |  |
| `scen:ManifestEntry` | — | Manifest Entry | One versioned item a scenario execution used: a governed configuration (key = configuration name, value = its version), a source repository (key = repository, value = commit), or a software package (key = package, value = version). Key via warrant:hasName, value via warrant:hasVersion, kind via scen:hasEntryKind. |
| `scen:ManifestEntryKind` | — | Manifest Entry Kind | Controlled vocabulary of manifest entry kinds. Named individuals only. |
| `scen:Scenario` | `warrant:VisualisableEntity` | Scenario | A simulated what-if case: cyberattack, failure, degraded operation, environmental, or unsafe control. The external scenario engine executes it. |
| `scen:ScenarioExecution` | `warrant:VisualisableEntity` | Scenario Execution | A specific execution instance of a Scenario, with state, timestamps, result, and the run manifest that makes it reproducible: execution mode, random seeds, scenario file and its hash, input dataset hash, start and finish times, and one manifest entry per configuration version, source commit and package version used (scen:hasManifestEntry). The run identifier is warrant:hasIdentifier. |
| `scen:ScenarioExecutionState` | — | Scenario Execution State | Controlled vocabulary for the lifecycle of a ScenarioExecution: PENDING → RUNNING → COMPLETED \| FAILED. Named individuals only. This is an execution lifecycle, not a dependability state; it must not be confused with di:DependabilityIndexState. Moved here from warrant-digital-twin, where the class existed without individuals. |
| `scen:ScenarioResult` | — | Scenario Result | Stores the outcome of a ScenarioExecution: result summary, the projected operational state if the scenario plays out (scen:hasProjectedState), and the quantitative DI forecasts it produced (scen:producesForecast → di:DIForecast), e.g. the projected system DI unmitigated and under each candidate response. Owned by this module; the DT module references but does not redefine it. |
| `scen:ScenarioTrigger` | — | Scenario Trigger |  |
| `scen:Threat` | `scen:ScenarioTrigger` | Threat |  |
| `scen:UnsafeControlScenario` | `scen:Scenario` | Unsafe Control Scenario |  |

## Controlled vocabularies (named individuals)

### `scen:ExecutionMode`

| Individual | Label | Description |
|---|---|---|
| `scen:LOCKSTEP` | LOCKSTEP | All services stepped by one simulated clock in one process; deterministic for a given manifest. |
| `scen:REPLAY` | REPLAY | Recorded operational data replayed open loop through the services; no closed-loop plant. |
| `scen:SERVICE` | SERVICE | Services run as separate processes exchanging messages in (scaled) real time; timing-dependent and not bit-reproducible. |

### `scen:ManifestEntryKind`

| Individual | Label | Description |
|---|---|---|
| `scen:CONFIGURATION_VERSION` | CONFIGURATION_VERSION |  |
| `scen:PACKAGE_VERSION` | PACKAGE_VERSION |  |
| `scen:SOURCE_COMMIT` | SOURCE_COMMIT |  |

### `scen:ScenarioExecutionState`

| Individual | Label | Description |
|---|---|---|
| `scen:COMPLETED` | COMPLETED | Execution finished; ScenarioResult available. |
| `scen:FAILED` | FAILED | Execution failed; partial results may be available. |
| `scen:PENDING` | PENDING | Scenario queued; trigger confirmed but execution not yet started. |
| `scen:RUNNING` | RUNNING | Execution in progress; projections being computed. |

## Object properties (12)

| Property | Domain | Range | Description |
|---|---|---|---|
| `scen:affects` | `scen:Scenario` ∪ `cdm:Deviation` ∪ `cdm:Hazard` | `davom:Component` ∪ `davom:System` ∪ `davom:VesselFunction` ∪ `davom:CommunicationLink` | affects |
| `scen:causes` | `scen:Scenario` | `cdm:Risk` ∪ `cdm:Hazard` | causes |
| `scen:hasEntryKind` | `scen:ManifestEntry` | `scen:ManifestEntryKind` | has entry kind |
| `scen:hasExecutionMode` | `scen:ScenarioExecution` | `scen:ExecutionMode` | has execution mode |
| `scen:hasExecutionState` | `scen:ScenarioExecution` | `scen:ScenarioExecutionState` | Lifecycle state of the execution (PENDING, RUNNING, COMPLETED, FAILED). Formerly ranged over di:DependabilityIndexState, which conflated the execution lifecycle with the operational state; the projected operational state is now scen:hasProjectedState on the result. |
| `scen:hasManifestEntry` | `scen:ScenarioExecution` | `scen:ManifestEntry` | has manifest entry |
| `scen:hasProjectedState` | `scen:ScenarioResult` | `di:DependabilityIndexState` | The operational state the scenario projects for the affected node or system if it plays out (unmitigated unless the result is for a specific response). |
| `scen:hasScenarioExecution` | `scen:Scenario` | `scen:ScenarioExecution` | has scenario execution |
| `scen:hasScenarioParameter` | `scen:Scenario` | `owl:Thing` | has scenario parameter |
| `scen:hasScenarioResult` | `scen:ScenarioExecution` | `scen:ScenarioResult` | has scenario result |
| `scen:hasTrigger` | `scen:Scenario` | `cdm:Deviation` ∪ `cdm:FailureMode` ∪ `scen:Failure` ∪ `scen:Threat` ∪ `warrant:EnvironmentalCondition` ∪ `scen:EventTrigger` | What starts the scenario. A cdm:FailureMode is the design-time trigger of an injected fault, typed by its HAZOP guideword; a cdm:Deviation is used when the scenario replays a detected deviation. |
| `scen:producesForecast` | `scen:ScenarioResult` | `di:DIForecast` | A DI forecast generated by this scenario execution: the projected node or system DI over the horizon, either unmitigated or conditional on a candidate response. Consumed by the Supervisor's predictive trigger (di:triggeredByForecast) and by REDS (mit:hasExpectedIndex). |

## Datatype properties (8)

| Property | Domain | Range | Description |
|---|---|---|---|
| `scen:finishedAt` | `scen:ScenarioExecution` | `xsd:dateTime` | finished at |
| `scen:hasDatasetHash` | `scen:ScenarioExecution` | `xsd:string` | Content hash of the input dataset (sha256, hex), for replayed or data-driven executions. |
| `scen:hasExecutionTimestamp` | `scen:ScenarioExecution` | `xsd:dateTime` | has execution timestamp |
| `scen:hasRandomSeed` | `scen:ScenarioExecution` | `xsd:integer` | A random seed used by the execution; one value per seed. |
| `scen:hasResultSummary` | `scen:ScenarioResult` | `xsd:string` | Human-readable outcome description of the scenario execution. |
| `scen:hasScenarioFile` | `scen:ScenarioExecution` | `xsd:string` | Repository-relative path of the scenario definition the execution ran. |
| `scen:hasScenarioHash` | `scen:ScenarioExecution` | `xsd:string` | Content hash of the scenario definition (sha256, hex). |
| `scen:startedAt` | `scen:ScenarioExecution` | `xsd:dateTime` | started at |

