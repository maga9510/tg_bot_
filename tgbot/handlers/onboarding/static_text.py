from tgbot.models import *
from tgbot.handlers.onboarding.loc import distance, get_address_from_coords


def cart_text(data, lang):
    if lang == 'uz':
        count = 0
        names = str()
        for i in data:
            num = 0
            product_data = Product.objects.filter(name=i.add_product)
            price = product_data[num].price
            names += f"\t➡️{product_data[num].name.capitalize()}\t{i.amount} dona. * {price} = {i.amount * price} so'm\n"
            count += i.amount * price
            num += 1
        price_dev = count + 10000
        call_cart_text = "Korzinadagilar:\n{name}\nTo'plam narx {price}\nDostavka xizmati 10.000 so'm\nTo'plam narx + Dostavka {price_dev}."
        text = call_cart_text.format(name=names, price=count, price_dev=price_dev)
        return text  
    else:
        count = 0
        names = str()
        for i in data:
            num = 0
            product_data = Product.objects.filter(name=i.add_product)
            price = product_data[num].price
            names += f"\t➡️{product_data[num].name.capitalize()}\t{i.amount} шт. * {price} = {i.amount * price} сум\n"
            count += i.amount * price
            num += 1
        price_dev = count + 10000
        call_cart_text = "В корзине:\n\n{name}\nОбший цена {price}\nЗа Доставку 10.000 сум\nОбший цена + Доставка {price_dev}."
        text = call_cart_text.format(name=names, price=count, price_dev=price_dev)        
        return text


def chek_out_text(data, lang):
    if lang =="uz":    
        text = f"Buyurtma raqami №:{str(data.id)}.\nTelefon raqami: {data.phone_number}.\nTo'lov turi :{data.payment}\n"
        all_price = int()
        for i in Cart.objects.filter(order_id_id=data.id):
            text += f"✅{i.add_product.name.capitalize()} | {i.amount}dona * {i.add_product.price} =  {i.amount * i.add_product.price} so'm\n\n"
            all_price += i.amount * i.add_product.price

        text += f"Dostavka narxi 10.000 so'm\nTo'plam narx {all_price + 10000}\nBuyurtmani tasdiqlaysizm?"
        return text
    else:
        text = f"Номер заказа №:{str(data.id)}.\nНомер телефона: {data.phone_number}.\nСпособ оплаты :{data.payment}\n"
        all_price = int()
        for i in Cart.objects.filter(order_id_id=data.id):
            text += f"✅{i.add_product.name.capitalize()} | {i.amount}шт. * {i.add_product.price} =  {i.amount * i.add_product.price} сум\n\n"
            all_price += i.amount * i.add_product.price

        text += f"Цена доставки 10.000 сум\nОбший цена {all_price + 10000}\nВы подтвеждайте заказ?"
        return text
        

def admin_text(data, lang):
    loc = data.user_id.locations.split()
    q = distance(x = float(loc[0]), y = float(loc[1]))
    if lang == "uz":
        text = f"№: {data.id} raqamli buyurtma.\nKlient raqami {data.phone_number}.\nManzil:\n{get_address_from_coords(data.user_id.locations)}.\n"
        for i in Cart.objects.filter(order_id_id=data.id): 
            text += f"🔖{i.add_product.name.capitalize()} | {i.amount}dona\n"
        text += f"Filiyal: {q['name']}\n"
        text += f"username: @{data.user_id.username}\n"
        return text
    else:
        text = f"№: {data.id} номер заказа.\nТелефон клиента: {data.phone_number}.\nАдрес:\n{get_address_from_coords(data.user_id.locations)}.\n"
        for i in Cart.objects.filter(order_id_id=data.id): 
            text += f"🔖{i.add_product.name.capitalize()} | {i.amount}шт.\n"
        text += f"Филиал: {q['name']}\n"
        text += f"username: @{data.user_id.username}\n"
        return text


def text_lang(lang):
    if lang == 'uz':    
        text = {
            'lang_text' : "Tilni tanlang???\n\tRu----🇷🇺\n\tUzb----🇺🇿",
            'start_not_created' : "Qaytganingizdan xursandmiz, {first_name}!",
            'start_created' : "{first_name} dostavka botga xush kelibsiz!!!!",
            'menu_button' : 'Menyulardan tanlang???',
            'correct' : "{product_name} korzinaga qo'shildi!!!",
            'loc_info' : "Lokatsiya haqida ma'lumot.",
            'empty_cart' : "Korzina hozircha bo'sh.",
            'sub_menu_text' : "Tanlang.",
            'clear_cart' : "Korzina tozalandi.",
            'new_phone_num_text' : "Telefon raqamingizni yuboring yoki raqamni kiriting ⤵️\n998991234567 ko'rinishida bo'lishi kerak.",
            'old_phone_num_text' : 'Sizning oldingi raqamingiz:{number}.\nNomerni almashtirishni hohlaysizmi???',
            'choice_paymant' : "To'lov usulini tanlang.",
            'chek_out_1': 'Xatolikni bartaraf etish uchun',
            'chek_out_2': "Ma'lumotlarni tekshirib chiqishingizni so'raymiz",
            'your_adres' : 'siz shu adresdami???',
            'main_menu' : "Bosh menu.",
            'manu' : "Menu.",
            'payment_chois': "To'lov usuli tanlandi.",
            'apcet': 'Buyurtma qabul qilindi.',
            'chek_out': 'Qayta chek out.',
            'pending': "Sizning №: {id} raqamli buyurtmangiz tayyorlanmoqda!!! ⏳⏳",
            'delivering': "🛵 Sizning №: {id} raqamli buyurtmangiz yo'lda.",
            'close' :"🚫 №: {id} raqamli buyurtma bekor qilindi.",
            'thenks':"№: {id} raqamli buyurtma ytkazib berildi\n😊 Bizni tanlaganinggiz uchun raxmat.",
            'change_lang': "O'zbek tliga o'zgartirildi",
            'my_orders': "Buyurtma raqami №: {id}\nBuyurtma holati {states}\nTelefon raqam: {ph_num}\n",
            "my_orders_1": "{name} * {amount}dona = {all_price} so'm\n",
            "my_orders_2": "To'lov turi {payment}\nTo'plam narxi {all_price}\n",
            'we': 'T-Bone',
            'error_menu_text': "Xatolik! Bunday menu topilmadi",
            'error_product_text': "Xatolik! Bunday maxsulot topilmadi",
            'states_pending_text': "Buyurtma tasdiqlanishi kutilmoqda",
            'states_preparing_text': "Buyurtma tayyorlanmoqda",
            'states_new_text': 'Buyurtma yangi ochilgan',
            'states_delivering_text': 'Buyurtma yetkazib berilmoqda',
            'states_accepted_text': 'Buyurtma yetkazib berildi',
            'states_declined_text': 'Buyurtma bekor qilindi',
            'states_archivad_text': 'Arxiv',
        }
        
        return text
    else:
        text = {
            'lang_text': "Выберите язык???\n\tRu----🇷🇺\n\tUzb----🇺🇿",
            'start_created': "{first_name} добро пожаловать к доставку боту!!!!",
            'start_not_created': "Мы рады вам {first_name}!",
            'menu_button' : 'Выберите меню???',
            'correct': "{product_name} добавлено к корзине!!!",
            'loc_info': "Информация о локации",
            'empty_cart': "Корзина пока пусто",
            'sub_menu_text': "Выберите",
            'clear_cart': "Корзина очищена",
            'new_phone_num_text': "Отправьте номер телефона или введите номер телефона ⤵️\n998991234567 как показано",
            'old_phone_num_text' :'Ваш номер:{number}.\nХотите поменять номер телефона???',
            'choice_paymant' : "Выберите способ оплаты",
            'chek_out_1': 'Что бы не было ошибок',
            'chek_out_2': 'Пожалуста проверти даные',
            'your_adres': 'Вы в этом адресе???',
            'main_menu': "Главное меню",
            'manu': "Меню",
            'payment_chois': "Выберите способ оплаты",
            'apcet': 'Ваш заказ принят',
            'chek_out': 'Повторное проверка',
            'pending': "Ваш заказ с №: {id} готовиться!!! ⏳⏳",
            'delivering': "🛵 Ваш заказ с №: {id} уже в пути",
            'close': "🚫 Заказ с номером №: {id} отменен.",
            'thenks': "Заказ с номером №: {id} получен\n😊 Спасибо что выбрали нас",
            'change_lang': "Бот перешол на руский язык",
            'my_orders': "Заказ с номером №: {id}\nСостаяние заказа [{states}]\nНомер телефона: {ph_num}\n\n",
            "my_orders_1": "{name} * {amount} = {all_price} сум\n\n",
            "my_orders_2": "Способ оплаты {payment}\nОбщая сумма  {all_price}\nУслуга таксиста 10.000 сум",
            'we': 'T-Bone',
            'error_menu_text': "Ошибка такого меню не найдено",
            'error_product_text': "Ошибка такого продукта не найдено",
            'states_pending_text': 'Заказ в ожидание подтверждение',
            'states_preparing_text': "Заказ готовитсяю",
            'states_new_text': 'Новый заказ',
            'states_delivering_text': 'Зоказ доставляется',
            'states_accepted_text': 'Заказ доставленно',
            'states_declined_text': 'Заказ отменен',
            'states_archivad_text': 'Архив',
        }
        return text

def kb_text(lang, txt):
    if lang == 'uz':    
        text = {
            'menu_kb_text' : '🍽 Menyu',
            'cart_kb_text' : '🧺 Savatcha',
            'orders_kb_text' : '📌 Buyurtmalarim',
            'settings_kb_text' : '⚙️ Sozlamar',
            'about_kb_text' : '📝 Biz haqimizda',
            'back_kb_text': '⬅️ Orqaga',
            'yes_kb_text': '✔️ Ha',
            'loc_kb_text': '📍 Lokatsiyani yuboring',
            'change_loc_kb_text': "Lokatsiyani o'zgartirish",
            "proceed": "✅ Davom etish!!!",
            'change_number_text': "Nomerni o'zgartirish",
            'cash_kb_text': "💵 Naqt",
            'terminal_kb_text': "💳 Terminal", 
            'click_kb_text': "📲 Click",
            'payme_kb_text': "📲 PayMe",
            'phone_kb_text': '📲 Telefon raqamingiz!!!',
        }  
        if txt == 0:
            return text
        else:
            return text[txt]
    else:
        text = {
            'menu_kb_text' : '🍽 Меню',
            'cart_kb_text' : '🧺 Корзина',
            'orders_kb_text' : '📌 Мои заказы',
            'settings_kb_text' : '⚙️ Настройки',
            'about_kb_text' : '📝 О нас',
            'back_kb_text': '⬅️ Назад',
            'yes_kb_text': '✔️ Да',
            'loc_kb_text': '📍 Отправьте локацию',
            'change_loc_kb_text': "Изменить локацию",
            "proceed": "✅ Продолжить!!!",
            'change_number_text': "Изменит нимер телефона",
            'cash_kb_text': "💵 Наличние",
            'terminal_kb_text': "💳 Терминал", 
            'click_kb_text': "📲 Click",
            'payme_kb_text': "📲 PayMe",
            'phone_kb_text': '📲 Номер телефона !!!',
        }
        if txt == 0:
            return text
        else:
            return text[txt]

def inline_kb_text_l(lang, txt):
    if lang == 'uz':
        text = {
            'corrected_order_text' : '✅ Buyurtmani tasdiqlash',
            'clear_cart_text' : "🚫 Korzinani bo'shatish",
            'add_to_cart_text' : "🧺 Korzinaga qo'shish.",
            'yes_i_kb_text' : '✅ Ha',
            'no_i_kb_text' : "❌ Yo'q",
        }
        return text[txt]
    else:
        text = {
            'corrected_order_text' : '✅ Подтвердить заказ',
            'clear_cart_text' : '🚫 Очистить корзину',
            'add_to_cart_text' : "🧺 Добавит в корзину.",
            'yes_i_kb_text' : '✅ Да',
            'no_i_kb_text' : "❌ Нет",
        }
        return text[txt]

def inline_kb_text(txt):
    text = {
        'uz_i_kb_text': "O'zbek tili 🇺🇿",
        'ru_i_kb_text': 'Руский язык 🇷🇺',
        'cancel_order_i_kb': '❌ Byurtmani bekor qilish',
        'confirm_i_kb_text': "👌 Tasdiqlash",
        'deliver_i_kb_text': "🛵 Yetkazib berish",
        'confirmed_i_kb_text': 'Byurtmani qabul qilindi',


    }
    return text[txt]