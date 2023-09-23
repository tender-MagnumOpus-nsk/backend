import requests
from asgiref.sync import async_to_sync

from celery import shared_task
from channels.layers import get_channel_layer

from chat_backend.chat.models import Message, MessageFile

ML_HOST = "http://192.168.2.231:8000/"


@shared_task
def send_message(id: str, question: str):
    res = requests.post(ML_HOST + "question", json={"query": question})
    if res.status_code == 200:
        channel_layer = get_channel_layer()
        data = res.json()
        for answer in data:
            if "type" in answer and answer["type"] == "file":
                try:
                    answer["file"] = MessageFile.objects.get(
                        question_num=answer["num"], name__iexact=answer["title"]
                    ).file.url
                except (KeyError, ValueError, MessageFile.DoesNotExist) as e:
                    print(e)
        async_to_sync(channel_layer.group_send)(
            f"messages_{id}", {"type": "message", "data": {"data": data}}
        )

        Message.objects.create(session_id=id, data=question)
        Message.objects.create(session_id=id, data=data, reply=True)
        return
    raise ValueError(res.status_code)
