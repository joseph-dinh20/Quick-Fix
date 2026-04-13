from rest_framework import serializers
from .models import Job, JobImage, JobApplication
from services.models import Service
from services.serializers import ServiceSerializer
from accounts.models import ServiceProvider, Profile, Language
from .utils import geolocator

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "name", "avatar"] 


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

    city = serializers.CharField(write_only=True, required=False)
    zip = serializers.CharField(write_only=True, required=False)

    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        required=False,  # optional field
        allow_null=True
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
            "latitude",
            "longitude",
            "images",
            "urgency",
            "city",
            "zip",
            "language"
        ]

    def create(self, validated_data):
        city = validated_data.pop("city", None)
        zip_code = validated_data.pop("zip", None)

        # convert city/zip to coordinates
        if city or zip_code:
            query = f"{city or ''} {zip_code or ''}".strip()
            location = geolocator.geocode(query)
            if location:
                validated_data["latitude"] = location.latitude
                validated_data["longitude"] = location.longitude
            print(validated_data["latitude"])
            print(validated_data["longitude"])

        images = validated_data.pop("images", [])
        services = validated_data.pop("services", [])

        profile = self.context["request"].user.profile

        language = validated_data.pop("language", None)
        if language is None:
            language = Language.objects.filter(name__iexact="English").first()
        

        job = Job.objects.create(customer=profile, language=language, **validated_data)
        job.services.set(services)

        for img in images:
            JobImage.objects.create(job=job, image=img)

        return job


class JobSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    services = ServiceSerializer(many=True)
    images = JobImageSerializer(many=True)
    customer = ProfileSerializer(read_only=True)
    languages = serializers.StringRelatedField()

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
            "is_favorited",
            "customer",
            "languages",
            "urgency",
            "status",
            'city',
            'state',
            'zip_code',
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
            "urgency",
            "status"
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    job_id = serializers.IntegerField(source="job.id", read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job_id",
            "job_title",
            "status",
            "created_at",
        ]