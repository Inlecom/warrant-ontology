# `warrant-di` — Dependability Index and Supervision

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/dependability-index#`  
**Prefix:** `di:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/dependability-index`  
**Imports:** `warrant-assurance`, `warrant-cdm`, `warrant-core`, `warrant-davom`, `warrant-observation`  
**Version:** `0.10-poc`

---

## Purpose

DI module: the Dependability Supervisor's outputs and configuration. Node-level DI with typed, per-hazard-class risk propagation (PropagatedRisk, RiskPropagationEdge, RiskPropagationParameter), hierarchical aggregation (DIWeight, aggregatesInto, SystemDependabilityIndex), attribute-wise operational state (DependabilityIndexState named individuals, DIThreshold per node and attribute, hasAttributeState), resilience triggers (ResilienceTrigger, ResilienceTriggerType, SupervisionConfiguration), DI forecasts (DIForecast, produced by the Digital Twin or a predictive service), calculation methods, and update events. All computation is external; the KG stores inputs, configured parameters, results and audit events.

**Role:** the Dependability Supervisor's outputs and configuration. Node and
system Dependability Index, typed per-hazard-class risk propagation,
hierarchical aggregation, attribute-wise operational state and its thresholds,
resilience triggers and their configuration, DI forecasts, calculation methods
and update events.

**Formulas (metadata only, computed externally)**

- Typed propagation: R_i^{h,(r+1)} = clip(R_i,0^h + ρ_h Σ_j w_j,i^h R_j^{h,(r)}, 0, 1), iterated to a fixed point over dependencies admissible for class h
- Node risk: R_i = max_h R_i^h; node DI: DI_i = clip(ND_i − β_i·R_i, 0, 1)
- Hierarchy: DI_p = Σ_{i∈ch(p)} γ_p,i·DI_i, recursively to DI_sys
- State: per attribute from τ^D > τ^C > τ^F > τ^U; S(t) = max over critical nodes and attributes
- Trigger: T_res = T_attr ∨ T_trend ∨ T_pred; margin MR = DI_sys − φ_DI

**Design rules**

1. `DependabilityIndexState` (label "Operational State") has exactly five named individuals: Normal ≺ Degraded ≺ Critical ≺ Failed ≺ Unsafe. Subclassing is prohibited.
2. **State is attribute-wise.** It is assigned from attribute values against `DIThreshold`s and reported with the index (`hasDIState`, `hasAttributeState`); the DI value never determines it. A single cybersecurity attribute breach moves the state out of Normal even when the composite is high.
3. The DI is a management-oriented composite: its value lies in its trend and its decomposition through the graph; absolute values are not comparable across vessels or modes.
4. `RiskPropagationEdge` is typed by hazard class and mirrors a `davom:Dependency` whose canonical type must be admissible for that class. Damping and tolerance live in `RiskPropagationParameter`.
5. `DIWeight` is reified (parent, child, value, context) so that `aggregatesInto` can be recursive and mode-dependent; `contributesTo` links a node score to its DI only.
6. `DIForecast` lives here (not in the DT module) so the Supervisor's predictive trigger and REDS can consume forecasts without importing warrant-digital-twin; the twin produces them (`dt:producesForecast`, `forecastProducedBy`).
7. State, trigger and DI are reported together, and DI_sys always with the Assurance Level (`isReportedWith`); they are recorded in the Living Dependability Case (`isRecordedIn`).

---

## Classes (17)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `di:DICalculationMethod` | `di:DependabilityEntity` , `warrant:CalculationMethod` | DI Calculation Method | Metadata identifying the external method and version that produced a DI, propagated risk, forecast, or update (formula family, aggregation operator, convergence settings). Numerical computation is external; this stores method identity only. |
| `di:DIForecast` | `di:DependabilityEntity` , `warrant:CalculationEntity` , `warrant:VisualisableEntity` | Dependability Index Forecast | A predicted value of a node or system DI over a horizon, produced by the Digital Twin's predictive simulation, a what-if scenario execution, or a predictive analytical service (di:forecastProducedBy → obs:DataSource; the Digital Twin is declared a DataSource in warrant-digital-twin). Two uses: (1) the Supervisor's anticipatory trigger T_pred, which fires when the forecast minimum over the planning horizon falls below the configured management floor (di:triggeredByForecast); (2) the expected effect E[DI_sys(t+Δt) \| u] of a candidate response u evaluated by REDS (mit:hasExpectedIndex). The forecast lives in this module so that both consumers reference a DI-module class and no module imports warrant-digital-twin. |
| `di:DIThreshold` | `di:DependabilityEntity` , `warrant:CalculationEntity` | Attribute State Threshold (alt: DI Threshold) | The severity thresholds τ^D > τ^C > τ^F > τ^U for one attribute (di:thresholdAppliesToAttribute) at one node (di:thresholdAppliesToNode), against which the attribute value d_i,k(t) is compared to assign its operational state: Normal if d ≥ τ^D (di:hasNormalMinimum), Degraded down to τ^C (di:hasCriticalThreshold), Critical down to τ^F (di:hasFailedThreshold), Failed down to τ^U (di:hasUnsafeThreshold), Unsafe below. Thresholds are approved, versioned configuration per vessel and mode (warrant:appliesUnder, warrant:hasVersion, warrant:approvedBy). The former DI-value bounds (di:hasLowerThreshold, di:hasUpperThreshold, attached to a state via di:hasThreshold) are deprecated: the DI does not determine the state. |
| `di:DIUpdateEvent` | `di:DependabilityEntity` | DI Update Event | Audit record of a DI value being recalculated by the Dependability Supervisor: which index was updated (di:updatesIndex), previous and new value, the health event or assurance degradation that triggered the recalculation (di:updateTriggeredBy), the method used and the supervisor that performed it. Timestamp via di:calculatedAt. One record per recalculation supports drift analysis and the audit trail from evidence to index. |
| `di:DIWeight` | `di:DependabilityEntity` , `warrant:CalculationEntity` | DI Aggregation Weight | The reified hierarchical aggregation weight γ_p,i^{m(t)} of child index i (di:weightChild) within parent index p (di:weightParent): DI_p = Σ_{i ∈ ch(p)} γ_p,i·DI_i, with the weights of one parent under one context non-negative and summing to one. Mode-dependent controlled configuration: warrant:appliesUnder, warrant:hasVersion, warrant:approvedBy. Reified so that the same child may carry different weights under different parents or modes. |
| `di:DependabilityEntity` | — | Dependability Entity | Abstract superclass for all DI-related entities. |
| `di:DependabilityIndex` | `di:DependabilityEntity` , `warrant:VisualisableEntity` | Dependability Index | Node-level DI for any node of the declared hierarchy (component, subsystem, function, system, or vessel): DI_i(t) = clip(ND_i(t) − β_i·R_i(t), 0, 1), where ND_i is the Node Dependability Score (assr:AssuranceScore via di:contributesTo) and R_i the aggregated propagated risk. Computed externally; inputs, weights and result stored in the KG with timestamp and method identity. The DI is a management-oriented composite: its primary value lies in its trend and in its decomposition through the graph (contributing attributes, source evidence, local hazards, typed dependency paths). It does not determine the operational state (di:hasDIState), which is assigned attribute-wise; the same DI value may accompany different states. Absolute values are not comparable across vessels or differently weighted modes. |
| `di:DependabilityIndexState` | `di:DependabilityEntity` | Operational State (alt: Dependability Index State) | The five-valued operational state vocabulary (Normal ≺ Degraded ≺ Critical ≺ Failed ≺ Unsafe) used at three levels: per attribute value (di:hasAttributeState on assr:AssuranceAttributeValue), per node and per system (di:hasDIState on DependabilityIndex and SystemDependabilityIndex). State is assigned attribute-wise from the configured thresholds (di:DIThreshold): Normal can be asserted only when every relevant attribute meets its Normal minimum; a node's or the system's state is the most severe attribute state across its (critical) nodes and attributes. The DI is reported alongside the state and never used to derive it, so a single cybersecurity attribute breach moves the state out of Normal even when the weighted composite remains high. The class name is retained for compatibility; the label reflects the semantics. MUST be represented as the five named individuals below. Subclassing DependabilityIndexState is PROHIBITED. |
| `di:DependabilityIndexValue` | `di:DependabilityEntity` | Dependability Index Value |  |
| `di:DependabilitySupervisor` | `obs:AnalyticalService` | Dependability Supervisor | The runtime service that combines the attribute assessments produced by Node Health Monitors (confidence-aware fusion), performs typed risk propagation over the graph, calculates node and system DI values, assigns the operational state from the attribute vector, monitors the DI trend, and raises resilience triggers. It computes system trustworthiness; it does not rank responses (mit:DecisionSupportService) or act (mit:ResilienceSupervisor). Modelled as an AnalyticalService subclass so that indices, states, triggers and update events carry provenance (di:performedBy, di:raisedBy). |
| `di:PropagatedRisk` | `di:DependabilityEntity` | Propagated Risk | The per-hazard-class propagated risk at a node after the fixed-point iteration: R_i^h(t) (di:hasPropagatedRiskValue) together with the local or residual term R_i,0^h(t) it started from (di:hasLocalRiskValue) and the hazard class h (di:forHazardClass). A node holds one PropagatedRisk per hazard class that can reach it; the node's aggregated risk R_i = max_h R_i^h is recorded on the DependabilityIndex (di:hasAggregatedRiskValue). |
| `di:ResilienceTrigger` | `di:DependabilityEntity` , `warrant:VisualisableEntity` | Resilience Trigger | A recorded firing of the resilience criterion T_res = T_attr ∨ T_trend ∨ T_pred by the Dependability Supervisor. Its type (di:hasTriggerType) records why diagnosis and resilience evaluation were initiated: an attribute breached its Normal minimum (di:triggeredByAttributeValue), the system DI declined persistently (di:triggeredByIndex), or a forecast predicted a floor crossing (di:triggeredByForecast). Any one term initiates the Knowledge Graph query and REDS evaluation (mit:ResponseEvaluation mit:respondsToTrigger); the query result, not the DI value alone, establishes the affected nodes, causes, controls and candidate responses. A trigger is recorded in the Living Dependability Case together with the state and DI. |
| `di:ResilienceTriggerType` | — | Resilience Trigger Type | Closed controlled vocabulary of the three terms of the resilience criterion. Named individuals only. |
| `di:RiskPropagationEdge` | `di:DependabilityEntity` | Risk Propagation Edge | A reified, typed propagation edge from upstream index j (di:propagationSource) to downstream index i (di:propagationTarget) carrying the weight w_j,i^h for hazard class h (di:forHazardClass, di:hasRiskPropagationWeight). It mirrors a structural davom:Dependency (di:mirrorsDependency) whose davom:hasDependencyType must be admissible for h; the edge exists only for admissible (dependency type, hazard class) pairs. Direction follows the dependency: davom:dependencySource → davom:dependencyTarget corresponds to di:propagationSource → di:propagationTarget; a bidirectional dependency is mirrored by two edges. |
| `di:RiskPropagationParameter` | `di:DependabilityEntity` , `warrant:CalculationEntity` | Risk Propagation Parameter | Controlled, versioned propagation parameters for one hazard class (di:forHazardClass) under one context: the damping factor ρ_h (di:hasDampingFactor, 0 ≤ ρ_h < 1; convergence also requires the spectral radius condition, checked externally) and the stopping tolerance (di:hasConvergenceTolerance). Derived from design-time hazard, asset, interface and dependency analyses and calibrated with Living Lab evidence only through controlled validation and change management (warrant:appliesUnder, warrant:hasVersion, warrant:approvedBy). |
| `di:SupervisionConfiguration` | `di:DependabilityEntity` , `warrant:CalculationEntity` | Supervision Configuration | The vessel- and mode-specific controlled parameters of the resilience criterion: trend window W (di:hasTrendWindow), sustained-decline slope threshold ε_W (di:hasTrendSlopeThreshold), prediction horizon T_p (di:hasPredictionHorizon), and DI management floor φ_DI (di:hasManagementFloor). Versioned and approved (warrant:hasVersion, warrant:approvedBy, warrant:validFrom/validTo), scoped by warrant:appliesUnder. If vessel mode or weights change, the trend window is restarted or the series rebased so that a configuration change is not mistaken for degradation. |
| `di:SystemDependabilityIndex` | `di:DependabilityEntity` , `warrant:VisualisableEntity` | System Dependability Index | Top-level DI_sys(t) of a vessel or system of systems, obtained by recursive hierarchical aggregation of the node indices that di:aggregatesInto it. Carries the system operational state S(t) (di:hasDIState, the most severe attribute state across critical nodes), the trend slope over the configured window (di:hasTrendSlope), the resilience margin to the configured management floor (di:hasResilienceMargin), the Assurance Level it must be reported with (di:isReportedWith), and the Living Dependability Case it is recorded in (di:isRecordedIn). State, trigger and DI are always reported together. |

## Controlled vocabularies (named individuals)

### `di:DependabilityIndexState`

| Individual | Label | Description |
|---|---|---|
| `di:CriticalState` | Critical | The most severe relevant attribute is below its Critical threshold but at or above its Failed threshold. Response: authorised mitigation and preservation of a fail-safe option. |
| `di:DegradedState` | Degraded | The most severe relevant attribute is below its Normal minimum but at or above its Critical threshold. Response: increased monitoring and confirmation of a fail-operational option. |
| `di:FailedState` | Failed | The most severe relevant attribute is below its Failed threshold but at or above its Unsafe threshold. Response: failover or transition to the fail-safe branch. |
| `di:NormalState` | Normal | Every relevant attribute meets its Normal minimum threshold (conjunction across the attribute vector). Response: routine monitoring. |
| `di:UnsafeState` | Unsafe | The most severe relevant attribute is below its Unsafe threshold. Response: the applicable emergency procedure. |

### `di:ResilienceTriggerType`

| Individual | Label | Description |
|---|---|---|
| `di:ATTRIBUTE_BREACH` | ATTRIBUTE_BREACH | T_attr: some relevant attribute value fell below its Normal minimum. Implements the ontology's definition of Normal and is independent of the aggregate DI. |
| `di:PREDICTED_FLOOR_CROSSING` | PREDICTED_FLOOR_CROSSING | T_pred: a Digital Twin or predictive forecast places the system DI below the configured management floor within the planning horizon (anticipatory warning before an observed breach). |
| `di:SUSTAINED_DECLINE` | SUSTAINED_DECLINE | T_trend: the system DI showed a negative slope of at least ε_W sustained over the configured window W (DI used as a trend signal). |

## Object properties (31)

| Property | Domain | Range | Description |
|---|---|---|---|
| `di:aggregatesInto` | `di:DependabilityIndex` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | Hierarchical aggregation: this child index contributes to the parent index of the enclosing node, with the weight γ_p,i recorded in a di:DIWeight. Replaces the former misuse of di:contributesTo between indices. |
| `di:appliesTo` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | `warrant:OperationalEntity` | The node this index characterises: a component, subsystem, function, system, or vessel (any operational entity in the declared hierarchy). |
| `di:configurationAppliesTo` | `di:SupervisionConfiguration` ∪ `di:RiskPropagationParameter` | `warrant:OperationalEntity` | The vessel or system for which this configuration was approved. |
| `di:contributesTo` | `assr:AssuranceScore` | `di:DependabilityIndex` | The Node Dependability Score ND_i (assr:AssuranceScore) that is the intrinsic input to this node's DI. For index-to-index hierarchical aggregation use di:aggregatesInto, not this property. |
| `di:contributesToSystem` | `di:DependabilityIndex` | `di:SystemDependabilityIndex` | A node DI aggregates directly into the system-level DI_sys (the top of the hierarchy). (sub-property of `di:aggregatesInto`) |
| `di:forHazardClass` | `di:PropagatedRisk` ∪ `di:RiskPropagationEdge` ∪ `di:RiskPropagationParameter` | `cdm:HazardClass` | The hazard class h to which this propagated-risk record, propagation edge, or parameter set applies. |
| `di:forecastProducedBy` | `di:DIForecast` | `obs:DataSource` | Provenance of the forecast: the Digital Twin, scenario engine, or predictive analytical service that produced it. |
| `di:forecastsIndex` | `di:DIForecast` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | forecasts index |
| `di:hasAttributeState` | `assr:AssuranceAttributeValue` | `di:DependabilityIndexState` | The local operational state s_i,k(t) assigned to one attribute value by comparing it with the node's threshold set for that attribute. Node and system states are the maximum over these. |
| `di:hasDIState` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | `di:DependabilityIndexState` | The operational state reported with this node or system index. Assigned attribute-wise (the most severe attribute state across the node's, or the critical nodes', attributes); NOT derived from the DI value. The property name is retained for compatibility. |
| `di:hasPropagatedRisk` | `di:DependabilityIndex` | `di:PropagatedRisk` | Associates the node DI with its per-hazard-class PropagatedRisk records R_i^h(t). |
| `di:hasThreshold` **DEPRECATED** | `di:DependabilityIndexState` | `di:DIThreshold` | DEPRECATED. Attached DI-value bounds to a state, implying that the state is derived from the DI. Thresholds now apply per attribute and node (di:thresholdAppliesToAttribute, di:thresholdAppliesToNode) with the four ordered values. Will be removed in the next minor release. |
| `di:hasTriggerType` | `di:ResilienceTrigger` | `di:ResilienceTriggerType` | has trigger type |
| `di:isRecordedIn` | `di:SystemDependabilityIndex` ∪ `di:DependabilityIndex` ∪ `di:ResilienceTrigger` ∪ `di:DIUpdateEvent` | `assr:LivingDependabilityCase` | Records this index, state, trigger, or update in the Living Dependability Case. |
| `di:isReportedWith` | `di:SystemDependabilityIndex` | `assr:AssuranceLevel` | The Assurance Level computed for the same reporting instant. The system DI (operational condition) and the AL (confidence in the evidence) must always be reported together. |
| `di:mirrorsDependency` | `di:RiskPropagationEdge` | `davom:Dependency` | The structural davom:Dependency this propagation edge is derived from. Its davom:hasDependencyType must be admissible for the edge's hazard class; its davom:hasDependencyWeight is the basis of the edge's propagation weight. |
| `di:performedBy` | `di:DIUpdateEvent` ∪ `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | `di:DependabilitySupervisor` | The Dependability Supervisor instance that computed this index or update. |
| `di:propagationSource` | `di:RiskPropagationEdge` | `di:DependabilityIndex` | The upstream DI node j in the propagation edge j→i. |
| `di:propagationTarget` | `di:RiskPropagationEdge` | `di:DependabilityIndex` | The downstream DI node i in the propagation edge j→i. |
| `di:raisedBy` | `di:ResilienceTrigger` | `di:DependabilitySupervisor` | raised by |
| `di:thresholdAppliesToAttribute` | `di:DIThreshold` | `assr:AssuranceAttribute` | threshold applies to attribute |
| `di:thresholdAppliesToNode` | `di:DIThreshold` | `warrant:OperationalEntity` | threshold applies to node |
| `di:triggeredByAttributeValue` | `di:ResilienceTrigger` | `assr:AssuranceAttributeValue` | For ATTRIBUTE_BREACH: the attribute value(s) that fell below their Normal minimum. |
| `di:triggeredByForecast` | `di:ResilienceTrigger` | `di:DIForecast` | For PREDICTED_FLOOR_CROSSING: the forecast that predicted the floor crossing. |
| `di:triggeredByIndex` | `di:ResilienceTrigger` | `di:SystemDependabilityIndex` ∪ `di:DependabilityIndex` | For SUSTAINED_DECLINE: the index whose trend breached the configured slope. |
| `di:updateTriggeredBy` | `di:DIUpdateEvent` | `obs:HealthEvent` ∪ `assr:AssuranceDegradation` ∪ `assr:AssuranceAttributeValue` | The health event, assurance degradation, or new attribute assessment that caused this recalculation. |
| `di:updatesIndex` | `di:DIUpdateEvent` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | updates index |
| `di:usesCalculationMethod` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` ∪ `di:PropagatedRisk` ∪ `di:DIForecast` ∪ `di:DIUpdateEvent` | `di:DICalculationMethod` | uses calculation method |
| `di:usesConfiguration` | `di:ResilienceTrigger` ∪ `di:SystemDependabilityIndex` ∪ `di:DependabilitySupervisor` | `di:SupervisionConfiguration` | The supervision configuration (window, slope threshold, horizon, floor) in force when the trigger was evaluated or the margin computed. |
| `di:weightChild` | `di:DIWeight` | `di:DependabilityIndex` | The child index i ∈ ch(p) this weight applies to. |
| `di:weightParent` | `di:DIWeight` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | The parent index p whose aggregation this weight belongs to. |

## Datatype properties (33)

| Property | Domain | Range | Description |
|---|---|---|---|
| `di:calculatedAt` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` ∪ `di:PropagatedRisk` ∪ `di:DIUpdateEvent` ∪ `assr:AssuranceScore` ∪ `assr:AssuranceLevel` ∪ `assr:CertificationReadiness` | `xsd:dateTime` | Timestamp of the external calculation that produced this value. Every calculated value retains its timestamp. |
| `di:forecastIssuedAt` | `di:DIForecast` | `xsd:dateTime` | forecast issued at |
| `di:forecastValidAt` | `di:DIForecast` | `xsd:dateTime` | The future instant the forecast value refers to. |
| `di:hasAggregatedRiskValue` | `di:DependabilityIndex` | `xsd:decimal` | R_i(t) = max_h R_i^h(t) (or another configured aggregator recorded in the method): the node's conservative aggregate over hazard classes that enters DI_i = clip(ND_i − β_i·R_i). |
| `di:hasAggregationOperator` | `di:DICalculationMethod` | `xsd:string` | The operator used to aggregate per-hazard-class risk at a node: MAX (default, conservative) or another validated aggregator where the hazard model supports accumulation. |
| `di:hasAggregationWeightValue` | `di:DIWeight` | `xsd:decimal` | γ_p,i: non-negative; the weights of one parent under one context sum to one. |
| `di:hasBetaWeight` | `di:DependabilityIndex` | `xsd:decimal` | The risk sensitivity coefficient β_i for this node in DI_i = clip(ND_i − β_i·R_i, 0, 1). Configured so that the risk penalty does not duplicate degradation already embedded in an attribute value. |
| `di:hasConvergenceTolerance` | `di:RiskPropagationParameter` | `xsd:decimal` | Iteration stops when the maximum node-wise change in propagated risk falls below this tolerance. |
| `di:hasCriticalThreshold` | `di:DIThreshold` | `xsd:decimal` | τ^C: below this (and below τ^D) the attribute is Critical rather than Degraded. |
| `di:hasDIValue` | `di:DependabilityIndex` | `xsd:decimal` | The computed node DI_i(t) in [0,1]. |
| `di:hasDampingFactor` | `di:RiskPropagationParameter` | `xsd:decimal` | ρ_h in [0,1): the damping factor of the propagation recurrence for hazard class h. Necessary but not sufficient for convergence; the spectral-radius condition spr(ρ_h·W^h) < 1 is checked by the external calculation. |
| `di:hasFailedThreshold` | `di:DIThreshold` | `xsd:decimal` | τ^F: below this the attribute is Failed rather than Critical. |
| `di:hasForecastConfidence` | `di:DIForecast` | `xsd:decimal` | Confidence in [0,1] the producing model attaches to the forecast; contributes to evidence quality. |
| `di:hasForecastHorizon` | `di:DIForecast` | `xsd:duration` | The horizon Δt or T_p over which the forecast was computed. |
| `di:hasForecastValue` | `di:DIForecast` | `xsd:decimal` | The predicted DI value in [0,1] at di:forecastValidAt, or the predicted minimum over the horizon when used for the T_pred test. |
| `di:hasLocalRiskValue` | `di:PropagatedRisk` | `xsd:decimal` | R_i,0^h(t) in [0,1]: the local or residual risk for hazard class h at this node before propagation, grounded in the design-time risk evaluation (cdm:Risk with the impact triple, or a control's residual risk). |
| `di:hasLowerThreshold` **DEPRECATED** | `di:DIThreshold` | `xsd:decimal` | DEPRECATED: DI-value bound. Use the four ordered attribute thresholds (di:hasNormalMinimum, di:hasCriticalThreshold, di:hasFailedThreshold, di:hasUnsafeThreshold). Will be removed in the next minor release. |
| `di:hasManagementFloor` | `di:SupervisionConfiguration` | `xsd:decimal` | φ_DI^{m}: the configured DI management floor for the vessel and mode; used by T_pred and the resilience margin. Not an operational-state threshold. |
| `di:hasNewValue` | `di:DIUpdateEvent` | `xsd:decimal` | has new value |
| `di:hasNormalMinimum` | `di:DIThreshold` | `xsd:decimal` | τ^D: the attribute value at or above which the attribute is Normal. |
| `di:hasPredictionHorizon` | `di:SupervisionConfiguration` | `xsd:duration` | T_p: the planning horizon over which a forecast floor crossing triggers resilience evaluation. |
| `di:hasPreviousValue` | `di:DIUpdateEvent` | `xsd:decimal` | has previous value |
| `di:hasPropagatedRiskValue` | `di:PropagatedRisk` | `xsd:decimal` | R_i^h(t) in [0,1]: the propagated risk for hazard class h at this node after iteration to the fixed point. |
| `di:hasResilienceMargin` | `di:SystemDependabilityIndex` | `xsd:decimal` | MR(t) = DI_sys(t) − φ_DI^{m(t)}: distance to the configured management floor. An anticipatory management quantity, not an operational-state definition; meaningful only for the vessel, mode, weights and floor it was configured for. |
| `di:hasRiskPropagationWeight` | `di:RiskPropagationEdge` | `xsd:decimal` | The typed weight w_j,i^h on this propagation edge for its hazard class, derived from davom:hasDependencyWeight on the mirrored Dependency. |
| `di:hasSystemDIValue` | `di:SystemDependabilityIndex` | `xsd:decimal` | The computed DI_sys(t) in [0,1]. |
| `di:hasSystemWeight` **DEPRECATED** | `di:DependabilityIndex` | `xsd:decimal` | DEPRECATED: flat aggregation weight on the node. Use a reified di:DIWeight (weightParent, weightChild, hasAggregationWeightValue) so that weights are per parent and per mode. Will be removed in the next minor release. |
| `di:hasTrendSlope` | `di:SystemDependabilityIndex` | `xsd:decimal` | slope_W(DI_sys)(t): the slope of the system DI over the configured trend window (per hour), evaluated only while the weighting configuration is unchanged. |
| `di:hasTrendSlopeThreshold` | `di:SupervisionConfiguration` | `xsd:decimal` | ε_W: the magnitude of negative slope (per hour) that constitutes a sustained decline. |
| `di:hasTrendWindow` | `di:SupervisionConfiguration` | `xsd:duration` | W: the window over which the sustained-decline slope is evaluated. |
| `di:hasUnsafeThreshold` | `di:DIThreshold` | `xsd:decimal` | τ^U: below this the attribute is Unsafe. Ordering 1 ≥ τ^D > τ^C > τ^F > τ^U ≥ 0 is checked externally and by SHACL. |
| `di:hasUpperThreshold` **DEPRECATED** | `di:DIThreshold` | `xsd:decimal` | DEPRECATED: DI-value bound. Use the four ordered attribute thresholds. Will be removed in the next minor release. |
| `di:triggeredAt` | `di:ResilienceTrigger` | `xsd:dateTime` | triggered at |

