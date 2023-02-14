
from config import bot, dp 
from aiogram import executor
from keyboard import get_keyboard
from aiogram.types import Message
from callback import handle_callback
from aplications import Applications
import asyncio
from messages import joined_messages, help_messages

class BotMain:
    def __init__(self):
        dp.register_message_handler(self.handle_new_member, content_types=["new_chat_members"])
        dp.register_message_handler(self.handle_commands, commands=['start','help','open'])
        dp.register_callback_query_handler(self.callback, lambda c: c.data in ['price', 'contact', 'adress', 'filial', 'card', 'alamedin', 'bezymyan', 'aitmatov', 'kiev' ])
        dp.register_message_handler(self.handle_message)
    
    async def handle_new_member(self, message: Message):
        user = message.from_user
        if user.username:
            name = f"@{user.username}"
        
        else:
            name = user.first_name

        text = joined_messages(name)
        await bot.send_message(chat_id=message.chat.id, text = text, reply_markup=get_keyboard('joined'))
 
    async def handle_commands(self, message: Message):
        user = message.from_user
        if user.username:
            name = f"@{user.username}"
        
        else:
            name = user.first_name
        if message.text == '/start':
            if message.chat.type == 'private':
                text = joined_messages(name)
                await bot.send_message(message.chat.id,text=text, reply_markup=get_keyboard('start'))

            else:
                text = joined_messages(name)
                msg = await bot.send_message(message.chat.id,text=text, reply_markup=get_keyboard('joined'))

                await asyncio.sleep(30)
                await bot.delete_message(chat_id=message.chat.id, message_id= msg.message_id)

        
        elif message.text == '/help':
            text_help = help_messages()
            await bot.send_message(message.chat.id, text=text_help)
        
        elif message.text == '/open':
            if message.chat.type == 'private':
                applications = Applications(message)
                await applications.aplications_people(message)

            else:
                await bot.send_message(chat_id=message.chat.id, text = "Команда работает только в личном чате!!!")

    async def handle_message(self, message: Message):
        text = message.text.lower()
        text = message.text.lower()
        messages = ["как открыть карта", " как открыть виртуальный аккаунт", "как открыть карту", "как открыть виртуальный аккаунт", "как открыть аккаунт", "виртуальный аккаунт бесплатный", "сколько стоить открыть карту", "сколько стоить открыть аккаунт", "как открыть аккаунт в фанате"]
    
        for message_to_check in messages:
            if message_to_check in text:
                text_help = help_messages()
                await bot.send_message(chat_id=message.chat.id, text=text_help)
        




    async def callback(self, call):
        await handle_callback(call)
            




if __name__ == '__main__':
    BotMain()
    executor.start_polling(dp, skip_updates=True)