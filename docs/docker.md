# Docker Guide

This guide covers Docker setup, deployment, and management for the Django Bookstore application.

## 🐳 Overview

The application is containerized using Docker and Docker Compose with the following services:

- **web** - Django application server
- **db** - PostgreSQL database
- **nginx** - Reverse proxy and static file server

## 📁 Docker Files

### Core Files
- `Dockerfile` - Django application container
- `docker-compose.yml` - Multi-container orchestration
- `docker-compose.env` - Environment variables
- `nginx.conf` - Nginx configuration
- `start.sh` - Application startup script
- `.dockerignore` - Files to exclude from build context

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+

### Start the Application
```bash
# Navigate to the bookstore directory
cd bookstore

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Access the Application
- **Web Interface**: http://localhost
- **Admin Interface**: http://localhost/admin
- **API**: http://localhost/api/

## ⚙️ Configuration

### Environment Variables

The application uses `docker-compose.env` for configuration:

```bash
# Database Configuration
DB_NAME=bookstore
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# External Database Port (to avoid conflicts)
EXTERNAL_DB_PORT=5433
```

### Port Configuration

- **Web Application**: Port 80 (HTTP)
- **Database (External)**: Port 5433 (to avoid conflicts with local PostgreSQL)
- **Database (Internal)**: Port 5432

## 🏗️ Service Details

### Web Service
```yaml
web:
  build: .
  ports:
    - "8000:8000"
  volumes:
    - .:/app
    - static_volume:/app/staticfiles
    - media_volume:/app/media
  environment:
    - DB_HOST=db
    - DB_PORT=5432
  depends_on:
    - db
  env_file:
    - docker-compose.env
```

**Features:**
- Django application server
- Automatic database migrations
- Book data import on first run
- Static and media file serving
- Health checks

### Database Service
```yaml
db:
  image: postgres:15
  environment:
    POSTGRES_DB: ${DB_NAME}
    POSTGRES_USER: ${DB_USER}
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  ports:
    - "5433:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  env_file:
    - docker-compose.env
```

**Features:**
- PostgreSQL 15
- Persistent data storage
- Health checks
- Configurable credentials

### Nginx Service
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - static_volume:/app/staticfiles
    - media_volume:/app/media
  depends_on:
    - web
```

**Features:**
- Reverse proxy to Django
- Static file serving
- Media file serving
- Gzip compression
- Security headers

## 🔧 Development

### Local Development with Docker

```bash
# Start development environment
docker compose up -d

# View application logs
docker compose logs -f web

# Access Django shell
docker compose exec web python manage.py shell

# Run Django commands
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic

# Access database
docker compose exec db psql -U postgres -d bookstore
```

### Rebuilding Containers

```bash
# Rebuild and restart
docker compose up -d --build

# Rebuild specific service
docker compose build web
docker compose up -d web
```

### Database Management

```bash
# Create database backup
docker compose exec db pg_dump -U postgres bookstore > backup.sql

# Restore database backup
docker compose exec -T db psql -U postgres bookstore < backup.sql

# Reset database (WARNING: This will delete all data)
docker compose down -v
docker compose up -d
```

## 📊 Monitoring

### View Logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs web
docker compose logs db
docker compose logs nginx

# Follow logs in real-time
docker compose logs -f web
```

### Health Checks
```bash
# Check service status
docker compose ps

# Check application health
curl http://localhost/api/health/

# Check database connection
docker compose exec web python manage.py check --database default
```

### Resource Usage
```bash
# View resource usage
docker stats

# View specific container stats
docker stats bookstore-web-1
```

## 🚀 Production Deployment

### Production Configuration

1. **Update Environment Variables**
   ```bash
   # Set production values in docker-compose.env
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   SECRET_KEY=your-production-secret-key
   DB_PASSWORD=your-secure-production-password
   ```

2. **SSL/HTTPS Setup**
   - Use a reverse proxy (like Traefik or Nginx Proxy Manager)
   - Configure SSL certificates
   - Update ALLOWED_HOSTS

3. **Database Security**
   - Use strong passwords
   - Restrict database access
   - Regular backups

### Production Commands
```bash
# Production deployment
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Update application
git pull
docker compose build
docker compose up -d

# Database migrations
docker compose exec web python manage.py migrate
```

## 🔒 Security

### Security Best Practices

1. **Environment Variables**
   - Never commit secrets to version control
   - Use strong, unique passwords
   - Rotate secrets regularly

2. **Network Security**
   - Use internal networks for service communication
   - Expose only necessary ports
   - Use firewall rules

3. **Container Security**
   - Keep base images updated
   - Run containers as non-root users
   - Use minimal base images

### Security Headers

Nginx is configured with security headers:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

## 🐛 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# If port 5432 is already in use
# The application uses port 5433 externally
# Check if another PostgreSQL is running
sudo systemctl stop postgresql
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x start.sh
```

#### Database Connection Issues
```bash
# Check database logs
docker compose logs db

# Test database connection
docker compose exec web python manage.py dbshell
```

#### Static Files Not Loading
```bash
# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Check nginx configuration
docker compose exec nginx nginx -t
```

### Debug Mode

Enable debug mode for development:
```bash
# In docker-compose.env
DEBUG=True
```

### Reset Everything
```bash
# Stop and remove all containers, networks, and volumes
docker compose down -v

# Remove all images
docker compose down --rmi all

# Start fresh
docker compose up -d
```

## 📈 Performance

### Optimization Tips

1. **Database Optimization**
   - Use database indexes
   - Optimize queries
   - Regular maintenance

2. **Static Files**
   - Use CDN for static files
   - Enable gzip compression
   - Optimize images

3. **Caching**
   - Implement Redis caching
   - Use database query caching
   - Cache API responses

### Scaling

For high-traffic applications:
- Use multiple web containers
- Implement load balancing
- Use external database service
- Add Redis for caching

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Nginx Docker Image](https://hub.docker.com/_/nginx)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
