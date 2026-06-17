# `warrant-di` — Dependability Index Module

**Namespace:** `https://w3id.org/warrant/di#`  
**Prefix:** `di:`  
**Status:** Stable  
**Role:** Quantification layer — defines the Dependability Index (DI), a time-varying scalar that expresses the current dependability health of a vessel function, system, or vessel as a whole.

---

## Purpose

`warrant-di` is where all upstream analysis converges into a **single actionable number per monitored entity**. The Dependability Index integrates assurance scores, risk propagation, and penalties into a scalar in [0, 1] that supports:

- Real-time operational monitoring (is this function safe to rely on right now?)
- Decision support in the Digital Twin (which function is most degraded?)
- Scenario "what-if" analysis (how would this failure propagate?)
- Mitigation triggering (has DI crossed a threshold requiring action?)

---

## Class Hierarchy

```
DependabilityEntity  (from warrant-core)
├── DependabilityIndex        (per-entity DI)
├── SystemDependabilityIndex  (vessel-level aggregate DI)
├── PropagatedRisk            (risk contribution propagated across a dependency edge)
├── RiskPropagationEdge       (weighted edge encoding how DI propagates between entities)
├── DependabilityIndexState   (abstract state class — DO NOT subclass)
├── DIThreshold               (threshold value that triggers a state transition)
├── DIWeight                  (γ weight for SystemDI aggregation)
├── DICalculationMethod       (record of the method used for a DI computation)
└── DIUpdateEvent             (audit record of a DI recalculation)
```

---

## DI States — Named Individuals Only

`DependabilityIndexState` is a **closed vocabulary** defined entirely as named individuals. Subclassing `DependabilityIndexState` is **prohibited**. The five defined states are:

| Individual | Semantic | Suggested Display |
|---|---|---|
| `di:NormalState` | DI above upper threshold; entity fully dependable | Green |
| `di:DegradedState` | DI between thresholds; reduced but operable | Amber |
| `di:CriticalState` | DI below lower threshold; requires immediate attention | Orange |
| `di:FailedState` | Entity has failed; function cannot be performed | Red |
| `di:UnsafeState` | Entity poses active safety risk; immediate intervention required | Dark Red |

State assignment is performed by external computation comparing the current `DIValue` against the `DIThreshold` individuals defined for each entity.

---

## The DI Formula

### Per-entity DI

> **DI_i(t) = A_i(t) − β · R̃_i(t)**

Where:
- `A_i(t)` is the `AssuranceScore` value for entity *i* at time *t* (from `warrant-assurance`)
- `R̃_i(t)` is the normalised propagated risk reaching entity *i* (from `PropagatedRisk`)
- `β` is the `betaWeight` stored on the `DependabilityIndex` individual

### System-level DI

> **DI_sys(t) = Σ γᵢ · DI_i(t)**

Where:
- `γᵢ` is the `DIWeight` for entity *i* relative to the system
- The sum is over all monitored entities in the system

**The computation is external.** The KG stores:
- `AssuranceScore` inputs (from `warrant-assurance`)
- `PropagatedRisk` values
- `betaWeight` and `γᵢ` weights on DI individuals
- The resulting `DIValue` and `DIState`
- `DIUpdateEvent` audit records

---

## Risk Propagation

`RiskPropagationEdge` models how DI degradation in one entity propagates to dependent entities:

```
RiskPropagationEdge
  → di:propagationSource → DependabilityIndex (source entity)
  → di:propagationTarget → DependabilityIndex (target entity)
  → di:propagationWeight → xsd:decimal         (weight of propagation)
```

This enables graph-based propagation of risk across the dependency network defined in `warrant-davom`. The propagation weight corresponds to the `davom:weight` of the underlying `Dependency`.

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `di:appliesTo` | `DependabilityIndex` | `VesselFunction` / `System` | Entity this DI characterises |
| `di:hasDIState` | `DependabilityIndex` | `DependabilityIndexState` | Current state (named individual) |
| `di:hasDIThreshold` | `DependabilityIndex` | `DIThreshold` | State transition thresholds |
| `di:hasPropagatedRisk` | `DependabilityIndex` | `PropagatedRisk` | Incoming propagated risk |
| `di:propagationSource` | `RiskPropagationEdge` | `DependabilityIndex` | Source of propagation |
| `di:propagationTarget` | `RiskPropagationEdge` | `DependabilityIndex` | Target of propagation |
| `di:hasWeight` | `SystemDependabilityIndex` | `DIWeight` | Aggregation weight per entity |
| `di:triggeredBy` | `DIUpdateEvent` | `AssuranceDegradation` / `DetectionEvent` | What caused this update |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `di:DIValue` | `DependabilityIndex` | `xsd:decimal` | Current DI value [0, 1] |
| `di:betaWeight` | `DependabilityIndex` | `xsd:decimal` | Risk penalty weight β |
| `di:propagatedRiskValue` | `PropagatedRisk` | `xsd:decimal` | Normalised propagated risk value |
| `di:propagationWeight` | `RiskPropagationEdge` | `xsd:decimal` | Edge weight γ for propagation |
| `di:weightValue` | `DIWeight` | `xsd:decimal` | γᵢ weight for system DI aggregation |
| `di:thresholdValue` | `DIThreshold` | `xsd:decimal` | Numeric threshold value |
| `di:thresholdType` | `DIThreshold` | `xsd:string` | UPPER / LOWER / CRITICAL |
| `di:calculatedAt` | `DependabilityIndex` | `xsd:dateTime` | Timestamp of last DI update |
| `di:calculationMethod` | `DIUpdateEvent` | `xsd:string` | Identifier of method used |

---

## System DI Aggregation

`SystemDependabilityIndex` aggregates per-entity DI values into a vessel-level scalar. It is linked to the individual `DependabilityIndex` entities via `DIWeight` individuals, each carrying a `weightValue` that encodes the relative operational importance of that entity to the vessel as a whole.

```
SystemDependabilityIndex
  → di:hasWeight → DIWeight [weightValue: γᵢ]
      → di:appliesToComponent → DependabilityIndex (entity i)
```

---

## Design Principles

1. **DI states are closed.** The five named individuals are the only valid states. No new states can be added without ontology revision and stakeholder approval.
2. **Computation is external.** The formula runs in Python or a SPARQL update service; the KG stores only inputs, weights, results, and audit events.
3. **Every update is recorded.** A `DIUpdateEvent` individual is created for every DI recalculation, linking it to the triggering event and the method used. This enables full audit trails and drift analysis.
4. **Propagation follows dependency structure.** `RiskPropagationEdge` weights should be derived from the `davom:weight` values on the underlying `Dependency` individuals — the dependency model and the DI propagation model are intentionally aligned.

---

## Imports

- `warrant-core`
- `warrant-davom`
- `warrant-assurance`

---

## Downstream Dependents

`warrant-scenario` · `warrant-mitigation` · `warrant-digital-twin`
