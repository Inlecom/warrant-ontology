#!/usr/bin/env python3
"""
generate_module_docs.py — Regenerate docs/modules/warrant-<module>.md from the
Turtle sources so that the per-module documentation cannot drift from the
ontology.

Each page = a hand-maintained narrative block (NARRATIVE below) + tables of
classes, named individuals, object properties and datatype properties read
from the module file (labels, comments, domains, ranges, deprecation).

Usage:
    python scripts/generate_module_docs.py            # write all nine pages
    python scripts/generate_module_docs.py --check    # exit 1 if any page is stale

Install: pip install rdflib
"""

import sys
import pathlib
import textwrap

try:
    import rdflib
    from rdflib import RDF, RDFS, OWL
except ImportError:
    print("ERROR: rdflib not installed. Run: pip install rdflib", file=sys.stderr)
    sys.exit(1)

ROOT = pathlib.Path(__file__).parent.parent
ONT = ROOT / "ontology"
OUT = ROOT / "docs" / "modules"

SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")

PREFIXES = {
    "https://warrant-project.eu/ontology/core#": "warrant",
    "https://warrant-project.eu/ontology/davom#": "davom",
    "https://warrant-project.eu/ontology/observation#": "obs",
    "https://warrant-project.eu/ontology/cdm#": "cdm",
    "https://warrant-project.eu/ontology/assurance#": "assr",
    "https://warrant-project.eu/ontology/dependability-index#": "di",
    "https://warrant-project.eu/ontology/scenario#": "scen",
    "https://warrant-project.eu/ontology/mitigation#": "mit",
    "https://warrant-project.eu/ontology/digital-twin#": "dt",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
}

# file stem -> (namespace, prefix, title)
MODULES = [
    ("warrant-core",         "https://warrant-project.eu/ontology/core#",                "warrant", "Core"),
    ("warrant-davom",        "https://warrant-project.eu/ontology/davom#",               "davom",   "DAVOM (Dependability-Aware Vessel Operational Model)"),
    ("warrant-observation",  "https://warrant-project.eu/ontology/observation#",         "obs",     "Observation and Health Events"),
    ("warrant-cdm",          "https://warrant-project.eu/ontology/cdm#",                 "cdm",     "Causal Dependability Model"),
    ("warrant-assurance",    "https://warrant-project.eu/ontology/assurance#",           "assr",    "Assurance (Attribute Scoring and Living Dependability Case)"),
    ("warrant-di",           "https://warrant-project.eu/ontology/dependability-index#", "di",      "Dependability Index and Supervision"),
    ("warrant-scenario",     "https://warrant-project.eu/ontology/scenario#",            "scen",    "Scenario"),
    ("warrant-mitigation",   "https://warrant-project.eu/ontology/mitigation#",          "mit",     "Mitigation and Resilience Response"),
    ("warrant-digital-twin", "https://warrant-project.eu/ontology/digital-twin#",        "dt",      "Digital Twin"),
]

# Hand-maintained narrative per module. Keep this to purpose, role in the
# continuous-assurance loop, and design rules; the term tables are generated.
NARRATIVE = {
"warrant-core": """
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
""",
"warrant-davom": """
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
""",
"warrant-observation": """
**Role:** evidence layer. Metrics, observers (physical and virtual sensors,
probes, log collectors), measurements, analytical services, the structured
**health event** record and its two specialisations (detection events, which
identify a deviation, and predicted-condition events, which anticipate one),
node health monitors, human observations and operator inputs.

**The detection chain (mandatory)**

```
DataSource → obs:producesHealthEvent → HealthEvent
AnalyticalService / VirtualSensor / DetectionRule → obs:producesDetectionEvent → DetectionEvent
DetectionEvent → obs:detectionEventDetects → cdm:Deviation
```

A `Deviation` is reached only through a `DetectionEvent`. `obs:produces` ranges over
`Status | VirtualSensorOutput` only. `obs:detects` is a SPARQL shortcut.

**Design rules**

1. Operational entities *have* metrics (`hasDependabilityMetric`); components do not generate them.
2. `HealthEvent` carries the methodology's named record (id, time, source, affected asset, condition, confidence, severity, duration/persistence, operational impact, root cause, mission context, control status, trend). Fields may be unknown at creation and enriched as diagnosis proceeds; enrichment lineage uses `warrant:derivedFrom`.
3. `PredictedConditionEvent` is not bound by the detection-event rule; quantitative DI forecasts are `di:DIForecast`, not health events.
4. `NodeHealthMonitor` is an `AnalyticalService` at component, function or system level; monitors exchange health events along the dependency topology and produce the attribute assessments (`assr:AssuranceAttributeValue`) the Supervisor fuses.
5. Raw telemetry stays outside the graph (`hasExternalRecordReference`, `hasExternalTimeSeriesId`).
""",
"warrant-cdm": """
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
""",
"warrant-assurance": """
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
""",
"warrant-di": """
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
""",
"warrant-scenario": """
**Role:** what-if semantics. Scenario types (cyberattack, failure, degraded
operation, environmental, unsafe control), triggers, executions with a
lifecycle state, and results that carry a projected operational state and
produce DI forecasts.

**Design rules**

1. The graph defines scenario semantics; the external scenario engine (typically hosted by the Digital Twin) executes them and writes back `ScenarioResult`.
2. `ScenarioExecutionState` (PENDING, RUNNING, COMPLETED, FAILED) is an execution lifecycle; it is not a dependability state. The projected operational state is `hasProjectedState` on the result.
3. `producesForecast` is how a scenario execution feeds the Supervisor's predictive trigger and the REDS expected-effect estimate.
""",
"warrant-mitigation": """
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
""",
"warrant-digital-twin": """
**Role:** the semantic interface between the graph and the Digital Twin, in
both directions. The twin *consumes* the graph (visualises, monitors, executes
scenarios, stores results, receives updates) and *produces* inputs to it: it is
an `obs:DataSource` (state estimation, virtual sensing, health events), it
provides virtual sensors, and it produces `di:DIForecast`s that feed the
Supervisor's predictive trigger and REDS's expected-effect estimates.

**Design rules**

1. Thin integration layer: no domain concept is defined here. `warrant:VisualisableEntity` lives in core; modules mark their classes visualisable without importing this module.
2. No module imports warrant-digital-twin. The DT → Supervisor/REDS direction is realised by placing the forecast class in warrant-di and declaring `producesForecast` here.
3. The twin is advisory by design in the proof of concept: it presents evaluations and records operator responses; it does not act.
4. `dt:ScenarioExecutionState` is deprecated; use `scen:ScenarioExecutionState`.
""",
}


def qname(term):
    s = str(term)
    for ns, p in PREFIXES.items():
        if s.startswith(ns):
            return f"`{p}:{s[len(ns):]}`"
    return f"`{s}`"


def lit(g, s, p):
    v = g.value(s, p)
    return str(v) if v is not None else ""


def expr(g, node):
    """Render a domain/range node: IRI or an owl:unionOf list."""
    if node is None:
        return "—"
    if isinstance(node, rdflib.BNode):
        lst = g.value(node, OWL.unionOf)
        if lst is not None:
            items = list(rdflib.collection.Collection(g, lst))
            return " ∪ ".join(qname(i) for i in items)
        return "(anonymous)"
    return qname(node)


def one_line(text, width=None):
    t = " ".join(text.split())
    return t.replace("|", "\\|")


def render(stem, ns, prefix, title):
    g = rdflib.Graph().parse(str(ONT / f"{stem}.ttl"), format="turtle")
    onto = next(g.subjects(RDF.type, OWL.Ontology))
    # owl:imports are relative IRIs (<warrant-core.ttl>); rdflib resolves them
    # against the file location, so keep only the module name.
    imports = sorted(str(i).replace("\\", "/").rsplit("/", 1)[-1].replace(".ttl", "")
                     for i in g.objects(onto, OWL.imports))
    local = lambda s: str(s).startswith(ns)

    def deprecated(s):
        return (s, OWL.deprecated, rdflib.Literal(True)) in g

    classes = sorted((s for s in g.subjects(RDF.type, OWL.Class) if local(s)), key=str)
    oprops = sorted((s for s in g.subjects(RDF.type, OWL.ObjectProperty) if local(s)), key=str)
    dprops = sorted((s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if local(s)), key=str)
    vocab_classes = [c for c in classes if any(local(i) for i in g.subjects(RDF.type, c))]

    out = []
    out.append(f"# `{stem}` — {title}\n")
    out.append("<!-- GENERATED FILE: narrative lives in scripts/generate_module_docs.py; tables come from the .ttl. Do not edit by hand. -->\n")
    out.append(f"**Namespace:** `{ns}`  ")
    out.append(f"**Prefix:** `{prefix}:`  ")
    out.append(f"**Ontology IRI:** `{str(onto)}`  ")
    out.append(f"**Imports:** {', '.join(f'`{i}`' for i in imports) if imports else '(none)'}  ")
    out.append(f"**Version:** `{lit(g, onto, OWL.versionInfo)}`\n")
    out.append("---\n")
    out.append("## Purpose\n")
    out.append(one_line(lit(g, onto, RDFS.comment)).replace("\\|", "|") + "\n")
    out.append(textwrap.dedent(NARRATIVE.get(stem, "")).strip() + "\n")
    out.append("---\n")

    out.append(f"## Classes ({len(classes)})\n")
    out.append("| Class | Subclass of | Label | Description |")
    out.append("|---|---|---|---|")
    for c in classes:
        supers = " , ".join(qname(x) for x in g.objects(c, RDFS.subClassOf) if not isinstance(x, rdflib.BNode))
        label = lit(g, c, RDFS.label)
        alt = lit(g, c, SKOS.altLabel)
        if alt:
            label += f" (alt: {alt})"
        dep = " **DEPRECATED**" if deprecated(c) else ""
        out.append(f"| {qname(c)}{dep} | {supers or '—'} | {one_line(label)} | {one_line(lit(g, c, RDFS.comment))} |")
    out.append("")

    if vocab_classes:
        out.append("## Controlled vocabularies (named individuals)\n")
        for vc in vocab_classes:
            inds = sorted((i for i in g.subjects(RDF.type, vc) if local(i)), key=str)
            out.append(f"### {qname(vc)}\n")
            out.append("| Individual | Label | Description |")
            out.append("|---|---|---|")
            for i in inds:
                out.append(f"| {qname(i)} | {one_line(lit(g, i, RDFS.label))} | {one_line(lit(g, i, RDFS.comment))} |")
            out.append("")

    out.append(f"## Object properties ({len(oprops)})\n")
    out.append("| Property | Domain | Range | Description |")
    out.append("|---|---|---|---|")
    for p in oprops:
        dep = " **DEPRECATED**" if deprecated(p) else ""
        sub = g.value(p, RDFS.subPropertyOf)
        extra = f" (sub-property of {qname(sub)})" if sub is not None else ""
        out.append(f"| {qname(p)}{dep} | {expr(g, g.value(p, RDFS.domain))} | {expr(g, g.value(p, RDFS.range))} | {one_line(lit(g, p, RDFS.comment) or lit(g, p, RDFS.label))}{extra} |")
    out.append("")

    out.append(f"## Datatype properties ({len(dprops)})\n")
    out.append("| Property | Domain | Range | Description |")
    out.append("|---|---|---|---|")
    for p in dprops:
        dep = " **DEPRECATED**" if deprecated(p) else ""
        out.append(f"| {qname(p)}{dep} | {expr(g, g.value(p, RDFS.domain))} | {expr(g, g.value(p, RDFS.range))} | {one_line(lit(g, p, RDFS.comment) or lit(g, p, RDFS.label))} |")
    out.append("")

    # axioms this module asserts about other modules' terms (e.g. VisualisableEntity)
    foreign = sorted(set(
        f"{qname(s)} rdfs:subClassOf {qname(o)}"
        for s, o in g.subject_objects(RDFS.subClassOf)
        if not local(s) and not isinstance(o, rdflib.BNode)
    ))
    if foreign:
        out.append("## Axioms asserted about other modules' terms\n")
        for f in foreign:
            out.append(f"- {f}")
        out.append("")

    return "\n".join(out) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for stem, ns, prefix, title in MODULES:
        text = render(stem, ns, prefix, title)
        path = OUT / f"{stem}.md"
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path)
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"  wrote {path.relative_to(ROOT)}")
    if check:
        if stale:
            print("STALE module docs: " + ", ".join(str(p.relative_to(ROOT)) for p in stale), file=sys.stderr)
            sys.exit(1)
        print("Module docs are up to date.")


if __name__ == "__main__":
    main()
