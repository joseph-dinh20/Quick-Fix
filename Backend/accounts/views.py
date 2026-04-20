from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile, ServiceProvider, WorkImage, Language
from django.middleware.csrf import get_token

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import re

from services.models import Service
from .serializers import ServiceProviderSerializer, ProfileUpdateSerializer, ServiceProviderUpdateSerializer, MeSerializer, FavoriteProviderSerializer, ProviderApplicationSerializer
from jobs.models import Job
from reviews.models import Review
from django.db.models import Prefetch


from haversine import haversine, Unit

from django.db.models import Q
from .services import approve_application
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ProviderApplication
from services.models import Service

User = get_user_model()


def validate_password_strength(password):
    """
    Validate password meets security standards:
    - Minimum length of 8
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        errors.append("Password must contain at least one special character")
    
    return errors


@api_view(["POST"])
def signup(request):

    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=email).exists():
        return Response({"error": "User exists"}, status=400)

    # Validate password strength
    password_errors = validate_password_strength(password)
    if password_errors:
        return Response({"errors": password_errors}, status=400)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )

    profile = Profile.objects.get(user=user)
    profile.name = name
    profile.save()

    return Response({"message": "User created"})


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
    return Response(MeSerializer(request.user).data)


@api_view(["GET"])
def get_providers(request):
    providers = ServiceProvider.objects.all()
    serializer = ServiceProviderSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_provider(request, provider_id):
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
    except ServiceProvider.DoesNotExist:
        return Response({"error": "Provider not found"}, status=404)

    serializer = ServiceProviderSerializer(provider)
    return Response(serializer.data)


# @api_view(["GET"])
# def providers_by_service(request, service_id):
#     providers = ServiceProvider.objects.filter(services__id=service_id)
#     serializer = ServiceProviderSerializer(providers, many=True)
#     return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    print(request.data)
    profile = Profile.objects.get(user=request.user)

    serializer = ProfileUpdateSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_service_provider(request):
    print(request.data)

    provider = ServiceProvider.objects.get(profile__user=request.user)

    serializer = ServiceProviderUpdateSerializer(
        provider,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

        images = request.FILES.getlist("work_images")

        for img in images:
            WorkImage.objects.create(
                provider=provider,
                image=img
            )

        return Response(serializer.data)


    print(serializer.errors)   # add this
    return Response(serializer.errors, status=400)



@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_work_image(request, image_id):

    try:
        image = WorkImage.objects.get(id=image_id)

        # ensure the image belongs to the logged-in provider
        if image.provider.profile.user != request.user:
            return Response({"error": "Not authorized"}, status=403)

        image.delete()

        return Response({"message": "Image deleted"}, status=200)

    except WorkImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def provider_me(request):
    try:
        provider = ServiceProvider.objects.get(profile__user=request.user)
    except ServiceProvider.DoesNotExist:
        return Response({"error": "Service provider not found"}, status=404)

    serializer = ServiceProviderSerializer(provider)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_services(request):
    services = Service.objects.all().values("id", "name")
    return Response(list(services), status=status.HTTP_200_OK)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_provider_services(request):
    try:
        provider = ServiceProvider.objects.get(profile__user=request.user)
    except ServiceProvider.DoesNotExist:
        return Response(
            {
                "error": "Service provider not found",
                "user_id": request.user.id,
                "email": request.user.email,
            },
            status=status.HTTP_404_NOT_FOUND
        )

    service_ids = request.data.get("services", [])

    if not isinstance(service_ids, list):
        return Response(
            {"error": "services must be a list of service ids"},
            status=status.HTTP_400_BAD_REQUEST
        )

    valid_services = Service.objects.filter(id__in=service_ids)
    provider.services.set(valid_services)

    return Response(
        {
            "message": "Provider services updated successfully",
            "services": list(valid_services.values("id", "name"))
        },
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite_provider(request, provider_id):
    profile = request.user.profile
    service_provider = ServiceProvider.objects.get(id=provider_id)

    if profile.favorites.filter(id=provider_id).exists():

        profile.favorites.remove(service_provider)

        return Response({
            "message": "Provider unfavorited",
            },
            status=status.HTTP_200_OK
            )
    
    
    profile.favorites.add(service_provider)

    return Response({
        "message": "Provider favorited",
        },
        status=status.HTTP_200_OK
        )



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    profile = request.user.profile

    providers = profile.favorites.prefetch_related(
        Prefetch(
            "reviews",
            queryset=Review.objects.filter(reviewer=profile),
            to_attr="user_reviews"
        ),
        "services"
    )

    serializer = FavoriteProviderSerializer(
        providers,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def is_favorite_provider(request, provider_id):

    profile = request.user.profile

    is_favorite = profile.favorites.filter(id=provider_id).exists()

    return Response({
        "provider_id": provider_id,
        "is_favorite": is_favorite
    },
    status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_nearby_providers(request):

    lat = float(request.GET.get("lat"))
    lng = float(request.GET.get("lng"))
    max_distance = float(request.GET.get("max_distance", 25))  # default 25 miles

    user_coord = (lat, lng)
    nearby_providers = []
    providers = ServiceProvider.objects.select_related("profile").all()

    for provider in providers:

        profile = provider.profile

        if profile.latitude is None or profile.longitude is None:
            continue

        provider_coord = (profile.latitude, profile.longitude)
        distance = haversine(user_coord, provider_coord, unit=Unit.MILES)

        if distance <= max_distance:
            nearby_providers.append(provider)

    serializer = ServiceProviderSerializer(nearby_providers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_providers(request):
    providers = ServiceProvider.objects.all()

    query = request.GET.get("q")
    if query:
        providers = providers.filter(
            Q(profile__name__icontains=query) |
            Q(about_me__icontains=query) |
            Q(services__name__icontains=query) |
            Q(profile__city__icontains=query) |
            Q(profile__state__icontains=query)
        ).distinct()

    # Filter by Rating
    min_rating = request.GET.get("rating")
    if min_rating:
        try:
            providers = providers.filter(average_rating__gte=float(min_rating))
        except ValueError:
            return Response({"error": "Invalid rating"}, status=400)
    

    # Filter by services
    services = request.GET.get("services")
    if services:
        service_ids = [int(s) for s in services.split(",") if s.isdigit()]
        providers = providers.filter(services__id__in=service_id).distinct()

    # Filter by Budget
    max_budget = request.GET.get("budget")
    if max_budget:
        try:
            providers = providers.filter(price_per_hour__lte=float(max_budget))
        except ValueError:
            return Response({"error": "Invalid budget"}, status=400)

    # Filter location
    max_distance = request.GET.get("max_distance")
    if max_distance:
        try:
            max_distance = float(max_distance)
        except ValueError:
            return Response({"error": "Invalid distance"}, status=400)
        
        if request.user.is_authenticated:
            profile = getattr(request.user, "profile", None)
            if not profile:
                return Response({"error": "Profile not found"}, status=404)

            if profile.latitude is not None and profile.longitude is not None:
                user_coord = (profile.latitude, profile.longitude)

                filtered = []
                for provider in providers:
                    p = provider.profile

                    if p.latitude is None or p.longitude is None:
                        continue

                    distance = haversine(
                        user_coord,
                        (p.latitude, p.longitude),
                        unit=Unit.MILES
                    )

                    if distance <= max_distance:
                        filtered.append(provider)

                providers = filtered


    serializer = ServiceProviderSerializer(providers, many=True, context={"request":request})
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_provider_status(request, user_id):
    if not request.user.is_staff:
        return Response({"error": "Unauthorized"}, status=403)

    profile = Profile.objects.get(user_id=user_id)
    status_value = request.data.get("status")

    if status_value not in ["approved", "rejected"]:
        return Response({"error": "Invalid status"}, status=400)

    if status_value == "approved":
        application = profile.providerapplication  # adjust to your relation name
        approve_application(application)

    return Response({"message": "Updated", "status": status_value})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_provider(request):
    profile = request.user.profile

    experience = request.POST.get("experience", "")
    document = request.FILES.get("document")

    # 2. parse services
    skills = request.data.get("skills", "[]")

    if isinstance(skills, str):
        skills = json.loads(skills)

    if not isinstance(skills, list):
        skills = []

    # 3. create application
    application = ProviderApplication.objects.create(
        profile=profile,
        experience=experience,
        document=document,
        skills=skills  # (temporary fix OR replace with M2M later)
    )

    return Response({"message": "Application submitted"})


@api_view(["GET"])
def get_languages(request):
    languages = Language.objects.all()
    data = [{"id": l.id, "name": l.name} for l in languages]
    return Response(data)