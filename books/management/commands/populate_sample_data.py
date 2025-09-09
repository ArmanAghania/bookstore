from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import Category, Author, Book
from datetime import date


class Command(BaseCommand):
    help = "Populate database with sample data for testing"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Creating sample data...")

            # Create Categories
            categories_data = [
                {"name": "Fiction", "description": "Fictional literature and novels"},
                {
                    "name": "Non-Fiction",
                    "description": "Non-fictional books and biographies",
                },
                {
                    "name": "Science Fiction",
                    "description": "Science fiction and fantasy",
                },
                {"name": "Mystery", "description": "Mystery and thriller novels"},
                {"name": "Romance", "description": "Romance novels and love stories"},
                {"name": "Biography", "description": "Biographies and autobiographies"},
            ]

            categories = {}
            for cat_data in categories_data:
                category, created = Category.objects.get_or_create(
                    name=cat_data["name"],
                    defaults={"description": cat_data["description"]},
                )
                categories[cat_data["name"]] = category
                if created:
                    self.stdout.write(f"Created category: {category.name}")

            # Create Authors
            authors_data = [
                {
                    "name": "George Orwell",
                    "bio": "English novelist and essayist, best known for his dystopian novel 1984",
                    "birth_date": date(1903, 6, 25),
                    "nationality": "British",
                },
                {
                    "name": "F. Scott Fitzgerald",
                    "bio": "American novelist and short story writer, best known for The Great Gatsby",
                    "birth_date": date(1896, 9, 24),
                    "nationality": "American",
                },
                {
                    "name": "Harper Lee",
                    "bio": "American novelist best known for To Kill a Mockingbird",
                    "birth_date": date(1926, 4, 28),
                    "nationality": "American",
                },
                {
                    "name": "J.K. Rowling",
                    "bio": "British author, best known for the Harry Potter series",
                    "birth_date": date(1965, 7, 31),
                    "nationality": "British",
                },
                {
                    "name": "Agatha Christie",
                    "bio": "English writer known for her detective novels",
                    "birth_date": date(1890, 9, 15),
                    "nationality": "British",
                },
                {
                    "name": "Isaac Asimov",
                    "bio": "American writer and professor of biochemistry, known for science fiction",
                    "birth_date": date(1920, 1, 2),
                    "nationality": "American",
                },
            ]

            authors = {}
            for author_data in authors_data:
                author, created = Author.objects.get_or_create(
                    name=author_data["name"], defaults=author_data
                )
                authors[author_data["name"]] = author
                if created:
                    self.stdout.write(f"Created author: {author.name}")

            # Create Books
            books_data = [
                {
                    "title": "1984",
                    "isbn": "9780451524935",
                    "description": "A dystopian social science fiction novel about totalitarian control",
                    "author": authors["George Orwell"],
                    "category": categories["Science Fiction"],
                    "price": 15.99,
                    "publication_date": date(1949, 6, 8),
                    "page_count": 328,
                },
                {
                    "title": "The Great Gatsby",
                    "isbn": "9780743273565",
                    "description": "A classic American novel set in the Jazz Age",
                    "author": authors["F. Scott Fitzgerald"],
                    "category": categories["Fiction"],
                    "price": 12.99,
                    "publication_date": date(1925, 4, 10),
                    "page_count": 180,
                },
                {
                    "title": "To Kill a Mockingbird",
                    "isbn": "9780061120084",
                    "description": "A novel about racial injustice and childhood innocence",
                    "author": authors["Harper Lee"],
                    "category": categories["Fiction"],
                    "price": 14.99,
                    "publication_date": date(1960, 7, 11),
                    "page_count": 281,
                },
                {
                    "title": "Harry Potter and the Philosopher's Stone",
                    "isbn": "9780747532699",
                    "description": "The first book in the Harry Potter series",
                    "author": authors["J.K. Rowling"],
                    "category": categories["Fiction"],
                    "price": 16.99,
                    "publication_date": date(1997, 6, 26),
                    "page_count": 223,
                },
                {
                    "title": "Murder on the Orient Express",
                    "isbn": "9780062693662",
                    "description": "A detective novel featuring Hercule Poirot",
                    "author": authors["Agatha Christie"],
                    "category": categories["Mystery"],
                    "price": 13.99,
                    "publication_date": date(1934, 1, 1),
                    "page_count": 256,
                },
                {
                    "title": "Foundation",
                    "isbn": "9780553293357",
                    "description": "The first book in the Foundation series",
                    "author": authors["Isaac Asimov"],
                    "category": categories["Science Fiction"],
                    "price": 17.99,
                    "publication_date": date(1951, 5, 1),
                    "page_count": 244,
                },
                {
                    "title": "Animal Farm",
                    "isbn": "9780451526342",
                    "description": "An allegorical novella about farm animals",
                    "author": authors["George Orwell"],
                    "category": categories["Fiction"],
                    "price": 11.99,
                    "publication_date": date(1945, 8, 17),
                    "page_count": 112,
                },
                {
                    "title": "The Murder of Roger Ackroyd",
                    "isbn": "9780062079998",
                    "description": "A detective novel with an innovative narrative technique",
                    "author": authors["Agatha Christie"],
                    "category": categories["Mystery"],
                    "price": 14.99,
                    "publication_date": date(1926, 6, 1),
                    "page_count": 288,
                },
            ]

            for book_data in books_data:
                book, created = Book.objects.get_or_create(
                    isbn=book_data["isbn"], defaults=book_data
                )
                if created:
                    self.stdout.write(f"Created book: {book.title}")

            self.stdout.write(
                self.style.SUCCESS("Successfully populated database with sample data!")
            )
            self.stdout.write(f"Created {Category.objects.count()} categories")
            self.stdout.write(f"Created {Author.objects.count()} authors")
            self.stdout.write(f"Created {Book.objects.count()} books")
