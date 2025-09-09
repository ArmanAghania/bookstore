from django.contrib import admin
from .models import Category, Author, Book, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "created_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "nationality", "birth_date", "created_at"]
    search_fields = ["name", "nationality"]
    list_filter = ["nationality", "birth_date", "created_at"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "price",
        "publication_date",
        "created_at",
    ]
    list_filter = ["category", "author", "publication_date", "created_at"]
    search_fields = ["title", "isbn", "author__name", "category__name"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Basic Information", {"fields": ("title", "isbn", "description")}),
        (
            "Details",
            {
                "fields": (
                    "author",
                    "category",
                    "price",
                    "publication_date",
                    "page_count",
                )
            },
        ),
        ("Media", {"fields": ("cover_image",)}),
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
