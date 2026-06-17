# Deployment Guide

## Production Deployment Steps

### 1. Server Setup

#### System Requirements
- Ubuntu 20.04+ or similar Linux distribution
- 2GB RAM minimum (4GB recommended)
- 20GB storage minimum
- Python 3.12+
- PostgreSQL 12+
- Nginx
- Supervisor or systemd

### 2. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.12 python3.12-venv python3-pip postgresql postgresql-contrib nginx -y

# Install build dependencies
sudo apt install libpq-dev gcc -y
```

### 3. PostgreSQL Setup

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE backend_db;
CREATE USER backend_user WITH PASSWORD 'strong_password_here';
ALTER ROLE backend_user SET client_encoding TO 'utf8';
ALTER ROLE backend_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE backend_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE backend_db TO backend_user;
\q
```

### 4. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/backend
sudo chown $USER:$USER /var/www/backend

# Clone repository
cd /var/www/backend
git clone <your-repo-url> .

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/prod.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production settings
```

### 5. Environment Configuration

Edit `/var/www/backend/.env`:

```env
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://backend_user:strong_password_here@localhost:5432/backend_db

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 6. Database Migration

```bash
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 7. Gunicorn Setup

Create `/etc/systemd/system/backend.service`:

```ini
[Unit]
Description=Backend Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/backend
Environment="PATH=/var/www/backend/venv/bin"
ExecStart=/var/www/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start backend
sudo systemctl enable backend
sudo systemctl status backend
```

### 8. Nginx Configuration

Create `/etc/nginx/sites-available/backend`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /var/www/backend/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/backend/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 10. Firewall Configuration

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Docker Deployment

### 1. Build and Deploy

```bash
# Build images
docker-compose -f docker-compose.yml up --build -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

### 2. View Logs

```bash
docker-compose logs -f backend
```

### 3. Restart Services

```bash
docker-compose restart backend
```

## Monitoring & Maintenance

### 1. Log Monitoring

```bash
# Application logs
tail -f /var/www/backend/logs/django.log

# Systemd logs
sudo journalctl -u backend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Database Backup

```bash
# Backup database
pg_dump -U backend_user backend_db > backup_$(date +%Y%m%d).sql

# Restore database
psql -U backend_user backend_db < backup_20240101.sql
```

### 3. Application Updates

```bash
cd /var/www/backend
git pull origin main
source venv/bin/activate
pip install -r requirements/prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart backend
```

## Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY configured
- [ ] PostgreSQL with strong password
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Firewall configured (UFW/iptables)
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Database regular backups
- [ ] Log rotation configured
- [ ] Security updates enabled
- [ ] Environment variables secured
- [ ] Admin panel URL changed (optional)

## Performance Optimization

### 1. Database Optimization

```python
# Add database indexes (already configured in models)
python manage.py showmigrations
```

### 2. Caching (Optional)

Install Redis:
```bash
sudo apt install redis-server
pip install django-redis
```

Add to settings.py:
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

### 3. Static File Serving

Already configured with WhiteNoise for efficient static file serving.

## Troubleshooting

### Application Won't Start

```bash
sudo systemctl status backend
sudo journalctl -u backend -n 50
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U backend_user -d backend_db -h localhost
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
sudo systemctl restart backend
```

### High Memory Usage

```bash
# Monitor resources
htop

# Adjust Gunicorn workers
# Edit /etc/systemd/system/backend.service
# Reduce --workers count
```

## Support

For deployment issues, check:
- Application logs: `/var/www/backend/logs/django.log`
- System logs: `sudo journalctl -u backend`
- Nginx logs: `/var/log/nginx/error.log`
