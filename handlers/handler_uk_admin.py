from aiogram import types 
from keyboards.keyboard import get_keyboard
from config import bot
from handlers.aplications import Applications
from handlers.state_uk_admin import HandleMessageUkState,HandleMessageAdminState
import asyncio
from config import dp, bot
from handlers.base_uk_admin import get_address_list
from aiogram.dispatcher import FSMContext





class HandleMessageUK:
    def __init__(self, message: types.Message):
        self.message = message


    async def mailing_address_handle(self, message: types.Message):
        handle_message_uk_state = HandleMessageUkState(message)
        await handle_message_uk_state.mailing_address_state(message)

        
    
    async def mailing_house_number(self, message: types.Message):
        handle_message_uk_state = HandleMessageUkState(message)
        await handle_message_uk_state.mailing_house_number_state(message)

    
    async def mailing_car_number_uk(self, message: types.Message):
        message_car = Applications(message)
        await message_car.message_car_num(message)

    
    async def list_address_uk(self, message: types.Message):
        user_id = message.from_user.id
        address = await get_address_list(user_id)
        if address:
            message_text = 'Ваши адреса, по которым вы можете отправлять рассылку:\n\n'
            for num in address:
                for addr in num:
                    city = addr['city']
                    street = addr['address']
                    house = addr['house_number']
                    message_text += f"{city}, {street}, номер дома {house}\n\n"
                
            await bot.send_message(chat_id=message.from_user.id, text=message_text, reply_markup=get_keyboard('uk'))

    async def back_uk(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.answer('Главное меню', reply_markup=get_keyboard('uk'))

        else:
            await message.answer('Главное меню', reply_markup=get_keyboard('uk'))



class HandleMessageAdmin:
    def __init__(self, message: types.Message):
        self.message = message

    async def mailing_address_admin(self, message: types.Message):
        handle_message_admin_state = HandleMessageAdminState(message)
        await handle_message_admin_state.mailing_address_state_admin(message)

    async def mailing_house_number_admin(self, message: types.Message):
        handle_message_admin_state = HandleMessageAdminState(message)
        await handle_message_admin_state.mailing_house_number_state_admin(message)

    async def mailing_car_number_admin(self, message: types.Message):
        handle_message_admin_state = Applications(message)
        await handle_message_admin_state.message_car_num(message)

    async def list_address_admin(self, message: types.Message):
        pass

    async def mailing_address_all_user(self, message: types.Message):
        handle_message_admin_state = HandleMessageAdminState(message)
        await handle_message_admin_state.mailing_all_user(message)






    

