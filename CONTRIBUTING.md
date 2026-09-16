# Contributing to the WARRaNT KG Ontology

This guide describes how consortium partners contribute to the WARRaNT Knowledge Graph ontology repository.

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| New class/property | `feat/<module>/<short-name>` | `feat/cdm/environmental-constraint` |
| Bug/syntax fix | `fix/<module>/<issue>` | `fix/observation/produces-range` |
| Documentation | `docs/<topic>` | `docs/namespace-policy-update` |
| Example scenario | `example/<living-lab>/<scenario>` | `example/ll4/handover-v2` |

Work on `develop`; merge to `main` only for tagged releases.

---

## Pull Request Process

1. Branch from `develop`.
2. Run validation locally: `python scripts/validate_turtle.py --shacl` and `python scripts/run_queries.py` (after `python scripts/merge_ontology.py`).
3. If you changed a module, regenerate its documentation: `python scripts/generate_module_docs.py` (CI checks with `--check`).
4. Open a PR to `develop` with a clear description.
5. Request review from the module CODEOWNER.
6. Address all comments; at least one approval required.
7. Squash-merge to `develop`.

---

## How to Add an Example Individual

1. Use the instance namespace `https://warrant-project.eu/data/{context}#` — **never** the ontology module namespaces.
2. Create a new file in `examples/` or extend an existing file.
3. Use `cdm:hasDeviationType` with named `cdm:DeviationType` individuals — never instantiate deprecated deviation subclasses.
4. Use `di:hasDIState` with named `di:DependabilityIndexState` individuals — never subclass.
5. Follow the DetectionEvent production chain: `AnalyticalService → producesDetectionEvent → DetectionEvent → detectionEventDetects → Deviation`. A health event that does not identify a deviation is an `obs:HealthEvent` or `obs:PredictedConditionEvent`.
6. Assign operational states attribute-wise (`di:hasAttributeState` from `di:DIThreshold`s), never from the DI value.
7. Give scenario-specific individuals (indices, edges, events, triggers) scenario-specific local names so that files sharing a Living Lab namespace can be loaded together.
8. Run `python scripts/validate_turtle.py --shacl` before submitting; the example must conform to the shapes.

---

## How to Run Validation

```bash
# Install rdflib and pySHACL (once)
pip install rdflib pyshacl

# Validate all Turtle files (ontology/, examples/, shapes/) and run SHACL over the examples
python scripts/validate_turtle.py --shacl

# Build merged ontology and run the competency queries (regression test)
python scripts/merge_ontology.py
python scripts/run_queries.py

# Regenerate / check the per-module documentation
python scripts/generate_module_docs.py
python scripts/generate_module_docs.py --check
```

SHACL validation merges the nine modules into the data graph and runs with inference **off**: RDFS inference over `rdfs:range` would re-type individuals and mask `sh:class` violations.

---

## Mandatory Modelling Principles (must not be violated)

1. Human operators are **not components**. `davom:HumanOperator` and `davom:HumanOperatorRole` subclass `warrant:AgentEntity`.
2. Components do not generate metrics. Use `obs:hasDependabilityMetric` on operational entities.
3. Deviation typing: use `cdm:hasDeviationType` with `cdm:DeviationType` named individuals. Creating new deviation subclasses is **prohibited**.
4. Operational state: use named `di:DependabilityIndexState` individuals. Subclassing is **prohibited**. State is assigned attribute-wise from thresholds and reported with the DI; the DI value never determines it, and responses are invoked by a `di:ResilienceTrigger`, not by a DI value.
5. `obs:produces` range: `obs:Status` or `obs:VirtualSensorOutput` only. `cdm:Deviation` must not appear in the range.
6. The `warrant:VisualisableEntity` range class is defined in `warrant-core.ttl`. Do not redefine it elsewhere.
7. `warrant:VoyageSegment` and `warrant:OperationalMode` belong in `warrant-core.ttl`, not the CDM module.
8. Raw telemetry stays outside the KG; use `obs:hasExternalRecordReference` and `obs:hasExternalTimeSeriesId`.
9. Example individuals use `https://warrant-project.eu/data/{context}#` namespaces.
10. No computation is encoded in the ontology (fusion, node score, typed propagation, aggregation, state assignment, triggers, response ranking, Assurance Level, Certification Readiness). Store inputs, governed configuration with version and approval, results with timestamp and `warrant:CalculationMethod`, and audit events.
11. Every `davom:Dependency` carries a canonical `davom:hasDependencyType`; `dependencySource` is the upstream provider and `dependencyTarget` the downstream consumer.
12. `di:DIForecast` is owned by `warrant-di` and produced by the Digital Twin; no module imports `warrant-digital-twin`.
13. A module never declares terms in another module's namespace, and only asserts axioms about terms of modules it imports.

---

## Consortium Partner Requests

Partners without direct repository access should submit change requests as GitHub issues using the templates below.

---

## Issue Templates

### Modelling issue
```
**Module**: warrant-[module]
**Issue**: [description of the modelling problem]
**Affected class/property**:
**Proposed fix**:
```

### Example scenario request
```
**Living Lab**: LL1 / LL2 / LL3 / LL4
**Scenario description**:
**Key individuals needed**:
**Deviations involved (guideword)**:
```

### Bug / syntax issue
```
**File**:
**Line (approx)**:
**Error message**:
**Expected behaviour**:
```

---

## Deprecation Policy

Once a class or property is marked `owl:deprecated true`, it remains in the ontology for **one full minor release** before removal. This protects partner data pipelines that may reference deprecated terms. Partners should migrate to the replacement pattern during the deprecation window.

Current deprecated terms: see [CHANGELOG](CHANGELOG.md).
