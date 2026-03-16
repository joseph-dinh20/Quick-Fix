from rest_framework import serializers
from .models import Profile, ServiceProvider, WorkImage
from services.models import Service


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
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "avatar"]


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