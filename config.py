from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage    
from langdetect import detect


bot = Bot(token = 'Ваш токен')
dp = Dispatcher(bot, storage = MemoryStorage())

def check_language(text):
    try:
        language = detect(text)
        if language == 'ru':
            return True
        else:
            return False
    except:
        return False

def check_language_english(text):
    try:
        language = detect(text)
        if language == 'en':
            return True
        else:
            return False
    except:
        return False

def check_alpha_only(text):
    if text.isalpha():
        return True
    else:
        return False