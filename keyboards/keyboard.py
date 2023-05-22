import requests
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import rest_api




def get_keyboard(name: str, flag: bool = False,):

    if name == 'start':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Есть автомобиль'),
                             KeyboardButton('Я пешеход'))
    elif name == 'user':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('📨 Отправить сообщение'))
        keyboard.add(KeyboardButton('🚘 Список номеров'))
        keyboard.add(KeyboardButton('🏙 Список адресов'))
        keyboard.add(KeyboardButton('📍 Тех.поддержка'))
    elif name == 'add_num_car':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Добавить номер'))
        keyboard.add(KeyboardButton('Удалить номер'))
        keyboard.add(KeyboardButton('Назад'))
    elif name == 'add/delete_address':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Добавить адрес'))
        if not flag:
            keyboard.add(KeyboardButton('Удалить адрес'))

        keyboard.add(KeyboardButton('Назад'))

        
    elif name == 'uk':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('📨 Отправить рассылку'))
        keyboard.add(KeyboardButton('🏙 Список адресов УК'))
        keyboard.add(KeyboardButton('📍 Тех.поддержка'))
    elif name == 'uk_template':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{rest_api}/template/')
        template = req.json()
        for temp in template:
            keyboard.add(KeyboardButton(temp['template_id']))
        keyboard.add(KeyboardButton('Назад 🔙'))
    elif name == 'uk_malling_list':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('По адресу 🌅'))
        keyboard.add(KeyboardButton('По всем адресам 🌅'))
        keyboard.add(KeyboardButton('По номеру авто 🚘'))
        keyboard.add(KeyboardButton('Назад 🔙'))
    elif name == 'back_uk':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Назад 🔙'))
    elif name == 'admin':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Отправить рассылку 📨'))
        keyboard.add(KeyboardButton('🚘 Список номеров'))
        keyboard.add(KeyboardButton('🏙 Список адресов'))
        keyboard.add(KeyboardButton('📍 Тех.поддержка'))
    elif name == 'admin_malling_list':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('🌅 По адресу'))
        keyboard.add(KeyboardButton('🏚 По номеру дома'))
        keyboard.add(KeyboardButton('🚘 По номеру авто'))
        keyboard.add(KeyboardButton('Всем пользователям'))
        keyboard.add(KeyboardButton('Назад ◀'))
    return keyboard



def addres_kb(name: str, user_id):
    if name == 'address_keyboard':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{rest_api}/address/?user__user_id={user_id}')
        data = req.json()
        for response in data:
            keyboard.add(KeyboardButton(response['id']))
        keyboard.add(KeyboardButton('Назад'))
    
    elif name == 'car_number':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{rest_api}/number_car/?user__user_id={user_id}')
        data = req.json()
        for response in data:
            keyboard.add(KeyboardButton(response['car_num']))
        keyboard.add(KeyboardButton('Назад'))

    elif name == 'list_address_uk':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{rest_api}/address_uk/?user__user_id={user_id}')
        data = req.json()
        for response in data[0]['address']:
            print(response)
            address = response['address']
            house_humber = response['house_number']
            keyboard.add(KeyboardButton(f'{address},{house_humber}'))
        keyboard.add(KeyboardButton('Назад 🔙'))
    
    elif name == 'list_house_number_uk':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{rest_api}/address_uk/?user__user_id={user_id}')
        data = req.json()
        for response in data[0]['address']:
            keyboard.add(KeyboardButton(response['house_number']))
        keyboard.add(KeyboardButton('Назад 🔙'))

    return keyboard
        