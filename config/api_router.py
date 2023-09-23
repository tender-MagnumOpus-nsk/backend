from django.urls import include, path

from chat_backend.tickets.api.views import HitProxyView

app_name = "api"


urlpatterns = [
    path("ticket/", include("chat_backend.tickets.api.urls")),
    path("chat/", include("chat_backend.chat.api.urls")),
    path("hint/", HitProxyView.as_view()),
]
