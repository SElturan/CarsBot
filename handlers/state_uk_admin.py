import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.keyboard import get_keyboard, addres_kb,time_uk
from handlers.base import *
from handlers.base_uk_admin import *
from config import url, headers
from datetime import datetime


class HandleMessageUkState:
    def __init__(self, message: types.Message):
        self.message = message

        

    async def mailing_address_state(self, message: types.Message, state='*'):

        class MailingAddressState(StatesGroup):
            address = State()
            message_text = State()
            start_time = State()
            end_time = State()
            
        user_id = message.from_user.id
        try:
            await message.answer('Выберете адресс по которому хотите отправить сообщение', reply_markup=addres_kb('list_address_uk', user_id))
            await MailingAddressState.address.set()
        except IndexError:
            await message.answer('У вас нет адресов', reply_markup=get_keyboard('uk'))
            
            

        

        @dp.message_handler(state=MailingAddressState.address)
        async def city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['address'] = message.text
                user_id = message.from_user.id
                street = data['address']
                try:

                    street_parts = street.split(',')
                    street_name = street_parts[0] 
                    house_number = street_parts[1]
                    msg_id = await message_street(user_id,street_name,house_number)
                    if msg_id:
                        await message.answer('Выберите шаблон который хотите отправить', reply_markup=get_keyboard('uk_template'))
                        await MailingAddressState.next()
                    else:
                        await message.answer('По данному адресу нет пользователей или же у вас нет доступа на этот адрес', reply_markup=get_keyboard('uk'))
                        await state.finish()
                except IndexError:
                    await message.answer('У вас нет адресов', reply_markup=get_keyboard('uk'))

            
        @dp.message_handler(state=MailingAddressState.message_text)
        async def message_texts(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['message_text'] = message.text
                message_text =  data['message_text']
         
                templates = await get_template_text(message_text)
                if templates:
                    await message.answer('Выберите время начало', reply_markup=time_uk('time'))
                    await MailingAddressState.next()
                else:
                    await message.answer('Такого шаблона нет!', reply_markup=get_keyboard('uk'))
                    await state.finish()
           

        @dp.message_handler(state=MailingAddressState.start_time)
        async def start_time_func(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['start_time'] = message.text

                await message.answer('Выберите время окончания', reply_markup=time_uk('time'))
                await MailingAddressState.next()
        
        @dp.message_handler(state=MailingAddressState.end_time)
        async def start_time_func(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['end_time'] = message.text

                message_text = data['message_text']
                street = data['address']
                start_time = data['start_time']
                end_time = data['end_time']

                street_parts = street.split(',')
                street_name, house_number = street_parts[:2]
                templates = await get_template_text(message_text)
                for template in templates:
                    templates = template
                user_id = message.from_user.id
                nick = await get_uk_nick(user_id)
             
                if nick:
                    nick = "".join(nick)
                else:
                    nick = message.from_user.first_name
                current_date = datetime.now()

                # Форматирование даты в формате "день-месяц-год"
                formatted_date = current_date.strftime("%d-%m-%Y")
                
                text = f'Сообщение от УК {nick}\n\nУважаемые жильцы, по адресу {street}, {formatted_date} в период с {start_time} по {end_time} {template}'
              

                msg_id = await get_addres_uk(street_name, house_number)
                for users_id in msg_id:
                    try:

                        await bot.send_message(chat_id=users_id, text=text)
                    except Exception:
                        continue
                await bot.send_message(chat_id=message.from_user.id, text='Сообщение отправлено',reply_markup = get_keyboard('uk'))

                await state.finish()


            



    async def mailing_house_number_state(self,message: types.Message):
        class MailingHouseNumberState(StatesGroup):
            house_number = State()
            message_text= State()
        user_id = message.from_user.id
        await message.answer('Выберете номер дома по которому хотите отправить сообщение', reply_markup=addres_kb('list_house_number_uk', user_id))
        await MailingHouseNumberState.house_number.set()

        @dp.message_handler(state=MailingHouseNumberState.house_number)
        async def city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['house_number'] = message.text
                user_id = message.from_user.id
                house_number = data['house_number']
                msg_id = await message_house(user_id,house_number)
                if msg_id:
                    await message.answer('Введите сообщение которое хотите отправить', reply_markup=get_keyboard('uk_template'))
                    await MailingHouseNumberState.next()
                else:
                    await message.answer('По данному адресу нет пользователей или же у вас нет доступа на этот адрес', reply_markup=get_keyboard('uk_malling_list'))
                    await state.finish()

        
        @dp.message_handler(state=MailingHouseNumberState.message_text)
        async def message_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['message_text'] = message.text
                house_number = data['house_number']
                message_text = data['message_text']
                user_id = message.from_user.id
                nick = await get_uk_nick(user_id)
                text = f'Рассылка от УК {nick}\nДля дома №{house_number}\nОжидается: {message_text}\nТребуется убрать машины'
                msg_id = await get_house_uk(house_number)
                for user_id in msg_id:
                    await bot.send_message(chat_id=user_id, text=text)
                await message.answer('Сообщение отправлено', reply_markup=get_keyboard('uk'))
                await state.finish()

            



class HandleMessageAdminState:
    def __init__(self, message: types.Message):
        self.message = message


    
    async def mailing_address_state_admin(self, message: types.Message):
        class MailingAddressState(StatesGroup):
            address = State()
            message_text= State()
        await message.answer('Введите улицу по которому хотите отправить сообщение', reply_markup=ReplyKeyboardRemove())
        await MailingAddressState.address.set()

        @dp.message_handler(state=MailingAddressState.address)
        async def city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['address'] = message.text
                street = data['address']
                msg_id = await get_addres_uk(street)
                if msg_id:
                    await message.answer('Введите сообщение которое хотите отправить')
                    await MailingAddressState.next()
                else:
                    await message.answer('По данному адресу нет пользователей ', reply_markup=get_keyboard('admin'))
                    await state.finish()

        
        @dp.message_handler(state=MailingAddressState.message_text)
        async def message_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['message_text'] = message.text
                street = data['address']
                message_text = data['message_text']
                text = f'Рассылка от администратора {message.from_user.id}\n\nДля адреса:{street}\n\nСообщение: {message_text}'
                msg_id = await get_addres_uk(street)
                for user_id in msg_id:
                    await bot.send_message(chat_id=user_id, text=text)
                await message.answer('Сообщение отправлено', reply_markup=get_keyboard('admin_malling_list'))
                await state.finish()


    async def mailing_house_number_state_admin(self,message: types.Message):
        class MailingHouseNumberState(StatesGroup):
            house_number = State()
            message_text= State()

        await message.answer('Введите номер дома по которому хотите отправить сообщение', reply_markup=ReplyKeyboardRemove())
        await MailingHouseNumberState.house_number.set()

        @dp.message_handler(state=MailingHouseNumberState.house_number)
        async def city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['house_number'] = message.text
                house_number = data['house_number']
                msg_id = await get_addres_uk(house_number)
                
                if msg_id:
                    await message.answer('Введите сообщение которое хотите отправить')
                    await MailingHouseNumberState.next()
                else:
                    await message.answer('По данному адресу нет пользователей ', reply_markup=get_keyboard('admin_malling_list'))
                    await state.finish()

        
        @dp.message_handler(state=MailingHouseNumberState.message_text)
        async def message_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['message_text'] = message.text
                house_number = data['house_number']
                message_text = data['message_text']
                msg_id = await get_house_uk(house_number)
                text = f'Рассылка от администратора {message.from_user.id}\n\nДля дома№{house_number}\n\nСообщение: {message_text}'
                for user_id in msg_id:
                    await bot.send_message(chat_id=user_id, text=text)
                await message.answer('Сообщение отправлено', reply_markup=get_keyboard('admin'))
                await state.finish()


    async def mailing_all_user(self, message: types.Message):
        class MailingAllUser(StatesGroup):
            message_text= State()

        await message.answer('Введите сообщение которое хотите отправить', reply_markup=ReplyKeyboardRemove())
        await MailingAllUser.message_text.set()

        @dp.message_handler(state=MailingAllUser.message_text)
        async def message_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['message_text'] = message.text
                message_text = data['message_text']
                msg_id = await get_all_user()
                text = f'Рассылка от администратора {message.from_user.id}\n\nСообщение: {message_text}'
                for user_id in msg_id:
                    await bot.send_message(chat_id=user_id, text=text)
                await message.answer('Сообщение отправлено', reply_markup=get_keyboard('admin'))
                await state.finish()
