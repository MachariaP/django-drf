#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
#  Docker entrypoint – Django DRF (pretty + animated)
#  Author:  Phinehas Macharia
#  Date:    2025‑11‑13
# ──────────────────────────────────────────────────────────────

set -euo pipefail

# ────── Colors & spinner ─────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

spinner() {
    local pid=$1
    local delay=0.15
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local i=0
    while ps -p $pid > /dev/null; do
        printf "\r${BLUE}%s${NC} %s" "${spin:i++%${#spin}:1}" "$2"
        sleep $delay
    done
    printf "\r${GREEN}Done${NC} %s\n" "$2"
}

# ────── Helper: animated step ───────────────────────────────
step() {
    local msg=$1
    shift
    echo -n "${YELLOW}➜ $msg …${NC}"
    "$@" &
    spinner $! "$msg"
}

# ────── 1. Wait for Postgres ───────────────────────────────
step "Waiting for PostgreSQL" bash -c '
    until pg_isready -h "$POSTGRES_HOST" -p 5432 -U "$POSTGRES_USER" > /dev/null 2>&1; do
        sleep 1
    done
'

# ────── 2. Wait for Redis ───────────────────────────────────
step "Waiting for Redis" bash -c '
    until redis-cli -h redis ping | grep -q PONG > /dev/null 2>&1; do
        sleep 1
    done
'

# ────── 3. Django migrations ───────────────────────────────
step "Running migrations" python manage.py migrate --noinput

# ────── 4. Collect static files ────────────────────────────
step "Collecting static files" python manage.py collectstatic --noinput

# ────── 5. Create superuser (idempotent) ─────────────────────
step "Creating superuser" python manage.py createsuperuser \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" \
    --password "$DJANGO_SUPERUSER_PASSWORD" \
    --noinput || true

# ────── 6. Seed data (idempotent) ───────────────────────────
step "Seeding database" python manage.py seed_data || true   # ignore if command missing

# ────── 7. Start Gunicorn ───────────────────────────────────
echo -e "${GREEN}All systems GO! Starting Gunicorn…${NC}"
exec gunicorn your_project_name.wsgi:application \
    --config gunicorn_config.py \
    --bind 0.0.0.0:8000
