# WARRaNT KG Ontology

Formal OWL/RDF ontology for the **WARRaNT Knowledge Graph** — a Horizon Europe RIA project (101202581) developing a federated methodology and tools to assure the dependability of waterborne digital systems.

https://warrant-project.eu/

---

## Purpose

The WARRaNT ontology is the semantic specification of the WARRaNT continuous-assurance framework. It provides a shared vocabulary for the whole loop — design-time hazard knowledge → health events → node health monitoring → attribute-wise supervision and the Dependability Index → resilience decision and response → the Living Dependability Case — with the Digital Twin as both consumer and producer:

- **Vessel operational structure** (DAVOM): vessels, functions, systems, components, data flows, communication links, IEC 62443 zones and conduits, asset roles, human operator roles, typed dependencies.
- **Design-time knowledge** (CDM / HAZOP / FMEA / STPA / cyber assessment): deviations, hazards, risks with the impact triple, failure modes with FMEA ratings, threat scenarios, vulnerabilities, controls with residual risk, hazard classes with admissible propagation types.
- **Observation and health events**: metrics, observers, virtual sensors, the structured health-event record (detected and predicted), node health monitors, operator inputs.
- **Attribute assessment and the Living Dependability Case** (Assurance): attribute values with confidence and fusion, node dependability scores; requirements, claims, assumptions, evidence and obligations, nonconformities, Assurance Level, Certification Readiness.
- **Dependability Index and supervision** (DI): typed per-hazard-class risk propagation, hierarchical aggregation, attribute-wise operational state, resilience triggers and their configuration, DI forecasts.
- **Scenarios**: what-if cases, executions and results that produce forecasts.
- **Decision and response** (Mitigation): the response library, REDS response evaluations, IRDS response executions with authorisation and posture.
- **Digital Twin interface**: views, decision support, live updates, virtual sensing and forecast production.

---

## What is Inside the KG

- Semantic class and property definitions (200 classes, 194 object properties, 128 datatype properties, 70 named individuals across nine modules).
- Controlled vocabularies: deviation types, operational states, operational modes, dependency types, asset roles, hazard classes, monitoring levels, trigger types, strategy types, postures, authorisation, claim and obligation statuses, execution lifecycle states.
- Latest health events, attribute values, node scores, indices and states, triggers, evaluations, executions, claims and evidence.
- Governed configuration (weights, thresholds, floors, damping, decision weights) with version and approval.
- Scenario semantics and execution results.
- Traceability links from evidence through health events, indices, triggers and responses to claims and requirements.
- References to external time-series stores.

## What is Outside the KG

- Raw high-frequency sensor telemetry (use `obs:hasExternalTimeSeriesId`).
- All numerical computation: fusion, node score, propagation, aggregation, state assignment, triggers, response ranking, Assurance Level, Certification Readiness (external services store results in the KG with method identity and timestamp).
- Scenario engine execution (external engine stores `scen:ScenarioResult` in KG).
- Decisions about what evidence an authority must accept.
- Digital Twin rendering and UI.
- Work Packages, Tasks, Deliverables, and Partner data.

---

## Repository Structure

```
warrant-kg-ontology/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODEOWNERS
├── .gitignore
├── ontology/                   ← OWL Turtle module files
│   ├── warrant-core.ttl        ← shared superclasses, context, controlled vocabularies
│   ├── warrant-davom.ttl       ← vessel operational model (DAVOM)
│   ├── warrant-observation.ttl ← metrics, observers, detection events
│   ├── warrant-cdm.ttl         ← causal dependability model (STPA/HAZOP)
│   ├── warrant-assurance.ttl   ← assurance attributes, scores, degradation
│   ├── warrant-di.ttl          ← dependability index, risk propagation
│   ├── warrant-scenario.ttl    ← what-if scenario semantics
│   ├── warrant-mitigation.ttl  ← mitigation rules, failover, advisory actions
│   ├── warrant-digital-twin.ttl← DT interface, views, layers
│   ├── warrant-all.ttl         ← aggregated entry point (imports all modules)
│   └── catalog.xml             ← Protégé/OWLAPI IRI→file mapping
├── examples/                   ← instance data (data namespace)
│   ├── example-gnss-failover.ttl           ← LL4 MAI-W GNSS loss
│   ├── example-communication-degradation.ttl ← LL4 comm degradation
│   ├── example-smart-container-fire.ttl    ← LL2 AELER fire detection
│   ├── example-roc-handover.ttl            ← LL4 Use Case 2 handover
│   └── example-ecdis-spoofing.ttl          ← LL1 AIS spoofing
├── shapes/
│   └── warrant-core-shapes.ttl ← SHACL validation shapes (13 shapes)
├── queries/
│   └── competency-queries.sparql ← 10 competency queries
├── docs/
│   ├── modelling-conventions.md
│   ├── namespace-policy.md
│   ├── kg-boundary.md
│   ├── external-ontology-alignment.md
│   ├── stack-overview.md
│   └── modules/                ← per-module pages (generated) + warrant-integration.md
├── scripts/
│   ├── validate_turtle.py      ← Turtle syntax + namespace policy + SHACL (--shacl)
│   ├── merge_ontology.py       ← module merge → dist/
│   ├── run_queries.py          ← competency queries against merged ontology + examples
│   └── generate_module_docs.py ← regenerate docs/modules/*.md from the .ttl
├── tests/
├── dist/                       ← BUILD ARTEFACT; gitignored; never commit
└── .github/workflows/
    └── validate-ontology.yml   ← CI validation on PR and push
```

---

## How to Load the Ontology

### Load the full ontology in one operation (rdflib)

```python
import rdflib
g = rdflib.Graph()
g.parse("ontology/warrant-all.ttl", format="turtle")
```

### Load in Protégé / OWLAPI (with catalog.xml)

1. Open `ontology/warrant-all.ttl` in Protégé.
2. Protégé will use `ontology/catalog.xml` to resolve relative `owl:imports` to local files.
3. All 9 modules load automatically.

### Build merged file (for inspection)

```bash
pip install rdflib
python scripts/merge_ontology.py
# Output: dist/warrant-all-merged.ttl
```

---

## Module Ontology IRIs and Prefixes

| Module | IRI | Prefix |
|--------|-----|--------|
| Core | `https://warrant-project.eu/ontology/core` | `warrant:` |
| DAVOM | `https://warrant-project.eu/ontology/davom` | `davom:` |
| Observation | `https://warrant-project.eu/ontology/observation` | `obs:` |
| CDM | `https://warrant-project.eu/ontology/cdm` | `cdm:` |
| Assurance | `https://warrant-project.eu/ontology/assurance` | `assr:` |
| Dependability Index | `https://warrant-project.eu/ontology/dependability-index` | `di:` |
| Scenario | `https://warrant-project.eu/ontology/scenario` | `scen:` |
| Mitigation | `https://warrant-project.eu/ontology/mitigation` | `mit:` |
| Digital Twin | `https://warrant-project.eu/ontology/digital-twin` | `dt:` |

---

## Instance Namespace Policy

Data instances use a separate namespace from ontology terms:

```
https://warrant-project.eu/data/{context}#
```

| Context | Living Lab |
|---------|-----------|
| `ll1` | LL1 Danaos Containership |
| `ll2` | LL2 AELER Smart Container |
| `ll3` | LL3 DST NOVA Vessel |
| `ll4` | LL4 Seafar MAI-W / ROC |

Example:
```turtle
@prefix ll4: <https://warrant-project.eu/data/ll4#> .
ll4:MAI_W a davom:Vessel .
```

Never use module namespaces (`obs:`, `cdm:`, `davom:`) for instance IRIs.

---

## Using the Example Files

Example files in `examples/` illustrate the GNSS failover, communication degradation, smart container fire, ROC handover, and ECDIS spoofing scenarios. Load them together with the ontology:

```python
import rdflib
g = rdflib.Graph()
g.parse("ontology/warrant-all.ttl", format="turtle")
g.parse("examples/example-gnss-failover.ttl", format="turtle")
```

---

## Validation

```bash
pip install rdflib pyshacl
python scripts/validate_turtle.py --shacl     # syntax, namespace policy, SHACL over all examples
python scripts/merge_ontology.py && python scripts/run_queries.py   # competency queries
```

CI runs the syntax check automatically on every PR and push to `main`/`develop`.

## Methodology alignment

The ontology is aligned with the WARRaNT framework paper (*A Knowledge-Graph and Digital-Twin Framework for Continuous Dependability Assurance of Waterborne Cyber-Physical Systems*, draft v0409, September 2026). The mapping of the paper's mechanisms to modules, the module dependency graph, the cross-module property table and the design constraints are in [docs/modules/warrant-integration.md](docs/modules/warrant-integration.md). `examples/example-gnss-failover.ttl` is the reference instantiation cited by the paper.

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, PR process, how to propose classes and properties, and mandatory modelling principles.

See [docs/modelling-conventions.md](docs/modelling-conventions.md) for all naming and modelling rules.

---

## Version

`0.10-poc` — Pre-consortium-baseline proof of concept, aligned with the framework paper (September 2026). See [CHANGELOG.md](CHANGELOG.md).
Target consortium baseline release: `v0.1.0` (planned).

<img src="https://warrant-project.eu/wp-content/uploads/2025/07/europeanlogo.png" alt="Co-funded by the European Union" width="366" height="83">
