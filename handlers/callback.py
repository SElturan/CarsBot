from aiogram import types 
from keyboards.keyboard import get_keyboard
from config import bot
from handlers.aplications import Applications
import asyncio
from config import dp, bot
from aiogram import types
from .base import get_number_car, get_address, is_user_registered
from aiogram.dispatcher import FSMContext



class HandleMessage:
    def __init__(self, message: types.Message):
        # dp.register_callback_query_handler(self.callback, lambda c: c.data in ['add_address','added_num', 'message_car', 'list_number','list_address','back_user','add_house_num','delete_num','delete_house_num', 'delete_address'])

        self.message = message




    async def list_number(self, message: types.Message):
        user_id = message.from_user.id
        chekc_user = await is_user_registered(user_id)
       
        if chekc_user[0]['role'] == 'UK':
            markup=get_keyboard('uk')

        elif chekc_user[0]['role'] == 'admin':
            markup=get_keyboard('admin')
        
        else:
            markup=get_keyboard('add_num_car')
    
        car_num = await get_number_car(message.from_user.id)
        if car_num:
            message_text = 'Ваши номера автомобилей\n\n'
            for num in car_num:
                message_text += f'{num}\n\n'
            await bot.send_message(chat_id=message.from_user.id, text=message_text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Вы еще не добавили номер автомобиля', reply_markup=markup)

    async def list_address(self, message: types.Message):
        user_id = message.from_user.id
        chekc_user = await is_user_registered(user_id)
       
        if chekc_user[0]['role'] == 'UK':
            markup=get_keyboard('uk')

        elif chekc_user[0]['role'] == 'admin':
            markup=get_keyboard('admin')
        
        else:
            markup=get_keyboard('add/delete_address', flag=False)

        user_id = message.from_user.id
        address = await get_address(user_id)
        if address:
            message_text = 'Ваши адреса по которому будете получать рассылку\n\n'
            for num in address:
                city = num['city']
                street = num['address']
                house = num['house_number']
                id_adress = num['id']
                message_text += f"ID {id_adress}, {city}, {street}, {house}\n\n"
                
            await bot.send_message(chat_id=message.from_user.id, text=message_text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=message.from_user.id,  text='Вы еще не добавили адрес', reply_markup=markup)

    async def add_house_num(self, message: types.Message):
        add_house_num = Applications(message)
        await add_house_num.added_house(message)

    async def message_car(self, message: types.Message):
        message_car = Applications(message)
        await message_car.message_car_num(message)

    async def add_address(self, message: types.Message):
        add_address = Applications(message)
        await add_address.added_address(message)

    
    async def add_num_cars(self, message: types.Message):

        add_num_car = Applications(message)
        await add_num_car.add_num_cars(message)
       

    async def delete_num(self, message: types.Message):
        delete_num = Applications(message)
        await delete_num.deleted_car_num(message)
    
    async def delete_address(self, message: types.Message):
        delete_address = Applications(message)
        await delete_address.deleted_address(message)



    async def back(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()

        # Проверяем, есть ли текущее состояние
        if current_state is not None:
            # Отключаем все машины состояний
            await state.finish()
            await bot.send_message(chat_id=message.chat.id, text='Главное меню\n\nВыберите действие', reply_markup=get_keyboard('user'))

        else:
            await bot.send_message(chat_id=message.chat.id, text='Главное меню\n\nВыберите действие', reply_markup=get_keyboard('user'))

    




    
        

    

    

        


    

    
    
