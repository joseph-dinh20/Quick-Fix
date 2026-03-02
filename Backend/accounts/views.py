from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from django.middleware.csrf import get_token

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(["POST"])
def signup(request):

    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=email).exists():
        return Response({"error": "User exists"}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )

    profile = Profile.objects.get(user=user)
    profile.name = name
    profile.save()

    return Response({"message": "User created"})

User = get_user_model()
@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=user.username, password=password)
    if not user:
        return Response({"error": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    dj_login(request, user)

    return Response(
        {"message": "logged in", "user": {"id": user.id, "username": user.username, "email": user.email}},
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def logout(request):
    dj_logout(request)
    return Response({"message": "logged out"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def csrf(request):
    return Response({"csrfToken": get_token(request)})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return Response({"id": u.id, "username": u.username, "email": u.email})