from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from bot.utils.const_functions import GetImage, Mode
from bot.data.bot_text import BotText
from bot.database.api import DBApi

import logging as logger
import configparser
import os

__version__ = "0.1"

# -----------------------------PROJECT PATH-----------------------------
PATH = os.getcwd()

DB_PATH = os.path.join(PATH, "bot", "database", "data.db")
SETTINGS_PATH = os.path.join(PATH, "settings.ini")
# -------------------------------SETTINGS-------------------------------
BOT_CONFIG = configparser.ConfigParser()
BOT_CONFIG.read(SETTINGS_PATH)
BOT_CONFIG = BOT_CONFIG["SETTINGS"]

TOKEN = BOT_CONFIG["token"]
ADMIN_ID = BOT_CONFIG["admin_id"].strip().split(",")
BALANCE_FOR_REFERRAL = float(BOT_CONFIG["balance_for_referral"])
BALANCE_FOR_CLICKING = float(BOT_CONFIG["balance_for_clicking"])
MIN_WITHDRAW = float(BOT_CONFIG["min_withdraw"])
REDIRECT_LINK = BOT_CONFIG["redirect_link"]
FEEDBACK_LINK = BOT_CONFIG["feedback_link"]
MIN_REFERRAL_WITHDRAW = float(BOT_CONFIG["min_referral_withdraw"])

BOT_USERNAME = BOT_CONFIG["bot_username"]
ADMIN_ID = list(map(int, ADMIN_ID))
# -------------------------------AIOGRAM--------------------------------
bot = Bot(
	token=TOKEN,
	default=DefaultBotProperties(
		parse_mode="HTML"
	)
)
dp = Dispatcher(storage=MemoryStorage())
# -------------------------------LOGGING--------------------------------
logger.basicConfig(level=logger.INFO)
# -------------------------------FUNCTION-------------------------------
db = DBApi(DB_PATH)
TEXT = BotText()
get_image = GetImage(Mode.PATH)  # Изображения будут браться из папки ../images

# get_image = GetImage(Mode.DICT,
# 					 {"welcome": "URL | photoID | None",
# 					  "withdraw": "URL | photoID | None",
# 					  "promocode": "URL | photoID | None",
# 					  "admin_menu": "URL | photoID | None",
# 					  "tasks": "URL | photoID | None",
# 					  "profile": "URL | photoID | None"}
# 					 )
# ----------------------------------------------------------------------
