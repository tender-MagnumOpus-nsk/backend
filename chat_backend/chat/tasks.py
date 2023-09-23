from random import randint

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings

from chat_backend.chat.const import terms
from chat_backend.chat.models import Message, MessageFile
from pdf_highlighter import process_file

ML_HOST = settings.ML_HOST


questions = {}


@shared_task
def send_message(id: str, question: str):
    if question in questions and questions[question]:
        res_data = questions[question]
    else:
        res_q = requests.post(ML_HOST + "/question", json={"query": question})
        if res_q.status_code == 200:
            data = res_q.json()
            res_data = []
            names = []
            for i, answer in enumerate(data):
                try:
                    if answer["title"] not in names:
                        names.append(answer["title"])
                        if "type" in answer and answer["type"] == "file":
                            if q := MessageFile.objects.filter(
                                question_num=answer["num"],
                                name__icontains=answer["title"].split(".")[-1],
                            ):
                                q = q.first()
                                answer["file"] = q.file.url
                                if answer["highlights"]:
                                    rand = randint(1, 10000000)
                                    p_path = (
                                        q.file.path.replace(".pdf", "-" + str(rand))
                                        + ".pdf"
                                    )
                                    f = True
                                    for h in answer["highlights"]:
                                        if f:
                                            process_file(
                                                input_file=q.file.path,
                                                output_file=p_path,
                                                search_str=h,
                                            )
                                            f = False
                                        else:
                                            process_file(
                                                input_file=p_path,
                                                output_file=p_path,
                                                search_str=h,
                                            )

                                    answer["file"] = q.file.url.replace(
                                        q.file.url.split("/")[-1], p_path.split("/")[-1]
                                    )
                                res = ""
                                if answer["highlights"]:
                                    for h in answer["highlights"]:
                                        if h.lower() in terms:
                                            res += terms[h.lower()] + "\n"

                                answer["file_text"] = res if res else q.text
                                res_data.append(answer)
                        else:
                            res_data.append(answer)
                except (KeyError, ValueError, MessageFile.DoesNotExist) as e:
                    print(e)
            questions[question] = res_data
        else:
            raise ValueError(res_q.status_code)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"messages_{id}", {"type": "message", "data": {"data": res_data[:5]}}
    )

    Message.objects.create(session_id=id, data=question)
    Message.objects.create(session_id=id, data=res_data, reply=True)
    return
