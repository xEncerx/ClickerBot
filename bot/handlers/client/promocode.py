from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import types, Router, F

from bot.data.config import db, TEXT, get_image
from bot.utils.message import text_editor
from bot.state import Client
import bot.markups as nav

router = Router()

# Кнопка - Промокод
@router.callback_query(StateFilter(None), F.data == "enter_promocode")
async def promo_menu(call: types.CallbackQuery, state: FSMContext):
	await text_editor(TEXT.enter_promo,
					  event=call,
					  photo=get_image.promocode,
					  reply_markup=nav.back_button("main_menu"))
	await state.set_state(Client.Promo.get_promo)

# Обработка вводимого промокода, начисление баланса
@router.message(StateFilter(Client.Promo.get_promo), F.content_type == types.ContentType.TEXT)
async def enter_promo(message: types.Message, state: FSMContext):
	promocode = message.text
	promo_exists = await db.promocode.exists(promocode)

	if not promo_exists:
		await text_editor(TEXT.notExists.promo,
						  event=message,
						  reply_markup=nav.back_button("main_menu"))
		return

	promo_used = await db.promocode.is_used(message.from_user.id, promocode)
	if promo_used:
		await text_editor(TEXT.error.promo_used,
						  event=message,
						  reply_markup=nav.back_button("main_menu"))
		return

	balance = await db.client.get(message.from_user.id, "balance")
	promo_reward = await db.promocode.get_reward(promocode)
	await db.client.update(message.from_user.id, balance=balance+promo_reward)
	await db.promocode.set_used(message.from_user.id, promocode)

	await text_editor(TEXT.successful.used_promo.format(reward=promo_reward),
					  event=message,
					  reply_markup=nav.back_button("main_menu"))

	await state.clear()