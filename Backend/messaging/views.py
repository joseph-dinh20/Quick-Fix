# messaging/views.py
from rest_framework import generics, permissions
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).order_by("-created_at")
    

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        conversation_id = self.kwargs["conversation_id"]

        conversation = Conversation.objects.get(id=conversation_id)

        # user is part of conversation
        if user not in [conversation.user1, conversation.user2]:
            return Message.objects.none()

        return conversation.messages.all()
    

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_id = request.data.get("receiver_id")
        content = request.data.get("content")

        if not receiver_id or not content:
            return Response({"error": "receiver_id and content required"}, status=400)

        receiver = User.objects.get(id=receiver_id)

        # normalize order
        user1, user2 = (sender, receiver) if sender.id < receiver.id else (receiver, sender)

        conversation, _ = Conversation.objects.get_or_create(
            user1=user1,
            user2=user2
        )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content
        )

        return Response(MessageSerializer(message).data, status=201)