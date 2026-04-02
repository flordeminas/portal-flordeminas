# Flor de Minas Automatic Deploy Script
# Performs git add, commit, and push only if changes exist.

$cwd = "c:\Projetos\ZHC\website"
Set-Location -Path $cwd

# Sync layouts first
python _maintenance_scripts/sync_layout.py

# Check for changes
$status = git status --porcelain

if ($status) {
    Write-Host "Changes detected. Starting deployment..." -ForegroundColor Cyan
    
    git add .
    git commit -m "Scheduled deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push origin main
    
    Write-Host "Deploy successful! ✅" -ForegroundColor Green
} else {
    Write-Host "No changes detected. Skipping deploy. 💤" -ForegroundColor Gray
}
