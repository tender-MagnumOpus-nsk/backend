from django.urls import path

from chat_backend.chat.consumers import MessageConsumer

websocket_urlpatterns = [
    path("ws/messages/<str:id>", MessageConsumer.as_asgi()),
]
