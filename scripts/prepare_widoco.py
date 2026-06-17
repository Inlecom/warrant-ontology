#!/usr/bin/env python3
"""
prepare_widoco.py — Produce a WIDOCO-compatible single-ontology TTL.

WIDOCO uses OWLAPI internally, which rejects files containing more than one
owl:Ontology declaration.  The merged file has one per module.  This script:
  1. Loads the merged graph.
  2. Removes all module-level ontology subject triples
     (everything whose subject is one of the module IRI nodes).
  3. Injects a single clean owl:Ontology block for the aggregate IRI.
  4. Writes dist/warrant-widoco-input.ttl

Run this before generate_docs.sh / generate_docs.ps1.
"""
import sys, pathlib
try:
    import rdflib
    from rdflib import Graph, URIRef, Literal, Namespace
    from rdflib.namespace import OWL, RDF, RDFS, XSD, DCTERMS
except ImportError:
    print("pip install rdflib", file=sys.stderr); sys.exit(1)

ROOT     = pathlib.Path(__file__).parent.parent
MERGED   = ROOT / "dist" / "warrant-all-merged.ttl"
OUT      = ROOT / "dist" / "warrant-widoco-input.ttl"

# All per-module ontology IRIs (without trailing #)
MODULE_IRIS = [
    "https://warrant-project.eu/ontology/core",
    "https://warrant-project.eu/ontology/davom",
    "https://warrant-project.eu/ontology/observation",
    "https://warrant-project.eu/ontology/cdm",
    "https://warrant-project.eu/ontology/assurance",
    "https://warrant-project.eu/ontology/dependability-index",
    "https://warrant-project.eu/ontology/scenario",
    "https://warrant-project.eu/ontology/mitigation",
    "https://warrant-project.eu/ontology/digital-twin",
    "https://warrant-project.eu/ontology/all",
]
MODULE_URIS = {URIRef(iri) for iri in MODULE_IRIS}

# WARRaNT term namespaces — any subject IRI starting with these is a WARRaNT term
WARRANT_NS = [
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

# Term types that WIDOCO documents
TERM_TYPES = {
    OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
    OWL.AnnotationProperty, OWL.NamedIndividual,
    URIRef("http://www.w3.org/2000/01/rdf-schema#Class"),
}

if not MERGED.exists():
    print("Merged TTL not found. Running merge script...")
    import subprocess, sys as _sys
    r = subprocess.run([_sys.executable, str(ROOT / "scripts" / "merge_ontology.py")])
    if r.returncode != 0:
        print("Merge failed.", file=sys.stderr); sys.exit(1)

g = Graph()
g.parse(str(MERGED), format="turtle")
print(f"Loaded {len(g)} triples from {MERGED.name}")

# Strip all triples whose subject is a module ontology IRI
to_remove = [(s, p, o) for s, p, o in g if isinstance(s, URIRef) and s in MODULE_URIS]
for triple in to_remove:
    g.remove(triple)
print(f"Removed {len(to_remove)} ontology-header triples")

# Add rdfs:isDefinedBy to all WARRaNT classes, properties, and named individuals.
# WIDOCO uses this to discover which terms belong to the ontology being documented.
ONTO = URIRef("https://warrant-project.eu/ontology/")

def is_warrant_term(iri):
    return any(str(iri).startswith(ns) for ns in WARRANT_NS)

term_subjects = set()
for s in g.subjects():
    if not isinstance(s, URIRef):
        continue
    if not is_warrant_term(s):
        continue
    types = set(g.objects(s, RDF.type))
    if types & TERM_TYPES:
        term_subjects.add(s)
    # Also include named individuals typed as a WARRaNT class
    elif any(is_warrant_term(t) for t in types):
        term_subjects.add(s)

for term in term_subjects:
    g.add((term, RDFS.isDefinedBy, ONTO))

print(f"Added rdfs:isDefinedBy to {len(term_subjects)} terms")

# Inject single clean ontology declaration
g.add((ONTO, RDF.type,          OWL.Ontology))
g.add((ONTO, RDFS.label,        Literal("WARRaNT Knowledge Graph Ontology", lang="en")))
g.add((ONTO, RDFS.comment,      Literal(
    "WARRaNT ontology for dependability-aware vessel operations, causal dependability "
    "modelling, assurance, Dependability Index, scenarios, mitigation, and Digital Twin "
    "integration. Covers DAVOM, CDM, Assurance, DI, Scenario, Mitigation, and DT modules. "
    "Horizon Europe RIA 101202581.", lang="en")))
g.add((ONTO, DCTERMS.title,     Literal("WARRaNT KG Ontology")))
g.add((ONTO, DCTERMS.creator,   Literal("WARRaNT Consortium (Horizon Europe RIA 101202581)")))
g.add((ONTO, DCTERMS.issued,    Literal("2026-06-05", datatype=XSD.date)))
g.add((ONTO, OWL.versionInfo,   Literal("0.9-poc")))

OUT.parent.mkdir(parents=True, exist_ok=True)
g.serialize(destination=str(OUT), format="turtle")
print(f"Written {len(g)} triples to {OUT.relative_to(ROOT)}")
print("Ready for WIDOCO.")
