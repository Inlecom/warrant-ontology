# `warrant-core` — Core

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/core#`  
**Prefix:** `warrant:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/core`  
**Imports:** (none)  
**Version:** `1.0.0`

---

## Purpose

Shared superclasses, common properties, and controlled vocabularies used by all WARRaNT ontology modules.

**Role:** foundation layer. Abstract superclasses, operational context and the
`OperationalMode` vocabulary, the `VisualisableEntity` marker, the
`CalculationMethod` identity class, and the cross-cutting properties every
other module uses: context scoping (`appliesUnder`), lineage (`derivedFrom`),
identity/version, validity, and configuration governance (`approvedBy`,
`hasApprovalStatus`).

**Design rules**

1. Abstract only: data instances are always of a more specific subclass from a domain module.
2. `VisualisableEntity` lives here so that any module can mark its classes visualisable by importing only core.
3. `OperationalMode` is a closed vocabulary of named individuals (control-authority modes). The methodology's mission phase or operating mode m(t) used to scope weights, thresholds and floors is expressed by pointing `appliesUnder` at an `OperationalMode` or a `VoyageSegment`; the schema does not fix which.
4. Weights, thresholds, floors, damping factors and approved controls are governed configuration: they carry `hasVersion`, `approvedBy`, `hasApprovalStatus` and validity, and change only through a validated, approved process, never through runtime learning.
5. `CalculationMethod` records which external computation produced a result; no formula is encoded in the ontology.

---

## Classes (18)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `warrant:AgentEntity` | — | Agent Entity | Abstract superclass for all human agents: HumanOperator and HumanOperatorRole. Intentionally separate from warrant:OperationalEntity to enforce the principle that human operators are not components. The range of dt:visualises includes this class so that operator roles can be visualised by the Digital Twin. |
| `warrant:CalculationEntity` | — | Calculation Entity | Abstract superclass for entities that store calculation inputs, configured parameters (weights, thresholds, windows, horizons, floors, damping factors), results, and traceability. Numerical computation is always external; the KG stores only the artefacts. Subclasses live in the module that owns the quantity (e.g. assr:AssuranceWeight, di:DIThreshold, di:SupervisionConfiguration, di:DIForecast, assr:AssuranceLevel). |
| `warrant:CalculationMethod` | `warrant:CalculationEntity` | Calculation Method | Identity and version of an externally executed calculation (node dependability score, confidence fusion, typed risk propagation, hierarchical DI aggregation, state assignment, resilience trigger evaluation, response ranking, Assurance Level, Certification Readiness). The KG records which method produced a result; it never encodes the formula itself. Module-specific subclasses (e.g. di:DICalculationMethod) may add parameters. |
| `warrant:ContextEntity` | — | Context Entity | Abstract superclass for operational context elements: voyage segments, operational modes, and environmental conditions. |
| `warrant:EnvironmentalCondition` | `warrant:ContextEntity` | Environmental Condition | A contextual factor that influences deviations, hazards, risks, assurance scores, DI values, and scenario outcomes. Not a vessel component. |
| `warrant:EvidenceEntity` | — | Evidence Entity | Abstract superclass for all observation, measurement, and evidence entities. |
| `warrant:ExternalReference` | — | External Reference | A reference to an external standard, regulation, or guideline (e.g., IMO circular, IACS UR, DNV class notation, EMSA framework). Used to link KG elements to normative requirements without importing their content. |
| `warrant:InfrastructureCondition` | `warrant:EnvironmentalCondition` | Infrastructure Condition |  |
| `warrant:NetworkCoverageCondition` | `warrant:EnvironmentalCondition` | Network Coverage Condition |  |
| `warrant:OperationalContext` | `warrant:ContextEntity` | Operational Context | A description of the operational state or setting in which a vessel function is executed. |
| `warrant:OperationalEntity` | — | Operational Entity | Abstract superclass for all operational entities in a vessel system: components, systems, functions, data flows, and communication links. Human operators are NOT subclasses of this class; use warrant:AgentEntity instead. |
| `warrant:OperationalMode` | `warrant:ContextEntity` | Operational Mode | A controlled vocabulary class for the mode of vessel operation. Named individuals (not subclasses) enumerate the modes. Belongs here in the core/context module, NOT in the CDM module. |
| `warrant:SeaStateCondition` | `warrant:EnvironmentalCondition` | Sea State Condition |  |
| `warrant:TrafficCondition` | `warrant:EnvironmentalCondition` | Traffic Condition |  |
| `warrant:VisibilityCondition` | `warrant:EnvironmentalCondition` | Visibility Condition |  |
| `warrant:VisualisableEntity` | — | Visualisable Entity | Abstract marker class for any ontology entity that may be visualised by the Digital Twin. The range of dt:visualises is constrained to warrant:VisualisableEntity. This class is defined here in the core module — do NOT redefine it in the digital-twin module. |
| `warrant:VoyageSegment` | `warrant:ContextEntity` | Voyage Segment | A leg of a voyage characterised by a specific route segment, transit zone, or operational phase (e.g. port approach, lock transit, open sea). Belongs here in the core/context module, NOT in the CDM module. |
| `warrant:WeatherCondition` | `warrant:EnvironmentalCondition` | Weather Condition |  |

## Controlled vocabularies (named individuals)

### `warrant:OperationalMode`

| Individual | Label | Description |
|---|---|---|
| `warrant:AssistedOperationMode` | Assisted Operation Mode | Vessel is under human control with active decision-support assistance from the Digital Twin or an analytical service. |
| `warrant:AutonomousOperationMode` | Autonomous Operation Mode | Vessel is operating autonomously without active human control. Relevant to LL3 NOVA. |
| `warrant:DegradedOperationMode` | Degraded Operation Mode | One or more vessel functions are operating below normal capability; reduced-dependency fallback procedures are active. |
| `warrant:HandoverMode` | Handover Mode | A transient mode during transfer of control between ROC operator and onboard boatmaster, or between automation and human. Relevant to LL4 Use Case 2 (uncontrolled handover at Kreekraksluizen). |
| `warrant:ManualOperationMode` | Manual Operation Mode | Vessel is under direct manual control by onboard crew. |
| `warrant:RemoteOperationMode` | Remote Operation Mode | Vessel is under control of a remote operator via a Remote Operation Centre (ROC). Relevant to LL4 Seafar ROS. |

## Object properties (2)

| Property | Domain | Range | Description |
|---|---|---|---|
| `warrant:appliesUnder` | `owl:Thing` | `warrant:ContextEntity` | Scopes a configured artefact (attribute weight, aggregation weight, state threshold, DI management floor, supervision configuration, requirement, control) to the operational context in which it is valid: an OperationalMode, a VoyageSegment, or another ContextEntity. Weights, thresholds and floors are configured per vessel and mode/mission phase and are not comparable across contexts; an artefact with no appliesUnder triple is context-independent. |
| `warrant:derivedFrom` | `owl:Thing` | `owl:Thing` | Generic lineage relation: the subject was produced from the object by filtering, correlation, fusion, aggregation, or calculation. Used for health events enriched from other health events, fused attribute values derived from per-source estimates, evidence derived from observations, and calculated values that must retain provenance to their design-time source, analytical model, or runtime observation. Informative alignment: warrant:derivedFrom ≈ prov:wasDerivedFrom. |

## Datatype properties (11)

| Property | Domain | Range | Description |
|---|---|---|---|
| `warrant:approvedBy` | `owl:Thing` | `xsd:string` | The technical or assurance authority (organisation, role, or board) that approved a governed configuration artefact: ontology release, hazard model, threshold set, weight set, management floor, approved control, or claim wording. Together with warrant:hasVersion, warrant:validFrom and warrant:validTo this records that such artefacts change only through a validated, versioned, and approved process rather than through runtime learning. |
| `warrant:hasApprovalStatus` | `owl:Thing` | `xsd:string` | Governance status of a configuration artefact, e.g. PROPOSED, APPROVED, SUPERSEDED. Operational learning may propose a change (PROPOSED); it enters the operational baseline only when APPROVED. |
| `warrant:hasDescription` | `owl:Thing` | `xsd:string` | has description |
| `warrant:hasIdentifier` | `owl:Thing` | `xsd:string` | A stable identifier string for the entity (e.g. VF-RN-001, COMP-GNSS-RX-001). |
| `warrant:hasMaker` | `warrant:OperationalEntity` | `xsd:string` | Manufacturer or vendor name of a physical or software component (e.g. 'FURUNO', 'YOKOGAWA', 'AELER'). Use warrant:hasModel for the model designation and warrant:hasSoftwareVersion for the SW version string. |
| `warrant:hasModel` | `warrant:OperationalEntity` | `xsd:string` | Model or type designation of a component as given by the manufacturer (e.g. 'FMD3300', 'CMZ900D', 'FAR-2228'). Pair with warrant:hasMaker. |
| `warrant:hasName` | `owl:Thing` | `xsd:string` | has name |
| `warrant:hasSoftwareVersion` | `warrant:OperationalEntity` | `xsd:string` | Software or firmware version string as recorded in the equipment cybersecurity inventory (e.g. '2450074-05.12', '0359377-03.02'). Supports vulnerability tracking and patch management queries. |
| `warrant:hasVersion` | `owl:Thing` | `xsd:string` | has version |
| `warrant:validFrom` | `owl:Thing` | `xsd:dateTime` | valid from |
| `warrant:validTo` | `owl:Thing` | `xsd:dateTime` | valid to |

