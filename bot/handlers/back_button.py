from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import types, Router

from bot.data.config import TEXT, get_image
from bot.utils.message import text_editor
from bot.filters import StartsWith
import bot.markups as nav

router = Router()

# Кнопка назад
@router.callback_query(StateFilter("*"), StartsWith("back|"))
async def back_handler(call: types.CallbackQuery, state: FSMContext):
	action = call.data[5:]
	if action == "add_promo_menu":
		await text_editor(text=TEXT.admin.promo.add_menu,
						  event=call,
						  reply_markup=nav.create_promo_menu())
		return

	if action == "add_task_menu":
		await text_editor(TEXT.admin.task.add_menu,
						  event=call,
						  reply_markup=nav.add_task())
		return

	if await state.get_state():
		await state.clear()

	if action == "main_menu":
		await text_editor(TEXT.main_menu,
						  event=call,
						  photo=get_image.welcome,
						  reply_markup=nav.main_menu(call.from_user.id))

	if action == "earn_menu":
		await text_editor(text=TEXT.earn,
						  event=call,
						  reply_markup=nav.earn_keyboard())

	if action == "admin_menu":
		await text_editor(TEXT.admin.admin_menu.format(name=call.from_user.first_name),
						  event=call,
						  photo=get_image.admin_menu,
						  reply_markup=nav.admin_menu())
