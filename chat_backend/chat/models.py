import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Session(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"session: {self.id}"


class Message(models.Model):
    session = models.ForeignKey(
        "Session", related_name="messages", on_delete=models.CASCADE
    )
    data = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)

    class Meta:
        ordering = ["created"]


class MessageFile(models.Model):
    question_num = models.IntegerField()
    name = models.CharField(max_length=500, db_index=True)
    file = models.FileField(upload_to="files/")
    text = models.TextField(max_length=6000)

    def __str__(self):
        return self.name
