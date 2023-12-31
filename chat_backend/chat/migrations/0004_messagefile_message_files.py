# Generated by Django 4.2.5 on 2023-09-23 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_alter_message_options_message_reply"),
    ]

    operations = [
        migrations.CreateModel(
            name="MessageFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_num", models.IntegerField()),
                ("name", models.CharField(db_index=True, max_length=500)),
                ("file", models.FileField(upload_to="files/")),
            ],
        ),
        migrations.AddField(
            model_name="message",
            name="files",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="chat.messagefile",
            ),
        ),
    ]
