from bot.data.config import db, BALANCE_FOR_REFERRAL, bot, TEXT, get_image
from bot.utils.message import text_editor
import bot.markups as nav

from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types, Router

router = Router()

# Обработка /start + регистрация клиента
@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
	await state.clear()

	is_registered = await db.client.exists(message.from_user.id)
	if not is_registered:
		referrer_id = message.text[7:]
		if referrer_id == "":
			await db.client.add(message.from_user.id, username=message.from_user.username)

		else:
			if referrer_id == str(message.from_user.id):
				await bot.send_message(message.from_user.id, "Это ваша же ссылка 😰")
				return

			else:
				try:
					await db.client.add(message.from_user.id, referrer_id, message.from_user.username)
					referrer_balance = await db.client.get(referrer_id, "balance")
					new_balance = referrer_balance + BALANCE_FOR_REFERRAL
					await db.client.update(referrer_id, balance=new_balance)
					await bot.send_message(referrer_id,
										   TEXT.new_referrer.format(
											   username=message.from_user.username,
											   balance_for_referral=BALANCE_FOR_REFERRAL,
											   new_balance=new_balance)
										   )
				except: pass

	await text_editor(TEXT.welcome,
					  event=message,
					  photo=get_image.welcome,
					  reply_markup=nav.welcome_menu(message.from_user.id))