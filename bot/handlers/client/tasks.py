from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram import types, Router, F

from bot.data.config import db, TEXT, get_image, bot
from bot.utils.message import text_editor
from bot.utils.paginator import Paginator
from bot.filters import StartsWith
import bot.markups as nav

router = Router()

# Меню всех заданий
@router.callback_query(F.data == "tasks")
async def task_menu(call: types.CallbackQuery):
    completed_task = await db.task.get_completed_tasks(call.from_user.id)
    tasks = await db.task.get(completed_task=completed_task)

    if not tasks:
        await call.answer(TEXT.error.no_task, show_alert=True)
        return

    buttons = []
    for task in tasks:
        task_id = task.get("task_id")
        buttons.append(
            [
                InlineKeyboardButton(text=f"👉 Задание {task_id}", callback_data=f"task|{task_id}")
            ]
        )
    extra_button = [InlineKeyboardButton(text="🔙 Назад", callback_data="back|earn_menu")]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    paginator = Paginator(data=kb, dp=router, extra_buttons=extra_button)
    await text_editor(TEXT.choose_task,
                      event=call,
                      photo=get_image.tasks,
                      reply_markup=paginator())

# Отображение конкретного задания
@router.callback_query(StartsWith("task|"))
async def choose_task(call: types.CallbackQuery):
    task_id = call.data.split("|")[1]

    completed_task = await db.task.get_completed_tasks(call.from_user.id)
    if task_id in completed_task:
        await call.answer(TEXT.error.uncompleted_task, show_alert=True)
        return

    task = await db.task.get(task_id=task_id)
    description = task.get("description")
    reward = task.get("reward")

    file_data = task.get("file_id")
    if file_data:
        file_data = eval(file_data)
        file_type, file_id = file_data
    else:
        file_type = file_id = "unknown"
    kwargs = {file_type: file_id}

    await text_editor(TEXT.task_text.format(task_id=task_id,
                                            description=description,
                                            reward=reward),
                      event=call,
                      reply_markup=nav.complete_task(task_id),
                      **kwargs)

# Проверка выполнения задания(только подписка на канал/чат)
@router.callback_query(StartsWith("check_task|"))
async def complete_task(call: types.CallbackQuery):
    task_id = call.data.split("|")[1]
    completed_task = await db.task.get_completed_tasks(call.from_user.id)
    if task_id in completed_task:
        await call.answer(TEXT.error.uncompleted_task, show_alert=True)
        return

    task = await db.task.get(task_id=task_id)

    channel_id = task.get("channel_id")
    if not channel_id:
        await call.answer(TEXT.error.task_not_completed, show_alert=True)
        return

    try:
        user_status = await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)
    except TelegramBadRequest:
        await text_editor(TEXT.error.cant_check_subscription,
                          event=call,
                          reply_markup=nav.back_button("add_task_menu"))
        return

    if user_status.status == "left":
        await call.answer(TEXT.error.dont_subscribe, show_alert=True)
        return

    reward = task.get("reward")
    balance = await db.client.get(call.from_user.id, "balance")
    await db.client.update(call.from_user.id, balance=balance+reward)
    await db.task.add_completed_tasks(call.from_user.id, task_id)

    await text_editor(TEXT.successful.completed_task.format(task_id=task_id,
                                                            reward=reward),
                      event=call,
                      reply_markup=nav.earn_keyboard())
