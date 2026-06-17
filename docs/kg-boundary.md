# WARRaNT KG Ontology — KG Boundary

Version 0.9-poc | 2026-06-05

This document clarifies the boundary between what is represented inside the WARRaNT Knowledge Graph, what belongs to external project context, and what belongs to external runtime systems.

---

## 1. In-KG Content

The KG contains semantic definitions and structured instance data that:

- Represent the **vessel operational structure** (DAVOM): vessels, functions, systems, components, data flows, communication links, human operator roles, operational procedures.
- Represent the **causal dependability model** (CDM): deviations, hazards, risks, accidents, losses, unsafe control actions, process model flaws, safety constraints.
- Represent **assurance and dependability metrics**: metric types, assurance attributes, assurance scores, assurance weights, degradation events, penalties.
- Represent the **Dependability Index** and its propagation: node DI values, propagated risk, risk propagation edges, system DI, DI states (named individuals).
- Represent **scenario semantics**: scenario types, triggers, execution records, results.
- Represent **mitigation and failover semantics**: mitigation rules, advisory actions, failover procedures, redundant resources.
- Represent the **digital twin interface**: DT views, visualisation layers, decision-support views, update channels.
- Represent **controlled vocabularies**: `cdm:DeviationType`, `di:DependabilityIndexState`, `warrant:OperationalMode`.
- Store **traceability links** connecting detection events, deviations, hazards, risks, degradation, assurance scores, and DI values.
- Store **references to external data**: `obs:hasExternalRecordReference`, `obs:hasExternalTimeSeriesId`.

---

## 2. External Project Context

The following belong to WARRaNT project documents and deliverables but are **not top-level domain concepts** in the ontology:

- **Work Packages, Tasks, Deliverables**: project management structure (D1.x, T1.x, WP3). Expressed in grant agreement documents, not in the KG.
- **Partners**: Danaos, AELER, DST, Seafar, Inlecom, SINTEF Ocean/Digital, NTUA, DNV, Tecnalia, Konnecta, TU Delft, PoAB, VLTN. Not top-level KG classes.
- **Methodological Concept Layer**: STPA/HAZOP methodology documentation, HAZOP worksheets, STPA workbooks. These inform the ontology but are not stored in it.
- **Consolidated WARRaNT Concept Base**: whitepaper definitions, vocabulary alignment, concept hierarchy. Referenced in modelling decisions.
- **Living Lab descriptions**: the narrative context for LL1–LL4. The KG represents the vessel, functions, and scenarios — not the LL project description itself.

Domain knowledge in the KG is expressed in terms of **vessels, functions, systems, hazards, risks, and dependability metrics** — not in terms of project management structure.

---

## 3. External Runtime Systems

The following systems interact with the KG but are **not part of it**:

| System | Relationship to KG |
|--------|-------------------|
| Real-time telemetry platforms | KG stores references (`obs:hasExternalTimeSeriesId`) |
| Time-series databases (e.g. InfluxDB) | KG stores record references (`obs:hasExternalRecordReference`) |
| Event streams (e.g. Kafka) | KG receives processed events, not raw streams |
| Analytical services | KG stores their outputs (DetectionEvents, Statuses, DI values) |
| Virtual sensor execution engines | KG stores VirtualSensorOutput; computation is external |
| Scenario engine | KG defines semantics; engine executes and returns ScenarioResult |
| DI calculation service | Computes A_v, R̃_i, DI_i, DI_sys; KG stores inputs, weights, results |
| Digital Twin UI | Reads from KG via `dt:visualises`; renders views externally |
| Vessel systems (VCS, AMP, SP, AIP) | KG models their structural role; raw data stays external |
| Shore systems (ROC, shore APIs) | KG models ROC operator roles and communication links |
| Communication networks (LTE/5G, VSAT) | KG models as `davom:CommunicationLink` with metrics |

---

## 4. Principle: KG as Semantic Layer, Not Operational Database

The KG is a **semantic layer** that:
- Defines concepts and their relationships (ontology).
- Stores the latest significant states and events (not full time-series history).
- Stores calculation results and traceability (not the computation itself).
- Stores scenario semantics and results (not the simulation execution).
- Links to external systems via reference properties.

The KG does **not**:
- Store raw sensor readings at high frequency.
- Execute DI calculations, scenario simulations, or analytical rules.
- Implement the Digital Twin rendering or UI.
- Replace event streaming infrastructure.
