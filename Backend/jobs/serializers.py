from rest_framework import serializers
from .models import Job, JobImage
from services.models import Service
from services.serializers import ServiceSerializer
from accounts.models import ServiceProvider


class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImage
        fields = ["id", "image"]


class JobCreateSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True
    )

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "budget",
            "deadline",
            "request_type",
            "services",
            "images",
        ]

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        services = validated_data.pop("services", [])

        profile = self.context["request"].user.profile

        job = Job.objects.create(
            customer=profile,
            **validated_data
        )

        # set Many to Many
        job.services.set(services)

        # create images
        for img in images:
            JobImage.objects.create(job=job, image=img)

        return job


class JobSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    services = ServiceSerializer(many=True)
    images = JobImageSerializer(many=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "budget",
            "deadline",
            "is_open",
            "request_type",
            "created_at",
            "services",
            "images",
            "is_favorited"
        ]

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False

        try:
            service_provider = ServiceProvider.objects.get(profile__user=user)
            return obj in service_provider.favorited_jobs.all()
        except ServiceProvider.DoesNotExist:
            return False

          
class JobUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "budget",
            "deadline",
            "is_open",
            "request_type",
            "services",
        ]
