from rest_framework import serializers
from .models import Job


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