# Django Bookstore

A comprehensive Django-based bookstore application with REST API, user authentication, book management, and modern web interface.

## 📚 Overview

Django Bookstore is a full-featured web application for managing a book collection with the following capabilities:

- **Book Management**: Add, edit, delete, and search books
- **User Authentication**: JWT-based authentication system
- **Favorites System**: Users can mark books as favorites
- **Advanced Search**: Search books by title, author, category, and more
- **Bulk Operations**: Bulk delete books with filtering
- **Image Support**: Upload and manage book cover images
- **Admin Interface**: Django admin for data management
- **Docker Support**: Containerized deployment with Docker Compose

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bookstore
   ```

2. **Start the application**
   ```bash
   docker compose up -d --build
   ```

3. **Access the application**
   - Web Interface: http://localhost
   - Admin Interface: http://localhost/admin

### Manual Setup

See [Development Setup Guide](docs/development.md) for detailed instructions.

## 📖 Documentation

- **[API Documentation](docs/api.md)** - REST API endpoints and usage
- **[Docker Guide](docs/docker.md)** - Docker setup and deployment
- **[Development Setup](docs/development.md)** - Local development environment
- **[Deployment Guide](docs/deployment.md)** - Production deployment instructions
- **[Features Overview](docs/features.md)** - Detailed feature descriptions

## 🏗️ Architecture

### Backend
- **Django 5.2.5** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT Authentication** - User authentication
- **Django Admin** - Administrative interface

### Frontend
- **Vanilla JavaScript** - Frontend logic
- **Tailwind CSS** - Styling
- **Font Awesome** - Icons
- **Responsive Design** - Mobile-friendly interface

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy and static file serving
- **PostgreSQL** - Database server

## 🎯 Key Features

### Book Management
- ✅ Add, edit, and delete books
- ✅ Upload book cover images
- ✅ Search and filter books
- ✅ Bulk delete operations
- ✅ Book details with ratings and reviews

### User Features
- ✅ User registration and authentication
- ✅ JWT-based secure authentication
- ✅ User favorites system
- ✅ Personal dashboard

### Admin Features
- ✅ Django admin interface
- ✅ All models registered with custom admin
- ✅ Advanced filtering and search
- ✅ Bulk operations support

### API Features
- ✅ RESTful API endpoints
- ✅ Pagination support
- ✅ Advanced search and filtering
- ✅ JWT authentication
- ✅ Comprehensive error handling

## 🔧 Configuration

### Environment Variables

The application uses environment variables for configuration. See [Docker Guide](docs/docker.md) for details.

### Database

The application supports PostgreSQL (default) and SQLite (development).

## 📱 Screenshots

### Book Management Interface
- Modern, responsive design
- Advanced search and filtering
- Bulk operations support
- Image upload functionality

### User Dashboard
- Personal book collection
- Favorites management
- User profile management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the [documentation](docs/)
- Open an issue on GitHub
- Review the [API documentation](docs/api.md)

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added Docker support
- **v1.2.0** - Enhanced search and filtering
- **v1.3.0** - Added bulk operations and image support

---

**Built with ❤️ using Django and modern web technologies**
