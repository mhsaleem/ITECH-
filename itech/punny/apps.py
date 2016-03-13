from django.apps import AppConfig
from watson import search as watson


class PunnyAppConfig(AppConfig):
    name = "punny"

    def ready(self):
        pun = self.get_model("Pun")
        watson.register(pun, fields=("text", "owner", "tags__text"))
