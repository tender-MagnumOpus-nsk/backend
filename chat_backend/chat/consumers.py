import json

from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError

from chat_backend.chat.models import Session
from chat_backend.chat.tasks import send_message
from chat_backend.common.channels import BaseConsumer


class MessageConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None
        self.room_group_name = None
        self.session = None

    @database_sync_to_async
    def get_session(self) -> bool:
        try:
            self.session = Session.objects.get(id=self.id)
        except (Session.DoesNotExist, ValidationError):
            return False
        return True

    async def connect(self):
        try:
            self.id = self.scope["url_route"]["kwargs"]["id"]
        except KeyError:
            return

        self.room_group_name = f"messages_{self.id}"

        await self.accept()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        session_status = await self.get_session()
        if not session_status:
            await self.send_error("Session not found")
            await self.disconnect(close_code=None)
            return

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if type(text_data) is not str:
            await self.send_error("Validation error")
        else:
            send_message.apply_async(kwargs={"id": self.id, "question": text_data})
        return text_data

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False)

    async def message(self, event):
        data = event["data"]
        await self.send_json(data)
