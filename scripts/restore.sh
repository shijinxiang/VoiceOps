#!/usr/bin/env bash
# VoiceOps Disaster Recovery & Restore Script
set -euo pipefail

BACKUP_DIR="${1:-}"

if [ -z "${BACKUP_DIR}" ] || [ ! -d "${BACKUP_DIR}" ]; then
    echo "Usage: ./scripts/restore.sh <backup_directory_path>"
    exit 1
fi

echo "[VoiceOps Restore] Restoring system from: ${BACKUP_DIR}"

# 1. Restore SQLite database
if [ -f "${BACKUP_DIR}/voiceops.db" ]; then
    echo "  -> Restoring SQLite database..."
    cp "${BACKUP_DIR}/voiceops.db" "voiceops.db"
fi

# 2. Restore PostgreSQL if dump exists
if [ -f "${BACKUP_DIR}/postgres_dump.sql" ] && docker ps --format '{{.Names}}' | grep -q "voiceops-postgres"; then
    echo "  -> Restoring PostgreSQL database from dump..."
    cat "${BACKUP_DIR}/postgres_dump.sql" | docker exec -i voiceops-postgres psql -U voiceops -d voiceops_db
fi

# 3. Restore Storage
if [ -f "${BACKUP_DIR}/storage.tar.gz" ]; then
    echo "  -> Restoring audio storage files..."
    tar -xzf "${BACKUP_DIR}/storage.tar.gz" -C .
fi

echo "[VoiceOps Restore] Restoration completed successfully."
