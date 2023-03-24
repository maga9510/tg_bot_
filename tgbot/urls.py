from django.urls import path
from tgbot.views import *

urlpatterns = [
    path("", Contact_bot.as_view())
]