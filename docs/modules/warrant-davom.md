# `warrant-davom` — Digital Architecture of Vessel and Operations Model

**Namespace:** `https://w3id.org/warrant/davom#`  
**Prefix:** `davom:`  
**Status:** Stable  
**Role:** Structural layer — models the physical and functional decomposition of a vessel and its operational organisation.

---

## Purpose

`warrant-davom` defines the **physical architecture** of a vessel: how it is decomposed into functions, systems, subsystems, and components; how operators and their roles are organised; how components are linked by data flows and communication links; and how dependencies between elements are typed and weighted. It is the structural substrate on which all other domain modules anchor their entities — a `Deviation` always originates in a `Component`, a `DependabilityIndex` always applies to a `VesselFunction`.

---

## Class Hierarchy

### Vessel Decomposition

```
Vessel
└── VesselFunction          (what the vessel does)
    └── System              (implements a function)
        ├── NavigationSystem
        ├── PropulsionSystem
        ├── CommunicationSystem
        ├── PowerSystem
        └── SafetySystem
            └── Subsystem   (implements part of a system)
                └── Component   (leaf-level hardware/software element)
                    ├── SensorComponent
                    ├── ActuatorComponent
                    ├── ComputingComponent
                    ├── CommunicationComponent
                    ├── PowerComponent
                    ├── DisplayComponent
                    ├── NetworkComponent
                    └── SoftwareComponent
```

### Human Organisation

```
AgentEntity  (from warrant-core)
├── HumanOperator           (the person; NOT a Component)
└── HumanOperatorRole       (the capacity in which an operator acts)
    └── OperatorInterface   (the HMI through which roles interact with systems)
```

> **Critical design constraint:** `HumanOperator` and `HumanOperatorRole` are subclasses of `AgentEntity`, **not** `OperationalEntity` or `Component`. This reflects the WARRaNT principle that human operators are agents who supervise and act, not components that degrade.

### Operational Artefacts

| Class | Description |
|---|---|
| `ControlAction` | A directive issued by an operator or controller to a controlled process |
| `OperationalProcedure` | A defined sequence of steps for a specific operational situation |
| `DataFlow` | A directed data exchange between two components or systems |
| `CommunicationLink` | A physical or logical channel for data transmission |

### Dependency Model

```
Dependency
├── FunctionalDependency      (A requires B to perform its function)
├── DataDependency            (A requires data produced by B)
├── PowerDependency           (A requires power supplied by B)
├── CommunicationDependency   (A requires a communication channel through B)
├── HumanSupervisionDependency (A requires human oversight via B)
├── ServiceDependency         (A requires a service offered by B)
├── ControlDependency         (A is governed or commanded by B)
├── TimeDependency            (A requires synchronised timing from B)
└── RedundancyDependency      (A can be substituted by B)
```

Each `Dependency` individual carries:
- `davom:dependencySource` → the depending entity
- `davom:dependencyTarget` → the entity depended upon
- `davom:weight` (xsd:decimal) — criticality weight [0, 1]
- `davom:isCritical` (xsd:boolean) — flag for single-point-of-failure analysis

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `davom:hasFunction` | `Vessel` | `VesselFunction` | Links vessel to its operational functions |
| `davom:isSupportedBy` | `VesselFunction` | `System` | Links function to implementing system |
| `davom:hasSubsystem` | `System` | `Subsystem` | System decomposition |
| `davom:hasComponent` | `System` / `Subsystem` | `Component` | Component membership |
| `davom:usesCommunicationLink` | `VesselFunction` | `CommunicationLink` | Function uses a comm link |
| `davom:hasOperatorRole` | `Vessel` | `HumanOperatorRole` | Vessel has an assigned operator role |
| `davom:requiresOperatorRole` | `VesselFunction` | `HumanOperatorRole` | Function requires a specific role to operate |
| `davom:authorizes` | `HumanOperatorRole` | `ControlAction` | Role can issue this control action |
| `davom:executes` | `HumanOperatorRole` | `OperationalProcedure` | Role executes a procedure |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `davom:weight` | `Dependency` | `xsd:decimal` | Dependency criticality weight [0, 1] |
| `davom:isCritical` | `Dependency` | `xsd:boolean` | Whether dependency is a single point of failure |
| `davom:dependencyType` | `Dependency` | `xsd:string` | Textual type label |
| `davom:hasCapacity` | `Component` | `xsd:string` | Operational capacity description |
| `davom:serialNumber` | `Component` | `xsd:string` | Physical asset serial number |

---

## Design Principles

1. **Structural completeness.** Every entity in the KG that represents a physical or functional asset must be reachable from a `Vessel` via the decomposition hierarchy.
2. **Human operators are agents.** The `HumanOperator`/`HumanOperatorRole` distinction follows the STAMP/STPA convention: roles issue control actions and execute procedures; persons are not modelled as components.
3. **Dependency weighting.** The dependency sub-hierarchy enables graph-based propagation of risk and assurance degradation — weights are used directly in the DI computation (see `warrant-di`).
4. **`ControlAction` is shared.** `ControlAction` defined here is the same entity used by `warrant-cdm` as part of the STPA control loop — no duplication.

---

## Imports

- `warrant-core`

---

## Downstream Dependents

`warrant-cdm` · `warrant-observation` · `warrant-di` · `warrant-scenario` · `warrant-mitigation` · `warrant-digital-twin`
