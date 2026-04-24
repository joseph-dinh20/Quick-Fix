# messaging/utils.py
from .models import Conversation

def get_or_create_conversation(user_a, user_b):
    if user_a.id > user_b.id:
        user_a, user_b = user_b, user_a

    conversation, _ = Conversation.objects.get_or_create(
        user1=user_a,
        user2=user_b
    )
    return conversation