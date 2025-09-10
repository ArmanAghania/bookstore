from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

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
from .serializers import (
    CategorySerializer,
    AuthorSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
    FavoriteSerializer,
    BookSearchSerializer,
    BulkDeleteSerializer,
    GenreSerializer,
    CharacterSerializer,
    AwardSerializer,
    PublisherSerializer,
    LanguageSerializer,
    SeriesSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]
    ordering = ["name"]


class CharacterViewSet(viewsets.ModelViewSet):

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class AwardViewSet(viewsets.ModelViewSet):

    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "year"]
    ordering = ["-year", "name"]


class PublisherViewSet(viewsets.ModelViewSet):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class LanguageViewSet(viewsets.ModelViewSet):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "code"]
    ordering = ["name"]


class SeriesViewSet(viewsets.ModelViewSet):

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def search_all(self, request):
        search_query = request.query_params.get("search", "")
        queryset = self.get_queryset()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        queryset = queryset.order_by("name")[:100]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "nationality"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def search_all(self, request):
        search_query = request.query_params.get("search", "")
        queryset = self.get_queryset()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(nationality__icontains=search_query)
            )

        queryset = queryset.order_by("name")[:100]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):

    queryset = (
        Book.objects.select_related(
            "author", "category", "publisher", "language", "series"
        )
        .prefetch_related("genres", "characters", "awards")
        .all()
    )
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "category",
        "author",
        "publisher",
        "language",
        "series",
        "book_format",
        "publication_date",
        "average_rating",
    ]
    search_fields = ["title", "author__name", "description", "isbn"]
    ordering_fields = [
        "title",
        "price",
        "publication_date",
        "created_at",
        "average_rating",
        "num_ratings",
    ]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return BookCreateUpdateSerializer
        return BookDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def search(self, request):
        serializer = BookSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        queryset = self.get_queryset()
        data = serializer.validated_data

        if data.get("search"):
            search_term = data["search"]
            queryset = queryset.filter(
                Q(title__icontains=search_term)
                | Q(author__name__icontains=search_term)
                | Q(description__icontains=search_term)
                | Q(isbn__icontains=search_term)
                | Q(series__name__icontains=search_term)
                | Q(publisher__name__icontains=search_term)
            )

        if data.get("category"):
            queryset = queryset.filter(category_id=data["category"])
        if data.get("author"):
            queryset = queryset.filter(author_id=data["author"])
        if data.get("publisher"):
            queryset = queryset.filter(publisher_id=data["publisher"])
        if data.get("language"):
            queryset = queryset.filter(language_id=data["language"])
        if data.get("series"):
            queryset = queryset.filter(series_id=data["series"])
        if data.get("book_format"):
            queryset = queryset.filter(book_format=data["book_format"])

        if data.get("genres"):
            queryset = queryset.filter(genres__id__in=data["genres"]).distinct()

        if data.get("min_price"):
            queryset = queryset.filter(price__gte=data["min_price"])
        if data.get("max_price"):
            queryset = queryset.filter(price__lte=data["max_price"])

        if data.get("min_rating"):
            queryset = queryset.filter(average_rating__gte=data["min_rating"])
        if data.get("max_rating"):
            queryset = queryset.filter(average_rating__lte=data["max_rating"])

        if data.get("min_publication_date"):
            queryset = queryset.filter(
                publication_date__gte=data["min_publication_date"]
            )
        if data.get("max_publication_date"):
            queryset = queryset.filter(
                publication_date__lte=data["max_publication_date"]
            )

        if data.get("has_cover_image"):
            queryset = queryset.filter(
                Q(cover_image__isnull=False) | Q(cover_image_url__isnull=False)
            )

        if data.get("favorites_only") and request.user.is_authenticated:
            favorite_book_ids = Favorite.objects.filter(user=request.user).values_list(
                "book_id", flat=True
            )
            queryset = queryset.filter(id__in=favorite_book_ids)

        if data.get("ordering"):
            queryset = queryset.order_by(data["ordering"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BookListSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = BookListSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def bulk_delete(self, request):
        serializer = BulkDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_ids = serializer.validated_data["book_ids"]
        deleted_count, _ = Book.objects.filter(id__in=book_ids).delete()

        return Response(
            {
                "message": f"Successfully deleted {deleted_count} books.",
                "deleted_count": deleted_count,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def bulk_delete_filtered(self, request):

        search_serializer = BookSearchSerializer(data=request.query_params)
        search_serializer.is_valid(raise_exception=True)

        queryset = self.get_queryset()
        data = search_serializer.validated_data

        if data.get("search"):
            search_term = data["search"]
            queryset = queryset.filter(
                Q(title__icontains=search_term)
                | Q(author__name__icontains=search_term)
                | Q(description__icontains=search_term)
            )

        if data.get("category"):
            queryset = queryset.filter(category_id=data["category"])

        if data.get("author"):
            queryset = queryset.filter(author_id=data["author"])

        if data.get("min_price"):
            queryset = queryset.filter(price__gte=data["min_price"])
        if data.get("max_price"):
            queryset = queryset.filter(price__lte=data["max_price"])

        if data.get("min_publication_date"):
            queryset = queryset.filter(
                publication_date__gte=data["min_publication_date"]
            )
        if data.get("max_publication_date"):
            queryset = queryset.filter(
                publication_date__lte=data["max_publication_date"]
            )

        if data.get("favorites_only") and request.user.is_authenticated:
            favorite_book_ids = Favorite.objects.filter(user=request.user).values_list(
                "book_id", flat=True
            )
            queryset = queryset.filter(id__in=favorite_book_ids)

        deleted_count, _ = queryset.delete()

        return Response(
            {
                "message": f"Successfully deleted {deleted_count} books based on filters.",
                "deleted_count": deleted_count,
            },
            status=status.HTTP_200_OK,
        )


class FavoriteViewSet(viewsets.ModelViewSet):

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(
            "book", "book__author", "book__category"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        book_id = request.data.get("book_id")
        if not book_id:
            return Response(
                {"error": "book_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

        if not created:
            favorite.delete()
            return Response(
                {"message": "Book removed from favorites", "is_favorited": False}
            )
        else:
            return Response(
                {"message": "Book added to favorites", "is_favorited": True}
            )
