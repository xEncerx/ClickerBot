from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from config.database.data import DataBase
import os

db = DataBase(os.path.join(os.getcwd(), "config", "database", "data.db"))

# _________________________Настройка Бота____________________________
admin_id = [123, 63441]
token = "5df29:AsdfgM"
# ___________________________________________________________________

# ___________________________________________________________________
balance_for_referral = 20
balance_for_click = 0.5
money_name = "голды"
bot_username = "UserName"
min_withdraw = 200
redirect_link = "https://ya.ru"
min_referrer_withdraw = 1
feedback_link = ""
# ___________________________________________________________________
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
