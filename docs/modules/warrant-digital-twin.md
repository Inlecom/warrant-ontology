# `warrant-digital-twin` — Digital Twin

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/digital-twin#`  
**Prefix:** `dt:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/digital-twin`  
**Imports:** `warrant-core`, `warrant-davom`, `warrant-di`, `warrant-mitigation`, `warrant-observation`, `warrant-scenario`  
**Version:** `1.0.0`

---

## Purpose

Semantic interface between the WARRaNT KG and the Digital Twin: views, visualisation layers, decision-support, and update channels in both directions. The twin consumes the graph (visualises, monitors, executes scenarios, stores results) and produces inputs to it: as an observation data source (state estimation, virtual sensing, health events) and as the producer of DI forecasts used by the Dependability Supervisor and REDS. The KG defines what the DT executes, visualises, stores and forecasts — it does NOT implement the DT.

**Role:** the semantic interface between the graph and the Digital Twin, in
both directions. The twin *consumes* the graph (visualises, monitors, executes
scenarios, stores results, receives updates) and *produces* inputs to it: it is
an `obs:DataSource` (state estimation, virtual sensing, health events), it
provides virtual sensors, and it produces `di:DIForecast`s that feed the
Supervisor's predictive trigger and REDS's expected-effect estimates.

**Design rules**

1. Thin integration layer: no domain concept is defined here. `warrant:VisualisableEntity` lives in core; modules mark their classes visualisable without importing this module.
2. No module imports warrant-digital-twin. The DT → Supervisor/REDS direction is realised by placing the forecast class in warrant-di and declaring `producesForecast` here.
3. The twin is advisory by design in the proof of concept: it presents evaluations and records operator responses; it does not act.
4. `dt:ScenarioExecutionState` is deprecated; use `scen:ScenarioExecutionState`.

---

## Classes (5)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `dt:DecisionSupportView` | `dt:DigitalTwinView` | Decision Support View | A specialised DigitalTwinView for operator decision-support: presents the operational state and DI (always with the Assurance Level), active resilience triggers, the ranked REDS response evaluations with their expected-effect forecasts, the authorisation status of the selected response, and scenario results side-by-side. The operator approves or overrides from here; the input is recorded as evidence. |
| `dt:DigitalTwin` | `obs:DataSource` | Digital Twin | A synchronised digital representation of a vessel or system integrating physics-based models, data-driven models, virtual sensors, operational telemetry and simulation. It provides real-time state estimation, virtual sensing, predictive analysis, scenario exploration and what-if evaluation. Consumer role: executes scenarios, visualises indices, states, triggers, hazards, evaluations and failover procedures, monitors operational entities, and receives live updates from analytical services. Producer role: as an obs:DataSource its state estimates and predictions are admissible sources of measurements, virtual-sensor outputs and health events (obs:hasSource, obs:producesHealthEvent); it provides virtual sensors (dt:providesVirtualSensor); and it produces DI forecasts (dt:producesForecast → di:DIForecast) that feed the Supervisor's predictive resilience trigger and REDS's expected-effect estimates. |
| `dt:DigitalTwinView` | — | Digital Twin View | A configurable view displayed on the DT interface (e.g. vessel overview, function health panel, scenario panel). |
| `dt:ScenarioExecutionState` **DEPRECATED** | — | Scenario Execution State (DEPRECATED) | DEPRECATED. Use scen:ScenarioExecutionState (warrant-scenario), which carries the PENDING, RUNNING, COMPLETED and FAILED individuals and is the range of scen:hasExecutionState. This class had no individuals and no property used it. Will be removed in the next minor release. |
| `dt:VisualisationLayer` | — | Visualisation Layer | A rendering layer within a DigitalTwinView. Instances declare which KG entities they render via dt:visualises (e.g. DI heatmap layer, hazard overlay, alert layer). |

## Object properties (11)

| Property | Domain | Range | Description |
|---|---|---|---|
| `dt:executes` | `dt:DigitalTwin` | `scen:Scenario` | executes |
| `dt:hasLayer` | `dt:DigitalTwinView` | `dt:VisualisationLayer` | has layer |
| `dt:hasView` | `dt:DigitalTwin` | `dt:DigitalTwinView` | has view |
| `dt:monitors` | `dt:DigitalTwin` | `warrant:OperationalEntity` | monitors |
| `dt:producesForecast` | `dt:DigitalTwin` | `di:DIForecast` | The twin's predictive simulation or what-if analysis produced this DI forecast. This is the Digital Twin → Dependability Supervisor / REDS direction of the framework: the forecast is consumed by di:ResilienceTrigger (PREDICTED_FLOOR_CROSSING) and by mit:ResponseEvaluation (expected effect of a candidate response). Declared here so that neither warrant-di nor warrant-mitigation imports this module; the forecast should also carry di:forecastProducedBy pointing back at the twin. |
| `dt:providesVirtualSensor` | `dt:DigitalTwin` | `obs:VirtualSensor` | A virtual sensor (model-based state estimate) hosted by the twin, which may substitute a failed or untrusted physical observer (obs:substitutesFor) as a fail-operational response. |
| `dt:receivesUpdateFrom` | `dt:DigitalTwin` | `obs:DataSource` | Documents that the DT receives live updates from analytical services, sensors, node health monitors, or operator inputs. |
| `dt:representsStateOf` | `dt:DigitalTwin` | `davom:Vessel` | represents state of |
| `dt:storesResult` | `dt:DigitalTwin` | `scen:ScenarioExecution` | stores result |
| `dt:supportsDecision` | `dt:DigitalTwin` | `dt:DecisionSupportView` | supports decision |
| `dt:visualises` | `dt:DigitalTwin` ∪ `dt:VisualisationLayer` | `warrant:VisualisableEntity` | Range constrained to warrant:VisualisableEntity (defined in warrant-core.ttl). Do NOT use dt:VisualisableEntity. |

## Datatype properties (0)

| Property | Domain | Range | Description |
|---|---|---|---|

## Axioms asserted about other modules' terms

- `di:DependabilityIndex` rdfs:subClassOf `warrant:VisualisableEntity`
- `di:SystemDependabilityIndex` rdfs:subClassOf `warrant:VisualisableEntity`
- `scen:ScenarioExecution` rdfs:subClassOf `warrant:VisualisableEntity`
- `scen:Scenario` rdfs:subClassOf `warrant:VisualisableEntity`
- `warrant:AgentEntity` rdfs:subClassOf `warrant:VisualisableEntity`
- `warrant:OperationalEntity` rdfs:subClassOf `warrant:VisualisableEntity`

