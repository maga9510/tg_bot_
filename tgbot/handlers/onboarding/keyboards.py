from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from tgbot.models import *
from tgbot.handlers.onboarding.static_text import inline_kb_text, inline_kb_text_l, kb_text


def logic(data, cart, lang):
    q = list(data)
    length = len(q)
    keyboard = []
    if cart == 'cart':
        if length % 2 == 0:
            for e in range(0, length, 2):
                keyboard.append([InlineKeyboardButton(text= f'❌ {q[e].add_product.name}', callback_data=f'❌ {q[e].add_product.name}')\
                    ,InlineKeyboardButton(text = f'❌ {q[e+1].add_product.name}', callback_data=f'❌ {q[e+1].add_product.name}')])
        else:
            for i in range(0, length-1, 2):
                keyboard.append([InlineKeyboardButton(text= f'❌ {q[e].add_product.name}', callback_data=f'❌ {q[e].add_product.name}')\
                    ,InlineKeyboardButton(text = f'❌ {q[e+1].add_product.name}', callback_data=f'❌ {q[e+1].add_product.name}')])
            keyboard.append([InlineKeyboardButton(text= f'❌ {q[-1].add_product.name}', callback_data=f'❌ {q[-1].add_product.name}')])
        keyboard.append([InlineKeyboardButton(text=inline_kb_text_l(lang, txt='corrected_order_text'), callback_data='order'), InlineKeyboardButton(text=inline_kb_text_l(lang, txt='clear_cart_text'), callback_data='clear')])
        return keyboard    
    else:
        if length % 2 == 0:
            for e in range(0, length, 2):
                keyboard.append(list([KeyboardButton(f'{q[e]}'),KeyboardButton(f'{q[e+1]}')]))
        else:
            for i in range(0, length-1, 2):
                keyboard.append(list([KeyboardButton(f'{q[i]}'),KeyboardButton(f'{q[i+1]}')]))
            keyboard.append([KeyboardButton(f'{q[-1]}')])
        keyboard.append([KeyboardButton(text = kb_text(lang, txt='cart_kb_text')), KeyboardButton(text = kb_text(lang ,txt='back_kb_text'))])
        return keyboard


def start_kb(lang):
    keyboard = [[KeyboardButton(kb_text(lang ,txt='menu_kb_text'))], \
        [KeyboardButton(kb_text(lang ,txt='cart_kb_text')), KeyboardButton(kb_text(lang ,txt='orders_kb_text'))], \
            [KeyboardButton(kb_text(lang ,txt='settings_kb_text')),KeyboardButton(kb_text(lang ,txt='about_kb_text'))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def menu_kb(locations, lang):
    if locations == False:
        keyboard = [[KeyboardButton(kb_text(lang ,txt='loc_kb_text'), request_location=True)],[KeyboardButton(kb_text(lang ,txt='cart_kb_text')), KeyboardButton(kb_text(lang ,txt='back_kb_text'))]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        return reply_markup
    else:
        keyboard = [[KeyboardButton(kb_text(lang, txt='yes_kb_text'))], [KeyboardButton(kb_text(lang, txt='change_loc_kb_text'))],\
            [KeyboardButton(kb_text(lang ,txt='cart_kb_text')),KeyboardButton(kb_text(lang ,txt='back_kb_text'))]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        return reply_markup


def category_kb(lang):
    reply_markup = ReplyKeyboardMarkup(logic(data=Menu.objects.all(), cart='', lang=lang), resize_keyboard=True)
    return reply_markup


def product_kb(data, lang):
    reply_markup = ReplyKeyboardMarkup(logic(data=data, cart='', lang=lang), resize_keyboard=True)
    return reply_markup


def cart_kb(data, lang):
    reply_markup = InlineKeyboardMarkup(logic(data=data, cart='cart', lang=lang))
    return reply_markup


def back_kb(lang):
    keyboard = [[KeyboardButton(kb_text(lang ,txt='back_kb_text'))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def product_inline_kb(num, lang):
    keyboard = [[
    InlineKeyboardButton('➖', callback_data='-'),
    InlineKeyboardButton(f'{num}', callback_data='num'),
    InlineKeyboardButton('➕', callback_data='+')],[InlineKeyboardButton(inline_kb_text_l(lang, txt='add_to_cart_text'), callback_data='add_to_cart')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

    

def phone_number_kb(lang):
    keyboard = [[KeyboardButton(kb_text(lang, txt='phone_kb_text'), request_contact=True)], [KeyboardButton(kb_text(lang ,txt='back_kb_text'))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def change_phone_num_kb(lang):
    keyboard = [[KeyboardButton(kb_text(lang, txt='proceed'))], [KeyboardButton(kb_text(lang, txt='change_number_text'))], [KeyboardButton(kb_text(lang ,txt='back_kb_text'))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def payment_kb(lang):
    keyboard = [[KeyboardButton(kb_text(lang, txt='cash_kb_text')), KeyboardButton(kb_text(lang, txt='terminal_kb_text'))], \
        [KeyboardButton(kb_text(lang ,txt='back_kb_text'))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    return reply_markup


def chek_out_kb(lang):
    keyboard = [[InlineKeyboardButton(text = inline_kb_text_l(lang, txt='yes_i_kb_text'), callback_data='yes'), InlineKeyboardButton(inline_kb_text_l(lang, txt='no_i_kb_text'), callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def admin_state_kb(data):
    if data.states == "pending":
        keyboard = [[InlineKeyboardButton(text=inline_kb_text(txt='confirm_i_kb_text'), callback_data='ok')],[InlineKeyboardButton(text=inline_kb_text(txt='cancel_order_i_kb'), callback_data='close')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup
    elif data.states == "preparing":
        keyboard = [[InlineKeyboardButton(text=inline_kb_text(txt='deliver_i_kb_text'), callback_data='deliver')],[InlineKeyboardButton(text=inline_kb_text(txt='cancel_order_i_kb'), callback_data='close')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup
    elif data.states == "delivering":
        keyboard = [[InlineKeyboardButton(text=inline_kb_text(txt='confirmed_i_kb_text'), callback_data='apcet')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup


def lang_kb():
    keboard = [[InlineKeyboardButton(text=inline_kb_text(txt='uz_i_kb_text'), callback_data='uz'), InlineKeyboardButton(text=inline_kb_text(txt='ru_i_kb_text'), callback_data='ru')]]
    reply_markup = InlineKeyboardMarkup(keboard)
    return reply_markup




