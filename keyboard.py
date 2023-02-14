from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup



def get_keyboard(name: str):
    if name == 'start':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton('Прайс💵', callback_data='price'),
                    InlineKeyboardButton('Контакты📞', callback_data='contact'),
                    InlineKeyboardButton('Адрес📍', callback_data='adress'))
        keyboard.add(InlineKeyboardButton('Instagram', url = 'https://www.instagram.com/fanatkgz/'),
                     InlineKeyboardButton('Taplink', url = 'https://fanatkg.taplink.ws/'),
                     InlineKeyboardButton('Telegram', url = 'https://t.me/wearefanatkgz'),
                     )

        keyboard.add (InlineKeyboardButton('Открыть виртуальную карту💳', callback_data='card'))
    elif name == "joined":
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton('Прайс💵', callback_data='price'),
                    InlineKeyboardButton('Контакты📞', callback_data='contact'),
                    InlineKeyboardButton('Адрес📍', callback_data='adress'))
        keyboard.add(InlineKeyboardButton('Instagram', url = 'https://www.instagram.com/fanatkgz/'),
                     InlineKeyboardButton('Taplink', url = 'https://fanatkg.taplink.ws/'),
                     InlineKeyboardButton('Telegram', url = 'https://t.me/wearefanatkgz'),
                     )
        keyboard.add (InlineKeyboardButton('Открыть виртуальную карту💳', url ='https://t.me/FANAT_KG_bot'))
    elif name == "branches":
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton("Ауэзова 3В (Аламедин 1) ", callback_data="alamedin"))
        keyboard.add(InlineKeyboardButton("Безымянная 37/2 (PS/PC)", callback_data="bezymyan"))
        keyboard.add(InlineKeyboardButton("Айтматова 29", callback_data="aitmatov"))
        keyboard.add(InlineKeyboardButton("Киевская 190", callback_data="kiev"))
    
    elif name == "adres":
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton("Ауэзова 3В (Аламедин 1) ", url='https://2gis.kg/bishkek/firm/70000001057502973'))
        keyboard.add(InlineKeyboardButton("Безымянная 37/2 (PS/PC)", url = 'https://2gis.kg/bishkek/firm/70000001037603270'))
        keyboard.add(InlineKeyboardButton("Айтматова 29", url='https://2gis.kg/bishkek/firm/70000001030037152'))
        keyboard.add(InlineKeyboardButton("Киевская 190", url= 'https://2gis.kg/bishkek/firm/70000001024980588'))

    return keyboard
        