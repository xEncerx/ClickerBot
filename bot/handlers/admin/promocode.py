from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, Router
import asyncio

from bot.data.config import TEXT, db, bot, get_image
from bot.utils.const_functions import spliter
from bot.utils.message import text_editor
from bot.filters import IsAdmin, AnyData
from bot.state import Admin
import bot.markups as nav

router = Router()

# Обработка действий с кнопками промокода
@router.callback_query(StateFilter(None), IsAdmin(), AnyData("create_promo", "delete_promo", "print_all_promo"))
async def promo_action(call: types.CallbackQuery, state: FSMContext):
	action = call.data

	if action == "create_promo":
		await text_editor(TEXT.admin.promo.add_menu,
						  event=call,
						  reply_markup=nav.create_promo_menu())
		await state.set_state(Admin.AddPromo.data)
	elif action == "delete_promo":
		await text_editor(TEXT.admin.promo.delete_promo,
						  event=call,
						  reply_markup=nav.back_button("admin_menu"))
		await state.set_state(Admin.DeletePromo.get_promo)

	elif action == "print_all_promo":
		await call.message.delete()
		data = await db.promocode.get_all()

		for split_data in spliter(data, chunk=30):
			text = [f"➖ <code>{name}</code> | <code>{reward}</code>" for name, reward in split_data]
			await bot.send_message(call.from_user.id,
								   "\n".join(text))
			await asyncio.sleep(0.5)

		if get_image.admin_menu:
			await bot.send_photo(call.from_user.id,
								 photo=get_image.admin_menu,
								 caption=TEXT.admin.admin_menu.format(name=call.from_user.first_name),
								 reply_markup=nav.admin_menu())
		else:
			await bot.send_photo(call.from_user.id,
								   TEXT.admin.admin_menu.format(name=call.from_user.first_name),
								   reply_markup=nav.admin_menu())

# Обработка действий с промокодом
@router.callback_query(StateFilter(Admin.AddPromo.data), IsAdmin(),
					   AnyData("enter_promo", "enter_reward", "publish_promo"))
async def promo_handler(call: types.CallbackQuery, state: FSMContext):
	action = call.data
	if action == "enter_promo":
		await text_editor(TEXT.admin.promo.change_promo,
						  event=call,
						  reply_markup=nav.back_button("add_promo_menu"))
		await state.update_data(type="promocode")
	elif action == "enter_reward":
		await text_editor(TEXT.admin.promo.change_reward,
						  event=call,
						  reply_markup=nav.back_button("add_promo_menu"))
		await state.update_data(type="reward")

	elif action == "publish_promo":
		data = await state.get_data()
		promocode, reward = data.get("promocode"), data.get("reward")
		if not all([promocode, reward]):
			await call.answer(TEXT.admin.promo.dont_filled, show_alert=True)
			return

		feedback = await db.promocode.add(promocode, reward)
		if feedback:
			await call.answer(TEXT.admin.promo.added.format(promo=promocode, reward=reward),
							  show_alert=True)
		else:
			await call.answer(TEXT.admin.promo.dont_added, show_alert=True)

		await text_editor(TEXT.admin.admin_menu.format(name=call.from_user.first_name),
						  event=call,
						  photo=get_image.admin_menu,
						  reply_markup=nav.admin_menu())
		await state.clear()

# Получаем данные промокода от админа
@router.message(StateFilter(Admin.AddPromo.data), IsAdmin())
async def get_data(message: types.Message, state: FSMContext):
	state_data = await state.get_data()
	promocode = state_data.get("promocode")
	reward = state_data.get("reward", 0)
	data_type = state_data.get("type")
	input_data = message.text

	if data_type == "reward" and not input_data.isdigit():
		await text_editor(TEXT.error.not_digit,
						  event=message,
						  reply_markup=nav.back_button("add_promo_menu"))
		return

	if data_type == "promocode":
		await state.update_data(type=None,
								promocode=input_data,
								reward=reward)
	elif data_type == "reward":
		await state.update_data(type=None,
								promocode=promocode,
								reward=int(input_data))

	await text_editor(TEXT.admin.promo.add_menu,
					  event=message,
					  reply_markup=nav.create_promo_menu())
# Удаление промокода
@router.message(StateFilter(Admin.DeletePromo.get_promo), IsAdmin())
async def delete_promo(message: types.Message, state: FSMContext):
	promo = message.text
	if not await db.promocode.exists(promo):
		await text_editor(TEXT.notExists.promo,
						  event=message,
						  reply_markup=nav.back_button("admin_menu"))
		return

	await db.promocode.delete(promo)
	await text_editor(TEXT.admin.promo.deleted.format(promo=promo),
					  event=message,
					  reply_markup=nav.back_button("admin_menu"))
	await state.clear()
