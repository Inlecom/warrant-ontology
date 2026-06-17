#!/usr/bin/env python3
"""
run_queries.py — Execute the WARRaNT competency queries against the merged
ontology + all example files and print results.

Usage:
    python scripts/run_queries.py
    python scripts/run_queries.py --query 1          # run only Query 1
    python scripts/run_queries.py --format table     # table output (default)
    python scripts/run_queries.py --format csv       # CSV output

Install: pip install rdflib tabulate
"""

import sys, pathlib, argparse, re

try:
    import rdflib
except ImportError:
    print("pip install rdflib", file=sys.stderr); sys.exit(1)

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

ROOT      = pathlib.Path(__file__).parent.parent
QUERY_FILE = ROOT / "queries" / "competency-queries.sparql"
MERGED    = ROOT / "dist" / "warrant-all-merged.ttl"
EXAMPLES  = sorted((ROOT / "examples").glob("*.ttl"))

# ── Prefix block shared across all queries ─────────────────────────────────────
PREFIXES = """
PREFIX warrant: <https://warrant-project.eu/ontology/core#>
PREFIX davom:   <https://warrant-project.eu/ontology/davom#>
PREFIX obs:     <https://warrant-project.eu/ontology/observation#>
PREFIX cdm:     <https://warrant-project.eu/ontology/cdm#>
PREFIX assr:    <https://warrant-project.eu/ontology/assurance#>
PREFIX di:      <https://warrant-project.eu/ontology/dependability-index#>
PREFIX scen:    <https://warrant-project.eu/ontology/scenario#>
PREFIX mit:     <https://warrant-project.eu/ontology/mitigation#>
PREFIX dt:      <https://warrant-project.eu/ontology/digital-twin#>
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX ll1:     <https://warrant-project.eu/data/ll1#>
PREFIX ll2:     <https://warrant-project.eu/data/ll2#>
PREFIX ll4:     <https://warrant-project.eu/data/ll4#>
"""

def shorten(val):
    """Shorten IRI to prefix:local for display."""
    NS = {
        "https://warrant-project.eu/ontology/core#":               "warrant:",
        "https://warrant-project.eu/ontology/davom#":              "davom:",
        "https://warrant-project.eu/ontology/observation#":        "obs:",
        "https://warrant-project.eu/ontology/cdm#":                "cdm:",
        "https://warrant-project.eu/ontology/assurance#":          "assr:",
        "https://warrant-project.eu/ontology/dependability-index#":"di:",
        "https://warrant-project.eu/ontology/scenario#":           "scen:",
        "https://warrant-project.eu/ontology/mitigation#":         "mit:",
        "https://warrant-project.eu/ontology/digital-twin#":       "dt:",
        "https://warrant-project.eu/data/ll1#":                    "ll1:",
        "https://warrant-project.eu/data/ll2#":                    "ll2:",
        "https://warrant-project.eu/data/ll3#":                    "ll3:",
        "https://warrant-project.eu/data/ll4#":                    "ll4:",
    }
    s = str(val)
    for ns, prefix in NS.items():
        if s.startswith(ns):
            return prefix + s[len(ns):]
    return s if len(s) < 60 else "..." + s[-45:]

def parse_queries(path):
    """Parse queries from the .sparql file.

    Structure: header comment block (fenced with ##...) followed immediately
    by the SELECT block, then another fence for the next query header.
    Pattern: fence / QUERY N header / fence / SELECT block / fence / ...

    Strategy: split on fences, then pair each header chunk with the next
    SELECT chunk.
    """
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r'\n?#{40,}\n', text)

    queries = []
    pending_title = None

    for chunk in chunks:
        has_select = bool(re.search(r'\bSELECT\b', chunk, re.IGNORECASE))
        has_header = bool(re.search(r'#\s*QUERY\s+\d+', chunk, re.IGNORECASE))

        if has_header and not has_select:
            # This chunk is a query header — remember its title
            m = re.search(r'#\s*(QUERY\s+\d+[^:\n]*(?::\s*[^\n]+)?)', chunk, re.IGNORECASE)
            pending_title = m.group(1).strip()[:70] if m else "Query"
        elif has_select and pending_title:
            # This chunk is the SELECT body for the pending header
            # Strip trailing whitespace and any empty trailing ORDER lines
            sparql = chunk.strip()
            queries.append((pending_title, PREFIXES + sparql))
            pending_title = None
        elif has_select and has_header:
            # Header and SELECT in same chunk (shouldn't happen but handle it)
            m = re.search(r'#\s*(QUERY\s+\d+[^:\n]*(?::\s*[^\n]+)?)', chunk, re.IGNORECASE)
            title = m.group(1).strip()[:70] if m else "Query"
            sparql = re.search(r'(SELECT\b.*)', chunk, re.DOTALL | re.IGNORECASE).group(1).strip()
            queries.append((title, PREFIXES + sparql))

    return queries

def build_graph():
    g = rdflib.Graph()
    if not MERGED.exists():
        print("Merged TTL not found. Run: python scripts/merge_ontology.py")
        sys.exit(1)
    g.parse(str(MERGED), format="turtle")
    for ex in EXAMPLES:
        g.parse(str(ex), format="turtle")
    return g

def run_query(g, sparql_text):
    try:
        results = g.query(sparql_text)
        rows = []
        vars_ = [str(v) for v in results.vars]
        for row in results:
            rows.append([shorten(row[v]) if row[v] else "" for v in results.vars])
        return vars_, rows
    except Exception as e:
        return ["error"], [[str(e)]]

def print_table(title, vars_, rows, fmt="table"):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    if not rows:
        print("  (no results)")
        return
    print(f"  {len(rows)} row(s)\n")
    if fmt == "csv":
        print(",".join(vars_))
        for r in rows:
            print(",".join(f'"{v}"' for v in r))
    else:
        if HAS_TABULATE:
            print(tabulate(rows, headers=vars_, tablefmt="simple",
                           maxcolwidths=50))
        else:
            # Simple fallback
            col_w = [max(len(h), max((len(str(r[i])) for r in rows), default=0))
                     for i, h in enumerate(vars_)]
            header = "  " + "  ".join(h.ljust(w) for h, w in zip(vars_, col_w))
            print(header)
            print("  " + "  ".join("-"*w for w in col_w))
            for row in rows:
                print("  " + "  ".join(str(c).ljust(w) for c, w in zip(row, col_w)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=int, help="Run only query N")
    parser.add_argument("--format", choices=["table","csv"], default="table")
    args = parser.parse_args()

    queries = parse_queries(QUERY_FILE)
    if not queries:
        print("No queries parsed from file."); sys.exit(1)

    print(f"\nLoading graph...")
    g = build_graph()
    print(f"Graph loaded: {len(g)} triples ({len(EXAMPLES)} example files)")

    selected = [(i, t, q) for i, (t, q) in enumerate(queries, 1)
                if args.query is None or i == args.query]

    for i, title, sparql in selected:
        vars_, rows = run_query(g, sparql)
        print_table(f"Query {i}: {title}", vars_, rows, args.format)

    print(f"\nDone. {len(selected)} query/queries executed.")

if __name__ == "__main__":
    main()
