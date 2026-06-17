# WARRaNT KG Ontology — Modelling Conventions

Version 0.9-poc | 2026-06-05

---

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Class | PascalCase, English, no abbreviations | `DetectionEvent`, `VesselFunction` |
| Object property | camelCase, starts with a verb | `producesDetectionEvent`, `hasDIState` |
| Datatype property | camelCase, starts with `has` or `is` | `hasScoreValue`, `hasTimestamp` |
| Named individual (controlled vocab) | UPPER_SNAKE_CASE or PascalCase as fits | `cdm:UNAVAILABLE`, `di:CriticalState` |
| Module namespace prefix | short, lowercase | `warrant:`, `davom:`, `obs:`, `cdm:` |

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

---

## When to Create a New Class

Create a new class when there is a clearly distinct real-world concept that needs to carry its own properties and appear as a type in SPARQL queries. Prefer subclassing an existing class. Do not create a class merely to group instances — use properties instead.

## When to Create an Individual

Create a named individual for controlled vocabulary entries (e.g. `cdm:DeviationType`, `di:DependabilityIndexState`, `warrant:OperationalMode`) and for runtime instance data (in examples/ with the data namespace).

## When to Create a Controlled Vocabulary

Use a controlled vocabulary class (e.g. `cdm:DeviationType`) when:
- The set of values is small and stable.
- Values are reused across many instances.
- SPARQL filtering on specific values is required.

Instances of the vocabulary class are named individuals in the module namespace (not data instances).

## Simple Object Property vs. Reified Relationship Node

Use a **simple object property** (`davom:dependsOn`) when the relationship is binary with no additional attributes.

Use a **reified relationship node** (`davom:Dependency`, `di:RiskPropagationEdge`) when the relationship has attributes (e.g. weight, criticality, latency) that need to be stored and queried.

---

## How to Model Metrics

```turtle
# Correct: operational entity HAS a metric
ll4:ROCToVesselCommandLink obs:hasDependabilityMetric ll4:CommandLatencyMetric .

# WRONG: do not say a component "generates" or "creates" a metric
```

Observers (Sensor, AnalyticalService) **observe** or **consume** metrics. They do not create them.

---

## How to Model Observations

```
AnalyticalService  →  obs:consumes  →  Metric
AnalyticalService  →  obs:producesDetectionEvent  →  DetectionEvent
DetectionEvent     →  obs:detectionEventDetects   →  Deviation
```

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

All deviation typing must use `cdm:hasDeviationType` with the named `cdm:DeviationType` individuals:
`cdm:NO`, `cdm:LESS`, `cdm:MORE`, `cdm:LATE`, `cdm:WRONG`, `cdm:UNAVAILABLE`, `cdm:UNTRUSTED`, `cdm:INCONSISTENT`, `cdm:NOISY`, `cdm:SPOOFED`.

---

## How to Model Assurance Scores

The KG stores calculation inputs, weights, and results. Computation is external.

```turtle
ll4:NavigationAssuranceScore a assr:AssuranceScore ;
    assr:hasScoreValue "0.38"^^xsd:decimal ;
    di:calculatedAt    "2026-05-17T10:15:05Z"^^xsd:dateTime .

ll4:RemoteNavigationFunction assr:hasAssuranceScore ll4:NavigationAssuranceScore .
```

---

## How to Model DI States (MANDATORY)

```turtle
# Correct: named individual
ll4:RemoteNavigationDI di:hasDIState di:CriticalState .

# WRONG: subclassing DependabilityIndexState is prohibited
# ll4:CriticalNavigationState a di:DependabilityIndexState .  # DO NOT USE
```

Available named individuals: `di:NormalState`, `di:DegradedState`, `di:CriticalState`, `di:FailedState`, `di:UnsafeState`.

---

## How to Model External Data References

```turtle
obs:GNSSSignalQualityMetric obs:hasExternalTimeSeriesId "timeseries.gnss.signal_quality.MAI-W" .

obs:GNSSSignalMeasurement_T1 obs:hasExternalRecordReference
    "timeseries.gnss.signal_quality.MAI-W::1747476900" .
```

---

## How to Model Example Scenarios

1. Place example files in `examples/`.
2. Use the data namespace (`https://warrant-project.eu/data/{context}#`).
3. Include the full chain: Vessel → Function → System → Component → Metric → Measurement → DetectionEvent → Deviation → Hazard → Risk → AssuranceDegradation → AssuranceScore → DI.
4. Tag deviations with `cdm:hasDeviationType`.
5. Set `di:hasDIState` to a named individual.
6. Include at least one MitigationRule with an AdvisoryAction.
7. Include a DigitalTwin with `dt:visualises` assertions.

---

## Deprecation Rules

- Deviation subclasses (`cdm:UnavailableDeviation` etc.) are deprecated. Tag any existing ones: `owl:deprecated true ; rdfs:comment "Deprecated. Use cdm:hasDeviationType cdm:UNAVAILABLE instead."` Do not create new ones.
- `di:DependabilityIndexState` subclasses are prohibited. Use named individuals only.
- Deprecated terms remain for one minor release before removal (see CONTRIBUTING.md).

---

## Mandatory Principles Summary

| Principle | Rule |
|-----------|------|
| Human operators | Subclass `warrant:AgentEntity`, not `warrant:OperationalEntity` or `davom:Component` |
| Metrics | Operational entities have metrics; they do not generate them |
| Deviation typing | `cdm:hasDeviationType` + named individual only |
| DI state | Named `di:DependabilityIndexState` individuals only |
| Detection chain | `AnalyticalService → producesDetectionEvent → DetectionEvent → detectionEventDetects → Deviation` |
| `obs:produces` range | `obs:Status \| obs:VirtualSensorOutput` only; never `cdm:Deviation` |
| VisualisableEntity | Defined in `warrant-core.ttl`; do not redefine |
| VoyageSegment, OperationalMode | Core/context module, not CDM |
| Raw telemetry | Outside KG; use external reference properties |
| Example individuals | `https://warrant-project.eu/data/{context}#` namespace |
| Controlled vocabulary | Ontology module namespace |
