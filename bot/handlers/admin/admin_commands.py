from aiogram.types import FSInputFile, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from bot.data.config import TEXT, DB_PATH, bot, get_image
from bot.filters import IsAdmin, AnyContentType
from bot.utils.message import text_editor
from bot.state import Admin
import bot.markups as nav

from datetime import datetime

router = Router()

# Команда - /admin
@router.message(Command("admin"), IsAdmin())
async def command_enter(message: types.Message, state: FSMContext):
    await state.clear()

    await text_editor(TEXT.admin.admin_menu.format(name=message.from_user.first_name),
                      event=message,
                      photo=get_image.admin_menu,
                      reply_markup=nav.admin_menu())

# Кнопка - Admin Menu
@router.callback_query(F.data == "admin_menu", IsAdmin())
async def callback_enter(call: types.CallbackQuery):
    await text_editor(TEXT.admin.admin_menu.format(name=call.from_user.first_name),
                      event=call,
                      photo=get_image.admin_menu,
                      reply_markup=nav.admin_menu())

# Резервная копия Базы Данных
@router.message(Command("db_backup"), IsAdmin())
async def db_backup(message: types.Message, state: FSMContext):
    await state.clear()

    time = datetime.now().strftime('%H:%M %d.%m.%Y')

    await bot.send_document(message.from_user.id,
                            document=FSInputFile(DB_PATH),
                            caption=f"<b>📦 #BACKUP | <code>{time}</code></b>")

# Получение photo_id
@router.message(Command("file_id"), IsAdmin())
async def get_file_id(message: types.Message, state: FSMContext):
    await state.clear()

    await text_editor(TEXT.admin.send_image,
                      event=message,
                      reply_markup=nav.back_button("admin_menu"))
    await state.set_state(Admin.FileId.get_id)

# Отправка photo_id
@router.message(StateFilter(Admin.FileId.get_id), IsAdmin(), AnyContentType(ContentType.PHOTO))
async def return_file_id(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await message.reply(f"<b>📷 #PHOTO_ID\n<code>{photo_id}</code></b>")
    await state.clear()
