from django.core.management.base import BaseCommand
from books.models import Genre


class Command(BaseCommand):
    help = "Clean up malformed genre names in the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be cleaned without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        self.stdout.write("Cleaning up malformed genre names...")

        # Find genres that need cleaning
        genres_to_clean = []
        for genre in Genre.objects.all():
            original_name = genre.name
            cleaned_name = self.clean_genre_name(original_name)

            if original_name != cleaned_name:
                genres_to_clean.append((genre, original_name, cleaned_name))

        if not genres_to_clean:
            self.stdout.write(self.style.SUCCESS("No malformed genres found!"))
            return

        self.stdout.write(f"Found {len(genres_to_clean)} genres that need cleaning:")

        for genre, original, cleaned in genres_to_clean:
            self.stdout.write(f"  '{original}' -> '{cleaned}'")

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run mode - no changes made"))
            return

        # Clean up the genres
        cleaned_count = 0
        merged_count = 0

        for genre, original, cleaned in genres_to_clean:
            if not cleaned:  # Skip empty names
                self.stdout.write(f"Skipping empty genre: '{original}'")
                continue

            # Check if a genre with the cleaned name already exists
            existing_genre = Genre.objects.filter(name=cleaned).first()

            if existing_genre and existing_genre.id != genre.id:
                # Merge with existing genre
                self.stdout.write(f"Merging '{original}' into existing '{cleaned}'")

                # Move all books from the malformed genre to the clean one
                for book in genre.books.all():
                    book.genres.remove(genre)
                    book.genres.add(existing_genre)

                # Delete the malformed genre
                genre.delete()
                merged_count += 1
            else:
                # Just rename the genre
                self.stdout.write(f"Renaming '{original}' to '{cleaned}'")
                genre.name = cleaned
                genre.save()
                cleaned_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Cleanup completed!\n"
                f"Renamed: {cleaned_count}\n"
                f"Merged: {merged_count}"
            )
        )

    def clean_genre_name(self, name):
        """Clean a genre name by removing unwanted characters"""
        if not name:
            return ""

        # Remove quotes from start and end
        cleaned = name.strip()
        if cleaned.startswith("'") and cleaned.endswith("'"):
            cleaned = cleaned[1:-1]
        elif cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1]

        # Clean up any remaining quotes and whitespace
        cleaned = cleaned.strip("'\" \n\r\t")

        # Remove any colons that might be at the end
        if cleaned.endswith(":"):
            cleaned = cleaned[:-1].strip()

        # Remove any extra whitespace
        cleaned = cleaned.strip()

        # Limit length
        cleaned = cleaned[:50]

        return cleaned
