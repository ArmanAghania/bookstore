from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("books/", views.book_management, name="book_management"),
    path("favorites/", views.favorites, name="favorites"),
    path("logout/", views.logout_view, name="logout"),
]
