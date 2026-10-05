#!/usr/bin/env bash
# VoiceOps Production Backup Script (PostgreSQL + SQLite + Upload Storage)
set -euo pipefail

BACKUP_DIR="${1:-./backups/$(date +%Y%m%d_%H%M%S)}"
mkdir -p "${BACKUP_DIR}"

echo "[VoiceOps Backup] Starting system backup to: ${BACKUP_DIR}"

# 1. Backup SQLite database if present
if [ -f "voiceops.db" ]; then
    echo "  -> Backing up local SQLite database..."
    cp "voiceops.db" "${BACKUP_DIR}/voiceops.db"
fi

# 2. Backup PostgreSQL if container is running
if docker ps --format '{{.Names}}' | grep -q "voiceops-postgres"; then
    echo "  -> Backing up PostgreSQL container dump..."
    docker exec voiceops-postgres pg_dump -U voiceops -d voiceops_db > "${BACKUP_DIR}/postgres_dump.sql"
fi

# 3. Backup Audio Storage
if [ -d "storage" ]; then
    echo "  -> Backing up audio file storage directory..."
    tar -czf "${BACKUP_DIR}/storage.tar.gz" storage/
fi

# 4. Generate Checksum
cd "${BACKUP_DIR}"
sha256sum * > checksums.sha256 2>/dev/null || true
cd - > /dev/null

echo "[VoiceOps Backup] Backup completed successfully at ${BACKUP_DIR}"
