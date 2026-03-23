from rest_framework import serializers
from .models import Report


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "reported_profile",
            "reason",
            "details",
        ]