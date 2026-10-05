# VoiceOps Disaster Recovery & Restore Script for Windows PowerShell
param (
    [Parameter(Mandatory=$true)]
    [string]$BackupDir
)

if (-not (Test-Path $BackupDir)) {
    Write-Error "Backup directory $BackupDir not found!"
    exit 1
}

Write-Host "[VoiceOps Restore] Restoring system from: $BackupDir" -ForegroundColor Cyan

# 1. Restore SQLite
if (Test-Path "$BackupDir\voiceops.db") {
    Write-Host "  -> Restoring SQLite database..." -ForegroundColor Green
    Copy-Item "$BackupDir\voiceops.db" -Destination "voiceops.db" -Force
}

# 2. Restore PostgreSQL
if (Test-Path "$BackupDir\postgres_dump.sql") {
    Write-Host "  -> Restoring PostgreSQL dump..." -ForegroundColor Green
    Get-Content "$BackupDir\postgres_dump.sql" | docker exec -i voiceops-postgres psql -U voiceops -d voiceops_db
}

# 3. Restore Storage
if (Test-Path "$BackupDir\storage.zip") {
    Write-Host "  -> Restoring audio storage files..." -ForegroundColor Green
    Expand-Archive -Path "$BackupDir\storage.zip" -DestinationPath "storage" -Force
}

Write-Host "[VoiceOps Restore] Restoration completed successfully." -ForegroundColor Cyan
