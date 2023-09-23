from django.urls import path

from chat_backend.chat.api.views import CreateSessionAPIView, RetrieveDialogAPIView

app_name = "chat"
urlpatterns = [
    path("", CreateSessionAPIView.as_view()),
    path("<str:uuid>", RetrieveDialogAPIView.as_view()),
]
