#!/bin/bash

################################################################################
# PostgreSQL Database Setup Script
# 
# This script automates the installation and configuration of PostgreSQL
# for the Django REST Framework application.
#
# Usage: ./setup_postgres.sh
#
# What this script does:
# 1. Detects your operating system
# 2. Installs PostgreSQL (if not already installed)
# 3. Starts PostgreSQL service
# 4. Creates database and user
# 5. Configures database for Django
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Database configuration (change these as needed)
DB_NAME="${DB_NAME:-django_drf_db}"
DB_USER="${DB_USER:-django_user}"
DB_PASSWORD="${DB_PASSWORD:-change_this_password}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

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

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/debian_version ]; then
            OS="debian"
        elif [ -f /etc/redhat-release ]; then
            OS="redhat"
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
    print_info "Detected OS: $OS"
}

# Check if PostgreSQL is installed
check_postgres_installed() {
    if command -v psql &> /dev/null; then
        print_success "PostgreSQL is already installed"
        psql --version
        return 0
    else
        print_warning "PostgreSQL is not installed"
        return 1
    fi
}

# Install PostgreSQL on Debian/Ubuntu
install_postgres_debian() {
    print_info "Installing PostgreSQL on Debian/Ubuntu..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib libpq-dev
    print_success "PostgreSQL installed successfully"
}

# Install PostgreSQL on RedHat/CentOS/Fedora
install_postgres_redhat() {
    print_info "Installing PostgreSQL on RedHat/CentOS/Fedora..."
    sudo yum install -y postgresql postgresql-server postgresql-contrib postgresql-devel
    sudo postgresql-setup --initdb
    print_success "PostgreSQL installed successfully"
}

# Install PostgreSQL on macOS
install_postgres_macos() {
    print_info "Installing PostgreSQL on macOS..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew is not installed. Please install it first:"
        echo "Visit: https://brew.sh"
        exit 1
    fi
    
    brew install postgresql@15
    print_success "PostgreSQL installed successfully"
}

# Start PostgreSQL service
start_postgres() {
    print_info "Starting PostgreSQL service..."
    
    case $OS in
        debian)
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
            ;;
        redhat)
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
            ;;
        macos)
            brew services start postgresql@15
            ;;
        *)
            print_warning "Please start PostgreSQL manually for your system"
            ;;
    esac
    
    sleep 2  # Wait for service to start
    print_success "PostgreSQL service started"
}

# Check if PostgreSQL is running
check_postgres_running() {
    print_info "Checking if PostgreSQL is running..."
    
    if pg_isready -h $DB_HOST -p $DB_PORT &> /dev/null; then
        print_success "PostgreSQL is running"
        return 0
    else
        print_error "PostgreSQL is not running"
        return 1
    fi
}

# Create database and user
create_database() {
    print_info "Creating database and user..."
    
    # Check if running as postgres user or need sudo
    if [[ "$OS" == "macos" ]]; then
        PSQL_CMD="psql postgres"
    else
        PSQL_CMD="sudo -u postgres psql"
    fi
    
    # Create database
    $PSQL_CMD << EOF
-- Drop database if exists (for clean setup)
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;

-- Create user
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Create database
CREATE DATABASE $DB_NAME OWNER $DB_USER;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Connect to the new database and grant schema privileges
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;

-- Exit
\q
EOF
    
    print_success "Database '$DB_NAME' and user '$DB_USER' created successfully"
}

# Test database connection
test_connection() {
    print_info "Testing database connection..."
    
    # Set password for connection test
    export PGPASSWORD=$DB_PASSWORD
    
    if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT version();" &> /dev/null; then
        print_success "Database connection successful!"
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT version();"
    else
        print_error "Database connection failed"
        exit 1
    fi
    
    unset PGPASSWORD
}

# Generate DATABASE_URL
generate_database_url() {
    print_info "Generating DATABASE_URL for Django..."
    
    DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
    
    echo ""
    print_success "PostgreSQL setup complete!"
    echo ""
    echo "=================================================="
    echo "Database Configuration"
    echo "=================================================="
    echo "Database Name: $DB_NAME"
    echo "Database User: $DB_USER"
    echo "Database Password: $DB_PASSWORD"
    echo "Database Host: $DB_HOST"
    echo "Database Port: $DB_PORT"
    echo ""
    echo "Add this to your .env file:"
    echo "------------------------------------------------"
    echo "DATABASE_URL=$DATABASE_URL"
    echo "=================================================="
    echo ""
    print_warning "⚠️  Keep your database credentials secure!"
    print_warning "⚠️  Never commit .env file to version control!"
}

# Update .env file
update_env_file() {
    ENV_FILE="../django-api/.env"
    
    if [ -f "$ENV_FILE" ]; then
        print_info "Updating .env file..."
        
        # Backup existing .env
        cp "$ENV_FILE" "$ENV_FILE.backup"
        
        # Update DATABASE_URL
        if grep -q "DATABASE_URL=" "$ENV_FILE"; then
            sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME|" "$ENV_FILE"
        else
            echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME" >> "$ENV_FILE"
        fi
        
        print_success ".env file updated (backup saved as .env.backup)"
    else
        print_warning ".env file not found. Please create it manually with:"
        echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
    fi
}

# Main script
main() {
    echo "=================================================="
    echo "  PostgreSQL Setup Script for Django DRF"
    echo "=================================================="
    echo ""
    
    # Detect OS
    detect_os
    
    # Check if PostgreSQL is installed
    if ! check_postgres_installed; then
        case $OS in
            debian)
                install_postgres_debian
                ;;
            redhat)
                install_postgres_redhat
                ;;
            macos)
                install_postgres_macos
                ;;
            windows)
                print_error "Automated installation on Windows is not supported"
                print_info "Please install PostgreSQL from: https://www.postgresql.org/download/windows/"
                exit 1
                ;;
            *)
                print_error "Unsupported operating system"
                exit 1
                ;;
        esac
    fi
    
    # Start PostgreSQL
    start_postgres
    
    # Check if PostgreSQL is running
    if ! check_postgres_running; then
        print_error "Failed to start PostgreSQL"
        exit 1
    fi
    
    # Create database and user
    create_database
    
    # Test connection
    test_connection
    
    # Generate DATABASE_URL
    generate_database_url
    
    # Optionally update .env file
    read -p "Do you want to update the .env file automatically? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        update_env_file
    fi
    
    echo ""
    print_success "🎉 Setup complete! You can now run Django migrations."
    echo ""
    print_info "Next steps:"
    echo "  1. cd ../django-api"
    echo "  2. source venv/bin/activate  # (or venv\\Scripts\\activate on Windows)"
    echo "  3. python manage.py migrate"
    echo "  4. python manage.py createsuperuser"
    echo "  5. python manage.py runserver"
    echo ""
}

# Run main function
main
