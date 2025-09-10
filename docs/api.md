# API Documentation

This document provides comprehensive information about the Django Bookstore REST API.

## 🔗 Base URL

```
http://localhost/api/
```

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Authentication Endpoints

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Register
```http
POST /api/auth/user/
Content-Type: application/json

{
    "username": "new_user",
    "email": "user@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

## 📚 Books API

### List Books
```http
GET /api/books/
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `search` - Search term
- `category` - Category ID
- `author` - Author ID
- `ordering` - Sort field (title, price, publication_date, etc.)

**Response:**
```json
{
    "count": 1000,
    "next": "http://localhost/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "The Great Gatsby",
            "isbn": "9780743273565",
            "description": "A classic American novel...",
            "author": {
                "id": 1,
                "name": "F. Scott Fitzgerald"
            },
            "category": {
                "id": 1,
                "name": "Fiction"
            },
            "price": 12.99,
            "publication_date": "1925-04-10",
            "cover_image": "http://localhost/media/covers/gatsby.jpg",
            "average_rating": 4.2,
            "num_ratings": 150
        }
    ]
}
```

### Get Book Details
```http
GET /api/books/{id}/
```

### Create Book
```http
POST /api/books/
Content-Type: application/json

{
    "title": "New Book",
    "isbn": "9781234567890",
    "description": "Book description",
    "author": 1,
    "category": 1,
    "price": 15.99,
    "publication_date": "2024-01-01"
}
```

### Update Book
```http
PATCH /api/books/{id}/
Content-Type: application/json

{
    "title": "Updated Title",
    "price": 19.99
}
```

### Delete Book
```http
DELETE /api/books/{id}/
```

### Search Books
```http
GET /api/books/search/
```

**Query Parameters:**
- `search` - Search term
- `category` - Category ID
- `author` - Author ID
- `min_price` - Minimum price
- `max_price` - Maximum price
- `min_publication_date` - Start date (YYYY-MM-DD)
- `max_publication_date` - End date (YYYY-MM-DD)
- `favorites_only` - Show only user's favorites (true/false)

### Bulk Delete Books
```http
POST /api/books/bulk_delete/
Content-Type: application/json

{
    "book_ids": [1, 2, 3, 4, 5]
}
```

### Bulk Delete Filtered Books
```http
POST /api/books/bulk_delete_filtered/
Content-Type: application/json

{
    "search": "fiction",
    "category": 1,
    "author": 2
}
```

## 👥 Authors API

### List Authors
```http
GET /api/authors/
```

### Search Authors (Unpaginated)
```http
GET /api/authors/search_all/?search=stephen
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Stephen King",
        "nationality": "American",
        "birth_date": "1947-09-21",
        "bio": "American author of horror, supernatural fiction..."
    },
    {
        "id": 2,
        "name": "Stephen Hawking",
        "nationality": "British",
        "birth_date": "1942-01-08",
        "bio": "English theoretical physicist..."
    }
]
```

### Get Author Details
```http
GET /api/authors/{id}/
```

### Create Author
```http
POST /api/authors/
Content-Type: application/json

{
    "name": "New Author",
    "nationality": "American",
    "birth_date": "1980-01-01",
    "bio": "Author biography"
}
```

## 📂 Categories API

### List Categories
```http
GET /api/categories/
```

### Search Categories (Unpaginated)
```http
GET /api/categories/search_all/?search=fiction
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Science Fiction",
        "description": "Fiction dealing with futuristic concepts"
    },
    {
        "id": 2,
        "name": "Historical Fiction",
        "description": "Fiction set in the past"
    }
]
```

### Get Category Details
```http
GET /api/categories/{id}/
```

### Create Category
```http
POST /api/categories/
Content-Type: application/json

{
    "name": "New Category",
    "description": "Category description"
}
```

## ❤️ Favorites API

### List User Favorites
```http
GET /api/favorites/
```

**Response:**
```json
{
    "count": 25,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "book": {
                "id": 1,
                "title": "The Great Gatsby",
                "author": {
                    "id": 1,
                    "name": "F. Scott Fitzgerald"
                },
                "cover_image": "http://localhost/media/covers/gatsby.jpg"
            },
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### Add Favorite
```http
POST /api/favorites/
Content-Type: application/json

{
    "book_id": 1
}
```

### Remove Favorite
```http
DELETE /api/favorites/{id}/
```

### Toggle Favorite
```http
POST /api/favorites/toggle/
Content-Type: application/json

{
    "book_id": 1
}
```

## 🏷️ Additional APIs

### Genres
- `GET /api/genres/` - List genres
- `GET /api/genres/{id}/` - Get genre details
- `POST /api/genres/` - Create genre

### Publishers
- `GET /api/publishers/` - List publishers
- `GET /api/publishers/{id}/` - Get publisher details
- `POST /api/publishers/` - Create publisher

### Languages
- `GET /api/languages/` - List languages
- `GET /api/languages/{id}/` - Get language details
- `POST /api/languages/` - Create language

### Series
- `GET /api/series/` - List series
- `GET /api/series/{id}/` - Get series details
- `POST /api/series/` - Create series

## 📝 Error Handling

The API returns standard HTTP status codes and JSON error responses:

### 400 Bad Request
```json
{
    "field_name": ["This field is required."]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "A server error occurred."
}
```

## 🔍 Search Examples

### Search Books by Title
```http
GET /api/books/?search=gatsby
```

### Filter by Category and Author
```http
GET /api/books/?category=1&author=2
```

### Price Range Search
```http
GET /api/books/search/?min_price=10&max_price=25
```

### Date Range Search
```http
GET /api/books/search/?min_publication_date=2020-01-01&max_publication_date=2024-12-31
```

### Complex Search
```http
GET /api/books/search/?search=fiction&category=1&min_price=15&max_price=30&ordering=-publication_date
```

## 📊 Response Format

All list endpoints return paginated responses with the following structure:

```json
{
    "count": 1000,
    "next": "http://localhost/api/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
```

## 🔧 Rate Limiting

The API implements rate limiting to prevent abuse:
- **Authenticated users**: 1000 requests per hour
- **Anonymous users**: 100 requests per hour

## 📱 CORS Support

The API supports Cross-Origin Resource Sharing (CORS) for web applications.

## 🛠️ Development

For development and testing, you can use tools like:
- **Postman** - API testing
- **curl** - Command line testing
- **Django REST Framework browsable API** - Available at `/api/` endpoints

## 📚 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django Documentation](https://docs.djangoproject.com/)
