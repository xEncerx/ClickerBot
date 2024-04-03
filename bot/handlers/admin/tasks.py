from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ContentType as CType
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router, types

from bot.filters import IsAdmin, AnyData, AnyContentType
from bot.data.config import TEXT, db, bot
from bot.utils.message import text_editor
from bot.state import Admin
import bot.markups as nav

router = Router()

# Меню добавления задания
@router.callback_query(StateFilter(None), IsAdmin(), AnyData("add_task", "delete_task"))
async def add_menu(call: types.CallbackQuery, state: FSMContext):
    action = call.data
    if action == "add_task":
        await text_editor(TEXT.admin.task.add_menu,
                          event=call,
                          reply_markup=nav.add_task())
        await state.set_state(Admin.AddTask.data)
    elif action == "delete_task":
        await text_editor(TEXT.admin.task.task_id,
                          event=call,
                          reply_markup=nav.back_button("admin_menu"))
        await state.set_state(Admin.DeleteTask.task_id)

# Обработка кнопок добавления данных задания
@router.callback_query(StateFilter(Admin.AddTask.data), IsAdmin(),
                       AnyData("change_task_description", "change_task_reward",
                               "change_channel_id", "publish_task", "change_file_id"))
async def task_handler(call: types.CallbackQuery, state: FSMContext):
    action = call.data

    if action == "change_task_description":
        await text_editor(TEXT.admin.task.change_description,
                          event=call,
                          reply_markup=nav.back_button("add_task_menu"))
        await state.update_data(type="description")

    elif action == "change_task_reward":
        await text_editor(TEXT.admin.task.change_reward,
                          event=call,
                          reply_markup=nav.back_button("add_task_menu"))
        await state.update_data(type="reward")

    elif action == "change_channel_id":
        await text_editor(TEXT.admin.task.change_channelID,
                          event=call,
                          reply_markup=nav.back_button("add_task_menu"))
        await state.update_data(type="channel_id")

    elif action == "change_file_id":
        await text_editor(TEXT.admin.task.change_fileID,
                          event=call,
                          reply_markup=nav.back_button("add_task_menu"))
        await state.update_data(type="file_id")

    elif action == "publish_task":
        state_data = await state.get_data()

        description = state_data.get("description")
        reward = state_data.get("reward")
        channel_id = state_data.get("channel_id")
        file_id = state_data.get("file_id")

        if not all([description, reward]):
            await call.answer(TEXT.admin.task.not_filled, show_alert=True)
            return

        await db.task.add(description, reward, channel_id, file_id)
        await text_editor(TEXT.admin.task.added,
                          event=call,
                          reply_markup=nav.admin_menu())
        await state.clear()

# Получение и перезапись данных
@router.message(StateFilter(Admin.AddTask.data), IsAdmin(),
                AnyContentType(CType.PHOTO, CType.DOCUMENT, CType.TEXT))
async def get_data(message: types.Message, state: FSMContext):
    async def update_data():
        await state.update_data(type=None,
                                description=description,
                                reward=reward,
                                channel_id=channel_id,
                                file_id=file_id)

    state_data = await state.get_data()

    description = state_data.get("description")
    reward = state_data.get("reward", 0)
    channel_id = state_data.get("channel_id")
    file_id = state_data.get("file_id")
    data_type = state_data.get("type")

    if data_type == "file_id":
        if message.content_type == CType.DOCUMENT:
            file_id = ("document", message.document.file_id)
        elif message.content_type == CType.PHOTO:
            file_id = ("photo", message.photo[-1].file_id)
        await update_data()
        await text_editor(TEXT.admin.task.add_menu,
                          event=message,
                          reply_markup=nav.add_task())
        return

    input_data = message.text

    if data_type in ("reward", "channel_id") and not input_data.lstrip("-").isdigit():
        await text_editor(TEXT.error.not_digit,
                          event=message,
                          reply_markup=nav.back_button("add_task_menu"))
        return

    if data_type == "channel_id":
        me = await bot.get_me()
        try:
            channel_id = int(input_data)
            await bot.get_chat_member(chat_id=channel_id, user_id=me.id)
            await update_data()

        except TelegramBadRequest:
            await text_editor(TEXT.error.bot_not_chat_admin,
                              event=message,
                              reply_markup=nav.back_button("add_task_menu"))
            return

    if data_type == "reward":
        reward = int(input_data)
        await update_data()

    if data_type == "description":
        description = input_data
        await update_data()

    await text_editor(TEXT.admin.task.add_menu,
                      event=message,
                      reply_markup=nav.add_task())

@router.message(StateFilter(Admin.DeleteTask.task_id))
async def delete_task(message: types.Message, state: FSMContext):
    task_id = message.text
    if not task_id.isdigit():
        await text_editor(TEXT.admin.task.incorrect_task_type,
                          event=message,
                          reply_markup=nav.back_button("admin_menu"))
        return

    if not await db.task.exists(task_id):
        await text_editor(TEXT.notExists.task,
                          event=message,
                          reply_markup=nav.back_button("admin_menu"))
        return

    await db.task.delete(task_id)
    await text_editor(TEXT.admin.task.deleted.format(task_id=task_id),
                      event=message,
                      reply_markup=nav.back_button("admin_menu"))
    await state.clear()
