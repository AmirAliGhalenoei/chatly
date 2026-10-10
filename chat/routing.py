from django.urls import path
from . import consumers

ws_urlpatterns = [
    path("ws/group/<uuid:room_id>/", consumers.GroupChatConsumer.as_asgi()),
    path("ws/privat/<uuid:conversation_id>/", consumers.PrivatChatConsumer.as_asgi()),
]