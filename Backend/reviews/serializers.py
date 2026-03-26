from rest_framework import serializers
from .models import Review, ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["id", "image"]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source="reviewer.user.username", read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "reviewer_name",
            "service_provider",
            "rating",
            "comment",
            "created_at",
            "images"
        ]
        read_only_fields = ["reviewer"]