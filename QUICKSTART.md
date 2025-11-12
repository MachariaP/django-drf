# 🚀 Quick Start Guide - PostgreSQL Setup and Deployment

This is a condensed guide to get you started quickly. For detailed explanations, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## 📋 Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] PostgreSQL installed (or ready to install)
- [ ] Terminal/Command line access

---

## 🏃 Quick Setup (5 Minutes)

### Step 1: Clone and Setup Virtual Environment

```bash
# Clone repository
git clone https://github.com/MachariaP/django-drf.git
cd django-drf/django-api

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Setup PostgreSQL Database (Automated)

```bash
# Run the automated setup script
cd ../scripts
./setup_postgres.sh

# Follow the prompts to:
# - Install PostgreSQL (if needed)
# - Create database and user
# - Generate DATABASE_URL
```

**Or manually:**

```bash
# Access PostgreSQL
sudo -u postgres psql

# Run these commands:
CREATE DATABASE django_drf_db;
CREATE USER django_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE django_drf_db TO django_user;
\c django_drf_db
GRANT ALL ON SCHEMA public TO django_user;
\q
```

### Step 3: Configure Environment

```bash
cd ../django-api

# Copy example environment file
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

Update these values in `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://django_user:your_password@localhost:5432/django_drf_db
```

### Step 4: Initialize Django

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Step 5: Access Your API

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs (Swagger)**: http://localhost:8000/api/schema/swagger-ui/
- **API Docs (ReDoc)**: http://localhost:8000/api/schema/redoc/

---

## 🐳 Quick Docker Setup (Alternative)

If you prefer Docker:

```bash
# Navigate to project root
cd django-drf

# Copy Docker environment file
cp .env.docker.example .env

# Edit .env with your settings
nano .env

# Build and start containers
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
# http://localhost
```

---

## 🔥 Common Commands

### Development

```bash
# Start development server
python manage.py runserver

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Docker

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Run command in container
docker-compose exec web python manage.py [command]
```

### Database

```bash
# Backup database
./scripts/backup_database.sh

# Connect to PostgreSQL
psql -U django_user -d django_drf_db

# View tables
\dt

# Exit PostgreSQL
\q
```

---

## 🚀 Production Deployment Quick Guide

### Option 1: Traditional VPS (Ubuntu)

```bash
# On your server
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3-pip python3-dev libpq-dev postgresql nginx git

# 3. Clone repository
git clone https://github.com/MachariaP/django-drf.git
cd django-drf

# 4. Run setup script
cd scripts
./setup_postgres.sh

# 5. Configure Django
cd ../django-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 6. Setup environment
cp .env.example .env
nano .env  # Edit with production values (DEBUG=False)

# 7. Prepare Django
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 8. Configure Gunicorn service
sudo cp /path/to/gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 9. Configure Nginx
sudo cp nginx/conf.d/django.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# 10. Setup SSL (optional but recommended)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Option 2: Docker Deployment

```bash
# On your server
# Clone and configure
git clone https://github.com/MachariaP/django-drf.git
cd django-drf
cp .env.docker.example .env
nano .env  # Edit with production values

# Deploy
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 🔧 Troubleshooting Quick Fixes

### Can't connect to PostgreSQL?

```bash
# Check if running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Check connection
psql -U django_user -d django_drf_db
```

### Migration errors?

```bash
# Show migrations
python manage.py showmigrations

# Reset migrations (⚠️ development only!)
python manage.py migrate [app] zero
python manage.py migrate
```

### Docker issues?

```bash
# View logs
docker-compose logs -f web

# Restart containers
docker-compose restart

# Rebuild containers
docker-compose up -d --build --force-recreate
```

### Gunicorn not starting?

```bash
# Check status
sudo systemctl status gunicorn

# View logs
sudo journalctl -u gunicorn -n 50

# Test manually
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📚 Next Steps

1. **Read the full guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. **Explore the API**: Visit http://localhost:8000/api/schema/swagger-ui/
3. **Test endpoints**: Use the browsable API or tools like Postman
4. **Set up monitoring**: Configure logging and error tracking
5. **Enable backups**: Schedule the backup script with cron

---

## 🆘 Need Help?

- **Full Documentation**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **GitHub Issues**: https://github.com/MachariaP/django-drf/issues

---

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (50+ chars) | `django-insecure-...` |
| `DEBUG` | Debug mode (False in production) | `True` or `False` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection (optional) | `redis://localhost:6379/0` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,yourdomain.com` |

---

**🎉 Happy Coding!** Your Django REST Framework application is now set up with PostgreSQL!

For detailed explanations and advanced configuration, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
