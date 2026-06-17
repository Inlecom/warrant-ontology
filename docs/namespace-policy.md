# WARRaNT KG Ontology — Namespace Policy

Version 0.9-poc | 2026-06-05

---

## Base URI Policy

All WARRaNT ontology IRIs use the base `https://warrant-project.eu/`. The domain must be maintained by the project coordinator for the ontology to resolve. Persistent URI resolution is deferred to v1.0.0.

---

## Module Namespaces

| Module | Namespace | Prefix |
|--------|-----------|--------|
| Core | `https://warrant-project.eu/ontology/core#` | `warrant:` |
| DAVOM | `https://warrant-project.eu/ontology/davom#` | `davom:` |
| Observation | `https://warrant-project.eu/ontology/observation#` | `obs:` |
| CDM | `https://warrant-project.eu/ontology/cdm#` | `cdm:` |
| Assurance | `https://warrant-project.eu/ontology/assurance#` | `assr:` |
| Dependability Index | `https://warrant-project.eu/ontology/dependability-index#` | `di:` |
| Scenario | `https://warrant-project.eu/ontology/scenario#` | `scen:` |
| Mitigation | `https://warrant-project.eu/ontology/mitigation#` | `mit:` |
| Digital Twin | `https://warrant-project.eu/ontology/digital-twin#` | `dt:` |

---

## Instance (Data) Namespace Policy

Runtime data instances **MUST** use the data namespace pattern:

```
https://warrant-project.eu/data/{context}#
```

| Context | Living Lab | Namespace |
|---------|-----------|-----------|
| `ll1` | LL1 Danaos Containership | `https://warrant-project.eu/data/ll1#` |
| `ll2` | LL2 AELER Smart Container | `https://warrant-project.eu/data/ll2#` |
| `ll3` | LL3 DST NOVA Autonomous Vessel | `https://warrant-project.eu/data/ll3#` |
| `ll4` | LL4 Seafar MAI-W / ROC | `https://warrant-project.eu/data/ll4#` |

Ontology terms (classes, properties, named controlled-vocabulary individuals) use module namespaces. Data instances representing real or simulated entities use data namespaces.

---

## Prefix Conventions

Prefixes must be lowercase, short (≤ 6 characters), and stable across all files. The `warrant:` prefix is reserved for the core module; all other modules use their own distinct prefixes.

---

## Version IRI Policy

Version IRIs follow the pattern: `https://warrant-project.eu/ontology/{module}/{major}.{minor}`. Version-specific IRIs are not used until v1.0.0. Until then, `owl:versionInfo` carries the version string (e.g. `"0.9-poc"`).

---

## Naming Rules for Local Names

- Classes: PascalCase, English, no abbreviations (e.g. `DetectionEvent`, not `DetEvt`).
- Properties: camelCase (e.g. `hasDeviationType`, `producesDetectionEvent`).
- Named individuals (controlled vocabulary): UPPER_CASE for HAZOP guidewords (`cdm:UNAVAILABLE`); PascalCase for state individuals (`di:CriticalState`).

---

## Rules for Deprecating or Renaming Terms

1. Mark the term: `owl:deprecated true ; rdfs:comment "Deprecated. Use X instead."`.
2. The term remains for one full minor release.
3. Document the deprecation in CHANGELOG.md.
4. Notify all partners through the consortium communication channel.
5. Remove in the next minor release.

---

## Rules for Adding New Modules

1. Agree the module scope with the KG coordination team.
2. Choose a new unique namespace and prefix.
3. Add the module to `warrant-all.ttl` (owl:imports).
4. Add an entry to `catalog.xml`.
5. Document in README.md and namespace-policy.md.
6. Add a CODEOWNER entry.

---

## Rules for External Ontology Alignment

In v0.1.0, all external ontology alignment is **informative only** (rdfs:comment annotations). No `owl:equivalentClass`, `owl:sameAs`, or property substitutions are added. Normative alignment is deferred to v0.2.0 pending consortium agreement. See `docs/external-ontology-alignment.md`.

---

## Build Artefact Namespace

`dist/warrant-all-merged.ttl` is a CI build artefact produced by `scripts/merge_ontology.py`. It is listed in `.gitignore` and must never be committed. It must never be used as a namespace source. Prefer `ontology/warrant-all.ttl` with `owl:imports` for loading the full ontology.

---

## Informative External Ontology Alignment Annotations

The following informative alignments are recorded as `rdfs:comment` annotations in the module files. No normative assertions are made.

| WARRaNT term | External term | Fit |
|---|---|---|
| `obs:Observer` | `sosa:Sensor` (W3C SOSA/SSN) | close |
| `obs:Measurement` | `sosa:Observation` | close |
| `obs:Metric` | `ssn:Property` / `sosa:ObservableProperty` | close |
| `obs:hasValue` | `sosa:hasSimpleResult` | exact |
| `obs:hasUnit` | `qudt:unit` (QUDT) | close |
| `obs:hasTimestamp` | `sosa:resultTime` | exact |
| `mit:MitigationAction` | `saref:Command` (SAREF4ENER) | partial |
| `davom:ControlAction` | `saref:Command` | partial |
| `assr:Evidence` | `gsn:Evidence` (GSN/SACM) | close |
