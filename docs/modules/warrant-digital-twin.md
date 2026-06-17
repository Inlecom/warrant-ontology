# `warrant-digital-twin` — Digital Twin Module

**Namespace:** `https://w3id.org/warrant/dt#`  
**Prefix:** `dt:`  
**Status:** Stable  
**Role:** Integration layer — defines the Digital Twin as the semantic interface between the WARRaNT knowledge graph and operational visualisation, scenario execution, and decision support.

---

## Purpose

`warrant-digital-twin` is the **topmost layer** of the WARRaNT ontology stack. It does not introduce new domain concepts — it defines the *interface* through which the KG is made actionable: the Digital Twin entity that monitors operational assets, executes scenarios, visualises dependability state, and presents decision support to operators.

Every named individual of type `DigitalTwin` in the KG represents a specific vessel's or system's digital counterpart. Through the object properties defined in this module, that individual is connected to everything the KG knows about it.

---

## Class Hierarchy

```
DigitalTwin                    (the semantic twin entity)
├── DigitalTwinView            (a specific rendered view of the twin)
│   └── DecisionSupportView   (view presenting DI state + mitigations + scenario results)
├── VisualisationLayer         (a layer within a view rendering specific KG entities)
└── ScenarioExecutionState     (lifecycle state of a scenario run within the twin)
    [PENDING → RUNNING → COMPLETED | FAILED]
```

---

## The `VisualisableEntity` Bridge

The `dt:visualises` property has **`warrant:VisualisableEntity`** (defined in `warrant-core`) as its range. This means:

- Any class that is `rdfs:subClassOf warrant:VisualisableEntity` can be visualised by a `DigitalTwin` or `VisualisationLayer`
- The following classes from other modules are declared `VisualisableEntity`:
  - `Hazard`, `Risk`, `Accident`, `Loss` (from `warrant-cdm`)
  - `DependabilityIndex`, `SystemDependabilityIndex` (from `warrant-di`)
  - `Scenario`, `ScenarioExecution` (from `warrant-scenario`)
  - `MitigationAction`, `FailoverProcedure` (from `warrant-mitigation`)
  - `OperationalEntity`, `AgentEntity` (from `warrant-core`)

> **Design rationale:** `VisualisableEntity` lives in `warrant-core`, not here, to avoid circular imports. Any module can mark its classes as visualisable by importing only `warrant-core`.

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `dt:visualises` | `DigitalTwin` / `VisualisationLayer` | `VisualisableEntity` | Declares what this twin / layer renders |
| `dt:representsStateOf` | `DigitalTwin` | `Vessel` | The physical vessel this twin mirrors |
| `dt:monitors` | `DigitalTwin` | `OperationalEntity` | Entities the twin continuously monitors |
| `dt:executes` | `DigitalTwin` | `Scenario` | Scenario the twin can execute |
| `dt:storesResult` | `DigitalTwin` | `ScenarioExecution` | Execution records stored by the twin |
| `dt:receivesUpdateFrom` | `DigitalTwin` | `DataSource` | Live data feeds into the twin |
| `dt:hasView` | `DigitalTwin` | `DigitalTwinView` | Views available in this twin |
| `dt:hasLayer` | `DigitalTwinView` | `VisualisationLayer` | Layers within a view |
| `dt:supportsDecision` | `DigitalTwin` | `DecisionSupportView` | Decision support interface |

---

## Live Update Pattern

The Digital Twin stays synchronised with vessel state via `dt:receivesUpdateFrom`:

```
MAI_W_DigitalTwin : DigitalTwin
  → dt:receivesUpdateFrom → GNSSMonitoringService : AnalyticalService
  → dt:receivesUpdateFrom → NetworkMonitoringService : AnalyticalService
  → dt:receivesUpdateFrom → ROCHandoverCommLink : CommunicationLink
```

The `DataSource` range (from `warrant-observation`) includes `AnalyticalService`, `Observer`, and `HumanOperatorRole` — all valid sources of live updates.

---

## Scenario Execution Interface

The twin executes scenarios on demand or automatically when trigger conditions are met:

```
DigitalTwin
  → dt:executes → Scenario (from warrant-scenario)
      [trigger fires]
  ScenarioExecution created
      → scenario:hasResult → ScenarioResult
  DigitalTwin
      → dt:storesResult → ScenarioExecution
```

`ScenarioExecutionState` tracks the lifecycle:

| State | Meaning |
|---|---|
| `PENDING` | Scenario queued; trigger confirmed but execution not yet started |
| `RUNNING` | Execution in progress; DI projections being computed |
| `COMPLETED` | Execution finished; `ScenarioResult` available |
| `FAILED` | Execution failed; partial results may be available |

---

## Decision Support View

`DecisionSupportView` is the primary interface for the ROC operator or ship's officer. It presents:

1. **Current DI state** — per-function DI values with state colour coding
2. **Active deviations** — current `Deviation` individuals with type and source
3. **Active hazards and risks** — causal chain view
4. **Recommended mitigations** — `AdvisoryAction` individuals ranked by priority
5. **Scenario results** — projected DI if scenario plays out unmitigated vs. mitigated

---

## Per-Living-Lab Digital Twins

Each WARRaNT living lab has a dedicated `DigitalTwin` individual:

| Individual | Vessel | Living Lab |
|---|---|---|
| `MAI_W_DigitalTwin` | MAI-W (Type C tanker) | LL4 — Seafar (remote operation) |
| `LL2_DigitalTwin` | AELER cargo vessel | LL2 — AELER (smart containers) |
| `ContainerVessel_DigitalTwin` | Danaos containership | LL1 — Danaos (cybersecurity) |

---

## Design Principles

1. **Thin integration layer.** This module defines no new domain concepts — only the interface between the KG and its users. Domain knowledge lives in the upstream modules.
2. **`VisualisableEntity` enables open extension.** New modules can make their classes visualisable by declaring `rdfs:subClassOf warrant:VisualisableEntity` without touching this module.
3. **Scenarios are both declared and executed.** The same `Scenario` individual that documents a risk scenario in the safety analysis is the one the DT executes — no duplication or mapping required.
4. **Advisory by design.** The DT presents `AdvisoryAction` recommendations; it does not act autonomously in the current PoC. `MachineActionableAction` support is reserved for future autonomy levels.

---

## Imports

- `warrant-core`
- `warrant-davom`
- `warrant-observation`
- `warrant-di`
- `warrant-scenario`
- `warrant-mitigation`

---

## Upstream Dependencies

All WARRaNT modules. `warrant-digital-twin` is the only module that imports the full stack.
