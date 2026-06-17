# `warrant-observation` — Observation and Detection Module

**Namespace:** `https://w3id.org/warrant/observation#`  
**Prefix:** `obs:`  
**Status:** Stable  
**Role:** Evidence layer — models how metrics are collected, measurements are produced, and deviations are detected and grounded in auditable evidence.

---

## Purpose

`warrant-observation` defines the **epistemic substrate** of the WARRaNT KG. Every claim about a deviation, hazard, or assurance score must ultimately be traceable to an observation — a measurement taken by a sensor, a score computed by an analytical service, or a report filed by a human operator. This module defines that traceability chain and enforces the detection event rule that makes all deviation assertions auditable.

---

## Class Hierarchy

### Evidence Entities

```
EvidenceEntity  (from warrant-core)
├── DataSource
│   ├── Observer
│   │   ├── PhysicalSensor
│   │   ├── VirtualSensor
│   │   ├── CameraObserver
│   │   ├── RADARObserver
│   │   ├── LiDARObserver
│   │   └── AISObserver
│   ├── AnalyticalService     (rule engine, ML model, anomaly detector)
│   └── HumanOperatorRole     (imported from warrant-davom — acts as data source)
│
├── Metric
│   ├── DependabilityMetric
│   ├── SafetyMetric
│   ├── CybersecurityMetric
│   ├── AvailabilityMetric
│   ├── PerformanceMetric
│   ├── ResilienceMetric
│   ├── MaintainabilityMetric
│   └── ReliabilityMetric
│
├── Measurement               (a specific reading of a Metric at a point in time)
├── Status                    (a categorical state reading, e.g. ON/OFF, CONNECTED/DISCONNECTED)
├── Alert                     (a threshold-crossing notification)
├── DataQualityIndicator      (quality metadata attached to a Measurement)
├── ConfidenceLevel           (epistemic confidence score for an observation)
├── VirtualSensorOutput       (output of a VirtualSensor computation)
├── DetectionRule             (logic that governs when a DetectionEvent is produced)
├── HumanObservation          (a structured observation reported by a human)
├── OperatorInput             (a structured data entry by an operator)
└── DetectionEvent            (the auditable record that a deviation has been identified)
```

---

## The Detection Chain

The central architectural pattern of this module is the **detection chain**:

```
DataSource (Observer / AnalyticalService / HumanOperatorRole)
  → obs:producesDetectionEvent → DetectionEvent
      → obs:detectionEventDetects → Deviation    [red arrow — critical path]
```

### Why this matters

- **Auditability:** Every `Deviation` in the KG has a `DetectionEvent` that records *who* detected it, *when*, and *how*.
- **Separation of concerns:** The `AnalyticalService` is responsible for detection logic; the `Deviation` (defined in `warrant-cdm`) is responsible for causal reasoning. Neither crosses the other's boundary.
- **Prohibition:** An `AnalyticalService` must **never** produce a `Deviation` directly. The `DetectionEvent` step is mandatory.

### Detection chain example (GNSS loss)

```
GNSSMonitoringService : AnalyticalService
  → producesDetectionEvent → GNSSSignalLossDetectionEvent : DetectionEvent
      → detectionEventDetects → GNSSSignalLossDeviation : Deviation [hasDeviationType: UNAVAILABLE]
```

---

## Metric and Measurement Model

A `Metric` defines *what* is measured (unit, time-series reference, threshold). A `Measurement` is a concrete reading of that metric at a specific time.

| Property | Domain | Range | Description |
|---|---|---|---|
| `obs:hasMeasurement` | `Metric` | `Measurement` | Links metric to its recorded readings |
| `obs:value` | `Measurement` | `xsd:string` | Measured value with unit (e.g., "5.2 dBHz") |
| `obs:timestamp` | `Measurement` | `xsd:dateTime` | Observation timestamp |
| `obs:externalTSId` | `Metric` | `xsd:string` | Reference to external time-series database record |
| `obs:unit` | `Metric` | `xsd:string` | Unit of measurement |
| `obs:threshold` | `Metric` | `xsd:decimal` | Threshold that, if crossed, triggers detection |

---

## Virtual Sensors

`VirtualSensor` is a subclass of `Observer` that computes derived observations from raw data — model-based estimators, fusion algorithms, and ML inference engines are all modelled as `VirtualSensor`. Their outputs are `VirtualSensorOutput` individuals, which feed into `AnalyticalService` instances for deviation detection.

---

## Human Observations

`HumanObservation` and `OperatorInput` capture structured reports from human operators. They are produced by `HumanOperatorRole` acting in its data-source capacity and feed the same detection chain as sensor-based observations.

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `obs:producesDetectionEvent` | `DataSource` | `DetectionEvent` | Core detection chain step |
| `obs:detectionEventDetects` | `DetectionEvent` | `Deviation` | Grounds a deviation in evidence |
| `obs:consumes` | `AnalyticalService` | `Metric` | Service reads this metric |
| `obs:hasDependabilityMetric` | `Component` / `VesselFunction` | `Metric` | Asset has a monitored metric |
| `obs:supportsDetection` | `Measurement` | `DetectionEvent` | Measurement supports a detection |
| `obs:governedBy` | `DetectionEvent` | `DetectionRule` | Event produced under this rule |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `obs:detectedAt` | `DetectionEvent` | `xsd:dateTime` | Timestamp of detection |
| `obs:confidence` | `DetectionEvent` | `xsd:decimal` | Confidence score [0, 1] |
| `obs:alertLevel` | `Alert` | `xsd:string` | INFO / WARNING / CRITICAL |
| `obs:qualityScore` | `DataQualityIndicator` | `xsd:decimal` | Data quality score [0, 1] |
| `obs:ruleExpression` | `DetectionRule` | `xsd:string` | Rule logic (e.g., SPARQL, CEP expression) |

---

## Design Principles

1. **Every deviation must have a detection event.** This is the single most important constraint in the module. SPARQL integrity checks should verify that every `Deviation` individual is the target of exactly one `detectionEventDetects` triple.
2. **Metrics are reusable.** A `Metric` individual represents the abstract metric definition; `Measurement` individuals represent the time-series data. This separation supports time-series integration without bloating the KG.
3. **Humans are data sources too.** `HumanOperatorRole` is in the domain of `producesDetectionEvent` — human reports are first-class evidence, not second-class annotations.

---

## Imports

- `warrant-core`
- `warrant-davom`
- `warrant-cdm`

---

## Downstream Dependents

`warrant-assurance` · `warrant-di`
