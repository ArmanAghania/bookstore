"""
Management command to import books from CSV file
"""

import csv
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_date

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
)


class Command(BaseCommand):
    help = "Import books from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Path to the CSV file containing book data"
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of books to process in each batch (default: 100)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limit the number of books to import (for testing)",
        )
        parser.add_argument(
            "--skip-duplicates",
            action="store_true",
            help="Skip books with duplicate ISBN",
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        batch_size = options["batch_size"]
        limit = options["limit"]
        skip_duplicates = options["skip_duplicates"]

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Validate CSV headers
                required_fields = ["title", "author", "isbn"]
                missing_fields = [
                    field for field in required_fields if field not in reader.fieldnames
                ]
                if missing_fields:
                    raise CommandError(
                        f"Missing required fields in CSV: {missing_fields}"
                    )

                self.stdout.write(f"Starting import from {csv_file}")
                self.stdout.write(f"Available fields: {reader.fieldnames}")

                books_created = 0
                books_skipped = 0
                books_with_errors = 0
                batch_books = []
                batch_rows = []

                for row_num, row in enumerate(
                    reader, start=2
                ):  # Start at 2 because of header
                    if limit and row_num - 1 > limit:
                        break

                    try:
                        # Process each row
                        book_data = self.process_row(row, skip_duplicates)
                        if book_data:
                            batch_books.append(book_data)
                            batch_rows.append(row)  # Store raw row for M2M processing
                            books_created += 1
                        else:
                            books_skipped += 1

                        # Process batch when it reaches batch_size
                        if len(batch_books) >= batch_size:
                            self.create_books_batch(batch_books, batch_rows)
                            self.stdout.write(f"Processed {books_created} books...")
                            batch_books = []
                            batch_rows = []

                    except Exception as e:
                        books_with_errors += 1
                        logger.error(f"Error processing row {row_num}: {e}")
                        if books_with_errors > 100:  # Stop if too many errors
                            self.stdout.write(
                                self.style.ERROR("Too many errors, stopping import")
                            )
                            break

                # Process remaining books in final batch
                if batch_books:
                    self.create_books_batch(batch_books, batch_rows)

                # Final summary
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Import completed!\n"
                        f"Books created: {books_created}\n"
                        f"Books skipped: {books_skipped}\n"
                        f"Books with errors: {books_with_errors}"
                    )
                )

        except FileNotFoundError:
            raise CommandError(f"File not found: {csv_file}")
        except Exception as e:
            raise CommandError(f"Error importing books: {e}")

    def process_row(self, row, skip_duplicates):
        """Process a single CSV row and return book data"""
        title = row.get("title", "").strip()
        author_name = row.get("author", "").strip()
        isbn = row.get("isbn", "").strip()

        # Skip empty rows
        if not title or not author_name:
            return None

        # Handle ISBN (limit to 13 characters)
        if (
            not isbn or isbn == "9999999999999" or len(isbn) > 13
        ):  # Invalid or too long ISBN
            isbn = f"AUTO{hash(title + author_name) % 100000000:08d}"
        else:
            isbn = isbn[:13]  # Truncate to 13 characters

        # Check for duplicates
        if skip_duplicates and Book.objects.filter(isbn=isbn).exists():
            return None

        # Get or create author
        author = self.get_or_create_author(author_name)

        # Get or create category (from genres field)
        category = self.get_category_from_genres(row.get("genres", ""))

        # Parse price
        price = self.parse_price(row.get("price", ""))

        # Parse publication date
        publication_date = self.parse_date(
            row.get("publishDate") or row.get("firstPublishDate")
        )
        first_publication_date = self.parse_date(row.get("firstPublishDate"))

        # Parse page count
        page_count = self.parse_int(row.get("pages"))

        # Parse rating data
        average_rating = self.parse_rating(row.get("rating"))
        num_ratings = self.parse_int(row.get("numRatings")) or 0
        liked_percent = self.parse_int(row.get("likedPercent"))
        bbe_score = self.parse_int(row.get("bbeScore"))
        bbe_votes = self.parse_int(row.get("bbeVotes"))

        # Parse rating breakdown
        ratings_breakdown = self.parse_ratings_breakdown(row.get("ratingsByStars"))

        # Get or create publisher
        publisher = self.get_or_create_publisher(row.get("publisher", ""))

        # Get or create language
        language = self.get_or_create_language(row.get("language", ""))

        # Get or create series
        series = self.get_or_create_series(row.get("series", ""))

        # Parse book format
        book_format = self.parse_book_format(row.get("bookFormat", ""))

        # Process settings
        settings = self.parse_settings(row.get("setting", ""))

        return {
            "title": title[:500],  # Updated max_length
            "isbn": isbn,
            "description": row.get("description", "")[:5000],  # Increased limit
            "author": author,
            "category": category,
            "price": price,
            "publication_date": publication_date,
            "first_publication_date": first_publication_date,
            "page_count": page_count,
            "average_rating": average_rating,
            "num_ratings": num_ratings,
            "liked_percent": liked_percent,
            "bbe_score": bbe_score,
            "bbe_votes": bbe_votes,
            "ratings_5_star": ratings_breakdown.get("5", 0),
            "ratings_4_star": ratings_breakdown.get("4", 0),
            "ratings_3_star": ratings_breakdown.get("3", 0),
            "ratings_2_star": ratings_breakdown.get("2", 0),
            "ratings_1_star": ratings_breakdown.get("1", 0),
            "publisher": publisher,
            "language": language,
            "series": series,
            "series_info": row.get("series", "")[:100],
            "book_format": book_format,
            "edition": row.get("edition", "")[:100],
            "cover_image_url": row.get("coverImg", "")[:500],
            "settings": settings,
            "goodreads_id": row.get("bookId", "")[:100],
        }

    def get_or_create_author(self, author_name):
        """Get or create author from name"""
        # Handle multiple authors (take first one)
        if "," in author_name:
            author_name = author_name.split(",")[0].strip()

        # Remove illustrator info
        if "(" in author_name:
            author_name = author_name.split("(")[0].strip()

        author_name = author_name[:100]  # Limit to model max_length

        author, created = Author.objects.get_or_create(
            name=author_name,
            defaults={
                "bio": f"Author of books imported from CSV",
                "nationality": "Unknown",
            },
        )
        return author

    def get_category_from_genres(self, genres_str):
        """Extract and get/create category from genres string"""
        if not genres_str:
            return None

        # Parse genres (they appear to be in a list format)
        try:
            # Clean up the genres string
            genres_str = genres_str.strip("[]'\"")
            if genres_str:
                # Take the first genre
                first_genre = genres_str.split("',")[0].strip("'\"")
                # Remove any leading/trailing quotes that might be left
                first_genre = first_genre.strip("'\"")
                if first_genre:
                    category, created = Category.objects.get_or_create(
                        name=first_genre[:50],  # Limit to model max_length
                        defaults={"description": f"Category for {first_genre} books"},
                    )
                    return category
        except Exception:
            pass

        return None

    def parse_price(self, price_str):
        """Parse price from string"""
        if not price_str or price_str == '""':
            return Decimal("9.99")  # Default price

        try:
            # Clean price string
            price_str = str(price_str).replace("$", "").replace(",", "").strip()
            if price_str:
                price = Decimal(price_str)
                if price > 0 and price < 1000:  # Reasonable price range
                    return price
        except (InvalidOperation, ValueError):
            pass

        return Decimal("9.99")  # Default price

    def parse_date(self, date_str):
        """Parse publication date from string"""
        if not date_str:
            return datetime(2000, 1, 1).date()  # Default date

        try:
            # Try different date formats
            formats = ["%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"]

            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_str.strip(), fmt).date()
                    if parsed_date.year >= 1900 and parsed_date.year <= 2030:
                        return parsed_date
                except ValueError:
                    continue

            # Try Django's parse_date
            parsed_date = parse_date(date_str.strip())
            if parsed_date:
                return parsed_date

        except Exception:
            pass

        return datetime(2000, 1, 1).date()  # Default date

    def parse_int(self, int_str):
        """Parse integer from string"""
        if not int_str:
            return None

        try:
            value = int(float(str(int_str).replace(",", "").strip()))
            if 0 < value < 10000:  # Reasonable page count range
                return value
        except (ValueError, TypeError):
            pass

        return None

    def parse_rating(self, rating_str):
        """Parse average rating from string"""
        if not rating_str:
            return None
        try:
            rating = float(str(rating_str).strip())
            if 0.0 <= rating <= 5.0:
                return round(rating, 2)
        except (ValueError, TypeError):
            pass
        return None

    def parse_ratings_breakdown(self, ratings_str):
        """Parse ratings breakdown from string like "['3444695', '1921313', ...]" """
        breakdown = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
        if not ratings_str:
            return breakdown

        try:
            # Clean and parse the ratings array
            ratings_str = ratings_str.strip("[]'\"")
            if ratings_str:
                ratings_list = [r.strip("'\"") for r in ratings_str.split("',")]
                if len(ratings_list) >= 5:
                    breakdown["5"] = (
                        int(ratings_list[0]) if ratings_list[0].isdigit() else 0
                    )
                    breakdown["4"] = (
                        int(ratings_list[1]) if ratings_list[1].isdigit() else 0
                    )
                    breakdown["3"] = (
                        int(ratings_list[2]) if ratings_list[2].isdigit() else 0
                    )
                    breakdown["2"] = (
                        int(ratings_list[3]) if ratings_list[3].isdigit() else 0
                    )
                    breakdown["1"] = (
                        int(ratings_list[4]) if ratings_list[4].isdigit() else 0
                    )
        except (ValueError, IndexError):
            pass

        return breakdown

    def get_or_create_publisher(self, publisher_name):
        """Get or create publisher from name"""
        if not publisher_name or publisher_name.strip() == "":
            return None

        publisher_name = publisher_name.strip()[:200]
        publisher, created = Publisher.objects.get_or_create(name=publisher_name)
        return publisher

    def get_or_create_language(self, language_name):
        """Get or create language from name"""
        if not language_name or language_name.strip() == "":
            return None

        language_name = language_name.strip()
        # Map common language names to codes
        language_map = {
            "English": ("en", "English"),
            "Spanish": ("es", "Spanish"),
            "French": ("fr", "French"),
            "German": ("de", "German"),
            "Italian": ("it", "Italian"),
            "Portuguese": ("pt", "Portuguese"),
            "Russian": ("ru", "Russian"),
            "Japanese": ("ja", "Japanese"),
            "Chinese": ("zh", "Chinese"),
        }

        if language_name in language_map:
            code, name = language_map[language_name]
        else:
            code = language_name[:2].lower()
            name = language_name[:50]

        language, created = Language.objects.get_or_create(
            code=code, defaults={"name": name}
        )
        return language

    def get_or_create_series(self, series_str):
        """Get or create series from series string"""
        if not series_str or series_str.strip() == "":
            return None

        # Extract series name (remove #number if present)
        series_name = series_str.strip()
        if "#" in series_name:
            series_name = series_name.split("#")[0].strip()

        series_name = series_name[:200]
        if series_name:
            series, created = Series.objects.get_or_create(name=series_name)
            return series
        return None

    def parse_book_format(self, format_str):
        """Parse book format from string"""
        if not format_str:
            return None

        format_str = format_str.lower().strip()
        format_map = {
            "hardcover": "hardcover",
            "paperback": "paperback",
            "mass market paperback": "mass_paperback",
            "audiobook": "audiobook",
            "ebook": "ebook",
            "kindle": "ebook",
            "board book": "board_book",
        }

        return format_map.get(format_str, "other")

    def parse_settings(self, settings_str):
        """Parse story settings/locations from string"""
        if not settings_str:
            return None

        try:
            # Clean up the settings string (it's in array format)
            settings_str = settings_str.strip("[]'\"")
            if settings_str:
                # Join multiple settings with comma
                settings_list = [s.strip("'\"") for s in settings_str.split("',")]
                return ", ".join(settings_list)[:500]  # Limit length
        except Exception:
            pass

        return None

    def create_books_batch(self, books_data, batch_rows):
        """Create books in individual transactions"""
        for i, book_data in enumerate(books_data):
            try:
                with transaction.atomic():
                    # Create the book
                    book = Book.objects.create(**book_data)

                    # Add many-to-many relationships using corresponding row
                    if i < len(batch_rows):
                        row = batch_rows[i]
                        self.add_genres_to_book(book, row.get("genres", ""))
                        self.add_characters_to_book(book, row.get("characters", ""))
                        self.add_awards_to_book(book, row.get("awards", ""))

            except Exception as e:
                # Log error but continue with other books
                logging.error(
                    f'Error creating book "{book_data.get("title", "Unknown")}": {e}'
                )

    def add_genres_to_book(self, book, genres_str):
        """Add genres to book from genres string"""
        if not genres_str:
            return

        try:
            # Parse genres array like "['Young Adult', 'Fiction', ...]"
            genres_str = genres_str.strip()

            # Handle different formats
            if genres_str.startswith("[") and genres_str.endswith("]"):
                # Remove brackets and parse as list
                genres_str = genres_str[1:-1]

            # Split by comma and clean each genre
            genres_list = []
            if genres_str:
                # Split by comma, but be careful with commas inside quotes
                import re

                # Use regex to split by comma, but not inside quotes
                parts = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", genres_str)

                for part in parts:
                    # Clean up each genre
                    genre_name = part.strip()
                    # Remove quotes from start and end
                    if genre_name.startswith("'") and genre_name.endswith("'"):
                        genre_name = genre_name[1:-1]
                    elif genre_name.startswith('"') and genre_name.endswith('"'):
                        genre_name = genre_name[1:-1]

                    # Clean up any remaining quotes and whitespace
                    genre_name = genre_name.strip("'\" \n\r\t")

                    # Remove any colons that might be at the end
                    if genre_name.endswith(":"):
                        genre_name = genre_name[:-1].strip()

                    # Only add if it's not empty and not just whitespace
                    if genre_name and genre_name.strip():
                        genres_list.append(genre_name.strip()[:50])

            # Add genres to book (limit to first 5)
            for genre_name in genres_list[:5]:
                if genre_name:
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                    book.genres.add(genre)

        except Exception as e:
            # Log the error for debugging
            import logging

            logging.error(f"Error parsing genres '{genres_str}': {e}")
            pass

    def add_characters_to_book(self, book, characters_str):
        """Add characters to book from characters string"""
        if not characters_str:
            return

        try:
            # Parse characters array
            characters_str = characters_str.strip("[]'\"")
            if characters_str:
                characters_list = [c.strip("'\"") for c in characters_str.split("',")]
                for char_name in characters_list[:10]:  # Limit to first 10 characters
                    if char_name:
                        char_name = char_name.strip()[:200]
                        character, created = Character.objects.get_or_create(
                            name=char_name
                        )
                        book.characters.add(character)
        except Exception:
            pass

    def add_awards_to_book(self, book, awards_str):
        """Add awards to book from awards string"""
        if not awards_str:
            return

        try:
            # Parse awards array
            awards_str = awards_str.strip("[]'\"")
            if awards_str:
                awards_list = [a.strip("'\"") for a in awards_str.split("',")]
                for award_name in awards_list[:10]:  # Limit to first 10 awards
                    if award_name and award_name != "":
                        award_name = award_name.strip()[:500]

                        # Extract year if present
                        year = None
                        if "(" in award_name and ")" in award_name:
                            try:
                                year_str = award_name.split("(")[-1].split(")")[0]
                                if year_str.isdigit():
                                    year = int(year_str)
                            except:
                                pass

                        award, created = Award.objects.get_or_create(
                            name=award_name, year=year
                        )
                        book.awards.add(award)
        except Exception:
            pass
