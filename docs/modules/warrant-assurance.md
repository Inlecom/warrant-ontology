# `warrant-assurance` — Assurance Module

**Namespace:** `https://w3id.org/warrant/assurance#`  
**Prefix:** `assurance:`  
**Status:** Stable  
**Role:** Scoring layer — models the multi-attribute assurance framework that quantifies the dependability profile of operational entities across six assurance dimensions.

---

## Purpose

`warrant-assurance` defines the **assurance scoring framework** used to produce the per-entity assurance scores that feed the Dependability Index (DI) computation. It answers the question: *"Across safety, reliability, cybersecurity, resilience, availability, and maintainability — how assured are we that this entity can perform its function?"*

The assurance score is a weighted combination of attribute values. When a deviation is detected (via `warrant-cdm`), an `AssuranceDegradation` event is generated, which triggers reassessment and updates the relevant `AssuranceScore`. That score then contributes to the DI (see `warrant-di`).

---

## Class Hierarchy

```
AssuranceEntity   (top-level; all assurance concepts are subclasses)
├── AssuranceAttribute    (one of the six assurance dimensions)
│   ├── Reliability
│   ├── Safety
│   ├── Cybersecurity
│   ├── Resilience
│   ├── Availability
│   └── Maintainability
│
├── AssuranceScore        (the aggregate score for an entity at a point in time)
├── AssuranceAttributeValue  (the value of one attribute contributing to the score)
├── AssuranceWeight       (the weight of one attribute in the aggregate)
├── AssuranceDegradation  (event signalling that a score needs to be recalculated)
├── Penalty               (a quantified reduction applied to an attribute due to a deviation)
├── Evidence              (an EvidenceEntity used to support an assurance claim)
└── CalculationInput      (a typed input to the assurance formula)
```

---

## The Assurance Formula

The assurance score for an entity *v* at time *t* is:

> **A_v(t) = Σ βₖ · x_v^(k)**

Where:
- *βₖ* is the `AssuranceWeight` for attribute *k*
- *x_v^(k)* is the `AssuranceAttributeValue` for attribute *k* of entity *v*
- The sum is over the six `AssuranceAttribute` subclasses

**Important:** The computation itself is performed **externally** (Python, SPARQL update, or a dedicated reasoning service). The KG stores:
- The input weights (`AssuranceWeight` individuals)
- The attribute values (`AssuranceAttributeValue` individuals)
- The resulting score (`AssuranceScore` individual)
- The evidence supporting the attribute values (`Evidence` individuals)

The KG is the **ledger**, not the calculator.

---

## Degradation and Update Flow

When a `Deviation` is detected in `warrant-cdm`, the following flow is triggered:

```
Deviation
  → cdm:causesAssuranceDegradation → AssuranceDegradation
      → assurance:updatesAssuranceScore → AssuranceScore
          → assurance:hasAttributeValue → AssuranceAttributeValue (for each dimension)
              ↑
              assurance:applyPenalty → Penalty (if deviation warrants reduction)
```

The `AssuranceDegradation` individual records *which* deviations caused *which* degradation event. This creates a full audit trail from observed deviation to updated score.

---

## Assurance Attributes in Detail

| Attribute Class | What it measures | Example metric |
|---|---|---|
| `Reliability` | Probability of correct operation over time | MTBF, failure rate |
| `Safety` | Freedom from hazardous states | Hazard likelihood, safety constraint violations |
| `Cybersecurity` | Resistance to cyber threats | Vulnerability score, IDS alerts, spoofing events |
| `Resilience` | Ability to recover from disruption | Recovery time, failover success rate |
| `Availability` | Fraction of time the entity is operational | Uptime ratio, MTTR |
| `Maintainability` | Ease and speed of restoration | Mean time to repair, maintenance backlog |

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `assurance:hasAssuranceScore` | `OperationalEntity` | `AssuranceScore` | Links entity to its current score |
| `assurance:updatesAssuranceScore` | `AssuranceDegradation` | `AssuranceScore` | Degradation triggers score update |
| `assurance:causesAssuranceDegradation` | `Deviation` / `Hazard` / `UCA` | `AssuranceDegradation` | Causal link from CDM |
| `assurance:hasAttributeValue` | `AssuranceScore` | `AssuranceAttributeValue` | Score decomposed into attribute values |
| `assurance:hasWeight` | `AssuranceScore` | `AssuranceWeight` | Weight for each attribute |
| `assurance:applyPenalty` | `AssuranceDegradation` | `Penalty` | Penalty applied by this degradation |
| `assurance:supportedByEvidence` | `AssuranceAttributeValue` | `Evidence` | Evidence grounding the attribute value |
| `assurance:contributesTo` | `AssuranceScore` | `DependabilityIndex` | Score feeds DI computation |

---

## Key Datatype Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `assurance:scoreValue` | `AssuranceScore` | `xsd:decimal` | Aggregate score [0, 1] |
| `assurance:attributeValue` | `AssuranceAttributeValue` | `xsd:decimal` | Per-attribute value [0, 1] |
| `assurance:weightValue` | `AssuranceWeight` | `xsd:decimal` | Attribute weight [0, 1]; Σβₖ = 1 |
| `assurance:penaltyValue` | `Penalty` | `xsd:decimal` | Penalty magnitude [0, 1] |
| `assurance:calculatedAt` | `AssuranceScore` | `xsd:dateTime` | Score computation timestamp |
| `assurance:validUntil` | `AssuranceScore` | `xsd:dateTime` | Score expiry (triggers recomputation) |

---

## Relationship to Other Modules

| Module | Relationship |
|---|---|
| `warrant-cdm` | `Deviation`, `Hazard`, `UCA` trigger `AssuranceDegradation` |
| `warrant-observation` | `DetectionEvent` provides the evidence grounding attribute values |
| `warrant-di` | `AssuranceScore` is the primary input to the DI formula |
| `warrant-davom` | `VesselFunction`, `System`, `Component` are the entities scored |

---

## Design Principles

1. **Six fixed attributes.** The six `AssuranceAttribute` subclasses are fixed at the ontology level; new attribute types require ontology revision, not just data addition.
2. **Scores are time-stamped.** Every `AssuranceScore` individual carries `calculatedAt` and optionally `validUntil`, enabling temporal queries and drift detection.
3. **Evidence is mandatory for claims.** `AssuranceAttributeValue` individuals should be linked to at least one `Evidence` individual, tracing the claim to an observation.
4. **Computation is external.** The KG stores inputs and outputs; the formula runs in application code. This avoids coupling the ontology to a specific reasoning engine.

---

## Imports

- `warrant-core`
- `warrant-davom`
- `warrant-cdm`

---

## Downstream Dependents

`warrant-di`
