# 🚀 Render Deployment Guide

Complete guide to deploy your Django REST Framework API on Render.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Testing Your API](#testing-your-api)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying to Render, ensure you have:

- **GitHub Account** - Your code must be in a GitHub repository
- **Render Account** - Sign up at [render.com](https://render.com) (free tier available)
- **Git** - For pushing code to your repository

---

## Quick Start

### Option 1: Deploy with Blueprint (Recommended)

1. **Fork/Clone this repository to your GitHub account**

2. **Connect to Render:**
   - Go to [render.com](https://render.com) and sign in
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and set up both database and web service

3. **Set Required Environment Variables:**
   - Go to your web service dashboard
   - Navigate to "Environment" tab
   - Set `DJANGO_SUPERUSER_PASSWORD` (keep it secure!)

4. **Deploy:**
   - Render will automatically build and deploy your application
   - Wait for the build to complete (usually 5-10 minutes)

---

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Ensure your code is pushed to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify `render.yaml` exists** in your repository root

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended for easy integration)
3. Authorize Render to access your repositories

### Step 3: Deploy Using Blueprint

1. **From Render Dashboard:**
   - Click **"New"** button
   - Select **"Blueprint"**
   
2. **Connect Repository:**
   - Select your GitHub repository (`MachariaP/django-drf`)
   - Choose the branch to deploy (usually `main`)
   
3. **Review Blueprint:**
   - Render will parse `render.yaml`
   - You should see:
     - **PostgreSQL Database** (`django-drf-db`)
     - **Web Service** (`django-drf-api`)
   
4. **Configure Service Name:**
   - Optionally customize the service name
   - This will be part of your URL: `https://your-service-name.onrender.com`

### Step 4: Set Environment Variables

Render will create most environment variables automatically from `render.yaml`. However, you need to manually set:

1. **Go to your web service dashboard**
2. **Click "Environment" tab**
3. **Add/Update these variables:**

   | Variable | Value | Notes |
   |----------|-------|-------|
   | `DJANGO_SUPERUSER_PASSWORD` | Your secure password | **Required** - Admin password |
   | `DJANGO_SUPERUSER_USERNAME` | `admin` | Auto-set from `render.yaml` |
   | `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | Auto-set from `render.yaml` |
   | `SECRET_KEY` | Auto-generated | Render generates this |
   | `DATABASE_URL` | Auto-connected | From PostgreSQL service |
   | `DEBUG` | `False` | Auto-set for production |

### Step 5: Deploy!

1. **Click "Apply Blueprint"** or **"Create New Resources"**
2. Render will:
   - Create PostgreSQL database
   - Build Docker image
   - Run migrations
   - Collect static files
   - Start Gunicorn server
   
3. **Monitor the deployment:**
   - Click on your web service
   - View the "Logs" tab to see progress
   - Look for: ✅ "Initialization complete! 🌐 Starting Gunicorn server..."

4. **Wait for deployment** (typically 5-10 minutes for first deploy)

---

## Testing Your API

### 1. Access Your API

Your API will be available at: `https://your-service-name.onrender.com`

### 2. Test Health Endpoint

```bash
curl https://your-service-name.onrender.com/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "api": "running"
}
```

### 3. Create a User Account

**Endpoint:** `POST /api/register/`

```bash
curl -X POST https://your-service-name.onrender.com/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Expected Response:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "reviews_count": 0
  },
  "token": "your-auth-token-here",
  "message": "User created successfully"
}
```

**Save the token** - you'll need it for authenticated requests!

### 4. Login (Get Token for Existing Users)

**Endpoint:** `POST /api/token/`

```bash
curl -X POST https://your-service-name.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

**Expected Response:**
```json
{
  "token": "your-auth-token-here"
}
```

### 5. Test Authenticated Endpoints

Use the token to access protected endpoints:

```bash
# List all books
curl https://your-service-name.onrender.com/api/books/ \
  -H "Authorization: Token your-auth-token-here"

# List all authors
curl https://your-service-name.onrender.com/api/authors/ \
  -H "Authorization: Token your-auth-token-here"

# Create a review (requires authentication)
curl -X POST https://your-service-name.onrender.com/api/reviews/ \
  -H "Authorization: Token your-auth-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "book": 1,
    "rating": 5,
    "title": "Great book!",
    "comment": "I really enjoyed this book."
  }'
```

### 6. Explore API Documentation

Visit the interactive API documentation:

- **Swagger UI:** `https://your-service-name.onrender.com/api/docs/`
- **ReDoc:** `https://your-service-name.onrender.com/api/redoc/`

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Auto-connected from Render |
| `SECRET_KEY` | Django secret key | Auto-generated by Render |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | `YourSecurePassword123!` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | `admin@example.com` |
| `ALLOWED_HOSTS` | Allowed hosts | `*` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | Update in settings |
| `WEB_CONCURRENCY` | Number of Gunicorn workers | `2` (for free tier) |
| `THREADS_PER_WORKER` | Threads per worker | `4` |
| `WORKER_CLASS` | Gunicorn worker class | `gthread` |

---

## Available Endpoints

### Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health/` | Health check |
| `POST` | `/api/register/` | Register new user |
| `POST` | `/api/token/` | Login and get token |
| `GET` | `/api/docs/` | API documentation (Swagger) |
| `GET` | `/api/redoc/` | API documentation (ReDoc) |

### Protected Endpoints (Token Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/books/` | List all books |
| `POST` | `/api/books/` | Create a book |
| `GET` | `/api/books/{id}/` | Get book details |
| `GET` | `/api/authors/` | List all authors |
| `POST` | `/api/authors/` | Create an author |
| `GET` | `/api/categories/` | List all categories |
| `GET` | `/api/publishers/` | List all publishers |
| `GET` | `/api/reviews/` | List all reviews |
| `POST` | `/api/reviews/` | Create a review |

### Read-Only for Unauthenticated Users

Many endpoints allow GET requests without authentication but require a token for POST/PUT/DELETE operations.

---

## Troubleshooting

### Build Failures

**Issue:** Build fails during deployment

**Solutions:**
1. Check the build logs in Render dashboard
2. Ensure all dependencies are in `requirements.txt`
3. Verify `Dockerfile` is correct
4. Check that `render.yaml` syntax is valid

### Database Connection Issues

**Issue:** "Unable to connect to database"

**Solutions:**
1. Verify `DATABASE_URL` environment variable is set
2. Check that PostgreSQL service is running
3. Ensure database and web service are in the same region
4. Wait for database to fully initialize (can take 1-2 minutes)

### Health Check Failures

**Issue:** Service shows as unhealthy

**Solutions:**
1. Test health endpoint manually: `curl https://your-service.onrender.com/api/health/`
2. Check application logs for errors
3. Verify database migrations ran successfully
4. Ensure Gunicorn is running on port 8000

### Static Files Not Loading

**Issue:** Admin panel or static files return 404

**Solutions:**
1. Check that `collectstatic` ran during deployment (view logs)
2. Verify `STATIC_ROOT` is set correctly in settings
3. Ensure WhiteNoise is in `MIDDLEWARE`

### Application Not Starting

**Issue:** Application crashes on startup

**Solutions:**
1. Check logs for error messages
2. Verify all environment variables are set
3. Test locally with Docker: `docker-compose up`
4. Ensure migrations are up to date

### Out of Memory (Free Tier)

**Issue:** "Out of memory (used over 512Mi)"

**Solutions:**
1. The free tier has a 512MB memory limit
2. Reduce number of Gunicorn workers:
   - Set `WEB_CONCURRENCY=2` in environment variables (already configured in `render.yaml`)
   - Use `gthread` worker class for better memory efficiency (default)
   - Increase threads per worker: `THREADS_PER_WORKER=4` (default)
3. Memory breakdown:
   - 2 workers × ~100MB = 200MB
   - Base overhead = ~200MB
   - Total = ~400MB (safe for 512MB limit)
4. For higher traffic, consider upgrading to a paid plan with more memory

---

## Post-Deployment Tasks

### 1. Create Sample Data (Optional)

Access the admin panel and add sample data, or use the Django shell:

```bash
# From Render dashboard, use Shell
python manage.py shell
```

### 2. Set Up Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain and follow DNS instructions

### 3. Monitor Your Application

- **Metrics:** Render provides CPU, memory, and bandwidth metrics
- **Logs:** Access real-time logs from the dashboard
- **Alerts:** Set up email notifications for downtime

### 4. Upgrade Plan (If Needed)

The free tier is great for testing, but for production:
- Consider upgrading for better performance
- Get persistent disk storage
- Remove auto-sleep on inactivity

---

## Security Best Practices

1. **Never commit secrets** to your repository
2. **Use strong passwords** for `DJANGO_SUPERUSER_PASSWORD`
3. **Regenerate `SECRET_KEY`** if it's ever exposed
4. **Enable HTTPS only** (Render provides SSL by default)
5. **Update `ALLOWED_HOSTS`** to your actual domain
6. **Configure CORS** properly for your frontend
7. **Keep dependencies updated** regularly

---

## Next Steps

1. ✅ Deploy your API to Render
2. ✅ Test all endpoints
3. ✅ Create user accounts
4. ✅ Explore the API using Swagger docs
5. 🚀 Build a frontend application
6. 📱 Connect a mobile app
7. 🔧 Add more features to your API

---

## Support

- **Render Docs:** [https://render.com/docs](https://render.com/docs)
- **Django REST Framework:** [https://www.django-rest-framework.org](https://www.django-rest-framework.org)
- **Repository Issues:** Report bugs and request features on GitHub

---

## Summary

You now have a fully deployed Django REST Framework API on Render with:

✅ PostgreSQL database
✅ Health check endpoint
✅ User registration and authentication
✅ Token-based API access
✅ Interactive API documentation
✅ Production-ready configuration

**Your API is ready to use!** 🎉

Share the URL with your users and start building amazing applications!
