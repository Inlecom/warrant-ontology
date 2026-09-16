# `warrant-observation` — Observation and Health Events

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/observation#`  
**Prefix:** `obs:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/observation`  
**Imports:** `warrant-cdm`, `warrant-core`, `warrant-davom`  
**Version:** `0.10-poc`

---

## Purpose

Metrics, observers, measurements, analytical services, health events (detected and predicted), detection events, node health monitors, virtual sensors, data quality, human observations, and operator inputs.

**Role:** evidence layer. Metrics, observers (physical and virtual sensors,
probes, log collectors), measurements, analytical services, the structured
**health event** record and its two specialisations (detection events, which
identify a deviation, and predicted-condition events, which anticipate one),
node health monitors, human observations and operator inputs.

**The detection chain (mandatory)**

```
DataSource → obs:producesHealthEvent → HealthEvent
AnalyticalService / VirtualSensor / DetectionRule → obs:producesDetectionEvent → DetectionEvent
DetectionEvent → obs:detectionEventDetects → cdm:Deviation
```

A `Deviation` is reached only through a `DetectionEvent`. `obs:produces` ranges over
`Status | VirtualSensorOutput` only. `obs:detects` is a SPARQL shortcut.

**Design rules**

1. Operational entities *have* metrics (`hasDependabilityMetric`); components do not generate them.
2. `HealthEvent` carries the methodology's named record (id, time, source, affected asset, condition, confidence, severity, duration/persistence, operational impact, root cause, mission context, control status, trend). Fields may be unknown at creation and enriched as diagnosis proceeds; enrichment lineage uses `warrant:derivedFrom`.
3. `PredictedConditionEvent` is not bound by the detection-event rule; quantitative DI forecasts are `di:DIForecast`, not health events.
4. `NodeHealthMonitor` is an `AnalyticalService` at component, function or system level; monitors exchange health events along the dependency topology and produce the attribute assessments (`assr:AssuranceAttributeValue`) the Supervisor fuses.
5. Raw telemetry stays outside the graph (`hasExternalRecordReference`, `hasExternalTimeSeriesId`).

---

## Classes (33)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `obs:APIConnector` | `obs:Observer` | API Connector |  |
| `obs:Alert` | `obs:EvidenceEntity` | Alert |  |
| `obs:AnalyticalService` | `obs:DataSource` | Analytical Service | A computational service that consumes metrics and produces Status, VirtualSensorOutput, or HealthEvents (including DetectionEvents). It does NOT produce Deviation directly — use the DetectionEvent production path. The WARRaNT runtime agents are modelled as subclasses so that their outputs carry provenance: obs:NodeHealthMonitor (here), di:DependabilitySupervisor, mit:DecisionSupportService (REDS), and mit:ResilienceSupervisor (IRDS). |
| `obs:AvailabilityMetric` | `obs:Metric` | Availability Metric |  |
| `obs:ConfidenceLevel` | `obs:EvidenceEntity` | Confidence Level |  |
| `obs:CybersecurityMetric` | `obs:Metric` | Cybersecurity Metric |  |
| `obs:DataQualityIndicator` | `obs:EvidenceEntity` | Data Quality Indicator |  |
| `obs:DataQualityMetric` | `obs:Metric` | Data Quality Metric |  |
| `obs:DataSource` | `obs:EvidenceEntity` | Data Source | A source of measurements, observations, operator inputs, analytical outputs, or evidence. Subclasses include Observer, AnalyticalService, and system-level data producers. |
| `obs:DependabilityMetric` | `obs:Metric` | Dependability Metric |  |
| `obs:DetectionEvent` | `obs:HealthEvent` | Detection Event | A HealthEvent produced by a DetectionRule, AnalyticalService, NodeHealthMonitor, or VirtualSensor indicating that a Deviation has been detected. This is the ONLY production path to Deviation: AnalyticalService → producesDetectionEvent → DetectionEvent → detectionEventDetects → Deviation. obs:detects is a SPARQL shortcut only. Inherits the full health-event record from obs:HealthEvent. |
| `obs:DetectionRule` | `obs:EvidenceEntity` | Detection Rule |  |
| `obs:DiagnosticService` | `obs:Observer` | Diagnostic Service |  |
| `obs:EvidenceEntity` | `warrant:EvidenceEntity` | Evidence Entity (Observation) | Observation-module superclass for all observation and evidence entities. |
| `obs:HealthEvent` | `obs:EvidenceEntity` | Health Event | The structured health-event record into which runtime observations are transformed (detected, filtered, correlated, fused, contextualised, and classified against the hazard and remedy knowledge in the graph) and which Node Health Monitors exchange along dependency paths. It describes a detected fault, a predicted failure, or an abnormal operating condition. Its named fields map to properties as follows: eventId → warrant:hasIdentifier; time → obs:hasTimestamp; source/provenance → obs:hasSource and warrant:derivedFrom; affectedAsset → obs:affectsAsset; condition → obs:indicatesCondition (and, for a DetectionEvent, obs:detectionEventDetects); confidence → obs:hasConfidenceValue; severity → obs:hasSeverityLevel; duration/persistence → obs:hasDuration, obs:isPersistent; operationalImpact → obs:hasOperationalImpact; rootCause → obs:hasRootCause; missionContext → obs:hasMissionContext; controlStatus → obs:hasControlStatus; trend → obs:hasTrendIndicator. Fields may be unknown when the event is first created and enriched as diagnosis proceeds. A HealthEvent is admissible as the source of an assr:Evidence item and may challenge an assr:AssuranceClaim. Interpreted events reside in the graph; raw telemetry stays in the external store. |
| `obs:HumanObservation` | `obs:EvidenceEntity` | Human Observation | A human-reported observation about a metric, status, or deviation. |
| `obs:HumanPerformanceMetric` | `obs:Metric` | Human Performance Metric |  |
| `obs:LogCollector` | `obs:Observer` | Log Collector |  |
| `obs:Measurement` | `obs:EvidenceEntity` | Measurement | An observed value of a metric at a specific time. Raw high-frequency measurements are stored externally; only semantic events and latest states live in the KG. Use hasExternalRecordReference to link to the external store. |
| `obs:Metric` | `obs:EvidenceEntity` | Metric | A dependability-relevant measurable property of an operational entity (Component, System, VesselFunction, DataFlow, CommunicationLink, or HumanOperatorRole). Components have metrics; they do not generate metrics. |
| `obs:MonitoringLevel` | — | Monitoring Level | Controlled vocabulary for the hierarchy level at which a Node Health Monitor operates. As information moves upward the focus shifts from component observations to subsystem impacts, functional consequences, and system-level dependability implications. |
| `obs:NodeHealthMonitor` | `obs:AnalyticalService` | Node Health Monitor | A distributed reasoning agent responsible for one node (component, function, or system) that interprets local observations, evaluates potential future states, estimates operational consequences, and communicates dependency-aware health assessments to the monitors of dependent nodes. It produces HealthEvents for its node and attribute assessments (assr:AssuranceAttributeValue with source confidence) that the Dependability Supervisor fuses. Beyond fault severity it considers persistence and duration. Health information exchanged between monitors follows the dependency topology encoded in the graph (obs:exchangesHealthEventWith). |
| `obs:Observer` | `obs:DataSource` | Observer | An entity that observes, measures, or estimates a metric. Informative alignment: obs:Observer ≈ sosa:Sensor (W3C SOSA/SSN). |
| `obs:OperatorInput` | `obs:EvidenceEntity` | Operator Input |  |
| `obs:PerformanceMetric` | `obs:Metric` | Performance Metric |  |
| `obs:PredictedConditionEvent` | `obs:HealthEvent` | Predicted Condition Event | A HealthEvent that anticipates rather than detects: a predicted failure or degradation produced by a Node Health Monitor evaluating potential future states, a Digital Twin prediction, or a predictive analytical model. It carries the same record as any HealthEvent, with obs:indicatesCondition naming the anticipated Hazard, FailureMode, or Deviation and obs:hasConfidenceValue the prediction confidence. The detection-event rule does not apply: a PredictedConditionEvent does not assert that a Deviation has occurred. Quantitative DI forecasts are stored separately as di:DIForecast. |
| `obs:Probe` | `obs:Observer` | Probe |  |
| `obs:ReliabilityMetric` | `obs:Metric` | Reliability Metric |  |
| `obs:SafetyMetric` | `obs:Metric` | Safety Metric |  |
| `obs:Sensor` | `obs:Observer` | Sensor |  |
| `obs:Status` | `obs:EvidenceEntity` | Status |  |
| `obs:VirtualSensor` | `obs:Observer` | Virtual Sensor | Software-based observer that estimates a metric from other data streams (model-based estimator, observer bank, fusion algorithm, ML inference, or a Digital Twin state estimate). May substitute a failed physical observer (obs:substitutesFor), which is one of the fail-operational responses the resilience layer can select. Informative alignment: obs:VirtualSensor ≈ sosa:Sensor (software-only variant). |
| `obs:VirtualSensorOutput` | `obs:EvidenceEntity` | Virtual Sensor Output |  |

## Controlled vocabularies (named individuals)

### `obs:MonitoringLevel`

| Individual | Label | Description |
|---|---|---|
| `obs:COMPONENT_LEVEL` | COMPONENT_LEVEL | Monitor responsible for a Component or a Subsystem. |
| `obs:FUNCTION_LEVEL` | FUNCTION_LEVEL | Monitor responsible for a VesselFunction. |
| `obs:SYSTEM_LEVEL` | SYSTEM_LEVEL | Monitor responsible for a System, the Vessel, or a system of systems. |

## Object properties (26)

| Property | Domain | Range | Description |
|---|---|---|---|
| `obs:affectsAsset` | `obs:HealthEvent` | `warrant:OperationalEntity` ∪ `warrant:AgentEntity` | The affected component, subsystem, function, system, link, or operational role (health-event field affectedAsset). |
| `obs:captures` | `davom:OperatorInterface` | `obs:OperatorInput` | captures |
| `obs:consumes` | `obs:AnalyticalService` ∪ `obs:VirtualSensor` | `obs:Metric` | consumes |
| `obs:detectionEventDetects` | `obs:DetectionEvent` | `cdm:Deviation` | The terminal step of the production chain. A DetectionEvent identifies a specific Deviation individual. |
| `obs:detects` | `obs:DetectionEvent` | `cdm:Deviation` | SPARQL shortcut traversal property only. Domain is DetectionEvent (not AnalyticalService or Measurement directly). Production pattern: use obs:producesDetectionEvent + obs:detectionEventDetects. |
| `obs:estimates` | `obs:VirtualSensor` | `obs:Metric` | estimates |
| `obs:exchangesHealthEventWith` | `obs:NodeHealthMonitor` | `obs:NodeHealthMonitor` | Peer exchange of interpreted health assessments between Node Health Monitors. Which monitors receive updates is determined by the dependency topology in the graph: a monitor exchanges with the monitors of the nodes its node depends on and of the nodes that depend on it. |
| `obs:hasDataQuality` | `obs:Measurement` ∪ `obs:HumanObservation` ∪ `obs:OperatorInput` | `obs:DataQualityIndicator` | has data quality |
| `obs:hasDependabilityMetric` | `warrant:OperationalEntity` | `obs:Metric` | Associates a metric with an operational entity (Component, System, VesselFunction, HumanOperatorRole, DataFlow, CommunicationLink). |
| `obs:hasMeasurement` | `obs:Metric` | `obs:Measurement` | has measurement |
| `obs:hasMissionContext` | `obs:HealthEvent` | `warrant:ContextEntity` | Mission and operational context at the time of the event (health-event field missionContext): OperationalMode, VoyageSegment, or EnvironmentalCondition. |
| `obs:hasMonitoringLevel` | `obs:NodeHealthMonitor` | `obs:MonitoringLevel` | has monitoring level |
| `obs:hasRootCause` | `obs:HealthEvent` | `cdm:CausalEntity` ∪ `obs:HealthEvent` ∪ `warrant:OperationalEntity` | Root-cause information when known (health-event field rootCause): the originating deviation, failure mode, upstream health event, or upstream node identified by diagnosis (e.g. observer-based fault isolation) or by graph traversal along the dependency path. |
| `obs:hasSource` | `obs:EvidenceEntity` | `obs:DataSource` | Source of a measurement, observation, or analytical output. |
| `obs:indicates` | `obs:Measurement` | `obs:Status` | indicates |
| `obs:indicatesCondition` | `obs:HealthEvent` | `cdm:Hazard` ∪ `cdm:FailureMode` ∪ `cdm:Deviation` ∪ `cdm:ThreatScenario` | The condition or hazard class the event has been classified against in the design-time knowledge (health-event field condition). For a DetectionEvent the detected Deviation is asserted with obs:detectionEventDetects; this property may additionally name the Hazard or FailureMode the event was classified under. |
| `obs:measures` | `obs:Observer` | `obs:Metric` | measures |
| `obs:monitorsNode` | `obs:NodeHealthMonitor` | `warrant:OperationalEntity` | The component, subsystem, function, system, or vessel for which this Node Health Monitor is responsible. |
| `obs:observes` | `obs:Observer` ∪ `obs:HumanObservation` | `obs:Metric` ∪ `obs:Status` | observes |
| `obs:presents` | `davom:OperatorInterface` | `obs:Metric` ∪ `obs:Status` ∪ `obs:Alert` | presents |
| `obs:produces` | `obs:AnalyticalService` ∪ `obs:VirtualSensor` | `obs:Status` ∪ `obs:VirtualSensorOutput` | Range is Status or VirtualSensorOutput. cdm:Deviation is NOT in the range — deviations are reached only via the DetectionEvent production path. |
| `obs:producesDetectionEvent` | `obs:AnalyticalService` ∪ `obs:VirtualSensor` ∪ `obs:DetectionRule` | `obs:DetectionEvent` | produces detection event (sub-property of `obs:producesHealthEvent`) |
| `obs:producesHealthEvent` | `obs:DataSource` | `obs:HealthEvent` | A data source (sensor, virtual sensor, analytical service, Node Health Monitor, cybersecurity monitor, Digital Twin, operator role, or vessel automation system) produces a structured HealthEvent. obs:producesDetectionEvent is the specialisation for events that identify a Deviation. |
| `obs:substitutesFor` | `obs:VirtualSensor` | `obs:Observer` | The physical or other observer whose measurements this virtual sensor replaces when that observer is failed, degraded, or untrusted (virtual-sensor substitution, a fail-operational response). |
| `obs:supportsDetection` | `obs:Measurement` | `obs:DetectionEvent` | A measurement provides evidence contributing to a detection event. |
| `obs:supportsDetectionOf` | `obs:Observer` | `obs:DetectionRule` | supports detection of |

## Datatype properties (14)

| Property | Domain | Range | Description |
|---|---|---|---|
| `obs:hasConfidenceValue` | `obs:ConfidenceLevel` ∪ `obs:VirtualSensorOutput` ∪ `obs:HumanObservation` ∪ `obs:HealthEvent` | `xsd:decimal` | Confidence in [0,1] associated with a detection, prediction, estimate, or human observation. Confidence controls the influence of a source in attribute fusion and contributes to evidence quality; it is never multiplied into an operational value as a separate degradation. |
| `obs:hasControlStatus` | `obs:HealthEvent` | `xsd:string` | Current control or authorisation status of the condition (health-event field controlStatus): e.g. UNCONTROLLED, LOCALLY_CONTROLLED, MITIGATION_PENDING_AUTHORISATION, MITIGATED. A locally controlled fault may have limited influence on system dependability; the Supervisor evaluates both intrinsic severity and propagated consequences. |
| `obs:hasDuration` | `obs:HealthEvent` | `xsd:duration` | Observed or estimated duration of the condition (health-event field duration). Monitors weigh persistence: temporary disturbances may be negligible, persistent degradations progressively reduce assurance. |
| `obs:hasExternalRecordReference` | `obs:Measurement` | `xsd:string` | Key or URI pointing to the raw measurement record in an external time-series store. Prevents the KG from being used as a telemetry database. |
| `obs:hasExternalTimeSeriesId` | `obs:Metric` | `xsd:string` | Identifier of the metric's data stream in the external telemetry platform. |
| `obs:hasOperationalImpact` | `obs:HealthEvent` | `xsd:string` | Expected operational impact of the condition as assessed by the monitor (health-event field operationalImpact). |
| `obs:hasQualityValue` | `obs:DataQualityIndicator` | `xsd:decimal` | has quality value |
| `obs:hasSamplingRate` | `obs:Metric` ∪ `obs:Observer` | `xsd:decimal` | has sampling rate |
| `obs:hasSeverityLevel` | `obs:HealthEvent` | `xsd:string` | Severity classification of the event (health-event field severity), e.g. LOW, MEDIUM, HIGH, CRITICAL. Distinct from cdm:hasSeverity (a design-time risk score) and from the operational state, which is assigned attribute-wise by the Dependability Supervisor. |
| `obs:hasTimestamp` | `obs:Measurement` ∪ `obs:HumanObservation` ∪ `obs:OperatorInput` ∪ `obs:HealthEvent` | `xsd:dateTime` | has timestamp |
| `obs:hasTrendIndicator` | `obs:HealthEvent` | `xsd:string` | Direction of the monitored node's health as assessed by the monitor: IMPROVING, STABLE, or DECLINING. |
| `obs:hasUnit` | `obs:Measurement` ∪ `obs:Metric` | `xsd:string` | Unit of measurement as a string. Future alignment: obs:hasUnit ≈ qudt:unit. |
| `obs:hasValue` | `obs:Measurement` | `xsd:decimal` | has value |
| `obs:isPersistent` | `obs:HealthEvent` | `xsd:boolean` | True when the condition has persisted beyond the configured transient window and should be treated as a sustained degradation rather than a temporary disturbance. |

## Axioms asserted about other modules' terms

- `davom:HumanOperatorRole` rdfs:subClassOf `obs:DataSource`

