from django.apps import AppConfig


class TgbotConfig(AppConfig):
    name = 'tgbot'
    
    def ready(self):
        from tgbot import dispatcher
        dispatcher.ready()
