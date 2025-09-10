from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer, RegisterSerializer, UserUpdateSerializer


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view that returns JWT tokens with user info"""

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(generics.GenericAPIView):
    """
    Logout view to blacklist the refresh token
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        elif self.action in ["update", "partial_update"]:
            return UserSerializer
        elif self.action == "retrieve":
            return UserSerializer
        return UserSerializer

    @action(detail=False, methods=["get", "post", "put", "patch"])
    def me(self, request):
        """Custom action to get/update current user without requiring pk"""
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == "POST":
            # Handle user creation (registration)
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    UserSerializer(user).data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method in ["PUT", "PATCH"]:
            # Handle user update
            serializer = UserSerializer(
                request.user, data=request.data, partial=request.method == "PATCH"
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
