"""
Gunicorn configuration file for Django REST Framework application.

This file contains production-ready settings for running Django with Gunicorn.
Gunicorn is a Python WSGI HTTP server that handles concurrent requests.
"""

import multiprocessing
import os

# Server Socket
bind = "0.0.0.0:8000"  # Bind to all interfaces on port 8000
backlog = 2048  # Maximum number of pending connections

# Worker Processes
# Use WEB_CONCURRENCY environment variable if set, otherwise calculate based on CPU
# For memory-constrained environments (like Render free tier with 512MB), use fewer workers
# Default: 2 workers for free tier, or (2 x CPU cores) + 1 for unlimited resources
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
# Use gthread worker for better memory efficiency with threading
worker_class = os.getenv("WORKER_CLASS", "gthread")  # gthread is more memory-efficient than sync
worker_connections = 1000  # Maximum concurrent requests per worker
max_requests = 1000  # Restart workers after this many requests (prevents memory leaks)
max_requests_jitter = 50  # Randomize restart to prevent all workers restarting at once
timeout = 30  # Worker timeout in seconds
keepalive = 2  # Seconds to wait for requests on Keep-Alive connections

# Threading
# Use more threads per worker to handle concurrency with fewer worker processes
threads = int(os.getenv("THREADS_PER_WORKER", 4))  # Increased threads for gthread workers

# Server Mechanics
daemon = False  # Run in foreground (required for Docker)
pidfile = None  # No PID file needed for containerized deployments
umask = 0o007  # File permissions for created files
user = None  # Run as current user (set by Docker)
group = None  # Run as current group (set by Docker)
tmp_upload_dir = None  # Use default temp directory

# Logging
accesslog = "-"  # Log access to stdout
errorlog = "-"  # Log errors to stderr
loglevel = os.getenv("LOG_LEVEL", "info")  # Log level: debug, info, warning, error, critical
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Process Naming
proc_name = "django_drf"  # Process name visible in process lists

# Server Hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    print("🚀 Starting Gunicorn server...")

def on_reload(server):
    """Called when the configuration is reloaded."""
    print("🔄 Reloading Gunicorn configuration...")

def when_ready(server):
    """Called just after the server is started."""
    print(f"✅ Gunicorn server ready with {workers} workers!")
    print(f"📡 Listening on {bind}")

def worker_int(worker):
    """Called when a worker receives the INT or QUIT signal."""
    print(f"⚠️  Worker {worker.pid} interrupted")

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    print(f"❌ Worker {worker.pid} aborted")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    print(f"👷 Worker spawned (pid: {worker.pid})")

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    pass

def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    print(f"👋 Worker {worker.pid} exited")

def child_exit(server, worker):
    """Called just after a worker has been exited, in the master process."""
    pass

def pre_exec(server):
    """Called just before a new master process is forked."""
    print("🔄 Preparing to fork new master process...")

def pre_request(worker, req):
    """Called just before a worker processes the request."""
    # Useful for adding request tracking
    pass

def post_request(worker, req, environ, resp):
    """Called after a worker processes the request."""
    # Useful for cleanup or logging
    pass

def nworkers_changed(server, new_value, old_value):
    """Called just after num_workers has been changed."""
    print(f"👥 Number of workers changed from {old_value} to {new_value}")

# SSL/HTTPS (uncomment if using SSL directly with Gunicorn)
# keyfile = "/path/to/ssl/keyfile.key"
# certfile = "/path/to/ssl/certfile.crt"
# ssl_version = 2  # TLS version
# cert_reqs = 0  # Whether client certificate is required (0: no, 1: optional, 2: required)
# ca_certs = None  # CA certificates file
# ciphers = None  # Ciphers to use for SSL

# Security
limit_request_line = 4094  # Maximum size of HTTP request line in bytes
limit_request_fields = 100  # Maximum number of header fields
limit_request_field_size = 8190  # Maximum size of request header field in bytes

# Debugging
# reload = True  # Auto-reload on code changes (development only!)
# reload_extra_files = []  # Additional files to watch for reload
# spew = False  # Print every server request (very verbose)
# check_config = False  # Check configuration and exit

# Performance Tuning Tips:
# 1. For CPU-bound applications: workers = (2 x CPU cores) + 1
# 2. For I/O-bound applications: increase worker_connections and use async workers
# 3. Use threads for mixed workloads: threads = 2-4
# 4. Monitor memory usage and adjust workers accordingly
# 5. Use max_requests to prevent memory leaks from accumulating
# 6. Increase timeout for slow requests (large file uploads, complex queries)
# 7. Use --preload flag to reduce memory usage (loads app before forking)
# 
# Memory-Constrained Environments (e.g., Render Free Tier - 512MB):
# - Set WEB_CONCURRENCY=2 to limit workers
# - Use WORKER_CLASS=gthread for better memory efficiency
# - Increase THREADS_PER_WORKER=4 to handle more concurrent requests
# - Each worker uses ~60-100MB, so 2 workers + overhead fits in 512MB
# - Formula: (workers * avg_memory_per_worker) + base_overhead < total_memory
# - Example: (2 * 100MB) + 200MB overhead = ~400MB (safe for 512MB limit)

# Recommended Production Settings:
# - Use Nginx as reverse proxy in front of Gunicorn
# - Enable access logs for monitoring and debugging
# - Set appropriate timeout values based on your application
# - Use process managers like systemd or supervisor
# - Monitor worker memory usage and restart if necessary
# - Use connection pooling for database connections
# - Enable keepalive for better performance with HTTP/1.1
