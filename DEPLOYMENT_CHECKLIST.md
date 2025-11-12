# 📋 Deployment Checklist

Use this checklist to ensure a smooth deployment of your Django REST Framework application.

## 🔧 Pre-Deployment

### Development Environment

- [ ] All code changes committed to Git
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Dependencies updated in requirements.txt
- [ ] Database migrations created and tested
- [ ] Environment variables documented
- [ ] Static files working correctly
- [ ] Media uploads working correctly

### Security Review

- [ ] `DEBUG = False` in production settings
- [ ] `SECRET_KEY` is unique and secure (50+ characters)
- [ ] Database credentials are strong
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] CORS settings configured properly
- [ ] CSRF protection enabled
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] No sensitive data in version control
- [ ] `.env` file is gitignored
- [ ] SSL/TLS certificates ready (for HTTPS)

### Database

- [ ] PostgreSQL installed on production server
- [ ] Database created
- [ ] Database user created with proper permissions
- [ ] Database backup strategy in place
- [ ] Connection pooling configured (if needed)
- [ ] Database indexes optimized
- [ ] Backup script tested
- [ ] Restore procedure tested

### Server Setup

- [ ] Production server provisioned
- [ ] SSH access configured
- [ ] Firewall configured
  - [ ] Port 80 (HTTP) open
  - [ ] Port 443 (HTTPS) open
  - [ ] Port 22 (SSH) open
  - [ ] PostgreSQL port restricted to localhost
- [ ] Domain name configured and pointing to server
- [ ] SSL certificate obtained (Let's Encrypt or commercial)
- [ ] Nginx installed
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Redis installed (if using caching)

---

## 🚀 Deployment Steps

### 1. Server Preparation

- [ ] Update system packages: `sudo apt update && sudo apt upgrade -y`
- [ ] Install dependencies: `sudo apt install -y python3-pip python3-dev libpq-dev postgresql nginx git`
- [ ] Create application user: `sudo useradd -m -s /bin/bash django`
- [ ] Configure PostgreSQL
- [ ] Start PostgreSQL service

### 2. Application Setup

- [ ] Clone repository to `/home/django/django-drf`
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install Gunicorn: `pip install gunicorn`
- [ ] Create `.env` file with production settings
- [ ] Verify environment variables loaded correctly

### 3. Django Configuration

- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Test Django runs: `python manage.py check --deploy`
- [ ] Test Gunicorn: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`

### 4. Gunicorn Service

- [ ] Copy `gunicorn_config.py` to project directory
- [ ] Create systemd service file: `/etc/systemd/system/gunicorn.service`
- [ ] Configure service to run as django user
- [ ] Configure service to use virtual environment
- [ ] Start service: `sudo systemctl start gunicorn`
- [ ] Enable service: `sudo systemctl enable gunicorn`
- [ ] Verify service running: `sudo systemctl status gunicorn`
- [ ] Check socket created: `ls -la gunicorn.sock`

### 5. Nginx Configuration

- [ ] Copy `nginx.conf` to `/etc/nginx/`
- [ ] Copy `django.conf` to `/etc/nginx/sites-available/`
- [ ] Create symlink: `sudo ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/`
- [ ] Update server_name in config with your domain
- [ ] Test Nginx config: `sudo nginx -t`
- [ ] Restart Nginx: `sudo systemctl restart nginx`
- [ ] Enable Nginx: `sudo systemctl enable nginx`
- [ ] Verify Nginx running: `sudo systemctl status nginx`

### 6. SSL/HTTPS Setup

- [ ] Install Certbot: `sudo apt install -y certbot python3-certbot-nginx`
- [ ] Obtain certificate: `sudo certbot --nginx -d yourdomain.com`
- [ ] Test certificate: `sudo certbot renew --dry-run`
- [ ] Verify auto-renewal scheduled
- [ ] Update Nginx to use HTTPS
- [ ] Force HTTPS redirect
- [ ] Test HTTPS connection

### 7. Redis Setup (Optional)

- [ ] Install Redis: `sudo apt install -y redis-server`
- [ ] Configure Redis: `/etc/redis/redis.conf`
- [ ] Set supervised to systemd
- [ ] Start Redis: `sudo systemctl restart redis`
- [ ] Enable Redis: `sudo systemctl enable redis`
- [ ] Test connection: `redis-cli ping`

---

## ✅ Post-Deployment Verification

### Application Testing

- [ ] Application accessible at domain: `https://yourdomain.com`
- [ ] API root accessible: `https://yourdomain.com/api/`
- [ ] Admin panel accessible: `https://yourdomain.com/admin/`
- [ ] API documentation accessible: `https://yourdomain.com/api/schema/swagger-ui/`
- [ ] Static files loading correctly
- [ ] Media uploads working
- [ ] Database queries working
- [ ] Authentication working
- [ ] All API endpoints responding
- [ ] CORS configured correctly

### Service Health

- [ ] Gunicorn running: `sudo systemctl status gunicorn`
- [ ] Nginx running: `sudo systemctl status nginx`
- [ ] PostgreSQL running: `sudo systemctl status postgresql`
- [ ] Redis running (if used): `sudo systemctl status redis`
- [ ] No errors in Gunicorn logs: `sudo journalctl -u gunicorn -n 50`
- [ ] No errors in Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- [ ] Application health check passing: `curl https://yourdomain.com/api/`

### Security Verification

- [ ] HTTPS working with valid certificate
- [ ] HTTP redirects to HTTPS
- [ ] Security headers present (check with browser dev tools)
- [ ] HSTS header set
- [ ] No sensitive data in responses
- [ ] Admin panel requires authentication
- [ ] API endpoints require proper authentication
- [ ] Rate limiting working
- [ ] CSRF protection enabled

### Performance Testing

- [ ] Response times acceptable (< 200ms for simple endpoints)
- [ ] Database queries optimized (check Django Debug Toolbar in dev)
- [ ] Static files cached properly
- [ ] Gzip compression enabled
- [ ] No N+1 query problems
- [ ] Connection pooling working (if configured)

---

## 📊 Monitoring Setup

### Logging

- [ ] Application logs configured
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Access logs enabled
- [ ] Log rotation configured: `/etc/logrotate.d/django`
- [ ] Centralized logging (optional)

### Backups

- [ ] Database backup script working: `./scripts/backup_database.sh`
- [ ] Backup schedule configured (cron)
- [ ] Backup retention policy set
- [ ] Backup restore tested
- [ ] Off-site backup storage configured (optional)

### Monitoring Tools

- [ ] Uptime monitoring configured (UptimeRobot, Pingdom)
- [ ] Server monitoring (New Relic, Datadog, etc.)
- [ ] Application performance monitoring
- [ ] Error tracking (Sentry, Rollbar)
- [ ] Alert notifications configured (email, Slack)

---

## 🔄 Continuous Deployment

### CI/CD Pipeline

- [ ] GitHub Actions / GitLab CI configured
- [ ] Automated tests run on commit
- [ ] Automated deployment to staging
- [ ] Manual approval for production deployment
- [ ] Rollback procedure documented
- [ ] Deployment notifications configured

### Git Workflow

- [ ] Main/master branch protected
- [ ] Required reviews before merge
- [ ] Staging branch for pre-production testing
- [ ] Feature branches for development
- [ ] Semantic versioning used for releases
- [ ] Deployment tags created

---

## 📝 Documentation

- [ ] Deployment guide updated
- [ ] API documentation updated
- [ ] Environment variables documented
- [ ] Server architecture documented
- [ ] Troubleshooting guide updated
- [ ] Team onboarding guide created
- [ ] Runbook for common issues created

---

## 🚨 Rollback Procedure

In case of deployment issues:

1. **Stop new deployment:**
   ```bash
   sudo systemctl stop gunicorn
   ```

2. **Restore from backup:**
   ```bash
   gunzip -c backup_file.sql.gz | psql -U django_user -d django_drf_db
   ```

3. **Revert code:**
   ```bash
   git checkout previous-stable-tag
   python manage.py migrate
   ```

4. **Restart services:**
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl restart nginx
   ```

5. **Verify rollback:**
   ```bash
   curl https://yourdomain.com/api/
   sudo systemctl status gunicorn
   ```

---

## 📞 Support Contacts

- **DevOps Team**: [contact info]
- **Database Admin**: [contact info]
- **Security Team**: [contact info]
- **On-call Engineer**: [contact info]

---

## 🎉 Deployment Complete!

Once all items are checked:

- [ ] Notify team of successful deployment
- [ ] Update deployment log
- [ ] Monitor for 24-48 hours
- [ ] Schedule post-deployment review
- [ ] Document any issues or lessons learned

---

**Last Updated**: [Date]
**Deployed By**: [Name]
**Version**: [Version Number]
**Git Commit**: [Commit SHA]
