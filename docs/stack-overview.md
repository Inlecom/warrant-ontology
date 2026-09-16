# WARRaNT KG Ontology — Stack & Structure Overview

> Prepared for WARRaNT consortium partners · September 2026
> Repository: https://gitlab.com/konnecta/projects/warrant-ontology
> Version: 0.10-poc

---

## 1. What is this repository?

The WARRaNT KG Ontology repository is the **shared semantic foundation** for the WARRaNT Knowledge Graph. It provides a formal, machine-readable vocabulary that all consortium tools — the Digital Twin, the DI calculation service, the scenario engine, and the analytical services — use to represent and exchange dependability knowledge about waterborne digital systems.

In plain terms: it defines what words like *Deviation*, *Hazard*, *Dependability Index*, *AnalyticalService*, and *FailoverProcedure* mean, how they relate to each other, and what data they carry. Every partner building or consuming the WARRaNT KG works from this shared definition.

---

## 2. Ontology at a glance

The ontology covers 9 topic areas (DAVOM, Observation, CDM, Assurance, DI, Scenario, Mitigation, Digital Twin, and a shared Core), totalling **200 classes · 194 object properties · 128 datatype properties · 70 named individuals · 3,094 triples** across 9 module files (15 terms deprecated pending removal). Five Living Lab example files (LL1–LL4, 2,577 triples) demonstrate realistic scenarios; the LL4 GNSS failover example instantiates every layer of the framework. The ontology content is covered in `docs/modules/`; this document focuses on the repository infrastructure.

---

## 3. Repository structure

```
warrant-kg-ontology/
|
+-- ontology/                    <- OWL/Turtle source files (the ontology)
|   +-- warrant-core.ttl
|   +-- warrant-davom.ttl
|   +-- warrant-observation.ttl
|   +-- warrant-cdm.ttl
|   +-- warrant-assurance.ttl
|   +-- warrant-di.ttl
|   +-- warrant-scenario.ttl
|   +-- warrant-mitigation.ttl
|   +-- warrant-digital-twin.ttl
|   +-- warrant-all.ttl          <- imports all 9 modules (single entry point)
|   \-- catalog.xml              <- Protege / OWLAPI IRI-to-file mapping
|
+-- examples/                    <- Living Lab instance data (LL1-LL4)
|   +-- example-gnss-failover.ttl
|   +-- example-communication-degradation.ttl
|   +-- example-roc-handover.ttl
|   +-- example-smart-container-fire.ttl
|   \-- example-ecdis-spoofing.ttl
|
+-- shapes/
|   \-- warrant-core-shapes.ttl  <- SHACL validation shapes (13 shapes)
|
+-- queries/
|   \-- competency-queries.sparql <- 10 competency queries (regression tests)
|
+-- docs/
|   +-- visualise.html           <- interactive graph (D3 + N3.js, runs offline)
|   +-- stack-overview.md        <- this document
|   +-- modelling-conventions.md
|   +-- namespace-policy.md
|   +-- kg-boundary.md
|   +-- external-ontology-alignment.md
|   +-- modules/                 <- per-module pages (generated from the .ttl) and
|   |                               warrant-integration.md (data flow, constraints)
|   \-- html/                    <- WIDOCO HTML reference docs (generated; gitignored)
|
+-- scripts/
|   +-- validate_turtle.py       <- parse all TTL, check namespace policy, --shacl
|   +-- merge_ontology.py        <- merge 9 modules -> dist/warrant-all-merged.ttl
|   +-- run_queries.py           <- run the competency queries against merged + examples
|   +-- generate_module_docs.py  <- regenerate docs/modules/*.md (--check in CI)
|   +-- prepare_widoco.py        <- prepare single-ontology file for WIDOCO
|   +-- generate_docs.ps1        <- Windows: run WIDOCO via jar or Docker
|   \-- generate_docs.sh         <- Linux/macOS/CI: run WIDOCO via jar or Docker
|
+-- serve.ps1                    <- start local HTTP server (port 8000)
|
+-- dist/                        <- BUILD ARTEFACT - gitignored, never committed
|   +-- warrant-all-merged.ttl   <- all 9 modules merged
|   \-- warrant-widoco-input.ttl <- cleaned single-ontology file for WIDOCO
|
+-- .gitlab-ci.yml               <- GitLab CI pipeline
+-- .github/workflows/           <- GitHub Actions (kept for potential mirroring)
+-- README.md
+-- CONTRIBUTING.md
+-- CHANGELOG.md
\-- CODEOWNERS                   <- routes MR reviews to module owners
```

---

## 4. Toolchain

Four tools cover the full workflow from source editing to published documentation.

### 4.1 Validation

```powershell
python scripts/validate_turtle.py --shacl
```

- Parses every `.ttl` file under `ontology/`, `examples/` and `shapes/` using rdflib
- Reports triple count per file
- Warns if any example individual IRI uses an ontology module namespace (namespace policy check)
- Checks every example assertion against the declared `rdfs:domain` and `rdfs:range`, following subclasses and unions
- With `--shacl`: validates every example against the shapes with pySHACL (modules merged into the data graph, inference off)
- Exits 0 (all pass) or 1 (any failure or violation)

**Current status:** 16 files · 6,020 triples · 0 failures · zero domain and range violations · all five examples conform to the 13 shapes · all 10 competency queries return rows

### 4.2 Merge

```powershell
python scripts/merge_ontology.py
python scripts/merge_ontology.py --include-examples
```

Loads all 9 modules in dependency order and writes `dist/warrant-all-merged.ttl`. Required before running the interactive graph or WIDOCO. The `dist/` folder is gitignored — it is a build artefact, never committed.

### 4.3 Interactive Graph — `docs/visualise.html`

A fully **client-side** single-page application. Nothing is sent to an external server.

| Technology | Role |
|------------|------|
| N3.js | Parses Turtle directly in the browser |
| D3.js | Renders a force-directed graph |
| Python HTTP server | Serves local files so AJAX fetches work |

```powershell
.\serve.ps1
# then open: http://localhost:8000/docs/visualise.html
```

What you can do:
- Click any of the **9 module buttons** to load that module's classes and properties
- Click **Full Ontology** to load all 9 modules (3,000+ triples)
- Click any **Living Lab example button** (LL1–LL4) — loads instance data overlaid on the full ontology so individual nodes connect to their classes
- Pan, zoom, drag nodes to explore
- Click any node — right panel shows IRI, module, label, and full description
- Toggle labels on/off; Fit button re-centres the graph
- Nodes are colour-coded by module; deprecated classes shown in dashed red

### 4.4 WIDOCO Reference Documentation — `docs/html/index-en.html`

Generates a full HTML reference site (one page per class/property) from the ontology.

```powershell
.\scripts\generate_docs.ps1 -UseJar   # requires Java + scripts/widoco.jar
.\scripts\generate_docs.ps1            # requires Docker Desktop
```

Internal pipeline:

```
merge_ontology.py  -->  dist/warrant-all-merged.ttl
        |
prepare_widoco.py  -->  dist/warrant-widoco-input.ttl
   (strips 9 module ontology headers, adds rdfs:isDefinedBy to every term,
    injects single ontology IRI so WIDOCO recognises all terms as local)
        |
    WIDOCO jar      -->  docs/html/
```

Access via the HTTP server (WIDOCO uses AJAX to load page sections):

```
http://localhost:8000/docs/html/index-en.html
```

Sections generated:
- **Overview** — ontology metadata, version, authors, download links
- **Cross-reference** — Classes (200) · Object Properties (194) · Data Properties (128) · Named Individuals (70)
- Each entry displays the `rdfs:label` and full `rdfs:comment` from the TTL source

---

## 5. CI/CD — GitLab Pipeline

Repository: `git@gitlab.com:konnecta/projects/warrant-ontology.git`

The `.gitlab-ci.yml` runs automatically on every push and merge request:

```
Push to any branch / Merge Request
             |
             v
  +----------------------+
  |  validate-turtle     |  python scripts/validate_turtle.py
  |  (all branches/MRs)  |  Fails if any .ttl has a syntax error or
  |                      |  an example uses a module namespace for instances
  +----------+-----------+
             | pass
             v
  +----------------------+
  |   build-merged       |  merge_ontology.py + prepare_widoco.py
  |  (main + develop)    |  dist/ saved as downloadable pipeline artefact
  +----------------------+
```

**What consortium partners see in GitLab:**
- Green check / red cross next to every commit
- Merge Request blocked until `validate-turtle` passes
- `build-merged` job produces a **Download artefact** button — partners can download `dist/warrant-all-merged.ttl` directly from the CI run, without installing Python locally

---

## 6. How to contribute

Full details in `CONTRIBUTING.md`. Short version:

| Action | How |
|--------|-----|
| Propose a new class | Open a GitLab issue using the *New class proposal* template |
| Propose a new property | Open a GitLab issue using the *New property proposal* template |
| Add a Living Lab example | Add `examples/example-<ll>-<scenario>.ttl` using the data namespace |
| Fix a modelling issue | Branch from `develop` → MR → CODEOWNER review → merge |

Module ownership is defined in `CODEOWNERS`. Each of the 9 ontology modules is assigned to a team. MRs touching a module are automatically routed to that team for review.

---

## 7. Accessing the repository

```bash
git clone git@gitlab.com:konnecta/projects/warrant-ontology.git
cd warrant-ontology

# One-time setup
pip install rdflib

# Validate
python scripts/validate_turtle.py

# Build merged ontology (needed for graph + WIDOCO)
python scripts/merge_ontology.py

# Start docs server (Windows)
.\serve.ps1

# Open in browser
# http://localhost:8000/docs/visualise.html
# http://localhost:8000/docs/html/index-en.html
```

---

## 8. Version and roadmap

| Version | Status | Notes |
|---------|--------|-------|
| 0.9-poc | Superseded | 9 modules · 5 LL examples · CI pipeline · interactive graph · WIDOCO docs |
| **0.10-poc** | Current | Aligned with the framework paper (Sept 2026): health events and node health monitors, attribute-wise state, typed propagation, forecasts and triggers, REDS/IRDS records, Living Dependability Case; 13 shapes · 10 queries · generated module docs |
| **v0.1.0** | Planned | First consortium baseline release · removal of deprecated terms · LL3 example |
| **v0.2.0** | Planned | Normative SOSA/SSN/SACM alignment · additional SPARQL queries |

**Known limitations in 0.10-poc:**
- All numerical computation is external; the KG stores inputs, governed configuration and results only
- The mission-phase / operating-mode axis is expressed by scoping weights and thresholds with `warrant:appliesUnder` to an `OperationalMode` or `VoyageSegment`; the schema does not yet fix which, pending clarification of the paper's terminology
- LL3 (NOVA) examples not yet included; only the LL4 GNSS example exercises the full loop
- DLT-based identity management (KNT contribution) not yet modelled
- Deprecated terms (ten `cdm:*Deviation` subclasses, `di:hasThreshold`/`hasLowerThreshold`/`hasUpperThreshold`/`hasSystemWeight`, `dt:ScenarioExecutionState`) remain for one minor release

---

*WARRaNT KG Ontology repository · September 2026*
*https://gitlab.com/konnecta/projects/warrant-ontology*
