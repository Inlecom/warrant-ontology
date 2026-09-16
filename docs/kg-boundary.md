# WARRaNT KG Ontology — KG Boundary

Version 0.10-poc | 2026-09-06

This document clarifies the boundary between what is represented inside the WARRaNT Knowledge Graph, what belongs to external project context, and what belongs to external runtime systems.

---

## 1. In-KG Content

The KG contains semantic definitions and structured instance data that:

- Represent the **vessel operational structure** (DAVOM): vessels, functions, systems, components, data flows, communication links, security zones and conduits, asset roles, human operator roles, operational procedures, typed dependencies.
- Represent the **design-time knowledge** (CDM): deviations, hazards, risks with the impact triple, accidents, losses, failure modes with FMEA ratings, threat scenarios, vulnerabilities, controls with residual risk, unsafe control actions, process model flaws, safety constraints, hazard classes with their admissible propagation types.
- Represent **observations and health events**: metric types, observers, measurements (as semantic anchors), health events (detected and predicted), node health monitors, virtual sensors, operator inputs.
- Represent **attribute assessment**: attribute values with source confidence and fusion lineage, mode-scoped weights, node dependability scores.
- Represent the **Dependability Index and supervision**: node, link and system DI, per-hazard-class propagated risk and propagation edges, hierarchical aggregation weights, attribute thresholds and attribute-wise operational states (named individuals), supervision configuration, resilience triggers, DI forecasts, update events.
- Represent **scenario semantics**: scenario types, triggers, executions with lifecycle state, results with projected state and forecasts.
- Represent **responses**: the response library (rules, actions, failover procedures, redundant resources, recovery effects), REDS response evaluations (expected effect, cost, penalty, rank, admissibility), IRDS response executions (authorisation, posture, outcome).
- Represent the **Living Dependability Case**: requirements, claims with status, assumptions, evidence and obligations, nonconformities, Assurance Level, Certification Readiness.
- Represent the **digital twin interface**: DT views, visualisation layers, decision-support views, update channels, forecasts produced.
- Represent **controlled vocabularies**: deviation types, operational states, operational modes, dependency types, asset roles, hazard classes, monitoring levels, trigger types, strategy types, postures, authorisation statuses, claim and obligation statuses, execution lifecycle states.
- Store **traceability links** from evidence through health events, deviations, hazards, attribute values, indices, triggers, evaluations and executions to claims and requirements.
- Store **references to external data**: `obs:hasExternalRecordReference`, `obs:hasExternalTimeSeriesId`.

---

## 2. External Project Context

The following belong to WARRaNT project documents and deliverables but are **not top-level domain concepts** in the ontology:

- **Work Packages, Tasks, Deliverables**: project management structure (D1.x, T1.x, WP3). Expressed in grant agreement documents, not in the KG.
- **Partners**: Danaos, AELER, DST, Seafar, Inlecom, SINTEF Ocean/Digital, NTUA, DNV, Tecnalia, Konnecta, TU Delft, PoAB, VLTN. Not top-level KG classes.
- **Methodological Concept Layer**: STPA/HAZOP methodology documentation, HAZOP worksheets, STPA workbooks, FMEA worksheets, the cybersecurity risk assessment methodology. These inform the ontology (and their outputs are its intended inputs) but the methods themselves are not stored in it.
- **The framework paper's formulas**: the node score, confidence fusion, typed propagation, hierarchical aggregation, state assignment, resilience criterion, REDS objective, Assurance Level and Certification Readiness are documented in module headers as metadata and computed externally.
- **Living Lab descriptions**: the narrative context for LL1–LL4. The KG represents the vessel, functions, and scenarios — not the LL project description itself.

---

## 3. External Runtime Systems

The following systems interact with the KG but are **not part of it**:

| System | Relationship to KG |
|--------|-------------------|
| Real-time telemetry platforms | KG stores references (`obs:hasExternalTimeSeriesId`) |
| Time-series databases (e.g. InfluxDB) | KG stores record references (`obs:hasExternalRecordReference`) |
| Event streams (e.g. Kafka) | KG receives processed health events, not raw streams |
| Health-event processing (detect, filter, correlate, fuse, contextualise, classify) | KG stores the resulting `obs:HealthEvent`s with lineage; the processing is external |
| Node Health Monitors (Task 1.3 observer-based FDI and others) | Represented as `obs:NodeHealthMonitor` individuals for provenance; KG stores their health events and attribute assessments |
| Dependability Supervisor | Represented as `di:DependabilitySupervisor`; computes fusion, propagation, DI, state, trend, triggers externally; KG stores configuration, inputs and results |
| REDS (Risk Evaluation and Decision Support) | Represented as `mit:DecisionSupportService`; ranks alternatives externally; KG stores evaluations |
| IRDS (Intelligent Resilience and Dependability Supervisor) | Represented as `mit:ResilienceSupervisor`; coordinates authorised responses; KG stores executions |
| Virtual sensor execution engines | KG stores VirtualSensorOutput; estimation is external |
| Scenario engine | KG defines semantics; engine executes and returns ScenarioResult and forecasts |
| Digital Twin | Reads from KG via `dt:visualises`; renders views externally; writes back forecasts (`dt:producesForecast`), virtual-sensor outputs and predicted-condition events |
| Living Dependability Case tooling / assurance-case editors | KG holds claims, evidence, obligations and status; AL and CR are computed externally; acceptance judgement remains with the assuring stakeholder |
| Vessel systems (VCS, AMP, SP, AIP) | KG models their structural role; raw data stays external |
| Shore systems (ROC, shore APIs) | KG models ROC operator roles, communication links and conduits |
| Communication networks (LTE/5G, VSAT) | KG models as `davom:CommunicationLink` / `davom:Conduit` with metrics |

---

## 4. Principle: KG as Semantic Layer, Not Operational Database

The KG is a **semantic layer** that:
- Defines concepts and their relationships (ontology).
- Stores the latest significant states and events, and the audit records needed for traceability (not full time-series history).
- Stores governed configuration (weights, thresholds, floors, damping, decision weights) with version and approval, and calculation results with timestamp and method identity (not the computation itself).
- Stores scenario semantics and results (not the simulation execution).
- Links to external systems via reference properties.

The KG does **not**:
- Store raw sensor readings at high frequency.
- Execute fusion, propagation, DI, state assignment, trigger evaluation, response ranking, Assurance Level or readiness calculations, scenario simulations, or analytical rules.
- Decide what evidence an authority must accept.
- Implement the Digital Twin rendering or UI.
- Replace event streaming infrastructure.
