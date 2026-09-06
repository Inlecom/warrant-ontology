# `warrant-cdm` — Causal Dependability Model

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/cdm#`  
**Prefix:** `cdm:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/cdm`  
**Imports:** `warrant-core`, `warrant-davom`  
**Version:** `0.10-poc`

---

## Purpose

Causal Dependability Model supporting STPA/HAZOP/FMEA and cybersecurity-assessment causal reasoning. Core chain: Deviation → Hazard → Risk → Accident → Loss, with design-time Controls (and their residual risk) mitigating Hazards and ThreatScenarios, and HazardClasses declaring the dependency types over which each class of risk propagates.

**Role:** design-time knowledge layer. The causal chain
Deviation → Hazard → Risk → Accident → Loss, the STPA control loop
(controller, control action, controlled process, feedback, process model,
process-model flaw, unsafe control action), FMEA failure modes with their
ratings, cybersecurity threat scenarios and vulnerabilities, design-time
controls with residual risk, and the hazard classes that govern typed risk
propagation.

**Design rules**

1. `Deviation` is never subclassed; type it with `hasDeviationType` from the ten-value `DeviationType` vocabulary (also allowed on `ProcessModelFlaw`). The deprecated subclasses remain for one minor release.
2. `Risk` carries likelihood and the impact triple (safety, environmental, financial); `hasImpact` is the governing maximum.
3. `Control` is the design-time safeguard; it `mitigates` hazards, threat scenarios or failure modes and carries `hasResidualRisk`. Runtime responses live in `warrant-mitigation` and point back with `mit:implementsControl`.
4. `HazardClass` is a closed vocabulary (CYBER_THREAT, PHYSICAL_FAILURE, DATA_LOSS); each declares its admissible dependency types with `propagatesOverDependencyType`. Typed propagation follows only those types.
5. `ThreatScenario` is modelled with the same principles as a safety hazard; `scen:Threat` is a different thing (a scenario trigger).
6. The bridge to attribute scoring is `assr:causesAssuranceDegradation` (declared in warrant-assurance); `cdm:mayCause` stays inside the causal chain.

---

## Classes (31)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `cdm:Accident` | `cdm:CausalEntity` | Accident | Sudden, unwanted, unplanned event or sequence that has led to harm (Rausand & Haugen, 2020). |
| `cdm:CausalEntity` | — | Causal Entity | Abstract superclass for all entities in the causal dependability chain. |
| `cdm:CausalScenario` | `cdm:CausalEntity` | Causal Scenario |  |
| `cdm:Control` | `cdm:CausalEntity` | Control | A design-time safeguard, control, or mitigation measure identified by HAZOP, FMEA/FMECA, STPA, or the cybersecurity risk assessment and approved as part of the baseline (e.g. redundant positioning source, message authentication at a gateway, bridge access restriction). A Control mitigates one or more Hazards or ThreatScenarios (cdm:mitigates) and is associated with the residual risk that remains once it is in place (cdm:hasResidualRisk) rather than with an assumption of elimination. Design-time controls are what the Living Dependability Case holds claims about; the runtime response that activates or relies on a control is a mit:MitigationAction linked back through mit:implementsControl. Governed configuration: version, approval, and validity are recorded with warrant:hasVersion, warrant:approvedBy, warrant:validFrom/validTo. |
| `cdm:ControlStructure` | `cdm:CausalEntity` | Control Structure |  |
| `cdm:ControlledProcess` | `cdm:CausalEntity` | Controlled Process |  |
| `cdm:Controller` | `cdm:CausalEntity` | Controller |  |
| `cdm:Deviation` | `cdm:CausalEntity` , `warrant:VisualisableEntity` | Deviation | An abnormal condition relative to expected operation or data. Tag with cdm:hasDeviationType using a named cdm:DeviationType individual. Do NOT create Deviation subclasses — that pattern is deprecated. |
| `cdm:DeviationType` | — | Deviation Type | Controlled vocabulary of HAZOP guidewords. Use cdm:hasDeviationType to tag a Deviation individual. |
| `cdm:FailureMode` | `cdm:CausalEntity` | Failure Mode | A specific way in which a component or system can fail (FMEA/FMECA terminology). A FailureMode affects one or more components (cdm:affectsComponent) and produces one or more deviations (cdm:producesDeviation) that propagate into the causal chain. Use cdm:hasDeviationType on the produced Deviation to tag the HAZOP guideword. FMEA ratings are carried as typed integers (cdm:hasSeverityScore, cdm:hasOccurrenceScore, cdm:hasDetectionScore, cdm:hasRiskPriorityNumber) so that existing FMEA worksheets can be loaded as intended inputs to the graph. |
| `cdm:Feedback` | `cdm:CausalEntity` | Feedback |  |
| `cdm:Hazard` | `cdm:CausalEntity` , `warrant:VisualisableEntity` | Hazard | A system state or condition that may lead to an accident or loss. |
| `cdm:HazardClass` | — | Hazard Class | Closed controlled vocabulary of hazard classes used by typed risk propagation. Each class is associated at design time with the admissible set of dependency types through which its mechanism can act (cdm:propagatesOverDependencyType); the in-neighbourhood of a node during propagation contains only nodes connected by a dependency of an admissible type for that class. Risk is propagated per class and aggregated conservatively per node (max) by the external calculation. Adding a class requires ontology revision, as for DependabilityIndexState. |
| `cdm:InconsistentDeviation` **DEPRECATED** | `cdm:Deviation` | Inconsistent Deviation (DEPRECATED) (alt: INCONSISTENT) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:INCONSISTENT instead. Will be removed in v0.2.0. |
| `cdm:LateDeviation` **DEPRECATED** | `cdm:Deviation` | Late Deviation (DEPRECATED) (alt: LATE) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:LATE instead. Will be removed in v0.2.0. |
| `cdm:LessDeviation` **DEPRECATED** | `cdm:Deviation` | Less Deviation (DEPRECATED) (alt: LESS) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:LESS instead. Will be removed in v0.2.0. |
| `cdm:Loss` | `cdm:CausalEntity` | Loss | Unacceptable outcome: property damage, environmental damage, loss of life, or loss of mission. |
| `cdm:MoreDeviation` **DEPRECATED** | `cdm:Deviation` | More Deviation (DEPRECATED) (alt: MORE) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:MORE instead. Will be removed in v0.2.0. |
| `cdm:NoDeviation` **DEPRECATED** | `cdm:Deviation` | No Deviation (DEPRECATED) (alt: NO) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:NO instead. Will be removed in v0.2.0. |
| `cdm:NoisyDeviation` **DEPRECATED** | `cdm:Deviation` | Noisy Deviation (DEPRECATED) (alt: NOISY) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:NOISY instead. Will be removed in v0.2.0. |
| `cdm:ProcessModel` | `cdm:CausalEntity` | Process Model | The controller's internal model of the controlled process state. A ProcessModelFlaw arises when this model diverges from the actual state. |
| `cdm:ProcessModelFlaw` | `cdm:CausalEntity` | Process Model Flaw | A divergence between the controller's process model and actual process state, leading to an unsafe control action. |
| `cdm:Risk` | `cdm:CausalEntity` , `warrant:VisualisableEntity` | Risk | Evaluation of a hazard or threat scenario in terms of likelihood and impact. Impact is assessed separately against safety, environmental, and financial consequences (cdm:hasSafetyImpact, cdm:hasEnvironmentalImpact, cdm:hasFinancialImpact); the governing value recorded in cdm:hasImpact is the most severe of the three. A Risk may be the design-time (inherent) evaluation of a hazard or the residual risk that remains after a Control (cdm:hasResidualRisk). Tag with cdm:hasHazardClass so that runtime risk propagation follows only the admissible dependency types. |
| `cdm:SafetyConstraint` | `cdm:CausalEntity` | Safety Constraint | A constraint that, if violated, may lead to a hazard. |
| `cdm:SpoofedDeviation` **DEPRECATED** | `cdm:Deviation` | Spoofed Deviation (DEPRECATED) (alt: SPOOFED) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:SPOOFED instead. Will be removed in v0.2.0. |
| `cdm:ThreatScenario` | `cdm:CausalEntity` , `warrant:VisualisableEntity` | Threat Scenario | A cybersecurity threat scenario identified at design time through Cyber-HAZOP, STPA-Sec, vulnerability assessment, or threat modelling (e.g. GNSS spoofing, AIS manipulation, denial of service, unauthorised access, malware propagation, compromised software update, adversarial input to an AI-enabled function). Represented with the same principles as a safety Hazard: it exploits a Vulnerability, degrades assets, is evaluated as a Risk (likelihood and the impact triple), is mitigated by Controls, and carries a HazardClass (normally cdm:CYBER_THREAT). Distinct from scen:Threat, which is a trigger for a what-if Scenario. |
| `cdm:UnavailableDeviation` **DEPRECATED** | `cdm:Deviation` | Unavailable Deviation (DEPRECATED) (alt: UNAVAILABLE) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:UNAVAILABLE instead. Will be removed in v0.2.0. |
| `cdm:UnsafeControlAction` | `cdm:CausalEntity` | Unsafe Control Action | A control action that is missing, incorrect, late, early, stopped too soon, or applied too long (STPA terminology). |
| `cdm:UntrustedDeviation` **DEPRECATED** | `cdm:Deviation` | Untrusted Deviation (DEPRECATED) (alt: UNTRUSTED) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:UNTRUSTED instead. Will be removed in v0.2.0. |
| `cdm:Vulnerability` | `cdm:CausalEntity` | Vulnerability | A weakness of a component, system, link, data flow, zone, or procedure that a ThreatScenario can exploit (e.g. an unauthenticated broadcast protocol, an unpatched firmware version recorded in warrant:hasSoftwareVersion, an open update interface). Link to the affected asset with cdm:affectsComponent or cdm:degrades. |
| `cdm:WrongDeviation` **DEPRECATED** | `cdm:Deviation` | Wrong Deviation (DEPRECATED) (alt: WRONG) | DEPRECATED. Use cdm:Deviation with cdm:hasDeviationType cdm:WRONG instead. Will be removed in v0.2.0. |

## Controlled vocabularies (named individuals)

### `cdm:DeviationType`

| Individual | Label | Description |
|---|---|---|
| `cdm:INCONSISTENT` | INCONSISTENT | Conflicting or incoherent data from multiple sources. |
| `cdm:LATE` | LATE | Later than expected. |
| `cdm:LESS` | LESS | Less than intended quantity, flow, or signal. |
| `cdm:MORE` | MORE | More than intended quantity, flow, or signal. |
| `cdm:NO` | NO | No flow, no signal, function absent. |
| `cdm:NOISY` | NOISY | Excessive noise or degraded signal quality. |
| `cdm:SPOOFED` | SPOOFED | Data injected or manipulated by an adversary (cyberattack). |
| `cdm:UNAVAILABLE` | UNAVAILABLE | Component, service, or signal unavailable. |
| `cdm:UNTRUSTED` | UNTRUSTED | Source, identity, or integrity cannot be verified. |
| `cdm:WRONG` | WRONG | Wrong direction, content, or target. |

### `cdm:HazardClass`

| Individual | Label | Description |
|---|---|---|
| `cdm:CYBER_THREAT` | CYBER_THREAT | Cyber threats and attacks. Propagates over DATA and CONTROL dependencies (and CYBER paths and conduits), never over PHYSICAL dependencies. |
| `cdm:DATA_LOSS` | DATA_LOSS | Loss, unavailability, or corruption of a data product (e.g. position, heading, context data). Propagates over DATA and FUNCTIONAL dependencies. |
| `cdm:PHYSICAL_FAILURE` | PHYSICAL_FAILURE | Mechanical, thermal, electrical, or structural failure. Propagates over PHYSICAL and FUNCTIONAL dependencies. |

## Object properties (26)

| Property | Domain | Range | Description |
|---|---|---|---|
| `cdm:actsOn` | `davom:ControlAction` | `cdm:ControlledProcess` | acts on |
| `cdm:affectsComponent` | `cdm:FailureMode` ∪ `cdm:Vulnerability` | `davom:Component` | Links a FailureMode or Vulnerability to the component(s) it degrades, puts out of service, or exposes. Range is davom:Component; subclasses (SensorComponent, SoftwareComponent, etc.) are valid. |
| `cdm:degrades` | `cdm:Hazard` ∪ `cdm:Deviation` ∪ `cdm:ThreatScenario` ∪ `cdm:Vulnerability` | `davom:Component` ∪ `davom:System` ∪ `davom:VesselFunction` ∪ `davom:DataFlow` ∪ `davom:CommunicationLink` ∪ `davom:SecurityZone` | Links a hazard, deviation, threat scenario, or vulnerability to the assets it degrades or exposes: components, systems, functions, data flows, communication links (including conduits), or security zones. |
| `cdm:exploits` | `cdm:ThreatScenario` | `cdm:Vulnerability` | exploits |
| `cdm:hasDeviationType` | `cdm:Deviation` ∪ `cdm:ProcessModelFlaw` | `cdm:DeviationType` | Tags a Deviation individual (or a ProcessModelFlaw, whose divergence from reality is itself a guideword-typed condition, typically WRONG or LATE) with a HAZOP guideword from the cdm:DeviationType controlled vocabulary. |
| `cdm:hasEnvironmentalCondition` | `cdm:Risk` | `warrant:EnvironmentalCondition` | has environmental condition |
| `cdm:hasHazardClass` | `cdm:Hazard` ∪ `cdm:ThreatScenario` ∪ `cdm:Risk` ∪ `cdm:FailureMode` | `cdm:HazardClass` | Assigns the hazard class that governs how the risk attached to this hazard, threat scenario, failure mode, or risk propagates through the dependency graph. |
| `cdm:hasOperationalContext` | `cdm:CausalEntity` | `warrant:ContextEntity` | has operational context |
| `cdm:hasResidualRisk` | `cdm:Control` | `cdm:Risk` | The Risk that remains once this Control is in place. The design-time assessment iterates until residual risk meets the stated objectives; the same quantity is then tracked by monitoring during operation. |
| `cdm:influences` | `warrant:EnvironmentalCondition` | `cdm:Risk` | influences |
| `cdm:isCriticalUnder` | `cdm:Hazard` | `warrant:EnvironmentalCondition` | is critical under |
| `cdm:isEvaluatedAs` | `cdm:Hazard` ∪ `cdm:ThreatScenario` | `cdm:Risk` | Links a Hazard or ThreatScenario to its risk evaluation (likelihood and impact triple). |
| `cdm:isPerformedUnder` | `davom:ControlAction` | `warrant:OperationalMode` | is performed under |
| `cdm:issues` | `cdm:Controller` | `davom:ControlAction` | issues |
| `cdm:mayCause` | `cdm:Deviation` ∪ `cdm:ProcessModelFlaw` ∪ `cdm:UnsafeControlAction` | `cdm:Hazard` ∪ `cdm:UnsafeControlAction` | Causal propagation within the CDM chain. The link from a Deviation, Hazard, or UnsafeControlAction to an assr:AssuranceDegradation is expressed by assr:causesAssuranceDegradation (declared in warrant-assurance, which imports this module), not by this property. |
| `cdm:mayLeadTo` | `cdm:Hazard` ∪ `cdm:UnsafeControlAction` | `cdm:Accident` ∪ `cdm:Hazard` | may lead to |
| `cdm:mitigates` | `cdm:Control` | `cdm:Hazard` ∪ `cdm:ThreatScenario` ∪ `cdm:FailureMode` | A design-time Control reduces the likelihood or impact of a Hazard, ThreatScenario, or FailureMode. The remaining exposure is recorded with cdm:hasResidualRisk. |
| `cdm:modifiesImpactOf` | `warrant:EnvironmentalCondition` | `cdm:Risk` | modifies impact of |
| `cdm:modifiesLikelihoodOf` | `warrant:EnvironmentalCondition` | `cdm:Risk` | modifies likelihood of |
| `cdm:prevents` | `cdm:SafetyConstraint` | `cdm:Hazard` | prevents |
| `cdm:producesDeviation` | `cdm:FailureMode` | `cdm:Deviation` | Links a FailureMode to the Deviation(s) it generates, connecting FMEA failure mode analysis to the HAZOP/STPA causal chain. |
| `cdm:propagatesOverDependencyType` | `cdm:HazardClass` | `davom:DependencyType` | Declares, per hazard class, the admissible dependency types through which that class of risk can act. Declared in the ontology at design time, not inferred at runtime. This restriction is what distinguishes typed propagation from a single weighted adjacency. |
| `cdm:providesFeedback` | `cdm:ControlledProcess` | `cdm:Feedback` | provides feedback |
| `cdm:realises` | `cdm:Accident` | `cdm:Loss` | realises |
| `cdm:updates` | `cdm:Feedback` | `cdm:ProcessModel` | updates |
| `cdm:wasObservedUnder` | `cdm:Deviation` | `warrant:OperationalMode` | was observed under |

## Datatype properties (12)

| Property | Domain | Range | Description |
|---|---|---|---|
| `cdm:hasAcceptability` | `cdm:Risk` | `xsd:string` | has acceptability |
| `cdm:hasDetectionScore` | `cdm:FailureMode` | `xsd:integer` | FMEA detection rating (D): higher means harder to detect before effect. |
| `cdm:hasEnvironmentalImpact` | `cdm:Risk` | `xsd:decimal` | Impact on the environment (pollution, emissions), normalised to [0,1]. |
| `cdm:hasFinancialImpact` | `cdm:Risk` | `xsd:decimal` | Financial and operational impact (loss of mission, damage, liability), normalised to [0,1]. |
| `cdm:hasImpact` | `cdm:Risk` | `xsd:decimal` | Governing impact value: the most severe of cdm:hasSafetyImpact, cdm:hasEnvironmentalImpact, and cdm:hasFinancialImpact when the triple is recorded; otherwise the single assessed impact. |
| `cdm:hasLikelihood` | `cdm:Risk` | `xsd:decimal` | has likelihood |
| `cdm:hasOccurrenceScore` | `cdm:FailureMode` | `xsd:integer` | FMEA occurrence/probability rating (O). |
| `cdm:hasRiskLevel` | `cdm:Risk` | `xsd:string` | has risk level |
| `cdm:hasRiskPriorityNumber` | `cdm:FailureMode` | `xsd:integer` | FMEA risk priority number (RPN) as recorded in the worksheet. Stored, not computed, by the KG. |
| `cdm:hasSafetyImpact` | `cdm:Risk` | `xsd:decimal` | Impact on safety of life and the vessel, normalised to [0,1]. |
| `cdm:hasSeverity` | `cdm:Risk` | `xsd:decimal` | has severity |
| `cdm:hasSeverityScore` | `cdm:FailureMode` | `xsd:integer` | FMEA severity rating (S) of the failure mode's effect. |

