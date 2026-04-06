# Flor de Minas Deploy Script
# Usage: .\deploy.ps1 "mensagem do commit"
# If no message is provided, lists changed files and prompts.

param(
    [string]$Message
)

$cwd = "c:\Projetos\ZHC\website"
Set-Location -Path $cwd

# Sync layouts first
python _maintenance_scripts/sync_layout.py

# Check for changes
$status = git status --porcelain

if (-not $status) {
    Write-Host "No changes detected. Skipping deploy." -ForegroundColor Gray
    exit 0
}

Write-Host "Changes detected:" -ForegroundColor Cyan
git status --short

if (-not $Message) {
    $Message = Read-Host "Commit message"
}

if (-not $Message) {
    Write-Host "Commit message is required. Aborting." -ForegroundColor Red
    exit 1
}

git add .
git commit -m $Message
git push origin main

Write-Host "Deploy successful!" -ForegroundColor Green
