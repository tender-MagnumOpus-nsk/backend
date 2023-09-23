from rest_framework import generics
from rest_framework.permissions import AllowAny

from chat_backend.chat.api.serializers import SessionSerializer, DialogSerializer
from chat_backend.chat.models import Session


class CreateSessionAPIView(generics.CreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]


class RetrieveDialogAPIView(generics.RetrieveAPIView):
    lookup_url_kwarg = "uuid"
    lookup_field = "id"
    queryset = Session.objects.all()
    permission_classes = [AllowAny]
    serializer_class = DialogSerializer
