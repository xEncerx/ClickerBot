from aiogram.enums.chat_action import ChatAction
from aiogram import types, Router, F

from bot.data.config import TEXT, db, bot
from bot.filters import IsAdmin
import bot.markups as nav

from datetime import datetime, timedelta
from typing import Optional
import asyncio

router = Router()
semaphore = asyncio.Semaphore(200)

# Проверяем блокировку бота
async def send_chat_action(user_id) -> Optional[int]:
	try:
		async with semaphore:
			await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
			await asyncio.sleep(0.08)
		return None
	except:
		return user_id

# Считаем сколько пользователй заблокировало бота
async def get_blocked(user_ids: list[int]) -> int:
	tasks = [
		asyncio.ensure_future(send_chat_action(user_id)) for user_id in user_ids
	]
	blocked_users = await asyncio.gather(*tasks)
	count_block = len(
		[
			user_id for user_id in blocked_users if user_id
		]
	)
	return count_block

# Получаем данные о статистике бота
async def statistic_info() -> dict:
	data = await db.client.get_all(("user_id", "register_time"))
	now = datetime.now()
	count_all = len(data)

	result = {
		"hour": 0,
		"day": 0,
		"week": 0,
		"month": 0,
		"block": 0,
		"all": count_all
	}

	for user_id, time in data:
		time = datetime.strptime(time, '%H:%M %d.%m.%Y')
		time_difference = now - time
		if time_difference <= timedelta(hours=1):
			result['hour'] += 1
		if time_difference <= timedelta(days=1):
			result['day'] += 1
		if time_difference <= timedelta(weeks=1):
			result['week'] += 1
		if time_difference <= timedelta(days=30):
			result['month'] += 1

	result["block"] = await get_blocked(
		[user_id for user_id, _ in data]
	)

	return result

# Ф-ция отправки статистики пользователю
async def send_statistic(call: types.CallbackQuery) -> None:
	await call.answer("⚠️ Вывод статистики может занять немного времени, если в боте много человек!", show_alert=True)
	data = await statistic_info()

	await bot.send_message(call.from_user.id,
					   TEXT.admin.statistic.format(hour=data.get("hour"),
												   day=data.get("day"),
												   week=data.get("week"),
												   month=data.get("month"),
												   block=data.get("block"),
												   all=data.get("all")),
					   reply_markup=nav.back_button("admin_menu"))

# Кнопка - Статистика
@router.callback_query(IsAdmin(), F.data == "statistic")
async def get_statistic(call: types.CallbackQuery):
	asyncio.create_task(send_statistic(call))
