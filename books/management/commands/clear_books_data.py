"""
Management command to clear books and related data (except users)
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import (
    Book,
    Author,
    Category,
    Genre,
    Character,
    Award,
    Publisher,
    Language,
    Series,
    Favorite,
)


class Command(BaseCommand):
    help = "Clear all books and related data (except users)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirm that you want to delete all data",
        )

    def handle(self, *args, **options):
        if not options["confirm"]:
            self.stdout.write(
                self.style.WARNING(
                    "This will delete ALL books and related data (except users)!\n"
                    "Use --confirm flag to proceed."
                )
            )
            return

        self.stdout.write("Starting to clear books and related data...")

        with transaction.atomic():
            # Clear in order to respect foreign key constraints
            # First clear many-to-many relationships
            self.stdout.write("Clearing many-to-many relationships...")

            # Clear favorites (user relationships)
            favorites_count = Favorite.objects.count()
            Favorite.objects.all().delete()
            self.stdout.write(f"Deleted {favorites_count} favorites")

            # Clear books (this will cascade to related data)
            books_count = Book.objects.count()
            Book.objects.all().delete()
            self.stdout.write(f"Deleted {books_count} books")

            # Clear remaining related objects
            authors_count = Author.objects.count()
            Author.objects.all().delete()
            self.stdout.write(f"Deleted {authors_count} authors")

            categories_count = Category.objects.count()
            Category.objects.all().delete()
            self.stdout.write(f"Deleted {categories_count} categories")

            genres_count = Genre.objects.count()
            Genre.objects.all().delete()
            self.stdout.write(f"Deleted {genres_count} genres")

            characters_count = Character.objects.count()
            Character.objects.all().delete()
            self.stdout.write(f"Deleted {characters_count} characters")

            awards_count = Award.objects.count()
            Award.objects.all().delete()
            self.stdout.write(f"Deleted {awards_count} awards")

            publishers_count = Publisher.objects.count()
            Publisher.objects.all().delete()
            self.stdout.write(f"Deleted {publishers_count} publishers")

            languages_count = Language.objects.count()
            Language.objects.all().delete()
            self.stdout.write(f"Deleted {languages_count} languages")

            series_count = Series.objects.count()
            Series.objects.all().delete()
            self.stdout.write(f"Deleted {series_count} series")

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleared all books and related data!\n"
                "Users and authentication data have been preserved."
            )
        )
