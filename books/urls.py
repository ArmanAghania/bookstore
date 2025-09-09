from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, AuthorViewSet, BookViewSet, FavoriteViewSet,
    GenreViewSet, CharacterViewSet, AwardViewSet, PublisherViewSet,
    LanguageViewSet, SeriesViewSet
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"genres", GenreViewSet)
router.register(r"characters", CharacterViewSet)
router.register(r"awards", AwardViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"languages", LanguageViewSet)
router.register(r"series", SeriesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
