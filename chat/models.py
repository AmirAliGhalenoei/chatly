from django.db import models
from django.conf import settings
import uuid
# Create your models here.


class Conversation(models.Model):
    CONVERSATION_TYPE = [
        ("privat","Privat"),
        ("group","Group"),
    ]
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=CONVERSATION_TYPE)
    group_name = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.type}"

class ConversationMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="members")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="conversations")
    joined_date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)


    