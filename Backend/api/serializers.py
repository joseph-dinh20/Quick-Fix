from rest_framework import serializers
from accounts.models import ProviderApplication


class ProviderApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderApplication
        fields = [
            "id",
            "full_name", "phone", "location", "bio",
            "credential_file",
            "status", "review_notes",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status", "review_notes", "created_at", "updated_at"
        ]

    def validate_phone(self, value):
        # value is a string here (not a dict)
        v = (value or "").strip()
        if len(v) < 7:
            raise serializers.ValidationError("Phone number looks too short.")
        return v