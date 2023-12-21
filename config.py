import re
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage    

url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address'
token = '902129e7249af3da7aa46056dd2211f02ca19f13'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Token 902129e7249af3da7aa46056dd2211f02ca19f13'
}



bot = Bot(token = '2140069643:AAFZTCK6sI9TW5dEip6BkqYcWyDGXfRmnpA')
dp = Dispatcher(bot, storage = MemoryStorage())


rest_api = 'http://193.233.233.66:8000/'
