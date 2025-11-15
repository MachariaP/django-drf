# 🚀 Complete PostgreSQL Setup and Deployment Guide

> A comprehensive, step-by-step guide for setting up PostgreSQL database and deploying your Django REST Framework application to production.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [PostgreSQL Installation](#postgresql-installation)
4. [Database Configuration](#database-configuration)
5. [Docker Setup](#docker-setup)
6. [Production Deployment](#production-deployment)
7. [Database Management](#database-management)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **Git** for version control
- **Terminal/Command Line** access
- **Text Editor** (VS Code, Sublime, etc.)
- **Admin/sudo privileges** (for PostgreSQL installation)

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/MachariaP/django-drf.git
cd django-drf

# Navigate to the Django project directory
cd django-api
```

### Step 2: Create Virtual Environment

Creating a virtual environment isolates your project dependencies from other Python projects.

**On Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Why Virtual Environment?**
- Keeps dependencies organized and isolated
- Prevents version conflicts with other projects
- Makes deployment easier by tracking exact package versions

### Step 3: Install Dependencies

```bash
# Upgrade pip (Python package manager)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**What gets installed?**
- Django 5.2.8 - Web framework
- djangorestframework 3.16.1 - REST API toolkit
- psycopg2-binary 2.9.11 - PostgreSQL adapter for Python
- django-cors-headers - Handle Cross-Origin requests
- drf-spectacular - API documentation
- And more...

---

## PostgreSQL Installation

PostgreSQL is a powerful, open-source relational database. Let's install it for your platform.

### Installation on Ubuntu/Debian Linux

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Verify installation
psycopg2-binary --version

# PostgreSQL service should start automatically
# Check status
sudo systemctl status postgresql
```

### Installation on macOS

**Option 1: Using Homebrew (Recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify installation
psql --version
```

**Option 2: Using Postgres.app**
1. Download from [https://postgresapp.com/](https://postgresapp.com/)
2. Move to Applications folder
3. Double-click to start
4. Click "Initialize" to create a new server

### Installation on Windows

**Option 1: Using Installer (Recommended)**
1. Download from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Follow the installation wizard:
   - Choose installation directory
   - Select components (PostgreSQL Server, pgAdmin, Command Line Tools)
   - Set data directory
   - Set password for postgres user (remember this!)
   - Choose port (default: 5432)
4. Complete installation

**Option 2: Using WSL (Windows Subsystem for Linux)**
```bash
# In WSL terminal
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

### Verify PostgreSQL Installation

```bash
# Check PostgreSQL version
psql --version
# Should output: psql (PostgreSQL) 15.x

# Check if service is running
# Linux
sudo systemctl status postgresql

# macOS (with Homebrew)
brew services list | grep postgresql

# Windows (in Command Prompt)
sc query postgresql-x64-15
```

---

## Database Configuration

### Step 1: Access PostgreSQL

**On Linux/macOS:**
```bash
# Switch to postgres user
sudo -u postgres psql

# Or directly
psql -U postgres
```

**On Windows:**
```bash
# Open Command Prompt or PowerShell
# Navigate to PostgreSQL bin directory
cd "C:\Program Files\PostgreSQL\15\bin"

# Connect to PostgreSQL
psql -U postgres
```

### Step 2: Create Database and User

Once you're in the PostgreSQL shell (you'll see `postgres=#`), run these commands:

```sql
-- Create a new database for your Django project
CREATE DATABASE django_drf_db;

-- Create a new user with a password
CREATE USER django_user WITH PASSWORD 'your_secure_password_here';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE django_drf_db TO django_user;

-- Grant schema privileges (PostgreSQL 15+)
\c django_drf_db
GRANT ALL ON SCHEMA public TO django_user;

-- Exit PostgreSQL
\q
```

**Security Best Practices:**
- Use a strong password (mix of letters, numbers, symbols)
- Never commit passwords to version control
- Use different credentials for development and production

### Step 3: Test Database Connection

```bash
# Test connection with new user
psql -U django_user -d django_drf_db -h localhost

# If successful, you'll see:
# django_drf_db=>

# List databases
\l

# Exit
\q
```

### Step 4: Configure Django Settings

Create a `.env` file in the `django-api` directory:

```bash
# Navigate to django-api directory
cd /path/to/django-drf/django-api

# Copy the example environment file
cp .env.example .env

# Edit the .env file
nano .env  # or use your preferred editor
```

Update your `.env` file with PostgreSQL credentials:

```env
# Django Configuration
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=True

# PostgreSQL Database Configuration
DATABASE_URL=postgresql://django_user:your_secure_password_here@localhost:5432/django_drf_db

# Cache Configuration (Optional - Redis)
# REDIS_URL=redis://localhost:6379/0

# AWS Configuration (Optional)
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_STORAGE_BUCKET_NAME=
# AWS_S3_REGION_NAME=us-east-1
```

**Understanding DATABASE_URL:**
```
postgresql://[user]:[password]@[host]:[port]/[database_name]
│            │      │          │      │      └─ Database name
│            │      │          │      └─ Port (5432 is PostgreSQL default)
│            │      │          └─ Host (localhost for local, IP/domain for remote)
│            │      └─ Password
│            └─ Username
└─ Database type
```

### Step 5: Generate Secret Key

Django needs a unique SECRET_KEY. Generate one:

```bash
# Method 1: Using Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Method 2: Using OpenSSL
openssl rand -base64 50
```

Copy the output and paste it into your `.env` file as the SECRET_KEY value.

### Step 6: Apply Database Migrations

Migrations create the necessary database tables based on your Django models.

```bash
# Make sure you're in django-api directory with activated virtual environment
cd django-api

# Apply migrations
python manage.py migrate

# You should see output like:
# Operations to perform:
#   Apply all migrations: admin, api, auth, contenttypes, sessions, authtoken
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   ...
```

**What just happened?**
- Django created all necessary tables in your PostgreSQL database
- Tables for authentication, sessions, API models (Book, Author, etc.)
- Indexes and constraints were applied

### Step 7: Create Superuser

Create an admin account to access Django admin panel:

```bash
python manage.py createsuperuser

# You'll be prompted for:
# Username: admin
# Email: admin@example.com
# Password: [enter secure password]
# Password (again): [confirm password]
```

### Step 8: Verify Database Setup

```bash
# Connect to PostgreSQL
psql -U django_user -d django_drf_db -h localhost

# List all tables
\dt

# You should see tables like:
# api_author
# api_book
# api_category
# api_publisher
# api_review
# auth_user
# authtoken_token
# ... and more

# Exit
\q
```

---

## Docker Setup

Docker provides a consistent environment across development and production. Let's set up Docker containers for PostgreSQL, Django, Nginx, and Redis.

> **📌 Note:** Recent improvements have been made to ensure reliable container startup. See [DOCKER_FIX_GUIDE.md](DOCKER_FIX_GUIDE.md) for details on the fixes applied to resolve container exit issues.

### Step 1: Install Docker

**On Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in for changes to take effect
```

**On macOS:**
1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Install and start Docker Desktop
3. Verify: `docker --version`

**On Windows:**
1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Install and start Docker Desktop
3. Enable WSL 2 backend (recommended)
4. Verify in PowerShell: `docker --version`

### Step 2: Verify Docker Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker
docker run hello-world
```

### Step 3: Build and Run Containers

```bash
# Navigate to project root
cd /path/to/django-drf

# Option 1: Quick automated test (recommended)
./scripts/test_docker_setup.sh

# Option 2: Manual setup
# Build Docker images
docker-compose build

# Start all services (PostgreSQL, Django, Redis, Nginx)
docker-compose up -d

# Check running containers
docker-compose ps
```

**What's running?**
- **db**: PostgreSQL 15 database
- **web**: Django application
- **redis**: Redis for caching
- **nginx**: Reverse proxy and static file server

### Step 4: Access the Application

```bash
# View logs
docker-compose logs -f web

# Access the application
# Open browser: http://localhost

# Access Django admin
# http://localhost/admin

# Access API
# http://localhost/api/

# Access API documentation
# http://localhost/api/schema/swagger-ui/
```

### Step 5: Execute Commands in Docker

```bash
# Run migrations in Docker
docker-compose exec web python manage.py migrate

# Create superuser in Docker
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Access PostgreSQL in Docker
docker-compose exec db psql -U django_user -d django_drf_db

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Stop and remove volumes (⚠️ This deletes data!)
docker-compose down -v
```

---

## Production Deployment

### Architecture Overview

```
Internet → [Nginx] → [Gunicorn] → [Django App] → [PostgreSQL]
                                                → [Redis]
```

**Components:**
- **Nginx**: Web server, reverse proxy, serves static files
- **Gunicorn**: Python WSGI HTTP server for Django
- **Django**: Your application
- **PostgreSQL**: Database
- **Redis**: Cache and session storage

### Deployment Options

#### Option 1: Traditional VPS Deployment (DigitalOcean, Linode, AWS EC2)

**Step 1: Provision Server**

Create a Ubuntu 22.04 server with:
- At least 2GB RAM
- 20GB storage
- SSH access enabled

**Step 2: Connect to Server**

```bash
# SSH into your server
ssh root@your-server-ip

# Or if using key-based authentication
ssh -i /path/to/private-key.pem ubuntu@your-server-ip
```

**Step 3: Initial Server Setup**

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx git curl

# Install Python 3.11 (if not available)
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

**Step 4: Create Application User**

```bash
# Create a user for running the application
sudo useradd -m -s /bin/bash django

# Switch to django user
sudo su - django
```

**Step 5: Clone Repository**

```bash
# As django user
cd ~
git clone https://github.com/MachariaP/django-drf.git
cd django-drf/django-api

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

**Step 6: Configure PostgreSQL**

```bash
# Switch back to root
exit

# Access PostgreSQL
sudo -u postgres psql

# Create production database
CREATE DATABASE django_drf_prod;
CREATE USER django_prod WITH PASSWORD 'very_secure_production_password';
GRANT ALL PRIVILEGES ON DATABASE django_drf_prod TO django_prod;
\c django_drf_prod
GRANT ALL ON SCHEMA public TO django_prod;
\q
```

**Step 7: Configure Environment Variables**

```bash
# As django user
sudo su - django
cd ~/django-drf/django-api

# Create production .env file
nano .env
```

Add production configuration:
```env
SECRET_KEY=generate-a-new-very-long-random-secret-key-for-production
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

DATABASE_URL=postgresql://django_prod:very_secure_production_password@localhost:5432/django_drf_prod

REDIS_URL=redis://localhost:6379/0

# Static and media files
STATIC_ROOT=/home/django/django-drf/django-api/staticfiles/
MEDIA_ROOT=/home/django/django-drf/django-api/media/
```

**Step 8: Collect Static Files and Migrate**

```bash
# Activate virtual environment
source ~/django-drf/django-api/venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

**Step 9: Configure Gunicorn**

The `gunicorn_config.py` file is already included. Test Gunicorn:

```bash
# Test Gunicorn
cd ~/django-drf/django-api
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Visit `http://your-server-ip:8000` to verify it works. Press Ctrl+C to stop.

**Step 10: Create Gunicorn Systemd Service**

```bash
# Exit to root user
exit

# Create systemd service file
sudo nano /etc/systemd/system/gunicorn.service
```

Paste this configuration:
```ini
[Unit]
Description=Gunicorn daemon for Django DRF
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/django-drf/django-api
Environment="PATH=/home/django/django-drf/django-api/venv/bin"
EnvironmentFile=/home/django/django-drf/django-api/.env
ExecStart=/home/django/django-drf/django-api/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/django/django-drf/django-api/gunicorn.sock \
          --config /home/django/django-drf/gunicorn_config.py \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable Gunicorn service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Check status
sudo systemctl status gunicorn
```

**Step 11: Configure Nginx**

The `nginx/nginx.conf` file is already included. Install it:

```bash
# Remove default Nginx config
sudo rm /etc/nginx/sites-enabled/default

# Create new config
sudo nano /etc/nginx/sites-available/django-drf
```

Paste (adjust domain and paths):
```nginx
upstream django {
    server unix:/home/django/django-drf/django-api/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    client_max_body_size 20M;
    
    location /static/ {
        alias /home/django/django-drf/django-api/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/django/django-drf/django-api/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/django-drf /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx
```

**Step 12: Setup SSL with Let's Encrypt (HTTPS)**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow prompts:
# Enter email
# Agree to terms
# Choose to redirect HTTP to HTTPS (recommended: option 2)

# Test auto-renewal
sudo certbot renew --dry-run
```

**Step 13: Setup Redis (Optional but Recommended)**

```bash
# Install Redis
sudo apt install -y redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf

# Find and change:
# supervised no → supervised systemd

# Restart Redis
sudo systemctl restart redis
sudo systemctl enable redis

# Test Redis
redis-cli ping
# Should respond: PONG
```

#### Option 2: Docker Production Deployment

Already configured in `docker-compose.yml` and `Dockerfile`. Simply:

```bash
# On production server
git clone https://github.com/MachariaP/django-drf.git
cd django-drf

# Create production .env
nano .env

# Build and start
docker-compose -f docker-compose.yml up -d --build

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

---

## Database Management

### Backup Database

**Manual Backup:**
```bash
# Local PostgreSQL
pg_dump -U django_user -d django_drf_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Production PostgreSQL
sudo -u postgres pg_dump django_drf_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Docker PostgreSQL
docker-compose exec db pg_dump -U django_user django_drf_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Automated Backup Script:**
```bash
# Use the provided script
chmod +x scripts/backup_database.sh
./scripts/backup_database.sh
```

### Restore Database

```bash
# Local PostgreSQL
psql -U django_user -d django_drf_db < backup_20240112_120000.sql

# Production
sudo -u postgres psql django_drf_prod < backup_20240112_120000.sql

# Docker
docker-compose exec -T db psql -U django_user -d django_drf_db < backup_20240112_120000.sql
```

### Database Migrations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback last migration
python manage.py migrate api 0001  # Replace with migration number

# Generate SQL for migration (without applying)
python manage.py sqlmigrate api 0001
```

---

## Monitoring and Maintenance

### View Logs

```bash
# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Docker logs
docker-compose logs -f web
docker-compose logs -f db
```

### System Monitoring

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check PostgreSQL connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check running processes
ps aux | grep gunicorn
ps aux | grep nginx
ps aux | grep postgres
```

### Performance Optimization

**PostgreSQL Tuning:**
```bash
# Edit PostgreSQL config
sudo nano /etc/postgresql/15/main/postgresql.conf

# Recommended settings for 2GB RAM:
shared_buffers = 512MB
effective_cache_size = 1536MB
maintenance_work_mem = 128MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 2621kB

# Restart PostgreSQL
sudo systemctl restart postgresql
```

**Django Caching:**
Already configured in settings.py. Ensure Redis is running for production.

### Restart Services

```bash
# Restart Gunicorn
sudo systemctl restart gunicorn

# Restart Nginx
sudo systemctl restart nginx

# Restart PostgreSQL
sudo systemctl restart postgresql

# Restart Redis
sudo systemctl restart redis

# Restart all Docker containers
docker-compose restart
```

---

## Troubleshooting

### Common Issues

#### Issue: Can't connect to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log

# Verify PostgreSQL is listening
sudo netstat -plunt | grep postgres
```

#### Issue: Database authentication failed

**Solution:**
```bash
# Check pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Ensure this line exists:
# local   all             all                                     peer
# host    all             all             127.0.0.1/32            md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Issue: Migrations fail

**Solution:**
```bash
# Show migration status
python manage.py showmigrations

# Fake problematic migration
python manage.py migrate --fake app_name migration_name

# Or reset migrations (⚠️ Development only!)
python manage.py migrate app_name zero
python manage.py migrate
```

#### Issue: Static files not loading

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings
# Verify Nginx configuration
sudo nginx -t

# Check file permissions
sudo chown -R django:www-data /home/django/django-drf/django-api/staticfiles/
sudo chmod -R 755 /home/django/django-drf/django-api/staticfiles/
```

#### Issue: Gunicorn won't start

**Solution:**
```bash
# Check Gunicorn service status
sudo systemctl status gunicorn

# View detailed logs
sudo journalctl -u gunicorn -n 50

# Test Gunicorn manually
sudo su - django
cd ~/django-drf/django-api
source venv/bin/activate
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Check socket file exists
ls -la /home/django/django-drf/django-api/gunicorn.sock
```

#### Issue: 502 Bad Gateway

**Solution:**
```bash
# Check if Gunicorn is running
sudo systemctl status gunicorn

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify socket connection in Nginx config
# Ensure Gunicorn socket matches Nginx upstream

# Restart both services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## Quick Reference Commands

### Development Commands

```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec web python manage.py migrate
```

### Database Commands

```bash
# Backup database
pg_dump -U django_user -d django_drf_db > backup.sql

# Restore database
psql -U django_user -d django_drf_db < backup.sql

# Connect to database
psql -U django_user -d django_drf_db
```

### Service Management

```bash
# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart postgresql

# Check service status
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status postgresql

# View service logs
sudo journalctl -u gunicorn -f
sudo journalctl -u nginx -f
```

---

## Next Steps

After successful deployment:

1. **Setup Monitoring** - Consider using tools like:
   - Sentry for error tracking
   - Datadog or New Relic for performance monitoring
   - UptimeRobot for uptime monitoring

2. **Implement CI/CD** - Automate deployment with:
   - GitHub Actions
   - GitLab CI
   - Jenkins

3. **Database Backups** - Setup automated backups:
   - Use `scripts/backup_database.sh` with cron
   - Cloud backup solutions (AWS RDS automated backups)

4. **Security Hardening**:
   - Keep packages updated
   - Use strong passwords
   - Enable firewall (ufw)
   - Regular security audits

5. **Performance Tuning**:
   - Enable Django caching
   - Optimize database queries
   - Use CDN for static files
   - Implement rate limiting

---

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Django and DRF documentation
3. Open an issue on GitHub
4. Check PostgreSQL logs

---

**🎉 Congratulations!** You now have a fully deployed Django REST Framework application with PostgreSQL!

