#!/usr/bin/env python3
"""
validate_turtle.py — WARRaNT ontology Turtle syntax validator.

Usage:
    python scripts/validate_turtle.py
    python scripts/validate_turtle.py --shacl      # also run SHACL shapes over examples

Checks:
- All .ttl files under ontology/, examples/ and shapes/ parse successfully with rdflib.
- Reports triple count per file.
- Warns if example individuals use ontology module namespaces as their IRI base.
- Checks every example assertion against the rdfs:domain and rdfs:range declared
  for its property, following rdfs:subClassOf and owl:unionOf. SHACL shapes do
  not do this: they constrain the shapes they target, not every property use,
  so domain and range errors pass validation silently.
- With --shacl: validates every example against shapes/*.ttl using pySHACL, with
  the ontology modules merged into the data graph and inference OFF
  (RDFS inference over rdfs:range/rdfs:domain would silently re-type individuals
  and mask sh:class violations).
- Exits 0 if all pass; exits 1 if any file fails (or any SHACL violation with --shacl).

Install: pip install rdflib          (pip install pyshacl for --shacl)
"""

import sys
import pathlib
import re

try:
    import rdflib
except ImportError:
    print("ERROR: rdflib not installed. Run: pip install rdflib", file=sys.stderr)
    sys.exit(1)

ROOT = pathlib.Path(__file__).parent.parent

MODULE_ORDER = [
    "warrant-core.ttl",
    "warrant-davom.ttl",
    "warrant-observation.ttl",
    "warrant-cdm.ttl",
    "warrant-assurance.ttl",
    "warrant-di.ttl",
    "warrant-scenario.ttl",
    "warrant-mitigation.ttl",
    "warrant-digital-twin.ttl",
]

MODULE_NAMESPACES = [
    "https://warrant-project.eu/ontology/core#",
    "https://warrant-project.eu/ontology/davom#",
    "https://warrant-project.eu/ontology/observation#",
    "https://warrant-project.eu/ontology/cdm#",
    "https://warrant-project.eu/ontology/assurance#",
    "https://warrant-project.eu/ontology/dependability-index#",
    "https://warrant-project.eu/ontology/scenario#",
    "https://warrant-project.eu/ontology/mitigation#",
    "https://warrant-project.eu/ontology/digital-twin#",
]

def find_ttl_files():
    files = []
    for folder in ["ontology", "examples", "shapes"]:
        p = ROOT / folder
        if p.exists():
            files.extend(sorted(p.rglob("*.ttl")))
    return files


MODULE_BASE = "https://warrant-project.eu/ontology/"

PREFIXES = {
    "core#": "warrant", "davom#": "davom", "observation#": "obs", "cdm#": "cdm",
    "assurance#": "assr", "dependability-index#": "di", "scenario#": "scen",
    "mitigation#": "mit", "digital-twin#": "dt",
}


def load_modules() -> "rdflib.Graph":
    g = rdflib.Graph()
    for name in MODULE_ORDER:
        g.parse(str(ROOT / "ontology" / name), format="turtle")
    return g


def _qname(term) -> str:
    s = str(term)
    for suffix, prefix in PREFIXES.items():
        if s.startswith(MODULE_BASE + suffix):
            return f"{prefix}:{s.split('#')[-1]}"
    if s.startswith("https://warrant-project.eu/data/"):
        ctx = s.split("/data/")[1].split("#")[0]
        return f"{ctx}:{s.split('#')[-1]}"
    return s


def run_domain_range() -> bool:
    """Check example assertions against declared domains and ranges."""
    from rdflib import RDF, RDFS, OWL
    import collections

    ont = load_modules()
    thing = rdflib.URIRef("http://www.w3.org/2002/07/owl#Thing")

    def class_expression(node):
        """An IRI, or the members of an owl:unionOf, or None if unconstrained."""
        if node is None:
            return None
        if isinstance(node, rdflib.BNode):
            lst = ont.value(node, OWL.unionOf)
            if lst is None:
                return None
            return set(rdflib.collection.Collection(ont, lst))
        return {node}

    ancestors_cache = {}

    def ancestors(cls):
        if cls in ancestors_cache:
            return ancestors_cache[cls]
        out, stack = set(), [cls]
        while stack:
            c = stack.pop()
            if c in out:
                continue
            out.add(c)
            stack.extend(x for x in ont.objects(c, RDFS.subClassOf)
                        if isinstance(x, rdflib.URIRef))
        ancestors_cache[cls] = out
        return out

    print()
    print("Domain and range check (declared rdfs:domain / rdfs:range, subclasses followed):")
    ok = True
    for ex in sorted((ROOT / "examples").glob("*.ttl")):
        data = rdflib.Graph().parse(str(ex), format="turtle")
        types = collections.defaultdict(set)
        for s, o in data.subject_objects(RDF.type):
            types[s].add(o)
        for s, o in ont.subject_objects(RDF.type):
            types[s].add(o)

        def kinds(node):
            out = set()
            for t in types.get(node, ()):
                out |= ancestors(t)
            return out

        problems = []
        for p in sorted(set(data.predicates()), key=str):
            if not str(p).startswith(MODULE_BASE):
                continue
            dom = class_expression(ont.value(p, RDFS.domain))
            rng = class_expression(ont.value(p, RDFS.range))
            for s, o in data.subject_objects(p):
                if dom and thing not in dom and types.get(s) and not (kinds(s) & dom):
                    problems.append(
                        f"domain  {_qname(p)}: subject {_qname(s)} is "
                        f"{'/'.join(sorted(_qname(t) for t in types[s]))}, "
                        f"declared domain {'/'.join(sorted(_qname(x) for x in dom))}")
                if (rng and thing not in rng and isinstance(o, rdflib.URIRef)
                        and types.get(o) and not (kinds(o) & rng)):
                    problems.append(
                        f"range   {_qname(p)}: object {_qname(o)} is "
                        f"{'/'.join(sorted(_qname(t) for t in types[o]))}, "
                        f"declared range {'/'.join(sorted(_qname(x) for x in rng))}")
        problems = sorted(set(problems))
        status = "OK   " if not problems else "FAIL "
        print(f"  {status} {ex.relative_to(ROOT)}  ({len(problems)} violation(s))")
        for msg in problems:
            print(f"        {msg}")
        if problems:
            ok = False
    return ok


def run_shacl() -> bool:
    """Validate each example against all shapes. Returns True if no violations."""
    try:
        import pyshacl
    except ImportError:
        print("ERROR: pyshacl not installed. Run: pip install pyshacl", file=sys.stderr)
        return False

    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

    ont = rdflib.Graph()
    for name in MODULE_ORDER:
        ont.parse(str(ROOT / "ontology" / name), format="turtle")

    shapes = rdflib.Graph()
    for shp in sorted((ROOT / "shapes").glob("*.ttl")):
        shapes.parse(str(shp), format="turtle")

    print()
    print("SHACL validation (inference off; ontology modules merged into the data graph):")
    ok = True
    for ex in sorted((ROOT / "examples").glob("*.ttl")):
        # Merge explicitly: pySHACL's ont_graph parameter only feeds the inference
        # step, so with inference off the module-defined named individuals
        # (di:*State, cdm:DeviationType values) would be invisible to sh:class.
        data = rdflib.Graph()
        data += ont
        data.parse(str(ex), format="turtle")
        conforms, report, _ = pyshacl.validate(
            data, shacl_graph=shapes,
            inference="none", abort_on_first=False,
        )
        results = list(report.subjects(rdflib.RDF.type, SH.ValidationResult))
        violations = [r for r in results
                      if report.value(r, SH.resultSeverity) == SH.Violation]
        warnings = [r for r in results if r not in violations]
        status = "OK   " if not violations else "FAIL "
        print(f"  {status} {ex.relative_to(ROOT)}  "
              f"({len(violations)} violation(s), {len(warnings)} warning(s))")
        for r in results:
            sev = str(report.value(r, SH.resultSeverity)).split("#")[-1]
            focus = report.value(r, SH.focusNode)
            msg = report.value(r, SH.resultMessage)
            print(f"        [{sev}] {focus}\n            {msg}")
        if violations:
            ok = False
    return ok


def check_namespace_violations(ttl_path: pathlib.Path, graph: rdflib.Graph) -> list[str]:
    """Warn if any subject IRI in examples/ uses a module namespace as its base."""
    if "examples" not in str(ttl_path):
        return []
    warnings = []
    for s in graph.subjects():
        s_str = str(s)
        for ns in MODULE_NAMESPACES:
            if s_str.startswith(ns):
                warnings.append(
                    f"  WARN  Instance IRI uses module namespace: {s_str}"
                )
    return warnings


def validate_file(ttl_path: pathlib.Path) -> tuple[bool, int, list[str]]:
    g = rdflib.Graph()
    try:
        g.parse(str(ttl_path), format="turtle")
        triple_count = len(g)
        warnings = check_namespace_violations(ttl_path, g)
        return True, triple_count, warnings
    except Exception as exc:
        return False, 0, [f"  ERROR {exc}"]


def main():
    files = find_ttl_files()
    if not files:
        print("No .ttl files found under ontology/ or examples/.")
        sys.exit(0)

    passed = 0
    failed = 0
    total_triples = 0

    for f in files:
        rel = f.relative_to(ROOT)
        ok, triples, messages = validate_file(f)
        if ok:
            status = "OK   "
            passed += 1
            total_triples += triples
            print(f"  {status} {rel}  ({triples} triples)")
        else:
            status = "FAIL "
            failed += 1
            print(f"  {status} {rel}")
        for msg in messages:
            print(msg)

    print()
    print(f"Results: {passed} passed, {failed} failed, {total_triples} total triples")

    if failed > 0:
        print("VALIDATION FAILED", file=sys.stderr)
        sys.exit(1)

    if not run_domain_range():
        print("DOMAIN/RANGE VALIDATION FAILED", file=sys.stderr)
        sys.exit(1)

    if "--shacl" in sys.argv[1:]:
        if not run_shacl():
            print("SHACL VALIDATION FAILED", file=sys.stderr)
            sys.exit(1)
        print("All examples conform to shapes.")

    print("All files valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
