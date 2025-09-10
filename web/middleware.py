"""
Custom middleware for JWT authentication in web views
"""

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users using JWT tokens stored in localStorage
    for web views that require authentication.
    """

    def process_request(self, request):
        # Skip API endpoints - they handle their own JWT authentication
        if request.path.startswith("/api/"):
            return None

        # Skip login and register pages to avoid redirect loops
        if request.path in ["/login/", "/register/", "/"]:
            return None

        # Check if the view requires authentication
        # This is a simple check - you might want to make this more sophisticated
        protected_paths = ["/dashboard/", "/books/", "/favorites/"]

        if not any(request.path.startswith(path) for path in protected_paths):
            return None

        # Try to get JWT token from localStorage via cookie
        # The frontend should set this cookie when storing the token
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            # No token found, redirect to login
            login_url = f"{reverse('web:login')}?next={request.path}"
            return HttpResponseRedirect(login_url)

        try:
            # Validate the token
            token = AccessToken(access_token)
            user_id = token.payload.get("user_id")

            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    request.user = user
                    request._dont_enforce_csrf_checks = True  # Skip CSRF for JWT auth
                    return None  # Authentication successful, continue
                except User.DoesNotExist:
                    # User doesn't exist, redirect to login
                    login_url = f"{reverse('web:login')}?next={request.path}"
                    return HttpResponseRedirect(login_url)

        except (InvalidToken, TokenError, jwt.ExpiredSignatureError):
            # Token is invalid or expired, redirect to login
            login_url = f"{reverse('web:login')}?next={request.path}"
            return HttpResponseRedirect(login_url)

        return None
