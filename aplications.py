from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import dp, bot , check_language, check_alpha_only
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class Applications:
    def __init__(self, message: types.Message):
        self.bot = bot
        self.message = message



    async def aplications_people(self, message:types.Message):

        class AplicationsFSM(StatesGroup):
            name = State()
            date = State()
            phone = State()
            account = State()
            password = State()
            branch = State()


        await AplicationsFSM.name.set()
        await message.answer('Отлично сейчас мы заполним небольшую анкету\nВведите имя и фамилию на русском и без цифр')


        @dp.message_handler(state=AplicationsFSM.name)
        async def name(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                if check_language(message.text):
                    data['name'] = message.text
                    await AplicationsFSM.next()
                
                    await message.answer('Введите дату рождения! в таком формате 01.01.2002')
    
                else:
                    await message.answer('Введите корректное имя и фамилию!')
                    return

        @dp.message_handler(state=AplicationsFSM.date)
        async def date(message: types.Message, state: FSMContext):

            async with state.proxy() as data:

                data['date'] = message.text
            await AplicationsFSM.next()
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("Отправить номер телефона📱", request_contact=True))
            await message.answer('Отправьте ваш номер телефона!',reply_markup=keyboard)

        @dp.message_handler(content_types=types.ContentTypes.CONTACT,state=AplicationsFSM.phone)
        async def phone(message: types.Contact, state: FSMContext):

            async with state.proxy() as data:
                data['phone'] = message.contact.phone_number
            await AplicationsFSM.next()
            await message.answer('Введите название аккаунта без цифр и на английском языке', reply_markup= ReplyKeyboardRemove())

        @dp.message_handler(state=AplicationsFSM.account)
        async def account(message: types.Message, state: FSMContext):
            
            
            async with state.proxy() as data:
                # if check_language_english(message.text):
                #     print('[p[]]')
                    # if check_alpha_only(message.text):
                    data['account'] = message.text
                    await AplicationsFSM.next()
                    await message.answer('Введите пароль для вашего аккаунта!')
                    # else:
                    #     await message.answer('Введите корректное название аккаунта без цифр!')
                    #     return
                # else:
                #     await message.answer('Введите корректное название аккаунта на английском языке!')
                #     return
        
        @dp.message_handler(state=AplicationsFSM.password)
        async def password(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['password'] = message.text
            await AplicationsFSM.next()
            await message.answer('Введите филиал где вы обычно играете!')

        @dp.message_handler(state=AplicationsFSM.branch)
        async def branch(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['branch'] = message.text
            await AplicationsFSM.next()
            data = await state.get_data()
            msg = (f'Имя и фамилия: {data["name"]}\nДата рождения: {data["date"]}\nНомер телефона: {data["phone"]}\nНазвание аккаунта: {data["account"]}\nПароль для аккаунта: {data["password"]}\nФилиал: {data["branch"]}')
            
            await state.finish()

            await bot.send_message(chat_id = 5954454881, text = msg)
            await message.answer(text = msg)
            await message.answer('Ваш аккаунт будет открыт в течении 24 часов.\nБудь фанатом вместе с нами!')


            






