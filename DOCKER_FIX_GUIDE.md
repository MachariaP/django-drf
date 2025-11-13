# Docker Container Startup Fix

## Problem
The `django-drf_web_1` container was exiting with code 1, causing the Docker Compose stack to fail.

## Root Causes Identified

1. **Missing curl**: The healthcheck in `docker-compose.yml` used `curl -f http://localhost:8000/api/` but curl was not installed in the `python:3.11-slim` base image.

2. **Static files path mismatch**: The nginx configuration referenced `/app/staticfiles/` and `/app/media/`, but the docker-compose.yml volume mounts used `/staticfiles` and `/media` (without the `/app` prefix).

3. **Unreliable database waiting**: The original setup used a simple `sleep 10` to wait for the database, which was not reliable and could cause the web service to try connecting before PostgreSQL was ready.

## Fixes Applied

### 1. Added curl to Dockerfile
```dockerfile
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    curl \  # Added this line
    && rm -rf /var/lib/apt/lists/*
```

### 2. Fixed nginx path configuration
Updated `nginx/conf.d/django.conf`:
- Changed `/app/staticfiles/` → `/staticfiles/`
- Changed `/app/media/` → `/media/`

### 3. Created robust entrypoint script
Created `scripts/docker-entrypoint.sh` that:
- Actively checks database connectivity (up to 30 attempts with 2s intervals)
- Checks Redis connectivity (up to 15 attempts with 2s intervals)
- Only runs migrations after database is confirmed ready
- Provides clear logging throughout the startup process
- Exits with error code 1 if database is unreachable

### 4. Updated docker-compose.yml
Changed from inline shell command to using the entrypoint script:
```yaml
web:
  build: .
  entrypoint: ["/usr/local/bin/docker-entrypoint.sh"]
  command: ["gunicorn", "--config", "gunicorn_config.py", "config.wsgi:application"]
```

## Usage

To use the fixed Docker setup:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# Check the status of all services
docker-compose ps

# View logs for a specific service
docker-compose logs web
docker-compose logs -f web  # Follow logs in real-time

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

## Expected Behavior

When you run `docker-compose up`, you should see output similar to:

```
web_1    | 🚀 Starting Django application...
web_1    | ⏳ Waiting for database to be ready...
web_1    |    Attempt 1/30 - Database not ready yet, retrying in 2 seconds...
web_1    |    Attempt 2/30 - Database not ready yet, retrying in 2 seconds...
web_1    | ✅ Database is ready!
web_1    | ⏳ Waiting for Redis to be ready...
web_1    | ✅ Redis is ready!
web_1    | 📦 Running database migrations...
web_1    | Operations to perform:
web_1    |   Apply all migrations: admin, api, auth, contenttypes, sessions, authtoken
web_1    | Running migrations:
web_1    |   No migrations to apply.
web_1    | 📁 Collecting static files...
web_1    | ✅ Initialization complete!
web_1    | 🌐 Starting Gunicorn server...
web_1    | 🚀 Starting Gunicorn server...
web_1    | ✅ Gunicorn server ready with 5 workers!
web_1    | 📡 Listening on 0.0.0.0:8000
```

All four services should be running:
- `django-drf_db_1` - PostgreSQL database (healthy)
- `django-drf_redis_1` - Redis cache (healthy)
- `django-drf_web_1` - Django application (healthy)
- `django-drf_nginx_1` - Nginx reverse proxy (healthy)

## Troubleshooting

### If the web container still exits with code 1:

1. **Check database connectivity**:
   ```bash
   docker-compose logs db
   ```
   Ensure PostgreSQL is starting without errors.

2. **Check web service logs**:
   ```bash
   docker-compose logs web
   ```
   Look for connection errors or other issues.

3. **Verify environment variables**:
   The docker-compose.yml has the database connection hardcoded. Make sure it matches the database service configuration:
   - Database: `django_drf_db`
   - User: `drf_user`
   - Password: `30937594PHINE`
   - Host: `db` (service name)
   - Port: `5432`

4. **Start services individually**:
   ```bash
   docker-compose up db redis  # Start database and redis first
   # Wait until both are healthy
   docker-compose up web       # Then start web service
   ```

5. **Clean restart**:
   ```bash
   docker-compose down -v  # Remove all containers and volumes
   docker-compose build --no-cache  # Rebuild without cache
   docker-compose up
   ```

### If nginx shows unhealthy:

The nginx service depends on the web service. If web is not responding on port 8000, nginx will fail its healthcheck. Ensure the web service is fully started and healthy first.

## Verification

Once all services are running, you can verify:

1. **Check API endpoint**:
   ```bash
   curl http://localhost/api/
   ```

2. **Access Django admin** (after creating a superuser):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   Then visit: http://localhost/admin/

3. **View API documentation**:
   - http://localhost/api/schema/swagger-ui/
   - http://localhost/api/schema/redoc/

## Files Modified

- `Dockerfile` - Added curl, added entrypoint script
- `docker-compose.yml` - Changed command to use entrypoint script
- `nginx/conf.d/django.conf` - Fixed static/media paths
- `scripts/docker-entrypoint.sh` - New file for robust service initialization
