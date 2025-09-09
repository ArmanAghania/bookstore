from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Language(models.Model):
    """Model for book languages"""

    code = models.CharField(max_length=10, unique=True)  # e.g., 'en', 'es', 'fr'
    name = models.CharField(max_length=50, unique=True)  # e.g., 'English', 'Spanish'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Model for book publishers"""

    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model for book genres"""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    """Model for book characters"""

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Award(models.Model):
    """Model for literary awards"""

    name = models.CharField(max_length=500)  # Some award names are very long
    year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ["name", "year"]

    def __str__(self):
        return f"{self.name} ({self.year})" if self.year else self.name


class Series(models.Model):
    """Model for book series"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Model for book categories"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Author(models.Model):
    """Model for book authors"""

    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Enhanced model for books"""

    # Basic Information
    title = models.CharField(max_length=500)  # Increased from 300
    isbn = models.CharField(max_length=13, unique=True, help_text="13-character ISBN")
    description = models.TextField(blank=True, null=True)

    # External IDs
    goodreads_id = models.CharField(max_length=100, blank=True, null=True)

    # Relationships
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name="books")
    characters = models.ManyToManyField(Character, blank=True, related_name="books")
    awards = models.ManyToManyField(Award, blank=True, related_name="books")
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    series = models.ForeignKey(
        Series, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )

    # Physical Properties
    page_count = models.PositiveIntegerField(blank=True, null=True)

    # Format choices
    FORMAT_CHOICES = [
        ("hardcover", "Hardcover"),
        ("paperback", "Paperback"),
        ("mass_paperback", "Mass Market Paperback"),
        ("audiobook", "Audiobook"),
        ("ebook", "E-book"),
        ("board_book", "Board Book"),
        ("other", "Other"),
    ]
    book_format = models.CharField(
        max_length=20, choices=FORMAT_CHOICES, blank=True, null=True
    )
    edition = models.CharField(max_length=100, blank=True, null=True)

    # Dates
    publication_date = models.DateField()
    first_publication_date = models.DateField(blank=True, null=True)

    # Pricing
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    # Ratings and Reviews
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    num_ratings = models.PositiveIntegerField(default=0)
    liked_percent = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Rating breakdown (from ratingsByStars field)
    ratings_5_star = models.PositiveIntegerField(default=0)
    ratings_4_star = models.PositiveIntegerField(default=0)
    ratings_3_star = models.PositiveIntegerField(default=0)
    ratings_2_star = models.PositiveIntegerField(default=0)
    ratings_1_star = models.PositiveIntegerField(default=0)

    # Best Books Ever specific scores
    bbe_score = models.PositiveIntegerField(blank=True, null=True)
    bbe_votes = models.PositiveIntegerField(blank=True, null=True)

    # Series Information
    series_info = models.CharField(
        max_length=100, blank=True, null=True
    )  # e.g., "Harry Potter #5"

    # Images
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)

    # Settings/Locations (stored as comma-separated values for simplicity)
    settings = models.TextField(
        blank=True, null=True, help_text="Story settings/locations"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
            models.Index(fields=["publication_date"]),
            models.Index(fields=["price"]),
            models.Index(fields=["average_rating"]),
            models.Index(fields=["num_ratings"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    @property
    def series_display(self):
        """Return formatted series information"""
        if self.series and self.series_info:
            return f"{self.series.name} - {self.series_info}"
        elif self.series:
            return self.series.name
        elif self.series_info:
            return self.series_info
        return None

    @property
    def rating_distribution(self):
        """Return rating distribution as percentages"""
        total = (
            self.ratings_5_star
            + self.ratings_4_star
            + self.ratings_3_star
            + self.ratings_2_star
            + self.ratings_1_star
        )
        if total == 0:
            return None
        return {
            "5": round((self.ratings_5_star / total) * 100, 1),
            "4": round((self.ratings_4_star / total) * 100, 1),
            "3": round((self.ratings_3_star / total) * 100, 1),
            "2": round((self.ratings_2_star / total) * 100, 1),
            "1": round((self.ratings_1_star / total) * 100, 1),
        }


class Favorite(models.Model):
    """Model for user's favorite books"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "book"]

    def __str__(self):
        return f"{self.user.username} likes {self.book.title}"
