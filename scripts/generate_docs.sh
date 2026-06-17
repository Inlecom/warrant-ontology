#!/usr/bin/env bash
# generate_docs.sh — Generate WIDOCO HTML documentation (Linux/macOS/CI).
#
# Prerequisites: Docker  (or Java 11+ with scripts/widoco.jar)
#
# Usage (from repo root):
#   bash scripts/generate_docs.sh           # Docker (default)
#   bash scripts/generate_docs.sh --jar     # widoco.jar

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MERGED_TTL="$REPO_ROOT/dist/warrant-all-merged.ttl"
WIDOCO_TTL="$REPO_ROOT/dist/warrant-widoco-input.ttl"
OUT_DIR="$REPO_ROOT/docs/html"

# Ensure merged TTL exists
if [ ! -f "$MERGED_TTL" ]; then
    echo "Merged TTL not found. Running merge script..."
    python "$REPO_ROOT/scripts/merge_ontology.py"
fi

# Produce WIDOCO-compatible single-ontology file
echo "Preparing WIDOCO input..."
python "$REPO_ROOT/scripts/prepare_widoco.py"

mkdir -p "$OUT_DIR"

if [ "$1" = "--jar" ]; then
    JAR="$REPO_ROOT/scripts/widoco.jar"
    if [ ! -f "$JAR" ]; then
        echo "ERROR: widoco.jar not found. Download from https://github.com/dgarijo/Widoco/releases"
        exit 1
    fi
    java -jar "$JAR" \
        -ontFile "$WIDOCO_TTL" \
        -outFolder "$OUT_DIR" \
        -rewriteAll \
        -getOntologyMetadata \
        -includeAnnotationProperties \
        -lang en \
        -noPlaceHolderText
else
    docker run --rm \
        -v "$REPO_ROOT:/repo" \
        dgarijo/widoco:latest \
        -ontFile /repo/dist/warrant-widoco-input.ttl \
        -outFolder /repo/docs/html \
        -rewriteAll \
        -getOntologyMetadata \
        -includeAnnotationProperties \
        -lang en \
        -noPlaceHolderText
fi

echo ""
echo "Done. Open: $OUT_DIR/index-en.html"
