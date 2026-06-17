# `warrant-cdm` — Causal Dependability Model

**Namespace:** `https://w3id.org/warrant/cdm#`  
**Prefix:** `cdm:`  
**Status:** Stable  
**Role:** Safety and causal reasoning layer — models the causal chain from deviations to losses, integrating STPA control-loop concepts with STAMP-aligned hazard and risk reasoning.

---

## Purpose

`warrant-cdm` is the **causal engine** of the WARRaNT ontology. It defines how failures and deviations propagate through a system to produce hazards, risks, and ultimately accidents and losses. It integrates two complementary frameworks:

- **STAMP/STPA** — models the control loop (Controller → ControlAction → ControlledProcess → Feedback → ProcessModel → ProcessModelFlaw → UnsafeControlAction → Hazard)
- **Safety causal chain** — models the consequence cascade (Deviation → Hazard → Risk → Accident → Loss)

Together, these allow the WARRaNT KG to represent both *why* an unsafe condition arose (STPA) and *what the consequences are* (safety causal chain).

---

## Class Hierarchy

### Safety Causal Chain

```
Deviation               ← detected by ObservationModule; typed by hasDeviationType
  └── mayCause →
Hazard
  └── isEvaluatedAs →
Risk
  └── mayCause →
Accident
  └── mayCause →
Loss
```

### STPA Control Loop

```
Controller              (operator, automated controller — maps to HumanOperatorRole / Component)
  └── issuesControlAction →
ControlAction           (defined in warrant-davom)
  └── actsOn →
ControlledProcess       (the system receiving the control input)
  └── producesFeedback →
Feedback
  └── informsProcessModel →
ProcessModel            (controller's belief about the controlled process)
  └── hasProcessModelFlaw →
ProcessModelFlaw        (divergence between belief and reality)
  └── mayCause →
UnsafeControlAction     (a control action that is wrong, missing, late, or in the wrong order)
  └── mayCause →
Hazard                  (entry into the safety causal chain)
```

### Supporting Classes

| Class | Description |
|---|---|
| `SafetyConstraint` | A constraint that, if violated, leads to a hazard; linked to a `ControlAction` |
| `EnvironmentalCondition` | Imported from `warrant-core`; contextualises hazard occurrence |
| `AssuranceDegradation` | A quantified degradation event signalling that assurance scores must be recalculated |

---

## Deviation Type Vocabulary

Deviations are not subclassed — they are typed via the `cdm:hasDeviationType` datatype property using a controlled vocabulary of named individuals. This design avoids class proliferation and enables uniform SPARQL filtering.

| Value | Meaning |
|---|---|
| `NO` | Expected action/signal did not occur |
| `LESS` | Output is below the expected threshold |
| `MORE` | Output exceeds the expected threshold |
| `LATE` | Action or output occurred outside the required time window |
| `WRONG` | Action or output is of the incorrect type, direction, or target |
| `UNAVAILABLE` | Resource or signal is entirely absent |
| `UNTRUSTED` | Data is present but fails integrity verification |
| `INCONSISTENT` | Signal is internally inconsistent or contradicts other sources |
| `NOISY` | Signal carries excessive noise masking the true value |
| `SPOOFED` | Signal is deliberately falsified by an adversary |

> **Deprecation notice:** Named subclasses of `Deviation` (e.g., `LateDeviation`, `SpoofedDeviation`) introduced in early drafts are **deprecated**. All new instances must use `cdm:hasDeviationType` on a plain `Deviation` individual.

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `cdm:mayCause` | `Deviation` / `UnsafeControlAction` / `Hazard` / `Accident` | Next in chain | Causal propagation link |
| `cdm:isEvaluatedAs` | `Hazard` | `Risk` | Links hazard to its risk assessment |
| `cdm:hasProcessModelFlaw` | `ProcessModel` | `ProcessModelFlaw` | Identifies model divergence |
| `cdm:informsProcessModel` | `Feedback` | `ProcessModel` | Feedback updates the controller's model |
| `cdm:actsOn` | `ControlAction` | `ControlledProcess` | Control action target |
| `cdm:producesFeedback` | `ControlledProcess` | `Feedback` | Process state feedback |
| `cdm:hasDeviationConstraint` | `SafetyConstraint` | `ControlAction` | Constraint guards against a specific UCA |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `cdm:hasDeviationType` | `Deviation` / `ProcessModelFlaw` | `xsd:string` | Controlled vocabulary value (see above) |
| `cdm:likelihood` | `Risk` | `xsd:decimal` | Probability of hazard occurrence [0, 1] |
| `cdm:impact` | `Risk` | `xsd:decimal` | Severity of consequence [0, 1] |
| `cdm:severity` | `Risk` | `xsd:decimal` | Combined severity score [0, 1] |
| `cdm:riskLevel` | `Risk` | `xsd:string` | Categorical level: Low / Medium / High / Critical |
| `cdm:acceptability` | `Risk` | `xsd:string` | Acceptable / Unacceptable / ALARP |

---

## The `AssuranceDegradation` Bridge

`AssuranceDegradation` is defined in `warrant-cdm` (not in `warrant-assurance`) because it is a **causal consequence** of a deviation — it belongs to the causal chain, not to the assurance computation machinery. When a `Deviation` is detected:

```
Deviation → cdm:causesAssuranceDegradation → AssuranceDegradation
                                               └── assurance:updatesAssuranceScore → AssuranceScore
```

This keeps the causal semantics in CDM and the scoring computation in the assurance module.

---

## Critical Path Rule

The **only** valid path from an observation to a `Deviation` is:

```
AnalyticalService / Observer
  → obs:producesDetectionEvent → DetectionEvent
      → obs:detectionEventDetects → Deviation
```

**Direct production of a `Deviation` by an `AnalyticalService` is prohibited.** This ensures all deviations are grounded in a recorded detection event and are therefore auditable.

---

## Design Principles

1. **Unified STAMP + safety causal chain.** Both frameworks terminate in `Hazard`, which is the bridge concept. STPA explains causation; the safety chain explains consequence.
2. **Deviation typing over subclassing.** The `hasDeviationType` vocabulary supports uniform querying across all deviation types without class proliferation.
3. **`AssuranceDegradation` as causal signal.** The bridge to `warrant-assurance` is explicit and typed — no implicit side-effects.

---

## Imports

- `warrant-core`
- `warrant-davom`

---

## Downstream Dependents

`warrant-assurance` · `warrant-observation` · `warrant-di` · `warrant-scenario` · `warrant-mitigation`
