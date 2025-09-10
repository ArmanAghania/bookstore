# Django Bookstore - Docker Setup

This Docker setup allows you to run the Django bookstore application in a containerized environment with PostgreSQL database and Nginx reverse proxy.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone the repository and navigate to the bookstore directory:**
   ```bash
   cd bookstore
   ```

2. **Update environment variables:**
   Edit `docker-compose.env` file and update the following variables:
   - `SECRET_KEY`: Change to a secure secret key
   - `DB_PASSWORD`: Set a secure database password
   - `ALLOWED_HOSTS`: Add your domain name

3. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Web interface: http://localhost
   - API documentation: http://localhost/api/schema/swagger-ui/
   - Admin panel: http://localhost/admin/ (admin/admin123)

## Services

- **web**: Django application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **nginx**: Reverse proxy and static file server (port 80)

## Features

- ✅ Automatic database migrations
- ✅ Book import from CSV file (books_1.Best_Books_Ever.csv)
- ✅ Superuser creation (admin/admin123)
- ✅ Static file serving via Nginx
- ✅ Media file handling
- ✅ Health checks for database

## Environment Variables

The `docker-compose.env` file contains all necessary environment variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (set to False for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_*`: Database connection settings
- `CORS_ALLOW_ALL_ORIGINS`: CORS settings
- `JWT_*`: JWT token settings

## Production Deployment

For production deployment:

1. **Update security settings in `docker-compose.env`:**
   ```env
   DEBUG=False
   SECRET_KEY=your-super-secure-secret-key
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Use a reverse proxy with SSL:**
   - Update nginx.conf to include SSL configuration
   - Use Let's Encrypt for SSL certificates

3. **Database backup:**
   ```bash
   docker-compose exec db pg_dump -U postgres bookstore > backup.sql
   ```

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Access Django shell
docker-compose exec web python manage.py shell

# Create new superuser
docker-compose exec web python manage.py createsuperuser

# Import books manually
docker-compose exec web python manage.py import_books books_1.Best_Books_Ever.csv

# Run tests
docker-compose exec web python manage.py test

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete all data)
docker-compose down -v
```

## Troubleshooting

1. **Database connection issues:**
   - Ensure PostgreSQL is running: `docker-compose ps`
   - Check database logs: `docker-compose logs db`

2. **Static files not loading:**
   - Rebuild the container: `docker-compose up --build`
   - Check nginx logs: `docker-compose logs nginx`

3. **Book import issues:**
   - Ensure CSV file exists in the bookstore directory
   - Check web service logs: `docker-compose logs web`

## File Structure

```
bookstore/
├── Dockerfile              # Django application container
├── docker-compose.yml      # Multi-container setup
├── docker-compose.env      # Environment variables
├── nginx.conf             # Nginx configuration
├── start.sh               # Application startup script
├── .dockerignore          # Docker ignore file
├── requirements.txt       # Python dependencies
└── books_1.Best_Books_Ever.csv  # Book data
```
