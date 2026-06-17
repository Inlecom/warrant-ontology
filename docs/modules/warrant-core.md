# `warrant-core` — WARRaNT Core Ontology Module

**Namespace:** `https://w3id.org/warrant/core#`  
**Prefix:** `warrant:`  
**Status:** Stable  
**Role:** Foundation layer — defines the top-level superclass hierarchy and shared contextual vocabulary used by every other WARRaNT module.

---

## Purpose

`warrant-core` establishes the abstract backbone of the WARRaNT knowledge graph. It does not model domain-specific phenomena (vessels, risks, sensors) — it defines the **abstract categories** that all other modules specialise. Any entity that participates in the WARRaNT ontology is a subclass of one of the seven top-level classes defined here.

---

## Top-Level Class Hierarchy

| Class | Role |
|---|---|
| `OperationalEntity` | Anything that operates, functions, or acts within the system boundary (vessels, functions, components, operators) |
| `AgentEntity` | Entities capable of autonomous or semi-autonomous action — human or machine agents |
| `ContextEntity` | Entities that describe the operating environment and situational context |
| `EvidenceEntity` | Observations, measurements, and outputs that provide epistemic grounding |
| `DependabilityEntity` | Quantitative assessments of system health and dependability |
| `MitigationEntity` | Rules and actions that respond to detected degradation |
| `VisualisableEntity` | Anything the Digital Twin is permitted to render or monitor |

> **Design note:** `VisualisableEntity` is defined here — not in `warrant-digital-twin` — so that any module can declare its classes as visualisable without creating a circular import dependency.

---

## Context Vocabulary

`ContextEntity` is specialised into the following subclasses, which describe the operational situation surrounding a vessel or system:

| Class | Description |
|---|---|
| `OperationalContext` | Aggregates the full set of contextual factors for a voyage or operation |
| `EnvironmentalCondition` | Physical environmental state (sea, weather, visibility, traffic) |
| `VoyageSegment` | A discrete segment of a voyage with a defined operational profile |
| `OperationalMode` | The mode in which a vessel or system is operating |

### `OperationalMode` Named Individuals

Six standard modes are defined as named individuals to provide a controlled vocabulary for mode-dependent reasoning:

| Individual | Meaning |
|---|---|
| `warrant:RemoteControlMode` | Vessel operated remotely from an ROC |
| `warrant:AutonomousMode` | Vessel operating without real-time human input |
| `warrant:ManualMode` | Vessel under direct helm control |
| `warrant:HandoverMode` | Transition between remote and manual control |
| `warrant:StandbyMode` | Vessel powered, systems active, not underway |
| `warrant:EmergencyMode` | Emergency protocols active |

### `EnvironmentalCondition` Subclasses

| Class | Description |
|---|---|
| `WeatherCondition` | Wind, precipitation, temperature |
| `SeaStateCondition` | Wave height, swell, Beaufort scale |
| `TrafficCondition` | Traffic density, encounter geometry |
| `InfrastructureCondition` | Locks, bridges, port approaches |
| `NetworkCoverageCondition` | Cellular/satellite connectivity availability |
| `VisibilityCondition` | Meteorological visibility |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `warrant:hasIdentifier` | `OperationalEntity` | `xsd:string` | Unique asset identifier |
| `warrant:hasName` | `OperationalEntity` | `xsd:string` | Human-readable name |
| `warrant:hasTimestamp` | `EvidenceEntity` | `xsd:dateTime` | Event or observation timestamp |
| `warrant:hasDescription` | (general) | `xsd:string` | Textual description |
| `warrant:hasVersion` | (general) | `xsd:string` | Version string |
| `warrant:livingLab` | `OperationalEntity` | `xsd:string` | WARRaNT living lab assignment |

---

## Design Principles

1. **Abstract only.** No class in `warrant-core` should be instantiated directly in data — instances are always of a more specific subclass from a domain module.
2. **`VisualisableEntity` belongs here.** All modules that produce visualisable knowledge graph entities mark their classes as `rdfs:subClassOf warrant:VisualisableEntity` — they import `warrant-core`, never `warrant-digital-twin`.
3. **Operational modes as named individuals.** Mode vocabulary is fixed at the ontology level; data consumers must not subclass `OperationalMode`.

---

## Imports

`warrant-core` has **no imports** from other WARRaNT modules. It imports only:

- `owl:` (OWL 2 DL)
- `rdfs:` / `rdf:`
- `xsd:`

---

## Downstream Dependents

Every other WARRaNT module imports `warrant-core`:

`warrant-davom` · `warrant-cdm` · `warrant-assurance` · `warrant-di` · `warrant-observation` · `warrant-scenario` · `warrant-mitigation` · `warrant-digital-twin`
