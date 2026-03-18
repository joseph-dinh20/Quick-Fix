from rest_framework import serializers
from .models import Job, JobImage
from services.models import Service
from services.serializers import ServiceSerializer


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

        # set M2M
        job.services.set(services)

        # create images
        for img in images:
            JobImage.objects.create(job=job, image=img)

        return job


class JobSerializer(serializers.ModelSerializer):
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
        ]