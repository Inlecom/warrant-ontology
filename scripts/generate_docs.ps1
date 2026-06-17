# generate_docs.ps1 — Generate WIDOCO HTML documentation for the WARRaNT ontology.
#
# Prerequisites:
#   - Docker Desktop running  (recommended, no Java needed)
#   OR
#   - Java 11+  and  widoco.jar downloaded to scripts/widoco.jar
#
# Usage (from repo root):
#   .\scripts\generate_docs.ps1              # Docker (default)
#   .\scripts\generate_docs.ps1 -UseJar     # widoco.jar
#
# Output: docs/html/   (browseable HTML; open docs/html/index-en.html)

param(
    [switch]$UseJar
)

$RepoRoot  = (Resolve-Path "$PSScriptRoot\..").Path
$MergedTtl = "$RepoRoot\dist\warrant-all-merged.ttl"
$OutDir    = "$RepoRoot\docs\html"

# Ensure merged TTL exists
if (-not (Test-Path $MergedTtl)) {
    Write-Host "Merged TTL not found. Running merge script first..." -ForegroundColor Yellow
    python "$RepoRoot\scripts\merge_ontology.py"
    if ($LASTEXITCODE -ne 0) { Write-Error "Merge failed."; exit 1 }
}

# Produce WIDOCO-compatible single-ontology file
Write-Host "Preparing WIDOCO input..." -ForegroundColor Cyan
python "$RepoRoot\scripts\prepare_widoco.py"
if ($LASTEXITCODE -ne 0) { Write-Error "prepare_widoco.py failed."; exit 1 }
$WidocoTtl = "$RepoRoot\dist\warrant-widoco-input.ttl"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

if ($UseJar) {
    $JarPath = "$PSScriptRoot\widoco.jar"
    if (-not (Test-Path $JarPath)) {
        Write-Error "widoco.jar not found at $JarPath. Download from https://github.com/dgarijo/Widoco/releases"
        exit 1
    }
    java -jar $JarPath `
        -ontFile $WidocoTtl `
        -outFolder $OutDir `
        -rewriteAll `
        -getOntologyMetadata `
        -includeAnnotationProperties `
        -lang en `
        -noPlaceHolderText
} else {
    # Docker — mounts repo into container; uses official WIDOCO image
    $DockerWidocoTtl = "/repo/dist/warrant-widoco-input.ttl"
    $DockerOutDir    = "/repo/docs/html"

    docker run --rm `
        -v "${RepoRoot}:/repo" `
        dgarijo/widoco:latest `
        -ontFile $DockerWidocoTtl `
        -outFolder $DockerOutDir `
        -rewriteAll `
        -getOntologyMetadata `
        -includeAnnotationProperties `
        -lang en `
        -noPlaceHolderText

    if ($LASTEXITCODE -ne 0) { Write-Error "WIDOCO Docker run failed."; exit 1 }
}

Write-Host ""
Write-Host "WIDOCO documentation generated." -ForegroundColor Green
Write-Host "Open: $OutDir\index-en.html"
