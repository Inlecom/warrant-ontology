# WARRaNT KG Ontology

Formal OWL/RDF ontology for the **WARRaNT Knowledge Graph** — a Horizon Europe RIA project (101202581) developing a federated methodology and tools to assure the dependability of waterborne digital systems.

https://warrant-project.eu/

---

## Purpose

The WARRaNT ontology provides a shared semantic vocabulary for:

- **Vessel operational structure** (DAVOM): vessels, functions, systems, components, data flows, communication links, human operator roles.
- **Causal dependability modelling** (CDM / STPA / HAZOP): deviations, hazards, risks, unsafe control actions, causal chains.
- **Assurance and dependability metrics**: assurance attributes, scores, degradation, weights.
- **Dependability Index** with risk propagation: node DI, propagated risk, system DI.
- **Scenarios**: what-if cases including cyberattack, failure, degraded operation, handover.
- **Mitigation and failover**: rules, advisory actions, failover procedures.
- **Digital Twin interface**: views, visualisation layers, decision-support, live update channels.

---

## What is Inside the KG

- Semantic class and property definitions.
- Controlled vocabularies: HAZOP deviation types (`cdm:DeviationType`), DI states (`di:DependabilityIndexState`), operational modes (`warrant:OperationalMode`).
- Latest states, detection events, assurance scores, DI values.
- Scenario semantics and execution results.
- Traceability links from detection to DI state.
- References to external time-series stores.

## What is Outside the KG

- Raw high-frequency sensor telemetry (use `obs:hasExternalTimeSeriesId`).
- DI numerical computation (external service stores results in KG).
- Scenario engine execution (external engine stores `scen:ScenarioResult` in KG).
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
│   └── warrant-core-shapes.ttl ← SHACL validation shapes (starter set)
├── queries/
│   └── competency-queries.sparql ← 6 competency queries
├── docs/
│   ├── modelling-conventions.md
│   ├── namespace-policy.md
│   ├── kg-boundary.md
│   └── external-ontology-alignment.md
├── scripts/
│   ├── validate_turtle.py      ← Turtle syntax + namespace policy checker
│   └── merge_ontology.py       ← module merge → dist/
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
pip install rdflib
python scripts/validate_turtle.py
```

CI runs this automatically on every PR and push to `main`/`develop`.

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, PR process, how to propose classes and properties, and mandatory modelling principles.

See [docs/modelling-conventions.md](docs/modelling-conventions.md) for all naming and modelling rules.

---

## Version

`0.9-poc` — Pre-consortium-baseline proof of concept.
Target consortium baseline release: `v0.1.0` (planned).

<img src="https://warrant-project.eu/wp-content/uploads/2025/07/europeanlogo.png" alt="Co-funded by the European Union" width="366" height="83">
