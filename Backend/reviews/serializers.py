from rest_framework import serializers

from accounts.models import Profile, ServiceProvider
from jobs.models import Job
from .models import Review, ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["id", "image"]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source="reviewer.user.username", read_only=True)
    reviewer_profile_name = serializers.CharField(source="reviewer.name", read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    service_provider_id = serializers.IntegerField(write_only=True)
    job_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "reviewer_name",
            "reviewer_profile_name",
            "service_provider",
            "service_provider_id",
            "job",
            "job_id",
            "rating",
            "comment",
            "created_at",
            "images",
        ]
        read_only_fields = ["reviewer", "service_provider", "job", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]

        # 🔥 If updating, skip provider/job validation
        if self.instance:
            return attrs

        user = request.user

        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        try:
            reviewer_profile = user.profile
        except Profile.DoesNotExist:
            raise serializers.ValidationError("No profile found for this user.")

        if reviewer_profile.role != Profile.USER:
            raise serializers.ValidationError("Only customers can leave reviews.")

        service_provider_id = attrs.get("service_provider_id")
        job_id = attrs.get("job_id")

        try:
            service_provider = ServiceProvider.objects.select_related("profile").get(id=service_provider_id)
        except ServiceProvider.DoesNotExist:
            raise serializers.ValidationError({"service_provider_id": "Service provider not found."})

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise serializers.ValidationError({"job_id": "Job not found."})

        if job.customer != reviewer_profile:
            raise serializers.ValidationError("You can only review providers for your own jobs.")

        if job.is_open:
            raise serializers.ValidationError("You can only review a completed or closed job.")

        if Review.objects.filter(reviewer=reviewer_profile, job=job).exists():
            raise serializers.ValidationError("You have already reviewed this job.")

        attrs["reviewer"] = reviewer_profile
        attrs["service_provider"] = service_provider
        attrs["job"] = job

        return attrs

    def create(self, validated_data):
        validated_data.pop("service_provider_id", None)
        validated_data.pop("job_id", None)
        return Review.objects.create(**validated_data)