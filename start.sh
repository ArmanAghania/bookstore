#!/bin/bash

set -e

echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser if it doesn't exist..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

echo "Checking if books need to be imported..."
BOOK_COUNT=$(python manage.py shell -c "from books.models import Book; print(Book.objects.count())" 2>/dev/null | tail -1)
if [ "$BOOK_COUNT" -eq 0 ] 2>/dev/null; then
    echo "No books found in database. Importing books from CSV..."
    if [ -f "books_1.Best_Books_Ever.csv" ]; then
        python manage.py import_books books_1.Best_Books_Ever.csv --batch-size 50
        echo "Books imported successfully"
    else
        echo "CSV file not found, skipping book import"
    fi
else
    echo "Books already exist in database ($BOOK_COUNT books). Skipping import."
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 bookstore.wsgi:application
