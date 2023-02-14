from aiogram import types 
from aiogram.types import MediaGroup
from keyboard import get_keyboard
from config import bot
from aplications import Applications
import asyncio

async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == 'price':
        
        message = ('Выберите филлиал')
        msg = await bot.send_message(callback_query.message.chat.id, message, reply_markup=get_keyboard('branches'))
        await asyncio.sleep(10)
        await bot.delete_message(callback_query.message.chat.id, msg.message_id)

    elif data == 'contact':
        await bot.send_message(callback_query.message.chat.id, 'Контакты наших филлиалов.\n\nБезымянная 37/2 - 022240404 PC - 0555404404 PS\n\nАуэзова 3В - 0505404404 PC и PS\n\nКиевская 190 - 0706 404 404 PC и PS\n\nАйтматова 29 - 0779404404 PC')
    elif data == 'adress':
        await bot.send_message(callback_query.message.chat.id, 'Выберите филлиал', reply_markup=get_keyboard('adres'))
    
    elif data == 'card':
        if callback_query.message.chat.type == 'private':
            applications = Applications(callback_query.message)
            await applications.aplications_people(callback_query.message)
        else:
            await bot.send_message(callback_query.message.chat.id, 'Для оформления карты обратитесь в личные сообщения боту')


    elif data == 'alamedin':
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
        media = MediaGroup()
        media.attach_photo(open("images/alamedin_comfort.png", "rb"))
        media.attach_photo(open("images/alamedin_vip.png", "rb"))
        media.attach_photo(open("images/alamedin_ps.png", "rb"))
        await bot.send_media_group(callback_query.message.chat.id, media)


    elif data == 'bezymyan':
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
        media = MediaGroup()
        media.attach_photo(open("images/bezymayn_comfort.png", "rb"))
        media.attach_photo(open("images/bezymayn_vip.png", "rb"))
        media.attach_photo(open("images/bezymayn_ps.png", "rb"))
        media.attach_photo(open("images/bezymayn_ps_vip.png", "rb"))

        await bot.send_media_group(callback_query.message.chat.id, media)

    elif data == 'aitmatov':
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
        media = MediaGroup()
        media.attach_photo(open("images/aitmatov.jpg", "rb"))
        media.attach_photo(open("images/aitmatov_vip.jpg", "rb"))

        await bot.send_media_group(callback_query.message.chat.id, media)

    elif data == 'kiev':
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
        media = MediaGroup()
        media.attach_photo(open("images/kiev_comfort.png", "rb"))
        media.attach_photo(open("images/kiev_vip.jpg", "rb"))
        media.attach_photo(open("images/kiev_ps.png", "rb"))
        media.attach_photo(open("images/kiev_ps_vip.png", "rb"))
        await bot.send_media_group(callback_query.message.chat.id, media)
