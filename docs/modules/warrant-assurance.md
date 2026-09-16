# `warrant-assurance` — Assurance (Attribute Scoring and Living Dependability Case)

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/assurance#`  
**Prefix:** `assr:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/assurance`  
**Imports:** `warrant-cdm`, `warrant-core`, `warrant-observation`  
**Version:** `0.10-poc`

---

## Purpose

Attribute scoring and the Living Dependability Case. Attribute scoring: the six dependability attributes (reliability, safety, cybersecurity, resilience, availability, maintainability), per-node attribute values d_i,k(t) with per-source confidence and fusion lineage, mode-dependent attribute weights α_i,k, and the Node Dependability Score ND_i(t) = Σ_k α_i,k·d_i,k(t) stored as assr:AssuranceScore. Living Dependability Case: Requirement, AssuranceClaim (with status), Assumption, Evidence and the traceable chain Evidence → AssuranceClaim → Requirement; EvidenceObligation as the declared reference set for evidence completeness; Nonconformity; AssuranceLevel (EC, EF, EQ, MC, TC); CertificationReadiness (AL, RC, NC); LivingDependabilityCase container. All formulas are metadata only; computation is external and results are written back with their method identity and timestamp.

**Role:** two responsibilities.

*Attribute scoring.* The six dependability attributes, per-node attribute
values d_i,k(t) with per-source confidence and fusion lineage, mode-scoped
attribute weights α, and the Node Dependability Score
ND_i(t) = Σ_k α_i,k·d_i,k(t), stored as `AssuranceScore` (IRI retained; label
"Node Dependability Score").

*Living Dependability Case.* `Requirement`, `AssuranceClaim` (with status),
`Assumption`, `Evidence` and the traceable chain Evidence → AssuranceClaim →
Requirement; `EvidenceObligation` as the declared reference set for evidence
completeness; `Nonconformity`; `AssuranceLevel` (EC, EF, EQ, MC, TC);
`CertificationReadiness` (AL, RC, NC); and the `LivingDependabilityCase`
container.

**Formulas (metadata only, computed externally)**

- Fusion: d_i,k = Σ_s q_i,k,s·d_i,k,s / Σ_s q_i,k,s
- Node score: ND_i = Σ_k α_i,k·d_i,k, α ≥ 0, Σ α = 1
- Assurance Level: AL = ω_EC·EC + ω_EF·EF + ω_EQ·EQ + ω_MC·MC + ω_TC·TC
- Certification Readiness: CR = g(AL, RC, NC), g agreed with the assuring authority

**Design rules**

1. `AssuranceScore` is the node dependability score, not the Assurance Level: the former is operational condition, the latter confidence in the evidence. They must be reported together (`di:isReportedWith`).
2. Attribute values are compared with per-attribute thresholds to assign the attribute-wise operational state (`di:hasAttributeState`); confidence weights fusion and never degrades the value.
3. Claim wording, requirement baseline and acceptance rules are version-controlled; only claim *status* changes at runtime.
4. Evidence completeness is computed against declared `EvidenceObligation`s (PRESENT / MISSING / STALE / UNTRACEABLE), never against whatever data happen to exist.
5. WARRaNT does not define admissible or sufficient evidence; AL and CR are management indicators, not regulatory decisions.
6. Records produced downstream (system DI, triggers, response evaluations and executions) attach to the case through `di:isRecordedIn` and `mit:isRecordedIn`, declared in those modules.

---

## Classes (26)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `assr:Assumption` | `assr:AssuranceEntity` | Assumption | A design-time assumption, scope statement, or context condition on which hazard analyses, controls, and claims rest (e.g. 'GNSS augmentation is available on the route', 'the ROC link latency stays below 300 ms'). Represented explicitly so that its invalidation during operation becomes a monitored condition: a HealthEvent may challenge it (assr:isChallengedBy), its validity status is tracked (assr:hasValidityStatus), and a changed or invalidated assumption may challenge previously supported claims (assr:challengesClaim). Informative alignment: ≈ SACM Assumption / gsn:Assumption. |
| `assr:AssuranceAttribute` | `assr:AssuranceEntity` | Assurance Attribute | A dependability quality dimension: reliability, safety, cybersecurity, resilience, availability, maintainability. |
| `assr:AssuranceAttributeValue` | `assr:AssuranceEntity` | Assurance Attribute Value | The normalised operational value d_i,k(t) in [0,1] of dependability attribute k for node i, measured or estimated against the applicable requirements before the risk penalty. A value may be a single-source estimate (assr:hasValueSource with assr:hasSourceConfidence q_i,k,s: a Node Health Monitor, physical or virtual sensor, analytical model, Digital Twin, or operator observation) or the fused value derived from several such estimates (warrant:derivedFrom the source values). Confidence controls the relative influence of a source in fusion; it is not multiplied into the value. The attribute value is what the Dependability Supervisor compares against the configured attribute thresholds to assign the attribute-wise operational state (di:hasAttributeState). Timestamp: assr:assessedAt; freshness: warrant:validTo. |
| `assr:AssuranceClaim` | `assr:AssuranceEntity` , `warrant:VisualisableEntity` | Assurance Claim | A claim that a requirement is met for a system element or function (e.g. 'navigation integrity is maintained during remote transit'). A claim addresses a Requirement (assr:addressesRequirement), applies to an OperationalEntity (assr:claimAppliesTo), declares the evidence it expects (assr:expectsEvidence), and carries a status (assr:hasClaimStatus) that is updated from evidence and context during operation. The approved claim wording, its requirement baseline and acceptance rules are version-controlled (warrant:hasVersion, warrant:approvedBy) and are never rewritten by runtime data. A claim is revalidated only when the stakeholder-defined evidence and authority conditions are satisfied. Informative alignment: ≈ gsn:Goal / SACM Claim. |
| `assr:AssuranceDegradation` | `assr:AssuranceEntity` | Assurance Degradation | A reduction in assurance score caused by a Deviation, Hazard, or UnsafeControlAction. |
| `assr:AssuranceEntity` | — | Assurance Entity | Abstract superclass for all assurance-related entities. |
| `assr:AssuranceLevel` | `assr:AssuranceEntity` , `warrant:CalculationEntity` , `warrant:VisualisableEntity` | Assurance Level (AL) | Confidence in the evidence supporting the dependability assessment: AL(t) = ω_EC·EC(t) + ω_EF·EF(t) + ω_EQ·EQ(t) + ω_MC·MC(t) + ω_TC·TC(t), where EC is evidence completeness against the declared obligations, EF evidence freshness, EQ evidence quality (validity, confidence, operating-domain coverage, uncertainty, agreement between independent sources), MC monitoring coverage, and TC traceability coverage. The component values, the result, the weight set used (assr:usesAssuranceLevelWeights) and the method identity (assr:usesCalculationMethod) are stored; the calculation is external; timestamp via di:calculatedAt. AL describes confidence in the evidence, not operational condition: it must always be reported together with the system DI (di:isReportedWith). A high DI with low AL is apparently satisfactory operation on weak evidence; a low DI with high AL is a well-supported finding of degradation. Neither changes the attribute-wise operational state. AL is a management indicator, not a regulatory or classification decision. |
| `assr:AssuranceLevelWeightSet` | `assr:AssuranceEntity` , `warrant:CalculationEntity` | Assurance Level Weight Set | The stakeholder-defined weights ω_EC, ω_EF, ω_EQ, ω_MC, ω_TC (non-negative, summing to one) and any mandatory gates used to compute an AssuranceLevel. Controlled configuration: warrant:hasVersion, warrant:approvedBy, warrant:appliesUnder. |
| `assr:AssuranceScore` | `assr:AssuranceEntity` | Node Dependability Score (ND) (alt: Assurance Score) | The intrinsic Node Dependability Score ND_i(t) = Σ_k α_i,k·d_i,k(t): the mode-weighted combination of a node's six attribute values before the explicit scenario-risk penalty. The IRI retains its historical local name (AssuranceScore); the concept is the node dependability score of the WARRaNT methodology and must not be confused with the Assurance Level (assr:AssuranceLevel), which measures confidence in the evidence rather than operational condition. Feeds into the node DI via di:contributesTo (DI_i = clip(ND_i − β_i·R_i)). Computed externally; timestamp via di:calculatedAt. |
| `assr:AssuranceWeight` | `assr:AssuranceEntity` , `warrant:CalculationEntity` | Assurance Weight | The attribute weight α_i,k in the Node Dependability Score. Weights depend on mission phase or operating mode, node criticality and approved operating policy: scope with warrant:appliesUnder, and record warrant:hasVersion, warrant:approvedBy, warrant:validFrom/validTo. They are configured for a defined vessel and mode and controlled rather than learned; consequently neither node scores nor the system DI are comparable across vessels or differently weighted modes. |
| `assr:Availability` | `assr:AssuranceAttribute` | Availability |  |
| `assr:CalculationInput` | `assr:AssuranceEntity` , `warrant:CalculationEntity` | Calculation Input | An input to the external assurance calculation (e.g. a normalised attribute value, weight). |
| `assr:CertificationReadiness` | `assr:AssuranceEntity` , `warrant:CalculationEntity` , `warrant:VisualisableEntity` | Certification Readiness (CR) | An evidence-management indicator, not a certification decision: CR(t) = g(AL(t), RC(t), NC(t)), increasing with the Assurance Level and with regulatory-requirement coverage RC and decreasing with unresolved nonconformities NC. The mapping g, its weights and any acceptance thresholds must be agreed with the relevant assurance, regulatory or classification authority; the KG stores the inputs, the result and the method identity only. |
| `assr:ClaimStatus` | — | Claim Status | Controlled vocabulary for the current evidential status of an AssuranceClaim. Named individuals only. |
| `assr:Cybersecurity` | `assr:AssuranceAttribute` | Cybersecurity |  |
| `assr:Evidence` | `assr:AssuranceEntity` | Evidence | An item of operational or design-time evidence organised by the Living Dependability Case. It supports or challenges one or more AssuranceClaims (assr:supportsClaim, assr:challengesClaim), is sourced from an observation, health event, measurement, virtual-sensor output, operator input, response record, or analytical output (assr:hasEvidenceSource), and carries collection time, validity window (warrant:validFrom/validTo, i.e. freshness), quality (assr:hasEvidenceQuality) and lineage (warrant:derivedFrom). Operator decisions and AI-generated recommendations enter the assurance record as evidence in their own right. Informative alignment: assr:Evidence ≈ gsn:Evidence / SACM Artifact. |
| `assr:EvidenceObligation` | `assr:AssuranceEntity` | Evidence Obligation | A stakeholder-declared expectation that a particular kind of evidence exists, is current, and is traceable for a claim or requirement (e.g. 'a position-integrity measurement not older than 60 s from an independent source'). Obligations form the declared reference set against which evidence completeness EC(t) is computed: EC reports how many obligations are PRESENT (fulfilled by current, traceable evidence), rather than counting whatever data happen to have been collected. An unfulfilled obligation is MISSING; one fulfilled only by evidence outside its validity period is STALE; one fulfilled by evidence whose source cannot be traced is UNTRACEABLE. Obligations do not declare that fulfilling evidence is acceptable; acceptance remains with the stakeholder. |
| `assr:LivingDependabilityCase` | `assr:AssuranceEntity` , `warrant:VisualisableEntity` | Living Dependability Case (LDC) | The assurance layer container for a vessel or system: it extends the design-time dependability case with current operational evidence while preserving the approved baseline (assr:hasBaselineVersion), configuration history and authority boundaries. It consolidates requirements, claims, assumptions, evidence and nonconformities (assr:includes*), the current Assurance Level and Certification Readiness, and the runtime records that downstream modules attach to it: system DI, operational state and resilience triggers (di:isRecordedIn) and evaluated and executed responses with their authority, timing, posture and outcome (mit:isRecordedIn). The LDC maintains the traceable path from Evidence through AssuranceClaim to Requirement continuously rather than only at audit points; it does not determine what evidence an authority must accept. |
| `assr:Maintainability` | `assr:AssuranceAttribute` | Maintainability |  |
| `assr:Nonconformity` | `assr:AssuranceEntity` | Nonconformity | A recorded departure from a requirement (audit finding, unmet regulatory obligation, invalidated control) with a severity and a resolution status. The number and severity of unresolved nonconformities is the NC(t) term of Certification Readiness. |
| `assr:ObligationStatus` | — | Obligation Status | Controlled vocabulary for the fulfilment status of an EvidenceObligation. Named individuals only. |
| `assr:Penalty` | `assr:AssuranceEntity` | Penalty | A quantified penalty applied to an assurance attribute value due to a specific event. |
| `assr:Reliability` | `assr:AssuranceAttribute` | Reliability |  |
| `assr:Requirement` | `assr:AssuranceEntity` | Requirement | A regulatory, stakeholder-declared, or assurance-objective requirement at the top of the traceability chain Evidence → AssuranceClaim → Requirement. Requirements are declared by the assuring stakeholder (operator, flag Administration, classification society, insurer) and may reference the governing standard through assr:hasRequirementSource (→ warrant:ExternalReference). Requirement wording is version-controlled (warrant:hasVersion, warrant:approvedBy) and may be scoped to a context (warrant:appliesUnder). Regulatory-requirement coverage RC(t) for Certification Readiness is computed over requirements whose category is REGULATORY. |
| `assr:Resilience` | `assr:AssuranceAttribute` | Resilience |  |
| `assr:Safety` | `assr:AssuranceAttribute` | Safety |  |

## Controlled vocabularies (named individuals)

### `assr:ClaimStatus`

| Individual | Label | Description |
|---|---|---|
| `assr:CLAIM_CHALLENGED` | CLAIM_CHALLENGED | An evidence item, health event, or invalidated assumption challenges the claim and the challenge has not been resolved. |
| `assr:CLAIM_SUPPORTED` | CLAIM_SUPPORTED | Current evidence supports the claim and no unresolved challenge exists (includes a claim revalidated after a challenge). |
| `assr:CLAIM_UNSUPPORTED` | CLAIM_UNSUPPORTED | No current, valid supporting evidence exists for the claim (e.g. expected evidence missing or stale). |

### `assr:ObligationStatus`

| Individual | Label | Description |
|---|---|---|
| `assr:MISSING` | MISSING | No fulfilling evidence exists. |
| `assr:PRESENT` | PRESENT | Fulfilled by evidence that is current and traceable. |
| `assr:STALE` | STALE | Fulfilling evidence exists but is outside its validity period. |
| `assr:UNTRACEABLE` | UNTRACEABLE | Fulfilling evidence exists but its source or provenance cannot be traced. |

## Object properties (33)

| Property | Domain | Range | Description |
|---|---|---|---|
| `assr:addressesRequirement` | `assr:AssuranceClaim` | `assr:Requirement` | The requirement this claim argues is satisfied. Second link of the chain Evidence → AssuranceClaim → Requirement. |
| `assr:assumptionAppliesTo` | `assr:Assumption` | `warrant:OperationalEntity` ∪ `cdm:CausalEntity` ∪ `assr:AssuranceClaim` ∪ `warrant:ContextEntity` | The element, hazard analysis artefact, claim, or context the assumption underpins. |
| `assr:caseAppliesTo` | `assr:LivingDependabilityCase` | `warrant:OperationalEntity` | The vessel or system of systems this Living Dependability Case is maintained for. |
| `assr:causesAssuranceDegradation` | `cdm:Deviation` ∪ `cdm:Hazard` ∪ `cdm:UnsafeControlAction` | `assr:AssuranceDegradation` | causes assurance degradation |
| `assr:challengesClaim` | `assr:Evidence` ∪ `obs:HealthEvent` ∪ `assr:Assumption` | `assr:AssuranceClaim` | An evidence item, a health event (e.g. GNSS spoofing detected), or a changed/invalidated assumption challenges a previously supported claim, prompting its re-evaluation. |
| `assr:claimAppliesTo` | `assr:AssuranceClaim` | `warrant:OperationalEntity` ∪ `cdm:Control` | The system element, function, or design-time control the claim is about. |
| `assr:derivesFromAssuranceLevel` | `assr:CertificationReadiness` | `assr:AssuranceLevel` | derives from assurance level |
| `assr:expectsEvidence` | `assr:AssuranceClaim` ∪ `assr:Requirement` | `assr:EvidenceObligation` | Declares an obligation that belongs to the reference set for this claim or requirement. |
| `assr:hasAssuranceAttribute` | `warrant:OperationalEntity` | `assr:AssuranceAttribute` | has assurance attribute |
| `assr:hasAssuranceLevel` | `assr:LivingDependabilityCase` | `assr:AssuranceLevel` | The current (latest) Assurance Level of the case; earlier values remain as history with their timestamps. |
| `assr:hasAssuranceScore` | `warrant:OperationalEntity` | `assr:AssuranceScore` | has assurance score |
| `assr:hasAttributeValue` | `assr:AssuranceAttribute` | `assr:AssuranceAttributeValue` | has attribute value |
| `assr:hasCertificationReadiness` | `assr:LivingDependabilityCase` | `assr:CertificationReadiness` | has certification readiness |
| `assr:hasClaimStatus` | `assr:AssuranceClaim` | `assr:ClaimStatus` | Current status from the assr:ClaimStatus vocabulary. Updated from evidence and context at runtime; the claim wording itself is not. |
| `assr:hasEvidenceSource` | `assr:Evidence` | `obs:EvidenceEntity` ∪ `obs:DataSource` | The observation-layer item this evidence is drawn from (a Measurement, HealthEvent, VirtualSensorOutput, HumanObservation, OperatorInput, Status) or the data source that produced it. Raw telemetry stays in the external store; the graph holds identifiers, provenance and interpreted evidential meaning. |
| `assr:hasObligationStatus` | `assr:EvidenceObligation` | `assr:ObligationStatus` | has obligation status |
| `assr:hasPenalty` | `assr:AssuranceDegradation` | `assr:Penalty` | has penalty |
| `assr:hasRequirementSource` | `assr:Requirement` | `warrant:ExternalReference` | The standard, regulation, guideline, or class notation from which the requirement derives (IMO, IACS UR E26/E27, IEC 62443, DNV RP, stakeholder policy). |
| `assr:hasValueSource` | `assr:AssuranceAttributeValue` | `obs:DataSource` | The source s (Node Health Monitor, sensor, virtual sensor, analytical service, Digital Twin, or operator role) that supplied this single-source attribute estimate. A fused value has no direct source; it is warrant:derivedFrom its source values. |
| `assr:hasWeight` | `assr:AssuranceAttribute` | `assr:AssuranceWeight` | has weight |
| `assr:includesAssumption` | `assr:LivingDependabilityCase` | `assr:Assumption` | includes assumption |
| `assr:includesClaim` | `assr:LivingDependabilityCase` | `assr:AssuranceClaim` | includes claim |
| `assr:includesEvidence` | `assr:LivingDependabilityCase` | `assr:Evidence` | includes evidence |
| `assr:includesNonconformity` | `assr:LivingDependabilityCase` | `assr:Nonconformity` | includes nonconformity |
| `assr:includesRequirement` | `assr:LivingDependabilityCase` | `assr:Requirement` | includes requirement |
| `assr:isChallengedBy` | `assr:Assumption` | `obs:HealthEvent` ∪ `assr:Evidence` | The health event or evidence that indicates the assumption may no longer hold. This is how an assumption's invalidation becomes a monitored condition. |
| `assr:isFulfilledBy` | `assr:EvidenceObligation` | `assr:Evidence` | The evidence item(s) currently satisfying this obligation. |
| `assr:relatesToRequirement` | `assr:Nonconformity` | `assr:Requirement` | relates to requirement |
| `assr:supportsClaim` | `assr:Evidence` | `assr:AssuranceClaim` | First link of the chain Evidence → AssuranceClaim → Requirement: this evidence item supports the claim. |
| `assr:updatesAssuranceScore` | `assr:AssuranceDegradation` ∪ `assr:CalculationInput` | `assr:AssuranceScore` | updates assurance score |
| `assr:usesAssuranceLevelWeights` | `assr:AssuranceLevel` | `assr:AssuranceLevelWeightSet` | uses assurance level weights |
| `assr:usesCalculationMethod` | `assr:AssuranceScore` ∪ `assr:AssuranceAttributeValue` ∪ `assr:AssuranceLevel` ∪ `assr:CertificationReadiness` | `warrant:CalculationMethod` | Identity and version of the external method that produced this score, fused value, Assurance Level, or readiness indicator. |
| `assr:wasTriggeredBy` | `assr:AssuranceDegradation` | `cdm:Deviation` ∪ `cdm:Hazard` ∪ `cdm:UnsafeControlAction` | Traceability: the Deviation, Hazard, or UnsafeControlAction that triggered this AssuranceDegradation. |

## Datatype properties (31)

| Property | Domain | Range | Description |
|---|---|---|---|
| `assr:assessedAt` | `assr:AssuranceAttributeValue` | `xsd:dateTime` | Time at which this attribute value was measured, estimated, or fused. |
| `assr:claimStatusUpdatedAt` | `assr:AssuranceClaim` | `xsd:dateTime` | claim status updated at |
| `assr:declaredBy` | `assr:Requirement` ∪ `assr:EvidenceObligation` ∪ `assr:AssuranceLevelWeightSet` | `xsd:string` | The assuring stakeholder (operator, flag Administration, classification society, insurer, project) that declared this requirement, obligation, or weight set. |
| `assr:evidenceCollectedAt` | `assr:Evidence` | `xsd:dateTime` | Time the evidence was collected or generated. Freshness is judged against warrant:validTo and the obligation's validity period. |
| `assr:hasAssuranceLevelValue` | `assr:AssuranceLevel` | `xsd:decimal` | AL(t), the weighted result. |
| `assr:hasAttributeValueNumber` | `assr:AssuranceAttributeValue` | `xsd:decimal` | The normalised attribute value d_i,k(t) in [0,1]; 1 is the best condition. |
| `assr:hasBaselineVersion` | `assr:LivingDependabilityCase` | `xsd:string` | Version of the approved design-time dependability case (claim wording, requirement baseline, model structure, acceptance rules) that this living case extends. Runtime data never rewrites the baseline; changes enter through the governed, versioned approval process. |
| `assr:hasCompletenessWeight` | `assr:AssuranceLevelWeightSet` | `xsd:decimal` | ω_EC |
| `assr:hasEvidenceCompleteness` | `assr:AssuranceLevel` | `xsd:decimal` | EC(t): share of declared evidence obligations that are PRESENT. |
| `assr:hasEvidenceFreshness` | `assr:AssuranceLevel` | `xsd:decimal` | EF(t): currency of the supporting evidence relative to the obligations' validity periods. |
| `assr:hasEvidenceQuality` | `assr:Evidence` | `xsd:decimal` | Quality of this evidence item in [0,1], combining source confidence, validity, operating-domain coverage, uncertainty, and agreement with independent sources. Input to EQ(t). |
| `assr:hasEvidenceQualityValue` | `assr:AssuranceLevel` | `xsd:decimal` | EQ(t): aggregate quality of the supporting evidence. |
| `assr:hasFreshnessWeight` | `assr:AssuranceLevelWeightSet` | `xsd:decimal` | ω_EF |
| `assr:hasMonitoringCoverage` | `assr:AssuranceLevel` | `xsd:decimal` | MC(t): share of relevant nodes and attributes under active monitoring. |
| `assr:hasMonitoringWeight` | `assr:AssuranceLevelWeightSet` | `xsd:decimal` | ω_MC |
| `assr:hasNonconformitySeverity` | `assr:Nonconformity` | `xsd:string` | MINOR, MAJOR, or CRITICAL, as classified by the assuring stakeholder. |
| `assr:hasNonconformitySeverityIndex` | `assr:CertificationReadiness` | `xsd:decimal` | NC(t): severity-weighted measure of unresolved nonconformities as defined by the agreed mapping g. |
| `assr:hasPenaltyValue` | `assr:Penalty` | `xsd:decimal` | has penalty value |
| `assr:hasQualityWeight` | `assr:AssuranceLevelWeightSet` | `xsd:decimal` | ω_EQ |
| `assr:hasReadinessValue` | `assr:CertificationReadiness` | `xsd:decimal` | CR(t) in [0,1]. |
| `assr:hasRequirementCategory` | `assr:Requirement` | `xsd:string` | REGULATORY, STAKEHOLDER, or ASSURANCE_OBJECTIVE. Regulatory-requirement coverage RC(t) is computed over REGULATORY requirements. |
| `assr:hasRequirementCoverage` | `assr:CertificationReadiness` | `xsd:decimal` | RC(t): coverage of applicable regulatory requirements by supported claims, in [0,1]. |
| `assr:hasScoreValue` | `assr:AssuranceScore` | `xsd:decimal` | The computed Node Dependability Score ND_i(t) in [0,1]. Stored by the external calculation service. |
| `assr:hasSourceConfidence` | `assr:AssuranceAttributeValue` | `xsd:decimal` | The explicit confidence q_i,k,s(t) in [0,1] the source attaches to this single-source estimate. Used as the weight in confidence-aware fusion and as an input to evidence quality; never applied as a separate degradation of the value. |
| `assr:hasTraceabilityCoverage` | `assr:AssuranceLevel` | `xsd:decimal` | TC(t): share of claims with a complete, traceable Evidence → Claim → Requirement chain. |
| `assr:hasTraceabilityWeight` | `assr:AssuranceLevelWeightSet` | `xsd:decimal` | ω_TC |
| `assr:hasUnresolvedNonconformityCount` | `assr:CertificationReadiness` | `xsd:integer` | Number of unresolved nonconformities at the time of calculation. |
| `assr:hasValidityPeriod` | `assr:EvidenceObligation` | `xsd:duration` | Maximum age of fulfilling evidence before the obligation becomes STALE. |
| `assr:hasValidityStatus` | `assr:Assumption` | `xsd:string` | VALID, UNDER_REVIEW, or INVALIDATED. |
| `assr:hasWeightValue` | `assr:AssuranceWeight` | `xsd:decimal` | The attribute weight α_i,k (non-negative; the weights of one node under one context sum to one). |
| `assr:isResolved` | `assr:Nonconformity` | `xsd:boolean` | is resolved |

