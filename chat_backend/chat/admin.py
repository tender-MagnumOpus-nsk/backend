from django.contrib import admin

from chat_backend.chat.models import MessageFile


@admin.register(MessageFile)
class MessageFileAdmin(admin.ModelAdmin):
    ...
