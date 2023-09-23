from rest_framework import serializers

from chat_backend.tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    current = serializers.IntegerField()

    class Meta:
        model = Ticket
        fields = ["name", "current", "max", "next"]


class HintSerializer(serializers.Serializer):
    query = serializers.CharField()


class HintResponseSerializer(serializers.Serializer):
    score = serializers.FloatField()
    answer = serializers.CharField()
