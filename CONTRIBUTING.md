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
2. Run validation locally: `python scripts/validate_turtle.py`
3. Open a PR to `develop` with a clear description.
4. Request review from the module CODEOWNER.
5. Address all comments; at least one approval required.
6. Squash-merge to `develop`.

---

## How to Add an Example Individual

1. Use the instance namespace `https://warrant-project.eu/data/{context}#` — **never** the ontology module namespaces.
2. Create a new file in `examples/` or extend an existing file.
3. Use `cdm:hasDeviationType` with named `cdm:DeviationType` individuals — never instantiate deprecated deviation subclasses.
4. Use `di:hasDIState` with named `di:DependabilityIndexState` individuals — never subclass.
5. Follow the DetectionEvent production chain: `AnalyticalService → producesDetectionEvent → DetectionEvent → detectionEventDetects → Deviation`.
6. Run `python scripts/validate_turtle.py` before submitting.

---

## How to Run Validation

```bash
# Install rdflib (once)
pip install rdflib

# Validate all Turtle files
python scripts/validate_turtle.py

# Build merged ontology
python scripts/merge_ontology.py
python scripts/merge_ontology.py --include-examples
```

---

## Mandatory Modelling Principles (must not be violated)

1. Human operators are **not components**. `davom:HumanOperator` and `davom:HumanOperatorRole` subclass `warrant:AgentEntity`.
2. Components do not generate metrics. Use `obs:hasDependabilityMetric` on operational entities.
3. Deviation typing: use `cdm:hasDeviationType` with `cdm:DeviationType` named individuals. Creating new deviation subclasses is **prohibited**.
4. DI state: use named `di:DependabilityIndexState` individuals. Subclassing is **prohibited**.
5. `obs:produces` range: `obs:Status` or `obs:VirtualSensorOutput` only. `cdm:Deviation` must not appear in the range.
6. The `warrant:VisualisableEntity` range class is defined in `warrant-core.ttl`. Do not redefine it elsewhere.
7. `warrant:VoyageSegment` and `warrant:OperationalMode` belong in `warrant-core.ttl`, not the CDM module.
8. Raw telemetry stays outside the KG; use `obs:hasExternalRecordReference` and `obs:hasExternalTimeSeriesId`.
9. Example individuals use `https://warrant-project.eu/data/{context}#` namespaces.

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
