# VoiceOps Production Backup Script for Windows PowerShell
param (
    [string]$BackupDir = ".\backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
)

Write-Host "[VoiceOps Backup] Starting system backup to: $BackupDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

# 1. Backup SQLite
if (Test-Path "voiceops.db") {
    Write-Host "  -> Backing up local SQLite database..." -ForegroundColor Green
    Copy-Item "voiceops.db" -Destination "$BackupDir\voiceops.db"
}

# 2. Backup PostgreSQL container if running
$pgContainer = docker ps --filter "name=voiceops-postgres" --format "{{.Names}}" 2>$null
if ($pgContainer -eq "voiceops-postgres") {
    Write-Host "  -> Backing up PostgreSQL container dump..." -ForegroundColor Green
    docker exec voiceops-postgres pg_dump -U voiceops -d voiceops_db > "$BackupDir\postgres_dump.sql"
}

# 3. Backup Storage
if (Test-Path "storage") {
    Write-Host "  -> Backing up storage directory..." -ForegroundColor Green
    Compress-Archive -Path "storage\*" -DestinationPath "$BackupDir\storage.zip" -Force
}

Write-Host "[VoiceOps Backup] Backup completed successfully at $BackupDir" -ForegroundColor Cyan
