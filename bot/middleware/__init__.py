# - *- coding: utf- 8 - *-

from aiogram import Dispatcher
from bot.middleware.throttling_middleware import ThrottlingMiddleware

def setup_middleware(dp: Dispatcher) -> None:
	dp.message.middleware(ThrottlingMiddleware())