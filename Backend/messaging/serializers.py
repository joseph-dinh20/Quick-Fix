# messaging/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MessageSerializer(serializers.ModelSerializer):
    sender = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "other_user", "last_message", "created_at"]

    def get_other_user(self, obj):
        user = self.context["request"].user
        other = obj.user2 if obj.user1 == user else obj.user1
        return SimpleUserSerializer(other).data

    def get_last_message(self, obj):
        last = obj.messages.order_by("-created_at").first()
        return MessageSerializer(last).data if last else None