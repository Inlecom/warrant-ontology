# Open Issues — WARRaNT KG Ontology

Working register of known gaps, decisions awaiting other partners, and
housekeeping. Maintained alongside the code: an entry is added when something
is found and removed when it is closed, with the closing commit noted.

Last reviewed: 2026-09-16, against `develop` at the merge of pull request #2.
Repository state at that review: 16 files, 7,641 triples, zero parse failures,
zero domain and range violations, all five examples conforming to the 13
shapes, all 10 competency queries returning rows, module docs current.

Severity is about consequence, not effort:

- **Blocking** — the repository asserts something that is wrong, or a stated
  constraint is not met. Fix before the next release.
- **Gap** — something the framework requires that is modelled nowhere yet.
- **Decision** — waiting on a partner or on the paper authors. We cannot close
  it ourselves.
- **Housekeeping** — tidiness, no effect on correctness.

---

## Blocking

### B1. Five deviations are asserted with no detection event

Design Constraint 1 says every `cdm:Deviation` is reached through an
`obs:DetectionEvent`. Five are not:

| File | Deviation |
|---|---|
| `examples/example-smart-container-fire.ttl` | `DevDownstreamLess` |
| `examples/example-smart-container-fire.ttl` | `DevPowerDegraded` |
| `examples/example-smart-container-fire.ttl` | `DevSensorNoisy` |
| `examples/example-smart-container-fire.ttl` | `DevUntrustedAlarmSource` |
| `examples/example-roc-handover.ttl` | `LateHandoverDeviation` |

Neither SHACL nor the domain and range check catches this, because the
constraint is about absence. It needs either a shape with a minimum count or a
competency query used as a gate. Owners: AELER for LL2, Seafar for the ROC
handover.

### B2. The competency queries do not run in CI

`queries/competency-queries.sparql` is treated as the regression suite, but
neither `.gitlab-ci.yml` nor `.github/workflows/validate-ontology.yml` runs
`scripts/run_queries.py`. A query that silently stops returning rows passes
both pipelines. This is how a modelling regression would reach `develop`
unnoticed, and it is the cheapest fix on this list: add the script to both
pipelines and fail the job on any query returning zero rows.

---

## Gaps

### G1. LL1 has no observation layer beneath its attribute values

Seven metrics are declared in `examples/example-ecdis-spoofing.ttl` and not one
of them carries a measurement. The sixteen attribute values are therefore
asserted directly, with an analytical service named as the source but nothing
observable underneath. See L2 below for what finalising LL1 requires.

### G2. No LL3 example

The DST NOVA vessel scenario is not modelled. LL3 is the only living lab with
no instance data.

### G3. Fifteen deprecated terms await removal

Ten `cdm:*Deviation` subclasses, `di:hasThreshold`, `di:hasLowerThreshold`,
`di:hasUpperThreshold`, `di:hasSystemWeight`, `dt:ScenarioExecutionState`.
Deprecated in 0.9-poc and 0.10-poc, scheduled for removal at v0.1.0. Removing
them is a breaking change and needs a note to consumers first.

---

## Decisions awaiting others

### D1. Mission phase versus operating mode

The paper uses the two terms interchangeably. Weights, thresholds and floors
are scoped with `warrant:appliesUnder` to either an `OperationalMode` or a
`VoyageSegment`, and the schema deliberately does not yet fix which. To be
settled with the paper authors.

### D2. The hazard class set

Three classes are modelled as named in the paper, with `CYBER_THREAT` also
propagating over the cyber dependency type. To be confirmed by the DI team.

### D3. Claim statuses and the Assurance Level weight set

Three claim statuses, with revalidation folded into supported. The weight set
is a five-component structure. Both to be confirmed by the assurance team.

### D4. Paper corrections owed to the authors

The companion note listing text in draft v0409 that the alignment makes stale,
and the ambiguities the ontology could not resolve, is held by KNT outside this
repository. It has not been delivered to the authors.

---

## LL1 finalisation

`examples/example-ecdis-spoofing.ttl` validates, exercises every layer the
framework defines, and every index in it is derivable by hand. It is not
final. Two separate things are outstanding, and they have different owners.

### L1. Forty-eight policy values need Danaos approval

These are the numbers chosen so the example is arithmetically complete. They
are plausible, not authoritative, and each carries
`warrant:hasApprovalStatus "PROPOSED"`:

| Count | Artefact | What Danaos needs to state |
|---|---|---|
| 16 | `assr:AssuranceWeight` | Attribute weights per node, per operating mode |
| 16 | `di:DIThreshold` | The four ordered state thresholds per attribute, per node |
| 4 | `di:DIWeight` | How node indices roll up to the vessel index |
| 4 | `assr:EvidenceObligation` | Which evidence is required, and its validity period |
| 3 | `assr:AssuranceClaim` | Whether the claims are worded as Danaos would state them |
| 1 | `di:SupervisionConfiguration` | Management floor, trend window and slope, prediction horizon |
| 1 | `di:RiskPropagationParameter` | Damping factor for cyber propagation |
| 1 | `mit:DecisionConfiguration` | The REDS cost and penalty weights |
| 1 | `assr:Requirement` | The company position cross-check interval and accepted sources |
| 1 | `assr:AssuranceLevelWeightSet` | The five Assurance Level component weights |

Until these are replaced, the file demonstrates the mechanism but states
nothing about the real vessel's dependability. This is the whole of what
blocks finalisation from the Danaos side.

### L2. What is modelled nowhere in LL1

These are ours, not Danaos's, and none of them are required for the file to be
correct. They are what separates LL1 from the LL4 reference example:

- **Measurements.** Seven metrics, zero measurements. Attribute values would be
  better grounded if at least the GNSS and AIS integrity metrics carried
  observed values that the health events reference.
- **Virtual sensing.** No `obs:VirtualSensor` or `obs:substitutesFor`, although
  the scenario is exactly one where a substitute traffic picture matters.
- **Predicted conditions.** No `obs:PredictedConditionEvent`, so LL1 raises
  attribute-breach and sustained-decline triggers but never a predicted floor
  crossing, and the prediction horizon in its configuration is unused.
- **The scenario layer.** No `scen:DegradedOperationScenario`,
  `scen:ScenarioExecution` or `scen:ScenarioResult`. The what-if forecasts
  attached to the three response evaluations are asserted rather than produced
  by a modelled scenario run.
- **Recovery effects.** No `mit:RecoveryEffect` on the executed response.
- **The Digital Twin is a stub.** One `dt:DigitalTwin` individual with no
  views, layers or decision support, although it is named as the producer of
  four forecasts.

A reasonable definition of done: L1 closed by Danaos, plus measurements and the
scenario layer from L2. Virtual sensing, predicted conditions, recovery effects
and the twin's views are worth having but are not what makes the example
truthful.

---

## Housekeeping

### H1. The stack overview names the wrong repository

`docs/stack-overview.md` states the repository is
`gitlab.com/konnecta/projects/warrant-ontology`, describes the GitLab pipeline
as the CI, and calls GitHub Actions a mirror kept for potential use. The work
is now happening on GitHub. Both CI configurations exist and both are current,
so nothing is broken, but the document misdirects a new partner.

### H2. Working notes are untracked and not ignored

The `Claude outputs/` folder appears in every `git status` and is not covered
by `.gitignore`, so it can be committed by accident.

---

## Closed

Nothing yet. Entries move here with the commit that closed them.
