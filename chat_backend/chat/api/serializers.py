from rest_framework import serializers

from chat_backend.chat.models import Message, Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["id", "created"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created": {"read_only": True},
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["data", "created", "reply"]
        extra_kwargs = {
            "created": {"read_only": True},
        }


class DialogSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ["id", "messages", "created"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created": {"read_only": True},
        }
