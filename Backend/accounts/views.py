from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile


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