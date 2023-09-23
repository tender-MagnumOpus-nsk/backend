from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework_proxy.views import ProxyView

from chat_backend.tickets.api.serializers import (
    TicketSerializer,
    HintSerializer,
    HintResponseSerializer,
)
from chat_backend.tickets.services import get_ticket_data


class RetrieveTicketSerializer(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = get_ticket_data(self.kwargs["uuid"])
        return Response(data)


app_name = "api"


class HitProxyView(generics.GenericAPIView, ProxyView):
    permission_classes = []
    source = "hint"
    http_method_names = ["post"]

    @extend_schema(
        request=HintSerializer(), responses={200: HintResponseSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
