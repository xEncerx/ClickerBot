from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, types, F

from bot.data.config import TEXT, db, bot
from bot.utils.message import text_editor
from bot.filters import IsAdmin
from bot.state import Admin
import bot.markups as nav

import asyncio

router = Router()

# Кнопка Создать рассылку
@router.callback_query(StateFilter(None), F.data == "mailing_menu", IsAdmin())
async def mailing_menu(call: types.CallbackQuery, state: FSMContext):
	await text_editor(text=TEXT.admin.mailing,
					  event=call,
					  reply_markup=nav.back_button("admin_menu"))
	await state.set_state(Admin.Mailing.get_data)

# Получаем данные для рассылки
@router.message(StateFilter(Admin.Mailing.get_data))
async def get_mailing_data(message: types.Message, state: FSMContext):
	await bot.send_message(message.from_user.id, "➖" * 10)
	msg = await message.copy_to(message.from_user.id)
	await bot.send_message(message.from_user.id,
						   f"{'➖' * 10}\n"
						   f"<i>Если вас все устраивает, нажмите подтвердить</i>\n"
						   f"<b>НЕ УДАЛЯЙТЕ ЭТО СООБЩЕНИЙ ВО ВРЕМЯ РАССЫЛКИ!!!</b>",
						   reply_markup=nav.confirm_menu())

	await state.set_state(Admin.Mailing.confirm)
	await state.update_data(data=msg)

# Создаем задачу для рассылки
@router.callback_query(StateFilter(Admin.Mailing.confirm), F.data == "confirm")
async def start_mailing(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	asyncio.create_task(
		sending_loop(data.get("message_id"), call.from_user.id)
	)
	await bot.send_message(call.from_user.id,
						   "📤 Рассылка началась",
						   reply_markup=nav.back_button("admin_menu"))
	await state.clear()

# Ф-ция рассылки
async def sending_loop(message_id: int, admin_chat_id: int):
	users = await db.client.get_all()
	sent, not_sent = 0, 0
	for user_id in users:
		try:
			await bot.copy_message(user_id, admin_chat_id, message_id)
			sent += 1
		except:
			not_sent += 1
		await asyncio.sleep(0.08)

	await bot.send_message(admin_chat_id,
						   f"📥 Рассылка закончилась\n"
						   f"{'➖' * 10}\n"
						   f"🔔 - {sent}\n"
						   f"🔕 - {not_sent}\n"
						   f"{'➖' * 10}",
						   reply_markup=nav.back_button("admin_menu"))