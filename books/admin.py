from django.contrib import admin
from .models import (
    Language,
    Publisher,
    Genre,
    Character,
    Award,
    Series,
    Category,
    Author,
    Book,
    Favorite,
)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at"]
    ordering = ["name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    ordering = ["name"]


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["name", "year"]
    search_fields = ["name"]
    list_filter = ["year"]
    ordering = ["-year", "name"]


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Basic Information", {"fields": ("name", "description")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "nationality", "birth_date", "created_at"]
    search_fields = ["name", "nationality", "bio"]
    list_filter = ["nationality", "birth_date", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Basic Information", {"fields": ("name", "bio")}),
        ("Personal Details", {"fields": ("birth_date", "nationality")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "price",
        "publication_date",
        "average_rating",
        "num_ratings",
        "created_at",
    ]
    list_filter = [
        "category",
        "author",
        "publisher",
        "language",
        "book_format",
        "publication_date",
        "average_rating",
        "created_at",
    ]
    search_fields = [
        "title",
        "isbn",
        "author__name",
        "category__name",
        "publisher__name",
        "series__name",
        "goodreads_id",
    ]
    readonly_fields = ["created_at", "updated_at", "rating_distribution"]
    filter_horizontal = ["genres", "characters", "awards"]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "isbn", "description", "goodreads_id")},
        ),
        ("Author & Publisher", {"fields": ("author", "publisher", "language")}),
        ("Categorization", {"fields": ("category", "genres", "characters", "awards")}),
        ("Series Information", {"fields": ("series", "series_info")}),
        ("Physical Properties", {"fields": ("page_count", "book_format", "edition")}),
        ("Dates", {"fields": ("publication_date", "first_publication_date")}),
        ("Pricing", {"fields": ("price",)}),
        (
            "Ratings & Reviews",
            {
                "fields": (
                    "average_rating",
                    "num_ratings",
                    "liked_percent",
                    "ratings_5_star",
                    "ratings_4_star",
                    "ratings_3_star",
                    "ratings_2_star",
                    "ratings_1_star",
                    "rating_distribution",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Best Books Ever",
            {"fields": ("bbe_score", "bbe_votes"), "classes": ("collapse",)},
        ),
        ("Media", {"fields": ("cover_image", "cover_image_url")}),
        ("Additional Information", {"fields": ("settings",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "book__title"]
    readonly_fields = ["created_at"]
