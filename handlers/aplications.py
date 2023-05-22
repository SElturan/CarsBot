import json
import re
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.keyboard import get_keyboard, addres_kb
from handlers.base import *
from config import url, headers


class Applications:
    def __init__(self, message: types.Message):
        self.bot = bot
        self.message = message


    async def aplications_people(self, message:types.Message):

        class AplicationsRegistration(StatesGroup):
            phone = State()



        await AplicationsRegistration.phone.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("Отправить номер телефона📱", request_contact=True))
        await message.answer(text='Подтвердите номер телефона', reply_markup=keyboard)

        @dp.message_handler(content_types=types.ContentTypes.CONTACT,state=AplicationsRegistration.phone)
        async def phone(message: types.Contact, state: FSMContext):

            async with state.proxy() as data:
                data['phone'] = message.contact.phone_number
                phone = data['phone']
                data = {
                        "user_id": message.from_user.id,
                        "first_name": message.from_user.first_name,
                        "phone_number": phone,
                        }


                
                await add_user(data)
                if add_user:
                    await message.answer('Выберите действие ', reply_markup=get_keyboard('user'))
                    await state.finish()
                else:
                    await message.answer('Ошибка регистрации')
                    await state.finish()

                await state.finish()


    async def add_num_cars(self, message:types.Message):
        class ApplicationsRegistrationCar(StatesGroup):
            car_num = State()

        await ApplicationsRegistrationCar.car_num.set()
        await message.answer('Введите номер автомобиля\nБез RUS')

        @dp.message_handler(state=ApplicationsRegistrationCar.car_num)
        async def car_num(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['car_num'] = message.text
                car_num = data['car_num']
                car_num = car_num.upper()
               

                car_num = car_num.replace('S', 'C').replace('Y', 'У')
                
                similar_chars = {
                    'А': 'A',
                    'В': 'B',
                    'Е': 'E',
                    'К': 'K',
                    'М': 'M',
                    'Н': 'H',
                    'О': 'O',
                    'Р': 'P',
                    'С': 'C',
                    'Т': 'T',
                    'У': 'Y',
                    'Х': 'X'
                }

                # Заменяем похожие символы в номере автомобиля на их английские аналоги
             
                for cyrillic_char, latin_char in similar_chars.items():
                    car_num = car_num.replace(cyrillic_char, latin_char)

                # Проверяем, соответствует ли номер формату
                car_num_pattern = re.compile(r'^[ABEKMHOPCTYX]{1}\d{3}[ABEKMHOPCTYX]{2}\d{2,3}$')
                
                if car_num_pattern.match(car_num):
                    # Если номер соответствует формату, то заменяем буквы на русские символы
                    car_num = car_num.replace('A', 'А').replace('B', 'В').replace('E', 'Е').replace('K', 'К').replace('M', 'М').replace('H', 'Н').replace('O', 'О').replace('P', 'Р').replace('C', 'С').replace('T', 'Т').replace('Y', 'У').replace('X', 'Х').replace('S', 'C').replace('Y', 'У').replace('RUS', '')
    

                    data_car = {
                    "user_id": message.from_user.id,
                    "car_num": car_num
                }
                    success = await add_num_car(data_car)
                    if success:
                        await message.answer('Вы успешно добавили номер', reply_markup=get_keyboard('user'))
                    else:
                        await message.answer('Вы добавили уже 3 номера', reply_markup=get_keyboard('user'))
                else:
                    await message.answer('Вы ввели некорректный номер. Номер автомобиля России должен иметь формат "A000AA00" или "000AA000", где "A" - это буквы русского алфавита, "0" - цифры. Без RUS', reply_markup=get_keyboard('user'))
                    
          
                await state.finish()

    async def aplications_car(self, message:types.Message):

        class AplicationsRegistrationCar(StatesGroup):
            phone = State()



        await AplicationsRegistrationCar.phone.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("Отправить номер телефона📱", request_contact=True))
        await message.answer(text='Подтвердите номер телефона', reply_markup=keyboard)

        @dp.message_handler(content_types=types.ContentTypes.CONTACT,state=AplicationsRegistrationCar.phone)
        async def phone(message: types.Contact, state: FSMContext):

            async with state.proxy() as data:
                data['phone'] = message.contact.phone_number

                phone = data['phone']




                data = {
                        "user_id": message.from_user.id,
                        "first_name": message.from_user.first_name,
                        "phone_number": phone,
                        }
                
                
                
                
                await add_user(data)
                if add_user:
                    await self.add_num_cars(message)
                                        
                else:
                    await message.answer('Ошибка регистрации')
                    await state.finish()

                








    async def added_address(self, message:types.Message):
        class AplicationsAddedAddress(StatesGroup):
            city = State()
            street = State()
            house_number = State()



        await AplicationsAddedAddress.city.set()
        await bot.send_message(chat_id=message.chat.id,text='Введите город')

        @dp.message_handler(state=AplicationsAddedAddress.city)
        async def city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                result = {'query': f'город {message.text}', 'count': 1}
                json_data = json.dumps(result)
                check_city = await post_dadata(headers, url, json_data)
                data['city'] = check_city
                
                if check_city:
                    await message.answer(f'Вы ввели корректный город {check_city}')
                    await message.answer('Введите улицу')
                    await AplicationsAddedAddress.next()
                else:
                    await message.answer('Город не найден\n\nПожалуйста введите корректный город')
                    return
                
        @dp.message_handler(state=AplicationsAddedAddress.street)
        async def street(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                сity_result = data['city']
                message_text = f'{сity_result} {message.text}'
                result = {'query': message_text, 'count': 1}
                json_data = json.dumps(result)
                check_street = await post_dadata_street(headers, url, json_data)
                
                data['street'] = check_street
                

                
                if check_street:
                   
                    await message.answer(f'Вы ввели корректную улицу {check_street}')
                    await message.answer('Введите номер дома')
                    await AplicationsAddedAddress.next()
                else:
                    await message.answer(f'Улица в этом городе не найдена!!\n\nПожалуйста введите корректный адрес')
                    return
                
        @dp.message_handler(state=AplicationsAddedAddress.house_number)
        async def house_number(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['house_number'] = message.text
                house_number = data['house_number']
                сity = data['city']
                street = data['street']
                

                data = {
                            "user_id": message.from_user.id,
                            "city": сity,
                            "address": street,
                            "house_number": house_number
                        }
                
              
                await add_address(data)
                if add_address:
                    await message.answer('Адрес добавлен', reply_markup=get_keyboard('user'))
                    await state.finish()
                else:
                    await message.answer('Ошибка добавления адреса')
                    await state.finish()

                

    

    async def message_car_num(self, message:types.Message):
        user_id = message.from_user.id
        chekc_user = await is_user_registered(user_id)
       
        if chekc_user[0]['role'] == 'UK':
            markup=get_keyboard('uk')

        elif chekc_user[0]['role'] == 'admin':
            markup=get_keyboard('admin')
        
        else:
            markup=get_keyboard('user')
    

        
        class AplicationsFSM(StatesGroup):
            car_num = State()
            message_text = State()
            car_num_user = State()

       
        await AplicationsFSM.car_num.set()
        await bot.send_message(chat_id=message.chat.id, text='Введите номер машины которому хотите отправить сообщение', reply_markup=ReplyKeyboardRemove())

        @dp.message_handler(state=AplicationsFSM.car_num)
        async def car_num(message: types.Message, state: FSMContext):
                
            async with state.proxy() as data:
                data['car_num'] = message.text
                car_num = data['car_num']
                car_num = car_num.upper()
                car_num = car_num.replace('A', 'А').replace('B', 'В').replace('E', 'Е').replace('K', 'К').replace('M', 'М').replace('H', 'Н').replace('O', 'О').replace('P', 'Р').replace('C', 'С').replace('T', 'Т').replace('Y', 'У').replace('X', 'Х').replace('S', 'C').replace('Y', 'У')
                data['car_num'] = car_num
                msg_id = await message_car_num(car_num)
                if msg_id:
                    await message.answer('Введите сообщение для рассылки по номеру')
                    await AplicationsFSM.next()
                else:
                    await message.answer('Такого номера нет в базе', reply_markup=markup)
                    await state.finish()
        

        @dp.message_handler(state=AplicationsFSM.message_text)
        async def message_text(message: types.Message, state: FSMContext):   
            async with state.proxy() as data:
                data['message_text'] = message.text
         
            await message.answer('Введите номер машины от которого хотите отправить сообщение', reply_markup=addres_kb('car_number', user_id=user_id))
            
            await AplicationsFSM.next()

                
        
        
        @dp.message_handler(state=AplicationsFSM.car_num_user)
        async def car_num_user(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['car_num_user'] = message.text
                car_num_user = data['car_num_user']
                car_num_user = car_num_user.upper()
                car_num_user = car_num_user.replace('A', 'А').replace('B', 'В').replace('E', 'Е').replace('K', 'К').replace('M', 'М').replace('H', 'Н').replace('O', 'О').replace('P', 'Р').replace('C', 'С').replace('T', 'Т').replace('Y', 'У').replace('X', 'Х').replace('S', 'C').replace('Y', 'У').replace('RUS', '')
                data['car_num_user'] = car_num_user
            user_car_num = message.from_user.id
            chekc_car_number = await get_number_car_check(user_car_num, car_num_user)
            if not chekc_car_number:
                await message.answer('У вас нет такого номера', reply_markup=markup)
                await state.finish()
            else:
                messages = data['message_text']
                car_num = data['car_num']
                message_text = f'ОТ НОМЕРА: {car_num_user}\nДЛЯ НОМЕРА: {car_num}\n\nСообщение:\n{messages}'

                msg_id = await message_car_num(car_num)
                if msg_id:
                    for user_id in msg_id:
                        try:
                            await bot.send_message(chat_id=user_id, text=message_text)
                            await state.finish()
                        except Exception:
                            continue
                        await message.answer('Сообщение отправлено', reply_markup=markup)
                        await state.finish()
                else:
                    await message.answer('Сообщение не отправлено', reply_markup=markup)
                    await state.finish()
                    


    async def deleted_car_num(self, message:types.Message):
        user_id = message.from_user.id
        chekc_user = await is_user_registered(user_id)
       
        if chekc_user[0]['role'] == 'UK':
            markup=get_keyboard('uk')

        elif chekc_user[0]['role'] == 'admin':
            markup=get_keyboard('admin')
        
        else:
            markup=get_keyboard('user')
    

        class AplicationsDeleteCar(StatesGroup):
            car_num = State()



        await AplicationsDeleteCar.car_num.set()
        await bot.send_message(chat_id=message.chat.id,  text='Выберите номер машины которую хотите удалить',reply_markup=addres_kb('car_number', user_id=user_id))

        @dp.message_handler(state=AplicationsDeleteCar.car_num)
        async def car_num(message: types.Message, state: FSMContext):

            async with state.proxy() as data:
                data['car_num'] = message.text
                car_num = data['car_num']
                car_num = car_num.upper()
                car_num = car_num.replace('A', 'А').replace('B', 'В').replace('E', 'Е').replace('K', 'К').replace('M', 'М').replace('H', 'Н').replace('O', 'О').replace('P', 'Р').replace('C', 'С').replace('T', 'Т').replace('Y', 'У').replace('X', 'Х').replace('S', 'C').replace('Y', 'У').replace('RUS', '')
                
                user_id = message.from_user.id
                deleted = await deleted_num_car(user_id,car_num)
                if deleted:
                    await message.answer('Номер удален', reply_markup=markup)
                    await state.finish()
                else:
                    await message.answer('Номер не найден', reply_markup=markup)
                    await state.finish()
            
                await state.finish()
                


    async def deleted_address(self, message:types.Message):

        class AplicationsDeleteAddress(StatesGroup):
            address = State()



        await AplicationsDeleteAddress.address.set()
        user_id = message.from_user.id
        await bot.send_message(chat_id=message.chat.id, text='Введите id вашего адреса которую хотите удалить', reply_markup=addres_kb('address_keyboard', user_id=user_id))

        @dp.message_handler(state=AplicationsDeleteAddress.address)
        async def address(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['address'] = message.text
                address = data['address']
                user_id = message.from_user.id
                deleted = await deleted_address(address, user_id)
                if deleted:
                    await message.answer('Адрес удален', reply_markup=get_keyboard('user'))
                    await state.finish()
                else:
                    await message.answer('Адрес не найден', reply_markup=get_keyboard('user'))
                    await state.finish()

                await state.finish()

    