# 📜 Deployment Scripts

This directory contains automation scripts for database setup, deployment, and maintenance.

## Available Scripts

### 🗄️ setup_postgres.sh

Automated PostgreSQL installation and configuration script.

**What it does:**
- Detects your operating system (Linux, macOS, Windows)
- Installs PostgreSQL if not already installed
- Creates database and user for Django
- Configures proper permissions
- Generates DATABASE_URL for your .env file
- Tests database connection

**Usage:**
```bash
chmod +x setup_postgres.sh
./setup_postgres.sh
```

**Environment Variables (optional):**
```bash
export DB_NAME="custom_db_name"
export DB_USER="custom_user"
export DB_PASSWORD="custom_password"
./setup_postgres.sh
```

**Supported Platforms:**
- ✅ Ubuntu/Debian Linux
- ✅ RedHat/CentOS/Fedora Linux
- ✅ macOS (with Homebrew)
- ⚠️ Windows (manual installation required)

---

### 💾 backup_database.sh

Database backup automation script with compression and retention management.

**What it does:**
- Creates timestamped PostgreSQL database dumps
- Compresses backups with gzip
- Automatically deletes backups older than retention period (default: 30 days)
- Lists all existing backups with sizes and dates

**Usage:**
```bash
chmod +x backup_database.sh
./backup_database.sh
```

**Configuration:**
Edit the script or set environment variables:
```bash
export BACKUP_DIR="/path/to/backups"
export BACKUP_RETENTION_DAYS="60"
./backup_database.sh
```

**Schedule with Cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/scripts/backup_database.sh

# Add weekly backup every Sunday at 3 AM
0 3 * * 0 /path/to/scripts/backup_database.sh
```

**Restore from Backup:**
```bash
# Decompress and restore
gunzip -c backup_file.sql.gz | psql -U django_user -d django_drf_db

# Or with Docker
gunzip -c backup_file.sql.gz | docker-compose exec -T db psql -U django_user -d django_drf_db
```

---

### 🚀 deploy.sh

Production deployment automation script.

**What it does:**
- Pulls latest code from Git repository
- Creates pre-deployment database backup
- Installs/updates Python dependencies
- Runs database migrations
- Collects static files
- Runs tests (in staging environment)
- Restarts application services (Gunicorn, Nginx)
- Performs health checks

**Usage:**
```bash
chmod +x deploy.sh

# Deploy to staging (default)
./deploy.sh staging

# Deploy to production
./deploy.sh production
```

**Prerequisites:**
- Git repository configured
- Virtual environment set up
- Gunicorn systemd service configured
- Nginx configured and running
- Database credentials in .env file

**Safety Features:**
- Confirmation prompt before deployment
- Automatic pre-deployment backup
- Git branch verification
- Test suite execution (staging)
- Health checks after deployment

**Environment-specific behavior:**

**Staging:**
- Checks out `staging` branch
- Runs full test suite
- Less strict confirmation

**Production:**
- Checks out `main` branch
- Skips tests for faster deployment
- Requires explicit "yes" confirmation
- Creates timestamped backups

---

## 📋 Script Maintenance

### Making Scripts Executable

After cloning the repository:
```bash
chmod +x scripts/*.sh
```

### Testing Scripts

**Dry run (without actual changes):**
Edit the script and add `set -n` at the top to check syntax without execution.

**Test in staging first:**
Always test deployment scripts in a staging environment before running in production.

### Customization

All scripts support environment variable configuration. You can:

1. **Set variables inline:**
   ```bash
   DB_NAME="mydb" DB_USER="myuser" ./setup_postgres.sh
   ```

2. **Export variables:**
   ```bash
   export DB_NAME="mydb"
   export DB_USER="myuser"
   ./setup_postgres.sh
   ```

3. **Use .env file:**
   Scripts automatically load variables from `../django-api/.env`

---

## 🔒 Security Best Practices

1. **Never commit database passwords** to version control
2. **Use strong passwords** for database users
3. **Restrict script permissions:**
   ```bash
   chmod 700 scripts/*.sh  # Only owner can execute
   ```
4. **Encrypt backups** if storing sensitive data:
   ```bash
   gpg -c backup_file.sql.gz  # Encrypt with GPG
   ```
5. **Use separate credentials** for development, staging, and production

---

## 📊 Monitoring

### Check Script Execution

**View cron job logs:**
```bash
# System log
tail -f /var/log/syslog | grep CRON

# Cron mail
mail  # If mail is configured
```

**Manual logging:**
Add to your cron job:
```bash
0 2 * * * /path/to/scripts/backup_database.sh >> /var/log/backup.log 2>&1
```

### Health Checks

**After deployment:**
```bash
# Check service status
sudo systemctl status gunicorn
sudo systemctl status nginx

# Check application response
curl http://localhost/api/

# View recent logs
sudo journalctl -u gunicorn -n 100
```

---

## 🐛 Troubleshooting

### Script Permission Denied

```bash
chmod +x scripts/script_name.sh
```

### PostgreSQL Connection Failed

```bash
# Verify PostgreSQL is running
sudo systemctl status postgresql

# Check connection parameters
psql -U django_user -d django_drf_db -h localhost

# Review pg_hba.conf for authentication rules
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

### Backup Script Fails

```bash
# Check disk space
df -h

# Verify backup directory permissions
ls -la /path/to/backups

# Test pg_dump manually
pg_dump -U django_user -d django_drf_db > test_backup.sql
```

### Deployment Script Issues

```bash
# Check Git repository status
git status
git branch -a

# Verify virtual environment
source venv/bin/activate
which python

# Check Gunicorn service
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50
```

---

## 📖 Additional Resources

- **Django Deployment Docs**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Gunicorn Documentation**: https://docs.gunicorn.org/
- **Nginx Documentation**: https://nginx.org/en/docs/

---

## 🤝 Contributing

If you improve these scripts:
1. Test thoroughly in a non-production environment
2. Document your changes
3. Submit a pull request with clear description

---

**Need help?** See the main [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for detailed setup instructions.
