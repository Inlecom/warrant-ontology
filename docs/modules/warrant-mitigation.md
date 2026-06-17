# `warrant-mitigation` — Mitigation Module

**Namespace:** `https://w3id.org/warrant/mitigation#`  
**Prefix:** `mitigation:`  
**Status:** Stable  
**Role:** Response layer — defines the vocabulary for mitigation rules, advisory actions, automated failover procedures, and their relationships to the deviations, hazards, and risks they address.

---

## Purpose

`warrant-mitigation` closes the monitoring loop. Once a deviation is detected and its causal consequences modelled (via `warrant-cdm`), and its DI impact quantified (via `warrant-di`), the system must recommend or enact a response. This module defines the full vocabulary for that response layer — from high-level rules that identify when mitigation is needed, to specific advisory actions for human operators, to automated failover procedures that execute without human intervention.

---

## Class Hierarchy

```
MitigationEntity   (top-level)
├── MitigationRule          (condition → action rule; the "if this, then that" logic)
├── MitigationAction        (abstract: anything that constitutes a mitigating action)
│   ├── AdvisoryAction      (advises a human operator; current PoC implementation)
│   └── MachineActionableAction  (future: directly executable by an automated agent)
├── FailoverProcedure       (a structured procedure for switching to a redundant resource)
├── RedundantResource       (a resource available to substitute a failed entity)
└── RecoveryEffect          (the quantified effect of a mitigation on DI and risk)
```

---

## The Mitigation Flow

```
Deviation / Hazard / Risk / DI state
  → mitigation:matchesRule → MitigationRule
      → mitigation:recommends → AdvisoryAction (or MachineActionableAction)
          → mitigation:activates → FailoverProcedure
              → mitigation:usesResource → RedundantResource
                  → mitigation:hasRecoveryEffect → RecoveryEffect
```

### Matching logic

A `MitigationRule` is matched when:
- A specific `Deviation` type is detected (`matchesDeviation`)
- A `Hazard` is triggered (`matchesHazard`)
- A `Risk` exceeds a threshold (`matchesRisk`)
- A DI state is entered (`matchesDIState`)

Multiple matching criteria can be combined — a rule fires when **all** specified conditions are satisfied.

---

## Advisory Actions (Current PoC)

`AdvisoryAction` is the primary implementation pattern in the WARRaNT living lab demonstrators. An advisory action presents a recommendation to a human operator through the Digital Twin interface. The operator decides whether to enact it.

Each `AdvisoryAction` individual carries:
- A human-readable description (`mitigation:description`)
- A priority level (`mitigation:priority`: IMMEDIATE / HIGH / MEDIUM / LOW)
- A target role (`mitigation:targetRole` → `HumanOperatorRole`)
- An optional deadline (`mitigation:respondBy`)

### Example

```turtle
:SwitchToINSAIS  a  mitigation:AdvisoryAction ;
    mitigation:description  "Activate INS/AIS positioning; notify ROC operator" ;
    mitigation:priority     "IMMEDIATE" ;
    mitigation:targetRole   :RemoteOperatorRole .
```

---

## Machine-Actionable Actions (Forward Compatibility)

`MachineActionableAction` is defined to support future automated response capabilities. In the current PoC, all instances are advisory — the class is present to avoid ontology revision when automation is introduced.

---

## Failover Procedures

`FailoverProcedure` models structured multi-step recovery procedures:

- **What is being switched:** the failed entity (`mitigation:addressesComponent` / `addressesSystem` / `addressesFunction` / `addressesLink`)
- **What it switches to:** the redundant resource (`mitigation:usesResource → RedundantResource`)
- **The expected effect:** the quantified DI recovery (`mitigation:hasRecoveryEffect → RecoveryEffect`)

### Example: GNSS → INS/AIS failover

```
GNSSFailoverRule : MitigationRule
  → matchesDeviation → GNSSSignalLossDeviation (UNAVAILABLE)
  → recommends → SwitchToINSAIS : AdvisoryAction
      → activates → INSPositioningFailover : FailoverProcedure
          → addressesFunction → RemoteNavigationFunction
          → usesResource → INSAISPositioningResource : RedundantResource
          → hasRecoveryEffect → INSFailoverEffect : RecoveryEffect
              → projectedDIGain: +0.28
```

---

## Recovery Effect

`RecoveryEffect` records the quantified impact of a mitigation on system health:

| Property | Range | Description |
|---|---|---|
| `mitigation:projectedDIGain` | `xsd:decimal` | Expected DI improvement after mitigation |
| `mitigation:projectedRiskReduction` | `xsd:decimal` | Expected risk score reduction |
| `mitigation:recoveryTime` | `xsd:duration` | Expected time to recover |
| `mitigation:confidence` | `xsd:decimal` | Confidence in the projected effect [0, 1] |

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `mitigation:matchesDeviation` | `MitigationRule` | `Deviation` | Rule matches this deviation type |
| `mitigation:matchesHazard` | `MitigationRule` | `Hazard` | Rule matches this hazard |
| `mitigation:matchesRisk` | `MitigationRule` | `Risk` | Rule matches this risk |
| `mitigation:matchesDIState` | `MitigationRule` | `DependabilityIndexState` | Rule fires in this DI state |
| `mitigation:recommends` | `MitigationRule` | `MitigationAction` | Rule recommends this action |
| `mitigation:activates` | `AdvisoryAction` | `FailoverProcedure` | Action activates this procedure |
| `mitigation:usesResource` | `FailoverProcedure` | `RedundantResource` | Procedure uses this resource |
| `mitigation:addressesComponent` | `FailoverProcedure` | `Component` | Component being recovered |
| `mitigation:addressesFunction` | `FailoverProcedure` | `VesselFunction` | Function being recovered |
| `mitigation:hasRecoveryEffect` | `FailoverProcedure` | `RecoveryEffect` | Quantified recovery projection |
| `mitigation:targetRole` | `AdvisoryAction` | `HumanOperatorRole` | Who should act on this advisory |

---

## Relationship to Other Modules

| Module | Relationship |
|---|---|
| `warrant-cdm` | Rules match `Deviation`, `Hazard`, `Risk` |
| `warrant-di` | Rules match `DependabilityIndexState`; recovery effects project DI changes |
| `warrant-davom` | Procedures address `Component`, `System`, `VesselFunction`, `CommunicationLink`; target `HumanOperatorRole` |
| `warrant-scenario` | Scenario results inform mitigation selection; mitigations can reference the scenarios they resolve |
| `warrant-digital-twin` | The DT presents `AdvisoryAction` recommendations and records operator responses |

---

## Design Principles

1. **Rules are declarative.** `MitigationRule` individuals declare matching conditions and recommendations; they do not contain procedural code. Execution logic lives in the application layer.
2. **Advisory first, automated later.** All current implementations use `AdvisoryAction`. `MachineActionableAction` is reserved for future autonomy levels without requiring ontology change.
3. **Recovery effects are projections.** `RecoveryEffect` values are estimates based on historical data, simulation, or expert judgement — they carry a `confidence` score to convey epistemic uncertainty.
4. **No datatype properties on `MitigationRule`.** Rules are structured via object properties only — matching conditions are typed entity references, not string expressions.

---

## Imports

- `warrant-core`
- `warrant-davom`
- `warrant-cdm`
- `warrant-di`

---

## Downstream Dependents

`warrant-digital-twin`
