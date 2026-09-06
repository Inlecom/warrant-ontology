# `warrant-davom` — DAVOM (Dependability-Aware Vessel Operational Model)

<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->

**Namespace:** `https://warrant-project.eu/ontology/davom#`  
**Prefix:** `davom:`  
**Ontology IRI:** `https://warrant-project.eu/ontology/davom`  
**Imports:** `warrant-core`  
**Version:** `1.0.0`

---

## Purpose

Dependability-Aware Vessel Operational Model: vessel, systems, functions, components, typed dependencies, data flows, communication links, IEC 62443 security zones and conduits, primary/supporting asset roles, and human operator roles.

**Role:** structural layer. Vessel decomposition (vessel, functions, systems,
subsystems, components), data flows and communication links, IEC 62443 security
zones and conduits, primary/supporting asset roles, human operator roles
(agents, not components), control actions and procedures, and typed, reified
dependencies over which risk propagates.

**Design rules**

1. `HumanOperator` and `HumanOperatorRole` subclass `warrant:AgentEntity`, never `OperationalEntity` or `Component`.
2. Use `dependsOn` for a bare traversal edge; use a reified `Dependency` when weight, criticality, latency, redundancy or propagation semantics must be recorded.
3. **Dependency direction:** `dependencySource` is the upstream provider (the entity depended upon), `dependencyTarget` the downstream consumer. Effects and propagated risk flow source → target, matching `di:propagationSource` → `di:propagationTarget`.
4. Every `Dependency` carries at least one canonical `hasDependencyType` (FUNCTIONAL, DATA, CONTROL, PHYSICAL, CYBER). The domain-specific subclasses refine but do not replace the canonical type; hazard classes declare which canonical types they propagate over.
5. `isBidirectional` is asserted only where the mechanism permits reverse propagation (some cyber paths, symmetric physical couplings).
6. `isCriticalNode` marks the nodes whose attribute states determine the system operational state.

---

## Classes (40)

| Class | Subclass of | Label | Description |
|---|---|---|---|
| `davom:ActuatorComponent` | `davom:Component` | Actuator Component |  |
| `davom:AssetRole` | — | Asset Role | Controlled vocabulary distinguishing primary assets (information and services of value: navigation data, positioning, route planning, propulsion control) from supporting assets (equipment, infrastructure, and human roles that store, process, or execute them), as used by the WARRaNT cybersecurity risk assessment methodology. Tag an operational entity with davom:hasAssetRole; every primary asset should be linked to at least one supporting asset through davom:supportsAsset, which serves as a graph-completeness check across the function and component layers. |
| `davom:CommunicationComponent` | `davom:Component` | Communication Component |  |
| `davom:CommunicationDependency` | `davom:Dependency` | Communication Dependency | Canonical type: davom:DATA (and davom:CYBER where the channel is a cyber path). |
| `davom:CommunicationLink` | `warrant:OperationalEntity` | Communication Link | A communication channel supporting data exchange, control, monitoring, or coordination between vessel, shore, or external entities. First-class operational entity; may have dependability metrics. Tag with davom:hasInterfaceType using a named davom:InterfaceType individual. |
| `davom:CommunicationSystem` | `davom:System` | Communication System |  |
| `davom:Component` | `warrant:OperationalEntity` | Component | A physical, software, cyber, data, communication, or sensor element. Human operators are NOT components; use warrant:AgentEntity subclasses instead. |
| `davom:Conduit` | `davom:CommunicationLink` | Conduit | A communication link that crosses a security-zone boundary in the IEC 62443-3-2 sense (e.g. the ship-shore wireless conduit). Declare the zones it joins with davom:connectsZone. Cyber effects propagate over conduits and over cyber/data/control dependencies, never over physical dependencies. |
| `davom:ControlAction` | `warrant:OperationalEntity` | Control Action | A command or intervention issued by a controller or authorised operator. |
| `davom:ControlDependency` | `davom:Dependency` | Control Dependency | Canonical type: davom:CONTROL. |
| `davom:CyberComponent` | `davom:Component` | Cyber Component |  |
| `davom:CyberDependency` | `davom:Dependency` | Cyber Dependency | Canonical type: davom:CYBER. |
| `davom:CyberPhysicalSystem` | `davom:System` | Cyber-Physical System |  |
| `davom:DataComponent` | `davom:Component` | Data Component |  |
| `davom:DataDependency` | `davom:Dependency` | Data Dependency | Canonical type: davom:DATA. |
| `davom:DataFlow` | `warrant:OperationalEntity` | Data Flow | A flow of data between systems, components, services, operators, or digital-twin elements. First-class operational entity; may have dependability metrics. |
| `davom:Dependency` | — | Dependency | A typed, reified dependency node. Direction convention: davom:dependencySource is the upstream entity (provider: the entity depended upon) and davom:dependencyTarget is the downstream entity (consumer: the entity that depends on it), so effects and propagated risk flow from source to target, matching di:propagationSource → di:propagationTarget on the mirrored RiskPropagationEdge. Use when weight, criticality, latency, redundancy level, or propagation semantics must be recorded alongside the relationship. Every Dependency should carry at least one davom:hasDependencyType from the five-value DependencyType vocabulary; the domain-specific subclasses below remain valid and refine, but do not replace, the canonical type. |
| `davom:DependencyType` | — | Dependency Type | Closed controlled vocabulary of the five canonical dependency types over which risk propagates: functional, data, control, physical, cyber. Each hazard class is associated at design time with the admissible subset of these types (cdm:propagatesOverDependencyType), and typed risk propagation follows only dependencies of an admissible type. Adding a value requires ontology revision. |
| `davom:FunctionalDependency` | `davom:Dependency` | Functional Dependency | Canonical type: davom:FUNCTIONAL. |
| `davom:HumanOperator` | `warrant:AgentEntity` | Human Operator | A person performing an operational role. Subclass of warrant:AgentEntity, NOT davom:Component. Example: a remote ROC operator or an onboard boatmaster. |
| `davom:HumanOperatorRole` | `warrant:AgentEntity` | Human Operator Role | A functional role associated with human operation (e.g. RemoteOperatorRole, OnboardBoatmasterRole). Subclass of warrant:AgentEntity, NOT davom:Component. Multiple HumanOperator individuals may perform the same role. |
| `davom:HumanSupervisionDependency` | `davom:Dependency` | Human Supervision Dependency | A dependency modelling the oversight relationship between a HumanOperatorRole and a system or function (e.g. ROC operator supervises remote navigation). Canonical type: davom:CONTROL. |
| `davom:InterfaceComponent` | `davom:Component` | Interface Component |  |
| `davom:InterfaceType` | — | Interface Type | Controlled vocabulary for the physical or logical interface technology of a CommunicationLink or DataFlow. Use davom:hasInterfaceType to tag a link individual. |
| `davom:OperationalDependency` | `davom:Dependency` | Operational Dependency | Canonical type: davom:FUNCTIONAL. |
| `davom:OperationalProcedure` | `warrant:OperationalEntity` | Operational Procedure | A defined sequence of operational or mitigation steps that may be executed by a HumanOperatorRole. |
| `davom:OperatorInterface` | `warrant:OperationalEntity` | Operator Interface | An HMI through which a human operator receives information or provides input. |
| `davom:OrganisationalSystem` | `davom:System` | Organisational System |  |
| `davom:PhysicalComponent` | `davom:Component` | Physical Component |  |
| `davom:PowerDependency` | `davom:Dependency` | Power Dependency | Canonical type: davom:PHYSICAL. |
| `davom:ProcedureDependency` | `davom:Dependency` | Procedure Dependency | Canonical type: davom:FUNCTIONAL. |
| `davom:SecurityZone` | — | Security Zone | A grouping of operational entities with common cybersecurity requirements, following the zone-and-conduit partitioning of IEC 62443-3-2 used by the WARRaNT cybersecurity risk assessment. Membership is asserted with davom:belongsToZone; zones are joined by davom:Conduit individuals. Not a vessel component and not a context entity. |
| `davom:SensorComponent` | `davom:Component` | Sensor Component |  |
| `davom:SoftwareComponent` | `davom:Component` | Software Component |  |
| `davom:SoftwareSystem` | `davom:System` | Software System |  |
| `davom:Subsystem` | `warrant:OperationalEntity` | Subsystem | A decomposition of a system into a more specific functional or technical unit. |
| `davom:System` | `warrant:OperationalEntity` | System | A technical, software, cyber-physical, communication, or organisational system supporting one or more vessel functions. |
| `davom:TechnicalSystem` | `davom:System` | Technical System |  |
| `davom:Vessel` | `warrant:OperationalEntity` | Vessel | The maritime asset or operational vessel represented in the KG. |
| `davom:VesselFunction` | `warrant:OperationalEntity` | Vessel Function | An operational capability that the vessel must provide (e.g. remote navigation, fire detection). |

## Controlled vocabularies (named individuals)

### `davom:AssetRole`

| Individual | Label | Description |
|---|---|---|
| `davom:PRIMARY_ASSET` | PRIMARY_ASSET | Information or service of value to the operation. Typically a VesselFunction or DataFlow. |
| `davom:SUPPORTING_ASSET` | SUPPORTING_ASSET | Equipment, infrastructure, software, or human role that stores, processes, transmits, or executes a primary asset. Typically a Component, System, CommunicationLink, or HumanOperatorRole. |

### `davom:DependencyType`

| Individual | Label | Description |
|---|---|---|
| `davom:CONTROL` | CONTROL | The source is commanded, supervised, or authorised by the target. |
| `davom:CYBER` | CYBER | Access, trust, or network reachability. May be bidirectional where the conduit permits reverse access, control, or trust exploitation; not assumed bidirectional in every case (see davom:isBidirectional). |
| `davom:DATA` | DATA | The source consumes a data product of the target. Effects normally propagate from provider to consumer. |
| `davom:FUNCTIONAL` | FUNCTIONAL | The source needs the target to deliver its function. Effects normally propagate from provider to consumer. |
| `davom:PHYSICAL` | PHYSICAL | Mechanical, thermal, electrical, or spatial coupling. May be directed or symmetric depending on the mechanism. |

### `davom:InterfaceType`

| Individual | Label | Description |
|---|---|---|
| `davom:AUDIO` | AUDIO | Analogue audio channel (e.g. VHF and bridge microphone feeds into VDR). |
| `davom:CONTACT` | CONTACT | Dry-contact (relay/digital I/O) interface, typically used for alarm and door-status signals into VDR and AMS. |
| `davom:LAN` | LAN | IEEE 802.3 Ethernet LAN (e.g. bridge navigation data bus, satellite LAN). |
| `davom:SERIAL` | SERIAL | Serial line conforming to IEC 61162 / NMEA 0183 (RS-422/RS-485). Dominant interface in navigation OT. |
| `davom:SERIAL_CONTACT` | SERIAL+CONTACT | Combined serial and dry-contact interface, as used on VDR inputs from engine control, watertight door, and AMS systems. |
| `davom:VIDEO` | VIDEO | Analogue or digital video signal (e.g. RADAR image feed into VDR). |
| `davom:WIRELESS` | WIRELESS | Radio-frequency wireless link (e.g. container gateway to vessel gateway, AIS VHF broadcast). |

## Object properties (28)

| Property | Domain | Range | Description |
|---|---|---|---|
| `davom:authorizes` | `davom:HumanOperatorRole` | `davom:ControlAction` | authorizes |
| `davom:belongsToZone` | `warrant:OperationalEntity` | `davom:SecurityZone` | Assigns a component, system, link, or data flow to an IEC 62443 security zone. |
| `davom:carriesDataFlow` | `davom:CommunicationLink` ∪ `davom:System` ∪ `davom:Component` | `davom:DataFlow` | carries data flow |
| `davom:connectsZone` | `davom:Conduit` | `davom:SecurityZone` | A Conduit joins two or more security zones; assert one triple per zone. |
| `davom:controls` | `davom:Component` ∪ `davom:HumanOperatorRole` | `davom:Component` | controls |
| `davom:dependencySource` | `davom:Dependency` | `warrant:OperationalEntity` | The upstream entity (provider) of the dependency: the entity depended upon. Effects propagate from source to target. |
| `davom:dependencyTarget` | `davom:Dependency` | `warrant:OperationalEntity` | The downstream entity (consumer) of the dependency: the entity that depends on the source. |
| `davom:dependsOn` | `warrant:OperationalEntity` | `warrant:OperationalEntity` | Simple traversal relation between operational entities. Use reified Dependency when weight, criticality, or redundancy level must be recorded. |
| `davom:executes` | `davom:HumanOperatorRole` | `davom:OperationalProcedure` | executes |
| `davom:hasAssetRole` | `warrant:OperationalEntity` ∪ `warrant:AgentEntity` | `davom:AssetRole` | Tags an operational entity or human operator role as a PRIMARY_ASSET or SUPPORTING_ASSET in the cybersecurity asset inventory. |
| `davom:hasComponent` | `davom:Subsystem` | `davom:Component` | has component |
| `davom:hasDataFlow` | `davom:VesselFunction` ∪ `davom:System` ∪ `davom:Component` | `davom:DataFlow` | has data flow |
| `davom:hasDependencyType` | `davom:Dependency` | `davom:DependencyType` | Tags a Dependency with one or more canonical propagation types from the davom:DependencyType vocabulary (FUNCTIONAL, DATA, CONTROL, PHYSICAL, CYBER). Used by typed risk propagation to decide whether a given hazard class may act through this dependency. |
| `davom:hasFunction` | `davom:Vessel` | `davom:VesselFunction` | has function |
| `davom:hasInterfaceType` | `davom:CommunicationLink` ∪ `davom:DataFlow` | `davom:InterfaceType` | Tags a CommunicationLink or DataFlow with a physical/logical interface technology from the davom:InterfaceType controlled vocabulary (LAN, SERIAL, CONTACT, SERIAL_CONTACT, VIDEO, AUDIO, WIRELESS). |
| `davom:hasOperatorRole` | `davom:Vessel` | `davom:HumanOperatorRole` | has operator role |
| `davom:hasSubsystem` | `davom:System` | `davom:Subsystem` | has subsystem |
| `davom:isSupportedBy` | `davom:VesselFunction` | `davom:System` | is supported by |
| `davom:operates` | `davom:HumanOperatorRole` | `davom:System` | operates |
| `davom:participatesIn` | `davom:HumanOperatorRole` | `davom:VesselFunction` | participates in |
| `davom:performsRole` | `davom:HumanOperator` | `davom:HumanOperatorRole` | performs role |
| `davom:providesDataTo` | `davom:Component` | `davom:Component` | provides data to |
| `davom:requiresOperatorRole` | `davom:VesselFunction` ∪ `davom:System` | `davom:HumanOperatorRole` | requires operator role |
| `davom:supervises` | `davom:HumanOperatorRole` | `davom:System` | supervises |
| `davom:supportsAsset` | `warrant:OperationalEntity` ∪ `warrant:AgentEntity` | `warrant:OperationalEntity` | Links a supporting asset to the primary asset it stores, processes, transmits, or executes. A primary asset with no incoming supportsAsset link is an incomplete asset inventory. |
| `davom:supportsDecisionOf` | `davom:System` | `davom:HumanOperatorRole` | supports decision of |
| `davom:supportsFunction` | — | — | supports function |
| `davom:usesCommunicationLink` | `davom:VesselFunction` ∪ `davom:System` ∪ `davom:DataFlow` | `davom:CommunicationLink` | uses communication link |

## Datatype properties (7)

| Property | Domain | Range | Description |
|---|---|---|---|
| `davom:hasConfidence` | `davom:Dependency` | `xsd:decimal` | has confidence |
| `davom:hasCriticality` | `davom:Dependency` | `xsd:string` | has criticality |
| `davom:hasDependencyWeight` | `davom:Dependency` | `xsd:decimal` | Structural weight of this dependency, mirrored at the DI level by di:hasRiskPropagationWeight on a RiskPropagationEdge. |
| `davom:hasLatency` | `davom:Dependency` | `xsd:decimal` | has latency |
| `davom:hasRedundancyLevel` | `davom:Dependency` | `xsd:integer` | has redundancy level |
| `davom:isBidirectional` | `davom:Dependency` | `xsd:boolean` | True when effects may propagate in both directions over this dependency (e.g. a cyber path whose conduit permits reverse access, or a symmetric physical coupling). Default when absent: directed from dependencySource (upstream provider) to dependencyTarget (downstream consumer). |
| `davom:isCriticalNode` | `warrant:OperationalEntity` | `xsd:boolean` | True when this node belongs to the critical node set whose attribute states determine the system operational state (the system state is the most severe attribute state across critical nodes). Node criticality also informs attribute and aggregation weights. Configured per vessel and mode (see warrant:appliesUnder on the weight and threshold artefacts). |

