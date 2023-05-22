
from config import bot, dp 
from aiogram import executor
from keyboards.keyboard import get_keyboard
from aiogram.types import Message
from handlers.base import is_user_registered, is_address_registered
from handlers.aplications import Applications
from handlers.callback import HandleMessage
from handlers.handler_uk_admin import HandleMessageUK, HandleMessageAdmin
from aiogram.dispatcher import FSMContext



class BotMain:
    def __init__(self):
        dp.register_message_handler(self.handle_commands, commands=['start','help','open'])
        dp.register_message_handler(self.handle_message,state='*', text = ['📨 Отправить сообщение', '🚘 Список номеров', '🏙 Список адресов', '📍 Тех.поддержка', 'Есть автомобиль', 'Удалить номер', 'Добавить номер', 'Назад', 'Добавить адрес',  'Удалить адрес', 'Назад', 'Я пешеход'])
        # dp.register_message_handler(self.back_user, state='*', text='Назад')
        dp.register_message_handler(self.handle_message_uk,state='*', text = ['📨 Отправить рассылку', '🏙 Список адресов УК',  'По адресу 🌅' , 'По всем адресам 🌅', 'По номеру авто 🚘', 'Назад 🔙',  ])
        dp.register_message_handler(self.handle_message_admin, text = ['Отправить рассылку 📨', '🏙 Список адресов УК',  '🌅 По адресу' , '🏚 По номеру дома','Всем пользователям', '🚘 По номеру авто', 'Назад ◀',  ])


        


    async def handle_commands(self, message: Message):
        if message.text == '/start':
            user_id = message.from_user.id
            chekc_user = await is_user_registered(user_id)
            
            if chekc_user:
                if chekc_user[0]['role'] == 'UK':
                    await message.answer('Вы  зарегистрированы как УК', reply_markup=get_keyboard('uk'))

                elif chekc_user[0]['role'] == 'admin':
                    await message.answer('Вы зарегистрированы как администратор', reply_markup=get_keyboard('admin'))
                
                else:
                    await message.answer('Вы зарегистрированы как пользователь', reply_markup=get_keyboard('user'))
            else:
                await message.answer('Вы не зарегистрированы\nПройдите регистрацию', reply_markup=get_keyboard('start'))


            




 


    async def handle_message(self, message: Message, state: FSMContext):
        handle_message = HandleMessage(message)

        if message.text == 'Я пешеход':
            applications = Applications(message)
            await applications.aplications_people(message)
            
        elif message.text == 'Есть автомобиль':
            applications = Applications(message)
            await applications.aplications_car(message)
            

    
        elif message.text == '📨 Отправить сообщение':
            
            await handle_message.message_car(message)

        elif message.text == '🚘 Список номеров':
            await handle_message.list_number(message)


        elif message.text == '🏙 Список адресов':
            await handle_message.list_address(message)


        elif message.text == '📍 Тех.поддержка':
            await message.answer('Тех.поддержка')

        elif message.text == 'Удалить номер':
           await handle_message.delete_num(message)

        elif message.text == 'Назад':

            current_state = await state.get_state()

            # Проверяем, есть ли текущее состояние
            if current_state is not None:
                # Отключаем все машины состояний
                await state.finish()
                await bot.send_message(chat_id=message.chat.id, text='Главное меню\n\nВыберите действие', reply_markup=get_keyboard('user'))

            else:
                await bot.send_message(chat_id=message.chat.id, text='Главное меню\n\nВыберите действие', reply_markup=get_keyboard('user'))

    

        elif message.text == 'Добавить номер':
            await handle_message.add_num_cars(message)

        elif message.text == 'Добавить адрес':
            await handle_message.add_address(message)

        elif message.text == 'Добавить № дома':
            await handle_message.add_house_num(message)

        elif message.text == 'Удалить адрес':
            await handle_message.delete_address(message)

        else:
            await message.answer('Введите команду')


    async def handle_message_uk(self, message: Message, state: FSMContext):
        handle_message = HandleMessageUK(message)

        if message.text == '📨 Отправить рассылку':
            await message.answer('Выберите тип рассылки!', reply_markup=get_keyboard('uk_malling_list'))
            
        elif message.text == '🏙 Список адресов УК':
            await handle_message.list_address_uk(message)

        elif message.text == 'По адресу 🌅':
            await handle_message.mailing_address_handle(message)


        elif message.text == 'По всем адресам 🌅':
            # await handle_message.mailing_house_number(message)
            await message.answer('КНопка пока не работает, но там логика точно такая же как и рассылка по адресу, только по всем адресам')

        elif message.text == 'По номеру авто 🚘':
            await handle_message.mailing_car_number_uk(message)

        elif message.text == 'Назад 🔙':
            await handle_message.back_uk(message, state)
        else:
            await message.answer('Введите команду')
        

    
    async def handle_message_admin(self, message: Message):
        handle_message = HandleMessageAdmin(message)

        if message.text == 'Отправить рассылку 📨':
            await message.answer('Выберите тип рассылки!', reply_markup=get_keyboard('admin_malling_list'))

        elif message.text == '🌅 По адресу':
            await handle_message.mailing_address_admin(message)

        elif message.text == '🚘 По номеру авто':
            await handle_message.mailing_car_number_admin(message)

        elif message.text == '🏚 По номеру дома':
            await handle_message.mailing_house_number_admin(message)
        
        elif message.text == 'Всем пользователям':
            await handle_message.mailing_address_all_user(message)

        elif message.text == 'Назад ◀':
            await message.answer('Главное меню!\n\nВыберите действие', reply_markup=get_keyboard('admin'))

      
        else:
            await message.answer('Введите команду')
            




if __name__ == '__main__':
    BotMain()
    executor.start_polling(dp, skip_updates=True)