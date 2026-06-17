#!/usr/bin/env python3
"""
validate_turtle.py — WARRaNT ontology Turtle syntax validator.

Usage:
    python scripts/validate_turtle.py

Checks:
- All .ttl files under ontology/ and examples/ parse successfully with rdflib.
- Reports triple count per file.
- Warns if example individuals use ontology module namespaces as their IRI base.
- Exits 0 if all pass; exits 1 if any file fails.

Install: pip install rdflib
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
    for folder in ["ontology", "examples"]:
        p = ROOT / folder
        if p.exists():
            files.extend(sorted(p.rglob("*.ttl")))
    return files


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
    else:
        print("All files valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
