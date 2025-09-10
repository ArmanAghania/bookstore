from rest_framework import serializers
from django.db.models import Q
from .models import (
    Category,
    Author,
    Book,
    Favorite,
    Genre,
    Character,
    Award,
    Publisher,
    Language,
    Series,
)
from django.conf import settings


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "name"]
        read_only_fields = ["id"]


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ["id", "name", "year"]
        read_only_fields = ["id"]


class PublisherSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Publisher
        fields = ["id", "name", "books_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_books_count(self, obj):
        return obj.books.count()


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "code", "name"]
        read_only_fields = ["id"]


class SeriesSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = ["id", "name", "books_count"]
        read_only_fields = ["id"]

    def get_books_count(self, obj):
        return obj.books.count()


class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "books_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_books_count(self, obj):
        return obj.books.count()


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "bio",
            "birth_date",
            "nationality",
            "books_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_books_count(self, obj):
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """Serializer for book list view with enhanced information"""

    author_name = serializers.CharField(source="author.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    publisher_name = serializers.CharField(source="publisher.name", read_only=True)
    language_name = serializers.CharField(source="language.name", read_only=True)
    series_name = serializers.CharField(source="series.name", read_only=True)
    is_favorited = serializers.SerializerMethodField()
    cover_image_display = serializers.SerializerMethodField()
    rating_display = serializers.SerializerMethodField()
    genres_display = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "author_name",
            "category_name",
            "publisher_name",
            "language_name",
            "series_name",
            "series_info",
            "price",
            "publication_date",
            "page_count",
            "cover_image",
            "cover_image_url",
            "cover_image_display",
            "average_rating",
            "num_ratings",
            "rating_display",
            "book_format",
            "genres_display",
            "is_favorited",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, book=obj).exists()
        return False

    def get_cover_image_display(self, obj):
        """Return cover image URL (either uploaded or external URL)"""
        if obj.cover_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
        return obj.cover_image_url

    def get_rating_display(self, obj):
        """Return formatted rating display"""
        if obj.average_rating:
            return f"{obj.average_rating}/5.0 ({obj.num_ratings:,} ratings)"
        return "No ratings yet"

    def get_genres_display(self, obj):
        """Return first 3 genres for display"""
        return [genre.name for genre in obj.genres.all()[:3]]


class BookDetailSerializer(serializers.ModelSerializer):
    """Serializer for book detail view with complete information"""

    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    awards = AwardSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    cover_image_display = serializers.SerializerMethodField()
    rating_distribution = serializers.ReadOnlyField()
    series_display = serializers.ReadOnlyField()
    settings_list = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "description",
            "goodreads_id",
            "author",
            "category",
            "publisher",
            "language",
            "series",
            "series_info",
            "series_display",
            "genres",
            "characters",
            "awards",
            "price",
            "publication_date",
            "first_publication_date",
            "page_count",
            "book_format",
            "edition",
            "cover_image",
            "cover_image_url",
            "cover_image_display",
            "average_rating",
            "num_ratings",
            "liked_percent",
            "ratings_5_star",
            "ratings_4_star",
            "ratings_3_star",
            "ratings_2_star",
            "ratings_1_star",
            "rating_distribution",
            "bbe_score",
            "bbe_votes",
            "settings",
            "settings_list",
            "is_favorited",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, book=obj).exists()
        return False

    def get_cover_image_display(self, obj):
        """Return cover image URL (either uploaded or external URL)"""
        if obj.cover_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
        return obj.cover_image_url

    def get_settings_list(self, obj):
        """Return settings as a list"""
        if obj.settings:
            return [s.strip() for s in obj.settings.split(",") if s.strip()]
        return []


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating books with enhanced fields"""

    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), required=False
    )
    characters = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Character.objects.all(), required=False
    )
    awards = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Award.objects.all(), required=False
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "isbn",
            "description",
            "goodreads_id",
            "author",
            "category",
            "publisher",
            "language",
            "series",
            "series_info",
            "genres",
            "characters",
            "awards",
            "price",
            "publication_date",
            "first_publication_date",
            "page_count",
            "book_format",
            "edition",
            "cover_image",
            "cover_image_url",
            "average_rating",
            "num_ratings",
            "liked_percent",
            "bbe_score",
            "bbe_votes",
            "settings",
        ]

    def validate_isbn(self, value):
        """Validate ISBN format"""
        if len(value) != 13:
            raise serializers.ValidationError(
                "ISBN must be exactly 13 characters long."
            )
        if not value.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits.")
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for user favorites"""

    book = BookListSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "book", "book_id", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        book_id = validated_data.pop("book_id")

        # Check if book exists
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

        # Check if already favorited
        if Favorite.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError("Book is already in favorites.")

        return Favorite.objects.create(user=user, book=book)


class BookSearchSerializer(serializers.Serializer):
    """Enhanced serializer for book search parameters"""

    search = serializers.CharField(
        required=False, help_text="Search in title, author name, or description"
    )
    category = serializers.IntegerField(
        required=False, help_text="Filter by category ID"
    )
    author = serializers.IntegerField(required=False, help_text="Filter by author ID")
    publisher = serializers.IntegerField(
        required=False, help_text="Filter by publisher ID"
    )
    language = serializers.IntegerField(
        required=False, help_text="Filter by language ID"
    )
    series = serializers.IntegerField(required=False, help_text="Filter by series ID")
    genres = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="Filter by genre IDs",
    )
    book_format = serializers.ChoiceField(
        choices=[choice[0] for choice in Book.FORMAT_CHOICES],
        required=False,
        help_text="Filter by book format",
    )
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, help_text="Minimum price"
    )
    max_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, help_text="Maximum price"
    )
    min_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        help_text="Minimum average rating",
    )
    max_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        help_text="Maximum average rating",
    )
    min_publication_date = serializers.DateField(
        required=False, help_text="Minimum publication date"
    )
    max_publication_date = serializers.DateField(
        required=False, help_text="Maximum publication date"
    )
    favorites_only = serializers.BooleanField(
        required=False, help_text="Show only user's favorite books"
    )
    has_cover_image = serializers.BooleanField(
        required=False, help_text="Filter books with cover images"
    )
    ordering = serializers.ChoiceField(
        choices=[
            "title",
            "-title",
            "price",
            "-price",
            "publication_date",
            "-publication_date",
            "average_rating",
            "-average_rating",
            "num_ratings",
            "-num_ratings",
            "created_at",
            "-created_at",
        ],
        required=False,
        help_text="Order results by field",
    )


class BulkDeleteSerializer(serializers.Serializer):
    """Serializer for bulk delete operations"""

    book_ids = serializers.ListField(
        child=serializers.IntegerField(), help_text="List of book IDs to delete"
    )

    def validate_book_ids(self, value):
        if not value:
            raise serializers.ValidationError("At least one book ID is required.")
        return value
