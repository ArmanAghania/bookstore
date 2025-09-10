# Development Setup Guide

This guide covers setting up the Django Bookstore application for local development.

## 🛠️ Prerequisites

### Required Software
- **Python 3.11+** - Programming language
- **PostgreSQL 13+** - Database (or SQLite for development)
- **Git** - Version control
- **Node.js 16+** (optional) - For frontend tooling

### Recommended Tools
- **VS Code** - Code editor with Python extension
- **Postman** - API testing
- **pgAdmin** - PostgreSQL administration
- **Docker Desktop** - Containerization (alternative to local setup)

## 🚀 Quick Start

### Option 1: Docker Development (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd bookstore

# Start development environment
docker compose up -d

# Access the application
# Web: http://localhost
# Admin: http://localhost/admin
```

### Option 2: Local Development

```bash
# Clone the repository
git clone <repository-url>
cd bookstore

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Set up database
python manage.py migrate
python manage.py createsuperuser
python manage.py import_books  # Import sample data

# Start development server
python manage.py runserver
```

## 📁 Project Structure

```
bookstore/
├── authentication/          # User authentication app
│   ├── models.py           # User model
│   ├── views.py            # Authentication views
│   └── serializers.py      # User serializers
├── books/                  # Books management app
│   ├── models.py           # Book, Author, Category models
│   ├── views.py            # API views
│   ├── serializers.py      # Data serializers
│   ├── admin.py            # Django admin configuration
│   └── management/         # Custom management commands
│       └── commands/
│           ├── import_books.py
│           └── clean_genres.py
            └── clear_books_data.py
├── web/                    # Web interface app
│   ├── views.py            # Web page views
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── bookstore/              # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI configuration
├── docs/                   # Documentation
├── media/                  # User uploaded files
├── staticfiles/            # Collected static files
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker configuration
├── Dockerfile              # Docker image definition
└── README.md               # Project documentation
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DB_NAME=bookstore_dev
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-development-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Database Setup

#### PostgreSQL (Recommended)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Ubuntu/Debian
brew install postgresql  # macOS

# Create database
sudo -u postgres createdb bookstore_dev
sudo -u postgres createuser --interactive  # Create user

# Update .env with database credentials
```

#### SQLite (Development Only)
```bash
# No additional setup required
# Django will create db.sqlite3 automatically
```

### Django Settings

Key settings in `bookstore/settings.py`:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='bookstore'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## 🗄️ Database Management

### Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Sample Data
```bash
# Import books from CSV
python manage.py import_books

# Clean up malformed genres
python manage.py clean_genres

# Create superuser
python manage.py createsuperuser
```

### Database Shell
```bash
# Access Django shell
python manage.py shell

# Access database shell
python manage.py dbshell
```

## 🔧 Development Tools

### Django Admin
- **URL**: http://localhost:8000/admin/
- **Features**: Full CRUD operations for all models
- **Customizations**: Enhanced admin interface with filters and search

### API Documentation
- **Browsable API**: http://localhost:8000/api/
- **Interactive**: Test endpoints directly in browser
- **Authentication**: Login with JWT tokens

### Debugging
```python
# Django Debug Toolbar (optional)
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test books

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Structure
```
books/
├── tests/
│   ├── test_models.py      # Model tests
│   ├── test_views.py       # API view tests
│   ├── test_serializers.py # Serializer tests
│   └── test_management.py  # Management command tests
```

### API Testing
```bash
# Using curl
curl -X GET http://localhost:8000/api/books/
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Using Django shell
python manage.py shell
>>> from books.models import Book
>>> Book.objects.count()
```

## 🎨 Frontend Development

### Static Files
```bash
# Collect static files
python manage.py collectstatic

# Watch for changes (development)
python manage.py runserver --settings=bookstore.settings_dev
```

### JavaScript Development
- **Location**: `web/static/web/js/`
- **Main Files**: `api.js`, page-specific scripts
- **Libraries**: Vanilla JavaScript, Tailwind CSS

### CSS Development
- **Framework**: Tailwind CSS
- **Custom CSS**: `web/static/web/css/`
- **Responsive**: Mobile-first design

## 🔄 Git Workflow

### Branch Strategy
```bash
# Main branches
main                    # Production-ready code
develop                 # Integration branch

# Feature branches
feature/user-auth       # New features
bugfix/search-error     # Bug fixes
hotfix/security-patch   # Critical fixes
```

### Commit Convention
```bash
# Format: type(scope): description
feat(auth): add JWT authentication
fix(api): resolve pagination issue
docs(readme): update installation guide
test(books): add model tests
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🚀 Deployment Preparation

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set secure `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Run security checks

### Security Checks
```bash
# Django security check
python manage.py check --deploy

# Check for security issues
pip install safety
safety check

# Check dependencies
pip install pip-audit
pip-audit
```

## 🐛 Common Issues

### Database Connection
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U postgres -d bookstore_dev
```

### Port Conflicts
```bash
# Check port usage
sudo netstat -tulpn | grep :8000
sudo lsof -i :8000

# Kill process using port
sudo kill -9 <PID>
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x manage.py
```

### Virtual Environment
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Additional Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Development Tools
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Postman](https://www.postman.com/)

### Learning Resources
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
