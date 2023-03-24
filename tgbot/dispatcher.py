from telegram import Bot
from tgbot.models import *
from dtb.settings import TELEGRAM_TOKEN, HOST
from tgbot.handlers.onboarding import handlers as onboarding_handler
from telegram.ext import (Dispatcher, Filters, CommandHandler, MessageHandler, CallbackQueryHandler)


def ready():
    """ Run bot in webhook mode """
    host_name = f"{HOST}/api/v1/" 
    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]
    print(f"Pooling of '{bot_link}' started\n")
    print(f"setting MASTER webhook at {host_name}")
    bot.set_webhook(host_name)  


bot: Bot = Bot(TELEGRAM_TOKEN)
dispatcher : Dispatcher = Dispatcher(bot, update_queue=None)
dispatcher.add_handler(CommandHandler("start", onboarding_handler.start ))
dispatcher.add_handler(MessageHandler(Filters.text, onboarding_handler.menu_all))
dispatcher.add_handler(CallbackQueryHandler(onboarding_handler.query_callback))
dispatcher.add_handler(MessageHandler(Filters.location, onboarding_handler.location_handler))
dispatcher.add_handler(MessageHandler(Filters.contact, onboarding_handler.contact)) 