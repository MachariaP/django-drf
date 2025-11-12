#!/bin/bash

################################################################################
# Production Deployment Script
# 
# This script automates the deployment of Django REST Framework application
# to a production server.
#
# Usage: ./deploy.sh [environment]
#   environment: staging, production (default: staging)
#
# What this script does:
# 1. Pulls latest code from Git
# 2. Installs/updates dependencies
# 3. Runs database migrations
# 4. Collects static files
# 5. Restarts application services
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
ENVIRONMENT="${1:-staging}"
PROJECT_DIR="/home/django/django-drf"
APP_DIR="$PROJECT_DIR/django-api"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="$PROJECT_DIR/backups"

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

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Confirm deployment
confirm_deployment() {
    echo "=================================================="
    echo "  Django DRF Deployment Script"
    echo "=================================================="
    echo ""
    print_warning "Environment: $ENVIRONMENT"
    print_warning "Project Directory: $PROJECT_DIR"
    echo ""
    
    if [ "$ENVIRONMENT" == "production" ]; then
        print_error "⚠️  WARNING: You are about to deploy to PRODUCTION! ⚠️"
        echo ""
        read -p "Are you sure you want to continue? (yes/no): " -r
        if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            print_info "Deployment cancelled"
            exit 0
        fi
    else
        read -p "Continue with deployment? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Deployment cancelled"
            exit 0
        fi
    fi
}

# Create backup before deployment
create_backup() {
    print_info "Creating backup before deployment..."
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/pre_deploy_backup_$TIMESTAMP.sql"
    
    # Load database credentials from .env
    if [ -f "$APP_DIR/.env" ]; then
        export $(grep -v '^#' $APP_DIR/.env | grep 'DATABASE_URL' | xargs)
        
        # Extract database info from DATABASE_URL
        # Format: postgresql://user:password@host:port/dbname
        DB_INFO=$(echo $DATABASE_URL | sed 's|postgresql://||')
        DB_USER=$(echo $DB_INFO | cut -d: -f1)
        DB_PASS=$(echo $DB_INFO | cut -d: -f2 | cut -d@ -f1)
        DB_HOST=$(echo $DB_INFO | cut -d@ -f2 | cut -d: -f1)
        DB_PORT=$(echo $DB_INFO | cut -d: -f2 | cut -d/ -f1)
        DB_NAME=$(echo $DB_INFO | cut -d/ -f2)
        
        export PGPASSWORD=$DB_PASS
        
        if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > "$BACKUP_FILE"; then
            gzip "$BACKUP_FILE"
            print_success "Database backup created: $BACKUP_FILE.gz"
        else
            print_warning "Database backup failed, but continuing deployment"
        fi
        
        unset PGPASSWORD
    else
        print_warning ".env file not found, skipping database backup"
    fi
}

# Pull latest code from Git
pull_code() {
    print_info "Pulling latest code from Git..."
    
    cd "$PROJECT_DIR"
    
    # Stash any local changes
    git stash
    
    # Pull latest changes
    if [ "$ENVIRONMENT" == "production" ]; then
        git checkout main
    else
        git checkout staging
    fi
    
    git pull origin $(git branch --show-current)
    
    print_success "Code updated successfully"
}

# Install/update dependencies
install_dependencies() {
    print_info "Installing/updating Python dependencies..."
    
    cd "$APP_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt --upgrade
    
    print_success "Dependencies installed/updated"
}

# Run database migrations
run_migrations() {
    print_info "Running database migrations..."
    
    cd "$APP_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Show pending migrations
    python manage.py showmigrations
    
    # Run migrations
    python manage.py migrate --noinput
    
    print_success "Database migrations completed"
}

# Collect static files
collect_static() {
    print_info "Collecting static files..."
    
    cd "$APP_DIR"
    source "$VENV_DIR/bin/activate"
    
    python manage.py collectstatic --noinput --clear
    
    print_success "Static files collected"
}

# Run tests (optional, recommended for staging)
run_tests() {
    if [ "$ENVIRONMENT" != "production" ]; then
        print_info "Running tests..."
        
        cd "$APP_DIR"
        source "$VENV_DIR/bin/activate"
        
        if python manage.py test; then
            print_success "All tests passed"
        else
            print_error "Tests failed!"
            read -p "Continue anyway? (y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_error "Deployment aborted due to test failures"
                exit 1
            fi
        fi
    fi
}

# Restart services
restart_services() {
    print_info "Restarting application services..."
    
    # Restart Gunicorn
    if sudo systemctl restart gunicorn; then
        print_success "Gunicorn restarted"
    else
        print_error "Failed to restart Gunicorn"
    fi
    
    # Reload Nginx
    if sudo systemctl reload nginx; then
        print_success "Nginx reloaded"
    else
        print_warning "Failed to reload Nginx"
    fi
    
    # Wait a moment for services to restart
    sleep 3
}

# Health check
health_check() {
    print_info "Performing health check..."
    
    # Check if Gunicorn is running
    if sudo systemctl is-active --quiet gunicorn; then
        print_success "Gunicorn is running"
    else
        print_error "Gunicorn is not running!"
    fi
    
    # Check if Nginx is running
    if sudo systemctl is-active --quiet nginx; then
        print_success "Nginx is running"
    else
        print_error "Nginx is not running!"
    fi
    
    # Check if application responds
    if curl -s -o /dev/null -w "%{http_code}" http://localhost/api/ | grep -q "200\|301\|302"; then
        print_success "Application is responding"
    else
        print_warning "Application may not be responding correctly"
    fi
}

# Show deployment summary
show_summary() {
    echo ""
    echo "=================================================="
    echo "  Deployment Summary"
    echo "=================================================="
    echo "Environment: $ENVIRONMENT"
    echo "Deployment Time: $(date)"
    echo "Git Branch: $(cd $PROJECT_DIR && git branch --show-current)"
    echo "Git Commit: $(cd $PROJECT_DIR && git rev-parse --short HEAD)"
    echo "=================================================="
    echo ""
}

# Main deployment process
main() {
    # Confirm deployment
    confirm_deployment
    
    # Create pre-deployment backup
    create_backup
    
    # Pull latest code
    pull_code
    
    # Install dependencies
    install_dependencies
    
    # Run migrations
    run_migrations
    
    # Collect static files
    collect_static
    
    # Run tests (staging only)
    run_tests
    
    # Restart services
    restart_services
    
    # Health check
    health_check
    
    # Show summary
    show_summary
    
    print_success "🎉 Deployment completed successfully!"
    echo ""
    print_info "Next steps:"
    echo "  • Monitor application logs: sudo journalctl -u gunicorn -f"
    echo "  • Check Nginx logs: sudo tail -f /var/log/nginx/error.log"
    echo "  • Verify application: curl http://localhost/api/"
    echo ""
}

# Run main function
main
