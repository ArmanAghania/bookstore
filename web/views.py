from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse


def home(request):
    """Home page with book listing"""
    return render(request, "web/home.html")


def login_page(request):
    """Login page - handles both GET and POST"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "/dashboard/")
                return redirect(next_url)
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
    return render(request, "web/dashboard.html")


def book_management(request):
    """Book management page"""
    return render(request, "web/book_management.html")


def favorites(request):
    """User favorites page"""
    return render(request, "web/favorites.html")


def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect("home")


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
