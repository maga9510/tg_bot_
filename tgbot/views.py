import json
from telegram import Update
from django.views import View
from django.http import HttpResponse
from dtb.settings import TELEGRAM_TOKEN
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from tgbot.dispatcher import bot as contact_bot, dispatcher as master_dispatcher


@method_decorator(csrf_exempt, 'dispatch')
class Contact_bot(View):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body)
            update: Update = Update.de_json(data, contact_bot)
            master_dispatcher.process_update(update)
        except Exception as e:
            print("\n\n Exception: \n")
            print(e)

        return HttpResponse("200", status=200)