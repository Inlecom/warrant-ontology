#!/usr/bin/env python3
"""
merge_ontology.py — WARRaNT ontology merge script.

Loads all ontology module files in dependency order, merges into one graph,
and writes to dist/warrant-all-merged.ttl.

Usage:
    python scripts/merge_ontology.py
    python scripts/merge_ontology.py --include-examples

Note: dist/ is gitignored. Use for local inspection and CI artefact generation only.

Install: pip install rdflib
"""

import sys
import argparse
import pathlib

try:
    import rdflib
except ImportError:
    print("ERROR: rdflib not installed. Run: pip install rdflib", file=sys.stderr)
    sys.exit(1)

ROOT = pathlib.Path(__file__).parent.parent
ONTOLOGY_DIR = ROOT / "ontology"
EXAMPLES_DIR = ROOT / "examples"
DIST_DIR = ROOT / "dist"

# Dependency order: core first, digital-twin last
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


def parse_file(path: pathlib.Path, graph: rdflib.Graph) -> int:
    before = len(graph)
    try:
        graph.parse(str(path), format="turtle")
    except Exception as exc:
        print(f"ERROR parsing {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    added = len(graph) - before
    print(f"  Loaded {path.relative_to(ROOT)}  (+{added} triples)")
    return added


def main():
    parser = argparse.ArgumentParser(description="Merge WARRaNT ontology modules.")
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="Include example Turtle files in the merged output.",
    )
    args = parser.parse_args()

    merged = rdflib.Graph()

    print("Loading ontology modules:")
    for module_name in MODULE_ORDER:
        path = ONTOLOGY_DIR / module_name
        if not path.exists():
            print(f"  MISSING {path}", file=sys.stderr)
            sys.exit(1)
        parse_file(path, merged)

    if args.include_examples:
        print("\nLoading example files:")
        for example in sorted(EXAMPLES_DIR.glob("*.ttl")):
            parse_file(example, merged)

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / "warrant-all-merged.ttl"
    merged.serialize(destination=str(out_path), format="turtle")

    print(f"\nTotal triples: {len(merged)}")
    print(f"Written to:    {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
