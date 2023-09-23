from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("ticket/", include("chat_backend.tickets.api.urls")),
    path("chat/", include("chat_backend.chat.api.urls")),
]
