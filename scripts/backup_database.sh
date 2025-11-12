#!/bin/bash

################################################################################
# Database Backup Script
# 
# This script creates backups of your PostgreSQL database.
# It can be run manually or scheduled with cron.
#
# Usage: ./backup_database.sh
#
# Cron example (daily backup at 2 AM):
# 0 2 * * * /path/to/scripts/backup_database.sh
################################################################################

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Load environment variables from .env file if it exists
if [ -f "../django-api/.env" ]; then
    export $(grep -v '^#' ../django-api/.env | xargs)
fi

# Database configuration
DB_NAME="${DB_NAME:-django_drf_db}"
DB_USER="${DB_USER:-django_user}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

# Backup configuration
BACKUP_DIR="${BACKUP_DIR:-../backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"  # Keep backups for 30 days
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_$TIMESTAMP.sql"
COMPRESSED_FILE="$BACKUP_FILE.gz"

# Helper functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Create backup directory if it doesn't exist
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        print_info "Created backup directory: $BACKUP_DIR"
    fi
}

# Perform database backup
perform_backup() {
    print_info "Starting database backup..."
    print_info "Database: $DB_NAME"
    print_info "Backup file: $BACKUP_FILE"
    
    # Set password for pg_dump
    export PGPASSWORD=$DB_PASSWORD
    
    # Perform backup
    if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -F p -f "$BACKUP_FILE"; then
        print_success "Database backup created successfully"
        
        # Compress the backup
        print_info "Compressing backup..."
        gzip "$BACKUP_FILE"
        print_success "Backup compressed: $COMPRESSED_FILE"
        
        # Show backup size
        BACKUP_SIZE=$(du -h "$COMPRESSED_FILE" | cut -f1)
        print_info "Backup size: $BACKUP_SIZE"
    else
        print_error "Database backup failed"
        exit 1
    fi
    
    unset PGPASSWORD
}

# Clean old backups
clean_old_backups() {
    print_info "Cleaning old backups (older than $BACKUP_RETENTION_DAYS days)..."
    
    # Find and delete old backups
    DELETED=$(find "$BACKUP_DIR" -name "${DB_NAME}_backup_*.sql.gz" -type f -mtime +$BACKUP_RETENTION_DAYS -delete -print | wc -l)
    
    if [ $DELETED -gt 0 ]; then
        print_success "Deleted $DELETED old backup(s)"
    else
        print_info "No old backups to delete"
    fi
}

# List existing backups
list_backups() {
    print_info "Existing backups:"
    echo "=================================================="
    
    if [ -d "$BACKUP_DIR" ]; then
        BACKUPS=$(find "$BACKUP_DIR" -name "${DB_NAME}_backup_*.sql.gz" -type f | sort -r)
        
        if [ -z "$BACKUPS" ]; then
            echo "No backups found"
        else
            echo "$BACKUPS" | while read backup; do
                SIZE=$(du -h "$backup" | cut -f1)
                DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$backup" 2>/dev/null || stat -c "%y" "$backup" 2>/dev/null | cut -d'.' -f1)
                echo "  • $(basename $backup) - $SIZE - $DATE"
            done
        fi
    else
        echo "Backup directory does not exist"
    fi
    
    echo "=================================================="
}

# Main function
main() {
    echo "=================================================="
    echo "  Database Backup Script"
    echo "=================================================="
    echo ""
    
    # Create backup directory
    create_backup_dir
    
    # Perform backup
    perform_backup
    
    # Clean old backups
    clean_old_backups
    
    # List all backups
    list_backups
    
    echo ""
    print_success "🎉 Backup completed successfully!"
    echo ""
    print_info "To restore this backup, run:"
    echo "  gunzip -c $COMPRESSED_FILE | psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
    echo ""
}

# Run main function
main
