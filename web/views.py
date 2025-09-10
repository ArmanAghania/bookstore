from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
import jwt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


def get_user_from_jwt(request):
    """Helper function to get user from JWT token in cookies"""
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return None

    try:
        token = AccessToken(access_token)
        user_id = token.payload.get("user_id")
        if user_id:
            return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, jwt.ExpiredSignatureError, User.DoesNotExist):
        pass

    return None


def home(request):
    """Home page with book listing"""
    user = get_user_from_jwt(request)
    return render(request, "web/home.html", {"user": user})


def login_page(request):
    """Login page - handles both GET and POST"""
    # Check if user is already authenticated via JWT
    user = get_user_from_jwt(request)
    if user:
        next_url = request.GET.get("next", "/dashboard/")
        return redirect(next_url)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Don't use Django session login - let the frontend handle JWT
                # The frontend will call the API to get JWT tokens
                messages.info(
                    request, "Please use the login form below to authenticate."
                )
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, "web/login.html")


def register_page(request):
    """Registration page"""
    return render(request, "web/register.html")


def dashboard(request):
    """User dashboard"""
    user = get_user_from_jwt(request)
    if not user:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    # Set the user in the request context for template rendering
    request.user = user
    return render(request, "web/dashboard.html", {"user": user})


def book_management(request):
    """Book management page"""
    user = get_user_from_jwt(request)
    if not user:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    request.user = user
    return render(request, "web/book_management.html", {"user": user})


def favorites(request):
    """User favorites page"""
    user = get_user_from_jwt(request)
    if not user:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    request.user = user
    return render(request, "web/favorites.html", {"user": user})


def logout_view(request):
    """Logout view"""
    # Clear Django session if it exists
    logout(request)

    # Create response and clear JWT cookies
    response = redirect("web:home")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response


# API proxy views (optional - for handling CORS or additional logic)
@csrf_exempt
def api_proxy(request, endpoint):
    """
    Optional API proxy view for handling requests that need server-side processing
    This can be used if you need to handle CORS or add additional server-side logic
    """
    # This is just a placeholder - you might not need this
    # since your frontend will call APIs directly
    return JsonResponse({"message": "API proxy endpoint"})
