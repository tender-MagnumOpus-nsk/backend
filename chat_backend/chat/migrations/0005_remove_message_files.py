# Generated by Django 4.2.5 on 2023-09-23 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0004_messagefile_message_files"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="files",
        ),
    ]
