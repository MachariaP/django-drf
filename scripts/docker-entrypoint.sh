#!/bin/bash
set -e

echo "🚀 Starting Django application..."

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if python -c "
import os
import sys
import psycopg2
try:
    conn_str = os.getenv('DATABASE_URL', '')
    if not conn_str:
        print('ERROR: DATABASE_URL not set')
        sys.exit(1)
    if 'postgres' in conn_str:
        # Parse connection string - handle both postgres:// and postgresql://
        import re
        # Normalize postgres:// to postgresql://
        conn_str = conn_str.replace('postgres://', 'postgresql://', 1)
        match = re.search(r'postgresql://([^:]+):([^@]+)@([^:/]+):?(\d+)?/(.+)', conn_str)
        if match:
            user, password, host, port, dbname = match.groups()
            port = port or '5432'
            print(f'Connecting to {host}:{port}/{dbname} as {user}...')
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                connect_timeout=5
            )
            conn.close()
            sys.exit(0)
        else:
            print(f'ERROR: Could not parse DATABASE_URL format')
            sys.exit(1)
    else:
        print(f'ERROR: DATABASE_URL does not contain postgres')
        sys.exit(1)
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
"; then
        echo "✅ Database is ready!"
        break
    fi
    
    attempt=$((attempt + 1))
    echo "   Attempt $attempt/$max_attempts - Database not ready yet, retrying in 2 seconds..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Failed to connect to database after $max_attempts attempts"
    exit 1
fi

# Wait for Redis to be ready (if configured)
if [ -n "$REDIS_URL" ]; then
    echo "⏳ Waiting for Redis to be ready..."
    redis_attempts=15
    redis_attempt=0
    
    while [ $redis_attempt -lt $redis_attempts ]; do
        if python -c "
import os
import sys
try:
    import redis
    r = redis.from_url(os.getenv('REDIS_URL'), socket_connect_timeout=5)
    r.ping()
    sys.exit(0)
except Exception as e:
    print(f'Redis connection failed: {e}')
    sys.exit(1)
" 2>/dev/null; then
            echo "✅ Redis is ready!"
            break
        fi
        
        redis_attempt=$((redis_attempt + 1))
        echo "   Attempt $redis_attempt/$redis_attempts - Redis not ready yet, retrying in 2 seconds..."
        sleep 2
    done
    
    if [ $redis_attempt -eq $redis_attempts ]; then
        echo "⚠️  Warning: Could not connect to Redis, continuing anyway..."
    fi
fi

# Run database migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput || echo "⚠️  Superuser creation skipped (may already exist)"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Initialization complete!"
echo "🌐 Starting Gunicorn server..."

# Execute the main command (passed as arguments to this script)
exec "$@"
