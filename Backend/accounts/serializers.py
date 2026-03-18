from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ServiceProvider, WorkImage
from services.models import Service
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from .utils import geolocator



class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = ["id", "image"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


class ServiceProviderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="profile.name")
    avatar = serializers.ImageField(source="profile.avatar")

    services = ServiceSerializer(many=True)
    work_images = WorkImageSerializer(many=True)
    
    city = serializers.CharField(source="profile.city")
    state = serializers.CharField(source="profile.state")

    latitude = serializers.FloatField(source="profile.latitude")
    longitude = serializers.FloatField(source="profile.longitude")

    class Meta:
        model = ServiceProvider
        fields = [
            "id",
            "name",
            "avatar",
            "price_per_hour",
            "about_me",
            "average_rating",
            "total_rating",
            "services",
            "work_images",
            "city",
            "state",
            "latitude",
            "longitude"
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "avatar", "city", "state"]

    def validate(self, attrs):
        city = attrs.get("city")
        state = attrs.get("state")

        try:
            # allow empty
            if not city and not state:
                return attrs

            if city:
                attrs["city"] = " ".join(word.capitalize() for word in city.split())
                if not geolocator.geocode(city, timeout=3):
                    raise serializers.ValidationError({"city": "Invalid city"})
                

            if state:
                attrs["state"] = " ".join(word.capitalize() for word in state.split())
                if not geolocator.geocode(state, timeout=3):
                    raise serializers.ValidationError({"state": "Invalid state"})

            if city and state:
                if not geolocator.geocode(f"{city}, {state}", timeout=3):
                    raise serializers.ValidationError({
                        "city": "City and state do not match"
                    })

        except (GeocoderTimedOut, GeocoderServiceError):
            raise serializers.ValidationError({
                "location": "Location service unavailable. Try again."
            })

        return attrs
    

    def update(self, instance, validated_data):
        city = validated_data.get("city")
        state = validated_data.get("state")

        try:
            query = f"{city}, {state}" if city and state else city or state
            location = geolocator.geocode(query, timeout=3)

            if location:
                instance.latitude = location.latitude
                instance.longitude = location.longitude

        except (GeocoderTimedOut, GeocoderServiceError):
            pass  # don't crash request

        return super().update(instance, validated_data)


class ServiceProviderUpdateSerializer(serializers.ModelSerializer):

    work_images = WorkImageSerializer(many=True, read_only=True)

    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True
    )

    class Meta:
        model = ServiceProvider
        fields = [
            "services",
            "about_me",
            "price_per_hour",
            "work_images"
        ]


class MeSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source="profile.avatar")
    city = serializers.CharField(source="profile.city")
    state = serializers.CharField(source="profile.state")

    latitude = serializers.FloatField(source="profile.latitude")
    longitude = serializers.FloatField(source="profile.longitude")

    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar", "city", "state", "latitude", "longitude"]