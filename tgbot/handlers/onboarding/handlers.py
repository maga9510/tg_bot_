from tgbot.models import *
from telegram.ext import CallbackContext, MessageHandler
from tgbot.handlers.onboarding.loc import get_address_from_coords
from telegram import Update, InputMediaPhoto, ReplyKeyboardRemove
from tgbot.handlers.onboarding.static_text import text_lang, kb_text, admin_text, cart_text, chek_out_text
from tgbot.handlers.onboarding.keyboards import (
    start_kb, payment_kb, menu_kb, product_inline_kb, 
    phone_number_kb, change_phone_num_kb, admin_state_kb, cart_kb, category_kb, product_kb, chek_out_kb, back_kb, lang_kb
    )


lang = 'uz'
plus = 1



def start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    if created:
        text = text_lang(lang)['start_created'].format(first_name=u.first_name)
    else:
        text = text_lang(lang)['start_not_created'].format(first_name=u.first_name)
    update.message.reply_text(text=text, reply_markup= start_kb(lang=lang))
    u.action = "home"
    u.save()


def location_handler(update: Update, context: MessageHandler):
    locations = update.message.location
    locations = f'{locations.longitude} {locations.latitude}'
    user_data = User.objects.get(user_id=update.message.from_user.id)
    user_data.locations = locations
    user_data.save()
    update.message.reply_text(text=get_address_from_coords(locations))
    update.message.reply_text(text=text_lang(lang)['your_adres'], reply_markup= menu_kb(locations=locations, lang=lang))


def contact(update: Update, context: MessageHandler):
    user_id = update.message.from_user.id
    data_order = Order.objects.get(user_id_id=user_id, states='new')
    data_order.phone_number = update.message.contact.phone_number
    data_order.save()
    data = User.objects.get(user_id=user_id)
    data.action = 'paymant'
    data.save()
    update.message.reply_text(text=text_lang(lang)['choice_paymant'], reply_markup= payment_kb(lang=lang))
    

def menu_all(update: Update, context: MessageHandler):
    chat_id = update.message.chat.id
    m_text = update.message.text
    user_id = update.message.chat.id
    user_data = User.objects.get(user_id=user_id)
    if m_text == kb_text(lang, txt='cart_kb_text'):
        try:
            order_data = Order.objects.get(user_id_id = user_id, states = 'new')
            data = Cart.objects.filter(order_id=order_data.id)
            if len(data) > 0 :
                update.message.reply_text(text = cart_text(data=data, lang=lang), reply_markup = cart_kb(data=data, lang=lang))
            else:
                pass
                update.message.reply_text(text = text_lang(lang)['empty_cart'])
        except:
            update.message.reply_text(text = text_lang(lang)['empty_cart'])
    action = user_data.action
    if action == "home":
        if m_text == kb_text(lang, txt='menu_kb_text'):
            locations = user_data.locations 
            if locations == None:
                update.message.reply_text(text = text_lang(lang)['loc_info'], reply_markup =menu_kb(locations=False, lang=lang))        
            else:
                update.message.reply_text(text=get_address_from_coords(locations))
                update.message.reply_text(text=text_lang(lang)['your_adres'], reply_markup=menu_kb(locations=locations, lang=lang))
            user_data.action = 'locations'
            user_data.save()
        elif m_text == kb_text(lang, txt='settings_kb_text'):
            update.message.bot.sendMessage(chat_id=chat_id, text=text_lang(lang)['lang_text'], reply_markup= lang_kb())
        elif m_text == kb_text(lang, txt='about_kb_text'):
            update.message.bot.send_message(chat_id, text=text_lang(lang)['we'])
        elif m_text == kb_text(lang ,txt='orders_kb_text'):
            cart_data = Cart.objects.select_related('order_id', 'add_product').filter(order_id__user_id=user_id)
            for i in cart_data:
                states = i.order_id.states
                if states == 'pending':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_pending_text'])
                elif states == 'preparing':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_preparing_text'])
                elif states == 'new':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_idphone_number, states = text_lang(lang)['states_new_text'])
                elif states == 'delivering':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_delivering_text'])
                elif states == 'accepted':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_accepted_text'])
                elif states == 'declined':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_declined_text'])
                elif states == 'archivad':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_archivad_text'])
                elif states == 'cancellation':
                    text = text_lang(lang)['my_orders'].format(id=i.order_id.id, ph_num = i.order_id.phone_number, states = text_lang(lang)['states_declined_text'])
                count = i.amount * i.add_product.price
                text += text_lang(lang)['my_orders_1'].format(name = i.add_product.name, amount=i.amount, all_price=count)
                text += text_lang(lang)['my_orders_2'].format(payment = i.order_id.payment, all_price=i.order_id.all_price)
                update.message.bot.send_message(chat_id, text)
    elif action == 'locations':
        if m_text == kb_text(lang, txt='yes_kb_text'):
            update.message.reply_text(text=text_lang(lang)['menu_button'], reply_markup=category_kb(lang=lang))
            user_data.action = 'menu'
            user_data.save()
        elif m_text == kb_text(lang, txt='change_loc_kb_text'):
            update.message.reply_text(text = text_lang(lang)['loc_info'], reply_markup =menu_kb(locations=False, lang=lang))  
            user_data.action = 'change_loc'
            user_data.save()
            pass
        elif m_text == kb_text(lang, txt='back_kb_text'):
            update.message.reply_text(text=text_lang(lang)['main_menu'], reply_markup=start_kb(lang=lang))
            user_data.action = 'home'
            user_data.save()
    elif action == 'change_loc':
        if m_text == kb_text(lang, txt='back_kb_text'):
            update.message.reply_text(text=get_address_from_coords(user_data.locations))
            update.message.reply_text(text=text_lang(lang)['your_adres'], reply_markup=menu_kb(locations=user_data.locations, lang=lang))
            user_data.action = 'locations'
            user_data.save()
        pass
    elif action == 'menu':
        if m_text == kb_text(lang, txt='back_kb_text'):
            update.message.reply_text(text=get_address_from_coords(user_data.locations))
            update.message.reply_text(text=text_lang(lang)['your_adres'], reply_markup=menu_kb(locations=user_data.locations, lang=lang))
            user_data.action = 'locations'
            user_data.save()
        elif m_text not in kb_text(lang, txt=0).values():
            try:
                menu_data= Menu.objects.get(title=m_text)
                filename = 'media/' + str(menu_data.images)
                update.message.bot.sendPhoto(update.effective_chat.id, photo=open(filename, 'rb'))
                product_data = Product.objects.filter(category__id=menu_data.id)
                update.message.reply_text(text = text_lang(lang)['sub_menu_text'], reply_markup=product_kb(data=product_data, lang=lang))
                user_data.action = 'sub_menu'
                user_data.action_item = menu_data.id
                user_data.save()
            except Menu.DoesNotExist:
                update.message.reply_text(text = text_lang(lang)['error_menu_text'])
    elif action == "sub_menu":
        global plus
        if m_text == kb_text(lang, txt='back_kb_text'):
            plus = 1
            update.message.reply_text(text=text_lang(lang)['manu'], reply_markup= category_kb(lang=lang))
            user_data.action = 'menu'
            user_data.save()
        elif m_text not in kb_text(lang, txt=0).values():
            try:
                plus = 1
                product_data= Product.objects.get(name=m_text)
                filename = 'media/' + str(product_data.image) 
                update.message.bot.sendPhoto(update.effective_chat.id,  caption=f'{product_data.name}\n{product_data.price}\n{product_data.description}', photo=open(filename, 'rb'),\
                                reply_markup= product_inline_kb(num=plus, lang=lang))
            except:
                update.message.reply_text(text = text_lang(lang)['error_product_text'])
    elif action == "phone":
        if m_text[0:3] == '998' and len(m_text) == 12 and m_text.isdigit():
            data_order = Order.objects.get(user_id_id=user_id, states='new')
            data_order.phone_number = m_text
            data_order.save()
            user_data.action = 'paymant'
            user_data.save()
            update.message.reply_text(text = text_lang(lang)['choice_paymant'], reply_markup = payment_kb(lang=lang))
        elif m_text == kb_text(lang, txt='back_kb_text'):
            product_data = Product.objects.filter(category__id=user_data.action_item)
            update.message.reply_text(text = text_lang(lang)['sub_menu_text'], reply_markup=product_kb(data=product_data, lang=lang))
            user_data.action = 'sub_menu'
            user_data.save()
    elif action == 'change_phone':
        if m_text == kb_text(lang, txt='proceed'):
            update.message.reply_text(text = text_lang(lang)['choice_paymant'], reply_markup = payment_kb(lang=lang))
            user_data.action = 'paymant'
            user_data.save()
        elif m_text == kb_text(lang, txt='back_kb_text'):
            product_data = Product.objects.filter(category__id=user_data.action_item)
            photo = product_data[0].category.images
            filename = 'media/' + str(photo)
            update.message.bot.sendPhoto(update.effective_chat.id, photo=open(filename, 'rb'))
            update.message.reply_text(text = text_lang(lang)['sub_menu_text'], reply_markup=product_kb(data=product_data, lang=lang))
            user_data.action = 'sub_menu'
            user_data.save()
        elif m_text == kb_text(lang, txt='change_number_text'):
            update.message.reply_text(text=  text_lang(lang)['new_phone_num_text'], reply_markup= phone_number_kb(lang=lang))
            user_data.action = 'phone'
            user_data.save()         
    elif action == 'paymant':
        if m_text == kb_text(lang, txt='cash_kb_text') or m_text == kb_text(lang, txt='terminal_kb_text') or m_text == kb_text(lang, txt='click_kb_text') or m_text == kb_text(lang, txt='payme_kb_text'):
            try:
                order_data = Order.objects.get(user_id_id=update.message.from_user.id, states='new')
                order_data.payment = m_text[2::]
                order_data.save()
                user_data.action = "chek_out"
                user_data.save()
                text = chek_out_text(data=order_data, lang=lang)
                update.message.reply_text(text = text_lang(lang)['chek_out_1'], reply_markup=ReplyKeyboardRemove())
                update.message.reply_text(text = text_lang(lang=lang)['chek_out_2'], reply_markup= back_kb(lang=lang))
                update.message.reply_text(text = text, reply_markup = chek_out_kb(lang=lang))
            except Order.DoesNotExist:
                pass
        elif m_text == kb_text(lang, txt='back_kb_text'):
            data = Order.objects.get(user_id_id=user_id, states='new')
            update.message.reply_text(text = text_lang(lang)['old_phone_num_text'].format(number = data.phone_number), reply_markup = change_phone_num_kb(lang=lang))
            user_data.action = 'change_phone'
            user_data.save()
    elif action == 'chek_out':
        if m_text == kb_text(lang, txt='back_kb_text'):
            m_id=  update.message.reply_text(text=  text_lang(lang)['choice_paymant'], reply_markup= payment_kb(lang=lang)).message_id
            user_data.action = 'paymant'
            user_data.save()
            update.message.bot.delete_message(chat_id, m_id-2)
    



def query_callback(update: Update, context: CallbackContext):
    global plus, lang
    query = update.callback_query.data
    update.callback_query.answer()
    user_id = update.callback_query.message.chat.id
    if query == '+':
        if plus <= 10:
            plus += 1
            update.callback_query.edit_message_caption(update.callback_query.message.caption, reply_markup=product_inline_kb(num=plus, lang=lang))

    elif query == '-':
        if plus >= 2:
            plus -= 1
            update.callback_query.edit_message_caption(update.callback_query.message.caption, reply_markup=product_inline_kb(num=plus, lang=lang))

    elif query == 'add_to_cart':
        num = update.callback_query.message.reply_markup.inline_keyboard[0][1]['text']
        name = update.callback_query.message.caption.split('\n')[0]
        product = Product.objects.get(name=name)
        s_text = text_lang(lang)['correct'].format(product_name=name,)
        order_data ,create = Order.objects.get_or_create(user_id_id=user_id, states='new')
        cart_data ,create = Cart.objects.update_or_create(order_id_id=order_data.id, add_product_id=product.id)
        cart_data.amount += int(num)
        order_data.all_price += int(cart_data.amount) * product.price
        cart_data.save()
        order_data.save()
        filename = 'media/' + str(product.category.images)
        update.callback_query.message.edit_media(media=InputMediaPhoto(media=open(filename, 'rb')))
        update.callback_query.message.reply_text(text=s_text)
        plus = 1

    elif query == "clear":
        # data_id = Order.objects.get(user_id_id=user_id, states='new').id
        # Cart.objects.filter(order_id_id=data_id). te()
        Cart.objects.select_related('order_id').filter(order_id__user_id=user_id, order_id__states='new').delete()
        update.callback_query.message.delete()
        update.callback_query.message.reply_text(text=text_lang(lang)['clear_cart'])

    elif query == "order":
        user_data = User.objects.get(user_id=user_id)
        data = Order.objects.get(user_id_id=user_id, states='new')
        if data.phone_number == '':
            update.callback_query.message.delete()
            update.callback_query.message.reply_text(text = text_lang(lang)['new_phone_num_text'], reply_markup = phone_number_kb(lang=lang))
            user_data.action = 'phone'
            user_data.save()
        else:
            update.callback_query.message.delete()
            update.callback_query.message.reply_text(text = text_lang(lang)['old_phone_num_text'].format(number = data.phone_number),\
                 reply_markup =  change_phone_num_kb(lang=lang))
            user_data.action = 'change_phone'
            user_data.save()

    elif query == 'yes':
        data = Order.objects.get(user_id_id=user_id, states='new')
        data.states = 'pending'
        data.save()
        user_data = User.objects.get(user_id=user_id)
        user_data.action = 'home'
        user_data.save()
        update.callback_query.message.delete()
        update.callback_query.message.reply_text(text=text_lang(lang)['apcet'], reply_markup= start_kb(lang=lang))
        context.bot.send_message(chat_id=-896089921, text=admin_text(data, lang=lang), reply_markup= admin_state_kb(data))

    elif query == "no":
        data = Cart.objects.select_related('order_id').filter(order_id__user_id=user_id, order_id__states='new')
        update.callback_query.message.delete()
        update.callback_query.message.reply_text(text = cart_text(data=data, lang=lang), reply_markup =  cart_kb(data=data, lang=lang))

    elif query == "ok":
        data = Order.objects.get(pk = int(update.callback_query.message.text.split()[1]))
        data.states = 'preparing'
        data.save()
        chat = data.user_id.user_id
        update.callback_query.edit_message_reply_markup(reply_markup= admin_state_kb(data))
        update.callback_query.message.bot.sendMessage(chat_id=chat, text=text_lang(lang)['pending'].format(id=data.id))

    elif query == "deliver":
        data = Order.objects.get(pk = int(update.callback_query.message.text.split()[1]))
        data.states = 'delivering'
        data.save()
        chat = data.user_id.user_id
        update.callback_query.edit_message_reply_markup(reply_markup= admin_state_kb(data))
        update.callback_query.message.bot.sendMessage(chat_id=chat, text=text_lang(lang)['delivering'].format(id=data.id))

    elif query == "close":
        data = Order.objects.get(pk = int(update.callback_query.message.text.split()[1]))
        data.states = 'cancellation'
        data.save()
        chat = data.user_id.user_id
        update.callback_query.message.delete()
        update.callback_query.message.bot.sendMessage(chat_id=chat, text=text_lang(lang)['close'].format(id=data.id))

    elif query == "apcet":
        data = Order.objects.get(pk = int(update.callback_query.message.text.split()[1]))
        data.states = 'accepted'
        data.save()
        chat = data.user_id.user_id
        update.callback_query.message.delete()
        update.callback_query.message.bot.sendMessage(chat_id=chat, text=text_lang(lang)['thenks'].format(id=data.id))

    elif query == 'num':
        pass
    
    elif query == "uz":
        data = User.objects.get(user_id = user_id)
        data.language_code = "uz"
        data.save()
        lang = "uz"
        text = text_lang(lang)['change_lang'].format(first_name=data.first_name)
        update.callback_query.message.delete()
        update.callback_query.message.reply_text(text=text, reply_markup= start_kb(lang=lang))
        
    elif query == 'ru':
        data = User.objects.get(user_id = user_id)
        data.language_code = "ru"
        data.save()
        lang = 'ru'
        text = text_lang(lang)['change_lang'].format(first_name=data.first_name)
        update.callback_query.message.delete()
        update.callback_query.message.reply_text(text=text, reply_markup= start_kb(lang=lang))

    else:
        name = query[2:]
        data = Cart.objects.select_related('order_id', 'add_product').filter(order_id__user_id=user_id, order_id__states='new', add_product__name = name).delete()
        data = Cart.objects.select_related('order_id').filter(order_id__user_id=user_id, order_id__states='new')
        if len(data) != 0:    
            update.callback_query.edit_message_text(cart_text(data=data, lang=lang), reply_markup =  cart_kb(data=data, lang=lang))
        else:
            update.callback_query.message.delete()
            update.callback_query.message.reply_text(text=text_lang(lang)['clear_cart'])



    
