from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat_backend.tickets"

    def ready(self):
        try:
            import chat_backend.tickets.signals  # noqa F401
        except ImportError:
            pass
