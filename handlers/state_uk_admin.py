import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.keyboard import get_keyboard, addres_kb
from handlers.base import *
from handlers.base_uk_admin import *
from config import url, headers
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# создаем экземпляр планировщика задач
scheduler = AsyncIOScheduler()

# запускаем планировщик задач
scheduler.start()



class HandleMessageUkState:
    def __init__(self, message: types.Message):
        self.message = message

        

    async def mailing_address_state(self, message: types.Message):
        class MailingAddressState(StatesGroup):
            address = State()
            message_text= State()
            date = State()
            
        user_id = message.from_user.id
        await message.answer('Выберете адресс по которому хотите отправить сообщение', reply_markup=addres_kb('list_address_uk', user_id))
        await MailingAddressState.address.set()

        @dp.message_handler(state=MailingAddressState.address)
        async def city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['address'] = message.text
                user_id = message.from_user.id
                street = data['address']
                street_parts = street.split(',')
                street_name = street_parts[0] 
                house_number = street_parts[1]
                msg_id = await message_street(user_id,street_name,house_number)
                if msg_id:
                    await message.answer('Введите сообщение которое хотите отправить', reply_markup=get_keyboard('uk_template'))
                    await MailingAddressState.next()
                else:
                    await message.answer('По данному адресу нет пользователей или же у вас нет доступа на этот адрес', reply_markup=get_keyboard('uk'))
                    await state.finish()

            
        @dp.message_handler(state=MailingAddressState.message_text)
        async def message_text(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['message_text'] = message.text
                street = data['address']
                street_parts = street.split(',')
                street_name = street_parts[0] 
                house_number = street_parts[1]
                message_text = data['message_text']
                template = await get_template_text(message_text)
                template = ''.join(template)
                data['message_text'] = template

                msg_id = await get_addres_uk(street_name, house_number)
                user_id = message.from_user.id
                response = await get_uk_nick(user_id)
                nick = ''.join(response)
                text = f'Сообщение от УК {nick}\n\nДля адреса: {street}\n\nСообщение: {template}'

                # Запрашиваем дату отправки сообщения у пользователя
                await message.answer('Введите дату отправки сообщения (в формате "ГГГГ-MM-ДД ЧЧ:ММ")', reply_markup=get_keyboard('back_uk'))
                await MailingAddressState.next()

        @dp.message_handler(state=MailingAddressState.date)
        async def message_date(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['date'] = message.text
                street = data['address']
                street_parts = street.split(',')
                street_name = street_parts[0] 
                house_number = street_parts[1]
                message_text = data['message_text']
                user_id = message.from_user.id
                response = await get_uk_nick(user_id)
                nick = ''.join(response)
                text = f'Сообщение от УК {nick}\n\nДля адреса: {street}\n\nСообщение: {message_text}'

                # Добавляем задачу в планировщик задач
                try:
                    date_time = datetime.strptime(data['date'], '%Y-%m-%d %H:%M')
                except ValueError:
                    await message.answer('Неправильный формат даты, введите дату в формате\n"ГГГГ-MM-ДД ЧЧ:ММ"', reply_markup=get_keyboard('back_uk'))
                    return

                # Проверяем, что заданная дата в будущем
                if date_time < datetime.now():
                    await message.answer('Вы указали прошедшую дату, введите дату в будущем', reply_markup=get_keyboard('back_uk'))
                    return

                # определим переменную send_message
                
                msg_id = await get_addres_uk(street_name, house_number)
                for users_id in msg_id:
                    
                    job = scheduler.add_job(
                        bot.send_message, 
                        trigger='date',
                        next_run_time=date_time,
                        args=[users_id, text],
                    )
                


                await message.answer(f'Сообщение будет отправлено {data["date"]}', reply_markup = get_keyboard('uk'))
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
