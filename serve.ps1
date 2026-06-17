# serve.ps1 — Start local HTTP server for WARRaNT ontology documentation.
# Run from repo root: .\serve.ps1
# Stop with Ctrl+C

$port = 8000
Write-Host ""
Write-Host "  WARRaNT Ontology Documentation" -ForegroundColor Cyan
Write-Host "  ================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Interactive graph:   " -NoNewline; Write-Host "http://localhost:$port/docs/visualise.html" -ForegroundColor Green
Write-Host "  WIDOCO reference:    " -NoNewline; Write-Host "http://localhost:$port/docs/html/index-en.html" -ForegroundColor Green
Write-Host ""
Write-Host "  Press Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

python -m http.server $port
