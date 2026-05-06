# messaging/urls.py
from django.urls import path
from .views import ConversationListView, MessageListView, SendMessageView

urlpatterns = [
    path("", ConversationListView.as_view()),
    path("<int:conversation_id>/messages/", MessageListView.as_view()),
    path("send/", SendMessageView.as_view()),
]