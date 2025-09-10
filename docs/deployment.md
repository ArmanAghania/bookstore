# Deployment Guide

This guide covers deploying the Django Bookstore application to production environments.

## 🚀 Deployment Options

### 1. Docker Deployment (Recommended)
- **Pros**: Consistent environment, easy scaling, container orchestration
- **Cons**: Requires Docker knowledge
- **Best for**: Most production scenarios

### 2. Traditional Server Deployment
- **Pros**: Full control, no container overhead
- **Cons**: Environment management complexity
- **Best for**: Legacy systems, specific requirements

### 3. Cloud Platform Deployment
- **Pros**: Managed services, auto-scaling, high availability
- **Cons**: Vendor lock-in, cost considerations
- **Best for**: High-traffic applications

## 🐳 Docker Production Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Domain name (optional)
- SSL certificate (for HTTPS)

### Production Configuration

#### 1. Environment Variables
Create `docker-compose.prod.env`:

```bash
# Database Configuration
DB_NAME=bookstore_prod
DB_USER=postgres
DB_PASSWORD=your_very_secure_password_here
DB_HOST=db
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-production-secret-key-min-50-characters-long
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 2. Production Docker Compose
Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    restart: unless-stopped
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - db
    env_file:
      - docker-compose.prod.env

  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - docker-compose.prod.env

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl  # SSL certificates
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### 3. Production Nginx Configuration
Create `nginx.prod.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    # Upstream
    upstream django {
        server web:8000;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Static files
        location /static/ {
            alias /app/staticfiles/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Media files
        location /media/ {
            alias /app/media/;
            expires 1y;
            add_header Cache-Control "public";
        }

        # API rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Login rate limiting
        location /api/auth/login/ {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Main application
        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Deployment Steps

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Application Deployment
```bash
# Clone repository
git clone <repository-url>
cd bookstore

# Set up environment
cp docker-compose.prod.env.example docker-compose.prod.env
# Edit docker-compose.prod.env with your values

# Set up SSL certificates (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
sudo chown -R $USER:$USER ssl/

# Deploy application
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run initial setup
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

#### 3. SSL Certificate Renewal
```bash
# Create renewal script
sudo crontab -e

# Add this line for automatic renewal
0 12 * * * /usr/bin/certbot renew --quiet && docker compose -f /path/to/bookstore/docker-compose.yml -f /path/to/bookstore/docker-compose.prod.yml restart nginx
```

## 🖥️ Traditional Server Deployment

### Prerequisites
- Ubuntu 20.04+ or CentOS 8+
- Python 3.11+
- PostgreSQL 13+
- Nginx
- SSL certificate

### Installation Steps

#### 1. System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3.11 python3.11-venv python3.11-dev postgresql postgresql-contrib nginx git
```

#### 2. Database Setup
```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE bookstore_prod;
CREATE USER bookstore_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE bookstore_prod TO bookstore_user;
\q
```

#### 3. Application Setup
```bash
# Create application user
sudo adduser --system --group bookstore
sudo mkdir -p /opt/bookstore
sudo chown bookstore:bookstore /opt/bookstore

# Clone and setup application
cd /opt/bookstore
sudo -u bookstore git clone <repository-url> .
sudo -u bookstore python3.11 -m venv venv
sudo -u bookstore venv/bin/pip install -r requirements.txt
```

#### 4. Configuration
```bash
# Create production settings
sudo -u bookstore cp .env.example .env
sudo -u bookstore nano .env

# Set up systemd service
sudo nano /etc/systemd/system/bookstore.service
```

Systemd service file:
```ini
[Unit]
Description=Django Bookstore Application
After=network.target

[Service]
Type=notify
User=bookstore
Group=bookstore
WorkingDirectory=/opt/bookstore
Environment=PATH=/opt/bookstore/venv/bin
ExecStart=/opt/bookstore/venv/bin/gunicorn --bind unix:/opt/bookstore/bookstore.sock bookstore.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 5. Nginx Configuration
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/bookstore
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /static/ {
        alias /opt/bookstore/staticfiles/;
    }

    location /media/ {
        alias /opt/bookstore/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/bookstore/bookstore.sock;
    }
}
```

#### 6. Start Services
```bash
# Enable and start services
sudo systemctl enable bookstore
sudo systemctl start bookstore
sudo systemctl enable nginx
sudo systemctl restart nginx

# Run initial setup
sudo -u bookstore /opt/bookstore/venv/bin/python manage.py migrate
sudo -u bookstore /opt/bookstore/venv/bin/python manage.py createsuperuser
sudo -u bookstore /opt/bookstore/venv/bin/python manage.py collectstatic --noinput
```

## ☁️ Cloud Platform Deployment

### AWS Deployment

#### 1. EC2 + RDS Setup
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Create RDS PostgreSQL instance
# Configure security groups
# Set up Elastic Load Balancer
```

#### 2. Application Deployment
```bash
# Use Docker deployment on EC2
# Configure RDS connection
# Set up CloudFront for static files
# Use Route 53 for DNS
```

### Google Cloud Platform

#### 1. Cloud Run Deployment
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/bookstore', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/bookstore']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'bookstore', '--image', 'gcr.io/$PROJECT_ID/bookstore', '--platform', 'managed', '--region', 'us-central1']
```

### Heroku Deployment

#### 1. Heroku Setup
```bash
# Install Heroku CLI
# Create Procfile
# Configure environment variables
# Deploy application
```

Procfile:
```
web: gunicorn bookstore.wsgi:application --log-file -
```

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up security headers
- [ ] Configure rate limiting
- [ ] Use strong database passwords
- [ ] Enable database SSL
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Backup strategy
- [ ] Monitor logs

### Security Headers
```python
# settings.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

## 📊 Monitoring and Logging

### Application Monitoring
```bash
# Set up logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/bookstore/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Checks
```python
# health_check.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        connection.ensure_connection()
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

## 🔄 Backup and Recovery

### Database Backup
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U bookstore_user bookstore_prod > $BACKUP_DIR/bookstore_$DATE.sql
find $BACKUP_DIR -name "bookstore_*.sql" -mtime +7 -delete
```

### Media Files Backup
```bash
# Backup media files
rsync -av /opt/bookstore/media/ /opt/backups/media/
```

## 🚀 Scaling Considerations

### Horizontal Scaling
- Use multiple application servers
- Implement load balancing
- Use external database service
- Add Redis for caching
- Use CDN for static files

### Performance Optimization
- Database query optimization
- Implement caching
- Use database indexes
- Optimize static files
- Enable gzip compression

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [SSL/TLS Best Practices](https://ssl-config.mozilla.org/)
- [Docker Production Best Practices](https://docs.docker.com/develop/dev-best-practices/)
