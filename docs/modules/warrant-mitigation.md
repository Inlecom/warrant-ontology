# `warrant-mitigation` — Mitigation and Resilience Response

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/mitigation#`  
**Prefix:** `mit:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/mitigation`  
**Imports:** `warrant-cdm`, `warrant-core`, `warrant-davom`, `warrant-di`, `warrant-observation`, `warrant-scenario`  
**Version:** `0.10-poc`

---

## Purpose

Mitigation rules, actions, failover procedures, redundant resources and recovery effects (the response library); REDS response evaluations with expected effect, cost, penalty, admissibility and rank; IRDS response executions with authorisation, posture and outcome; the response strategy, resilience posture and authorisation status vocabularies. Ranking and expected-effect estimation are external computations; the KG stores their inputs, configured weights and results.

**Role:** the adaptive dependability and resilience management loop, in three
layers: the design-time response library (rules, actions, failover procedures,
redundant resources, recovery effects), the REDS evaluation record
(`ResponseEvaluation`, one per alternative and trigger), and the IRDS
execution record (`ResponseExecution`, with authorisation, posture and
outcome).

**Objective (metadata only, computed externally)**

u* = argmax_{u ∈ U_safe} { E[DI_sys(t+Δt) | u] − λ·C(u) − η·V(u) }, with U_safe
containing only actions permitted by operational, safety, cybersecurity,
regulatory and human-authority constraints.

**Design rules**

1. Assessment (warrant-di), recommendation (`ResponseEvaluation`), authorisation and actuation (`ResponseExecution`) are distinct records with distinct agents (`DecisionSupportService`, `ResilienceSupervisor`).
2. Responses are invoked by a `di:ResilienceTrigger` (or a deviation/hazard/health event); the DI value itself never triggers a response. Matching on a DI-node state is retained for compatibility only.
3. Every action carries a strategy type and a default resilience posture (fail-operational or fail-safe); the posture in force is recorded on the execution and in the Living Dependability Case.
4. Actions implement design-time `cdm:Control`s (`implementsControl`) and may require authorisation from a human operator role; operator approvals and overrides are recorded as `obs:OperatorInput` and are admissible evidence.
5. In the proof of concept all actions are advisory (`AdvisoryAction`) or visualised procedures; `MachineActionableAction` is reserved.

---

## Classes (16)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `mit:AdvisoryAction` | `mit:MitigationAction` | Advisory Action | A human-directed advisory recommendation presented to the operator. All PoC mitigation instances must use this class. |
| `mit:AuthorisationStatus` | — | Authorisation Status | Closed controlled vocabulary for the authorisation state of a response execution. Named individuals only. |
| `mit:DecisionConfiguration` | `mit:MitigationEntity` , `warrant:CalculationEntity` | Decision Configuration | The controlled, versioned weights of the REDS objective for a vessel and context: cost weight λ (mit:hasCostWeight) and penalty weight η (mit:hasPenaltyWeight). warrant:appliesUnder, warrant:hasVersion, warrant:approvedBy. |
| `mit:DecisionSupportService` | `obs:AnalyticalService` | Risk Evaluation and Decision Support (REDS) | The runtime service that, when a resilience trigger fires, receives the attribute assessments, DI trend, predicted states and the Knowledge Graph diagnosis, compares feasible mitigation alternatives, estimates their expected effect with the Digital Twin, applies operational and authority constraints, and provides a ranked recommendation with an explanation and evidence trail (mit:ResponseEvaluation). It does not calculate the DI and does not execute actions. |
| `mit:FailoverProcedure` | `mit:MitigationEntity` , `warrant:VisualisableEntity` | Failover Procedure | A defined fallback or recovery process. In the WARRaNT proof of concept, failover procedures are visualised or advisory — they are NOT automatically executed. |
| `mit:MachineActionableAction` | `mit:MitigationAction` | Machine-Actionable Action | A subclass of MitigationAction representing an automation-executable action. Defined for semantic completeness and forward compatibility. All WARRaNT PoC instances MUST use mit:AdvisoryAction or mit:FailoverProcedure instead. Informative alignment: mit:MachineActionableAction ≈ saref:Command (SAREF4ENER). |
| `mit:MitigationAction` | `mit:MitigationEntity` , `warrant:VisualisableEntity` | Mitigation Action | A response alternative that reduces risk, restores an attribute, or limits DI degradation. Typed by mit:hasStrategyType (reconfiguration, logical isolation, redundancy activation, virtual-sensor substitution, communication rerouting, safe-degraded mode, recovery, enhanced monitoring, operator escalation), carries a default resilience posture (mit:hasDefaultPosture), may implement a design-time control (mit:implementsControl), and may require authorisation from a human operator role (mit:requiresAuthorisationFrom). Its evaluation for a specific trigger is a mit:ResponseEvaluation; its coordinated execution is a mit:ResponseExecution. |
| `mit:MitigationEntity` | — | Mitigation Entity | Abstract superclass for all mitigation-related entities. |
| `mit:MitigationRule` | `mit:MitigationEntity` | Mitigation Rule | A declarative rule of the response library matching a Deviation, Hazard, ResilienceTrigger, or operational state and recommending one or more MitigationActions as candidate alternatives. Rules populate the feasible set that REDS evaluates; they do not rank or execute. |
| `mit:RecoveryEffect` | `mit:MitigationEntity` | Recovery Effect | The expected effect of a failover procedure or action, as estimated at design time or by simulation: projected DI gain, projected risk reduction, recovery time, and the confidence of the projection. A runtime, trigger-specific expected effect is instead recorded as a di:DIForecast on a mit:ResponseEvaluation. |
| `mit:RedundantResource` | `mit:MitigationEntity` | Redundant Resource |  |
| `mit:ResiliencePosture` | — | Resilience Posture | Closed controlled vocabulary of the two qualitatively different assurance postures a response can place the system in. The Living Dependability Case records which posture was in force at each point of the operation. Named individuals only. |
| `mit:ResilienceSupervisor` | `obs:AnalyticalService` | Intelligent Resilience and Dependability Supervisor (IRDS) | The runtime resilience-orchestration layer. It receives health assessments, the operational state, DI and trend, Digital Twin forecasts and REDS recommendations, and coordinates the selected response only after the applicable automated or human authorisation condition is satisfied, recording action, authority, timing, posture and outcome (mit:ResponseExecution) in the Living Dependability Case. It selects between fail-operational and fail-safe postures, not merely between actions. |
| `mit:ResponseEvaluation` | `mit:MitigationEntity` , `warrant:CalculationEntity` , `warrant:VisualisableEntity` | Response Evaluation | The REDS record for one candidate response u in answer to one resilience trigger: the action evaluated, its expected effect E[DI_sys(t+Δt) \| u] as a di:DIForecast (typically produced by the Digital Twin or a scenario execution), the implementation cost or disruption C(u), the residual-exposure or soft-preference penalty V(u), whether the action is admissible (u ∈ U_safe) and, if not, which constraint it violates, the resulting rank, whether it is the recommendation, and a human-readable explanation. Hard constraint violations exclude an action from U_safe rather than penalising it twice. The ranking itself is computed externally with the weights in mit:DecisionConfiguration. |
| `mit:ResponseExecution` | `mit:MitigationEntity` , `warrant:VisualisableEntity` | Response Execution | The IRDS record of a selected response: the action executed and the evaluation it was selected from, the authorisation status and the authority that granted it (a human operator role or an automated authorisation service), authorisation, start and completion times, the resilience posture in force, the outcome and the post-response index, any operator input (approval, override, intervention) recorded as evidence, and the Living Dependability Case it is recorded in. Connects assessment and recommendation with accountable operational intervention; the outcome re-enters the loop at sensing. |
| `mit:ResponseStrategyType` | — | Response Strategy Type | Closed controlled vocabulary of the resilience strategies IRDS can coordinate: the seven kinds named in the framework paper plus logical isolation and enhanced monitoring, which the paper's cybersecurity section and the IRDS patent figure list as distinct mitigation classes. Named individuals only; adding a value requires ontology revision. |

## Controlled vocabularies (named individuals)

### `mit:AuthorisationStatus`

| Individual | Label | Description |
|---|---|---|
| `mit:AUTHORISATION_PENDING` | AUTHORISATION_PENDING | Recommended; the authorisation condition is not yet satisfied. |
| `mit:AUTHORISED` | AUTHORISED | The applicable automated or human authorisation condition is satisfied; IRDS may coordinate the response. |
| `mit:OVERRIDDEN` | OVERRIDDEN | The operator substituted a different action or intervened manually; the override is recorded as evidence. |
| `mit:REJECTED` | REJECTED | The responsible authority declined the recommended response. |

### `mit:ResiliencePosture`

| Individual | Label | Description |
|---|---|---|
| `mit:FAIL_OPERATIONAL` | FAIL_OPERATIONAL | The mission is preserved: the affected function continues to be delivered through redundancy, reconfiguration, or virtual-sensor substitution with degraded but acceptable performance. |
| `mit:FAIL_SAFE` | FAIL_SAFE | The mission objective is abandoned in favour of a state of reduced hazard exposure, e.g. a fail-safe trajectory bringing the vessel to a safe stop or holding state. The existence of a feasible fail-safe option is itself a precondition for continuing in the nominal mode. |

### `mit:ResponseStrategyType`

| Individual | Label | Description |
|---|---|---|
| `mit:COMMUNICATION_REROUTING` | COMMUNICATION_REROUTING | Reroute data or control traffic over an alternative link or conduit. |
| `mit:ENHANCED_MONITORING` | ENHANCED_MONITORING | Increase monitoring intensity or coverage of the affected node (higher sampling, additional observers, cross-checks) without changing its configuration; the response for a Degraded state and an accompaniment to recovery. |
| `mit:LOGICAL_ISOLATION` | LOGICAL_ISOLATION | Isolate a subsystem, zone, or conduit logically (network segmentation, service disablement, trusted-source substitution) to contain a cyber threat or a faulty element while the rest of the function continues. |
| `mit:OPERATOR_ESCALATION` | OPERATOR_ESCALATION | Escalate the situation to the responsible human operator for decision or intervention (human-in-the-loop escalation). |
| `mit:RECONFIGURATION` | RECONFIGURATION | Reconfigure the system or function to continue delivery (technical reconfiguration). |
| `mit:RECOVERY` | RECOVERY | Restore the affected element or service (restart, restore from backup, repair), including recovery sequencing across dependent elements. |
| `mit:REDUNDANCY_ACTIVATION` | REDUNDANCY_ACTIVATION | Activate a redundant resource or channel. |
| `mit:SAFE_DEGRADED_MODE` | SAFE_DEGRADED_MODE | Transition to a safe-degraded operating mode with reduced capability. |
| `mit:VIRTUAL_SENSOR_SUBSTITUTION` | VIRTUAL_SENSOR_SUBSTITUTION | Replace a failed, degraded or untrusted physical sensor by a virtual-sensor estimate (obs:substitutesFor). |

## Object properties (28)

| Property | Domain | Range | Description |
|---|---|---|---|
| `mit:activates` | `mit:MitigationAction` | `mit:FailoverProcedure` | activates |
| `mit:addresses` | `mit:FailoverProcedure` ∪ `mit:MitigationAction` | `davom:VesselFunction` ∪ `davom:System` ∪ `davom:Component` ∪ `davom:CommunicationLink` ∪ `davom:DataFlow` | The function, system, component, link, or data flow the procedure or action is intended to recover or protect. |
| `mit:authorisedBy` | `mit:ResponseExecution` | `davom:HumanOperatorRole` ∪ `obs:AnalyticalService` | The authority that satisfied the authorisation condition: a human operator role, or an automated authorisation service within the configured authority allocation. |
| `mit:coordinatedBy` | `mit:ResponseExecution` | `mit:ResilienceSupervisor` | coordinated by |
| `mit:evaluatedBy` | `mit:ResponseEvaluation` | `mit:DecisionSupportService` | evaluated by |
| `mit:evaluatedWithScenario` | `mit:ResponseEvaluation` | `scen:Scenario` | The what-if scenario whose execution produced the expected-effect forecast. |
| `mit:evaluatesAction` | `mit:ResponseEvaluation` | `mit:MitigationAction` | evaluates action |
| `mit:executesAction` | `mit:ResponseExecution` | `mit:MitigationAction` | executes action |
| `mit:hasAuthorisationStatus` | `mit:ResponseExecution` | `mit:AuthorisationStatus` | has authorisation status |
| `mit:hasDefaultPosture` | `mit:MitigationAction` ∪ `mit:FailoverProcedure` | `mit:ResiliencePosture` | The assurance posture (fail-operational or fail-safe) this action or procedure places the system in when executed as designed. |
| `mit:hasExpectedEffect` | `mit:FailoverProcedure` ∪ `mit:MitigationAction` | `mit:RecoveryEffect` | has expected effect |
| `mit:hasExpectedIndex` | `mit:ResponseEvaluation` | `di:DIForecast` | E[DI_sys(t+Δt) \| u]: the forecast of the system (or affected node) DI conditional on executing the evaluated action, estimated with the Digital Twin or a scenario execution. |
| `mit:hasOutcomeIndex` | `mit:ResponseExecution` | `di:DependabilityIndex` ∪ `di:SystemDependabilityIndex` | The index value recorded after the response, closing the loop from action to reassessment. A DI recovery is a trend signal; the graph and the affected claims must confirm that the diagnosed causes are resolved. |
| `mit:hasResiliencePosture` | `mit:ResponseExecution` | `mit:ResiliencePosture` | The posture (fail-operational or fail-safe) in force as a result of this execution. |
| `mit:hasStrategyType` | `mit:MitigationAction` ∪ `mit:FailoverProcedure` | `mit:ResponseStrategyType` | The kind of resilience strategy this response represents. Applies to a FailoverProcedure as much as to a MitigationAction: a procedure is a response with a strategy, not merely the thing an action activates. |
| `mit:implementsControl` | `mit:MitigationAction` ∪ `mit:FailoverProcedure` | `cdm:Control` | The design-time control (safeguard) that this runtime action activates or relies on. Links the runtime response back to the hazard analysis and to the claims the Living Dependability Case holds about the control. |
| `mit:isRecordedIn` | `mit:ResponseExecution` ∪ `mit:ResponseEvaluation` | `assr:LivingDependabilityCase` | Records the evaluation or execution (action, rationale, authority, timing, posture, outcome) in the Living Dependability Case. |
| `mit:isTriggeredBy` | `mit:MitigationAction` | `cdm:Deviation` ∪ `cdm:Hazard` ∪ `di:DependabilityIndexState` ∪ `di:ResilienceTrigger` ∪ `obs:HealthEvent` | The deviation, hazard, health event, resilience trigger, or state in response to which the action was recommended or executed. |
| `mit:matchesRule` | `cdm:Deviation` ∪ `cdm:Hazard` ∪ `di:DependabilityIndexState` ∪ `di:ResilienceTrigger` | `mit:MitigationRule` | A deviation, hazard, resilience trigger, or operational state matches a rule of the response library. Prefer matching on a ResilienceTrigger or attribute-wise state; matching on a DI-node state is retained for compatibility but the DI value itself never triggers a response. |
| `mit:performsMitigation` | `davom:HumanOperatorRole` | `mit:MitigationAction` | performs mitigation |
| `mit:recommends` | `mit:MitigationRule` ∪ `cdm:Risk` | `mit:MitigationAction` ∪ `mit:FailoverProcedure` | A rule (or a design-time risk evaluation) names a candidate response: either a MitigationAction, or a FailoverProcedure where the rule points straight at an existing procedure rather than at an advisory wrapping it. The runtime recommendation among candidates is mit:isRecommended on a ResponseEvaluation. |
| `mit:recordedOperatorInput` | `mit:ResponseExecution` | `obs:OperatorInput` | The operator approval, rejection, override, or intervention associated with this execution. Operator actions are part of the evolving dependability case and admissible as evidence. |
| `mit:requiresAuthorisationFrom` | `mit:MitigationAction` ∪ `mit:FailoverProcedure` | `davom:HumanOperatorRole` | The human operator role whose authorisation is a precondition for executing this action or procedure. A response with no such triple may be authorised automatically within the configured authority allocation. |
| `mit:respondsToTrigger` | `mit:ResponseEvaluation` | `di:ResilienceTrigger` | The resilience trigger that invoked this evaluation. All evaluations for one trigger form the ranked alternative set. |
| `mit:selectedFrom` | `mit:ResponseExecution` | `mit:ResponseEvaluation` | The evaluation whose action was selected; preserves the evidence trail from trigger to recommendation to execution. |
| `mit:uses` | `mit:FailoverProcedure` | `mit:RedundantResource` | uses |
| `mit:usesDecisionConfiguration` | `mit:ResponseEvaluation` | `mit:DecisionConfiguration` | uses decision configuration |
| `mit:violatesConstraint` | `mit:ResponseEvaluation` | `cdm:SafetyConstraint` ∪ `assr:Requirement` | For an inadmissible alternative: the operational, safety, cybersecurity, regulatory, or authority constraint that excludes it from U_safe. |

## Datatype properties (18)

| Property | Domain | Range | Description |
|---|---|---|---|
| `mit:authorisedAt` | `mit:ResponseExecution` | `xsd:dateTime` | authorised at |
| `mit:completedAt` | `mit:ResponseExecution` | `xsd:dateTime` | completed at |
| `mit:evaluatedAt` | `mit:ResponseEvaluation` | `xsd:dateTime` | evaluated at |
| `mit:hasCostWeight` | `mit:DecisionConfiguration` | `xsd:decimal` | λ: weight of the implementation cost term. |
| `mit:hasEffectConfidence` | `mit:RecoveryEffect` | `xsd:decimal` | Confidence in the projected effect, in [0,1] (historical data, simulation, or expert judgement). |
| `mit:hasExplanation` | `mit:ResponseEvaluation` | `xsd:string` | Human-readable rationale for the rank, referencing the diagnosis, constraints and expected effect. |
| `mit:hasImplementationCost` | `mit:ResponseEvaluation` | `xsd:decimal` | C(u): implementation cost or operational disruption of the alternative, normalised to [0,1]. |
| `mit:hasObjectiveValue` | `mit:ResponseEvaluation` | `xsd:decimal` | The computed value of E[DI_sys \| u] − λ·C(u) − η·V(u) for this alternative. |
| `mit:hasOutcome` | `mit:ResponseExecution` | `xsd:string` | Outcome of the response as assessed after execution (e.g. SUCCESSFUL, PARTIAL, FAILED) with a short description. |
| `mit:hasPenaltyWeight` | `mit:DecisionConfiguration` | `xsd:decimal` | η: weight of the residual-exposure penalty term. |
| `mit:hasProjectedIndexGain` | `mit:RecoveryEffect` | `xsd:decimal` | Expected DI improvement after the procedure or action, in [0,1]. |
| `mit:hasProjectedRiskReduction` | `mit:RecoveryEffect` | `xsd:decimal` | Expected reduction of the aggregated propagated risk, in [0,1]. |
| `mit:hasRank` | `mit:ResponseEvaluation` | `xsd:integer` | Rank among the admissible alternatives for the same trigger; 1 is the preferred response. |
| `mit:hasRecoveryTime` | `mit:RecoveryEffect` | `xsd:duration` | Expected time from activation to recovery of the addressed function. |
| `mit:hasResidualExposurePenalty` | `mit:ResponseEvaluation` | `xsd:decimal` | V(u): residual exposure or soft-preference penalty among otherwise feasible actions, normalised to [0,1]. Hard violations are excluded from U_safe, not penalised here. |
| `mit:isAdmissible` | `mit:ResponseEvaluation` | `xsd:boolean` | True when the action belongs to U_safe (permitted by operational, safety, cybersecurity, regulatory and human-authority constraints). |
| `mit:isRecommended` | `mit:ResponseEvaluation` | `xsd:boolean` | True for the alternative REDS presents as its recommendation (normally rank 1). |
| `mit:startedAt` | `mit:ResponseExecution` | `xsd:dateTime` | started at |

