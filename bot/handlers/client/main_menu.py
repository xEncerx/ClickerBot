from bot.data.config import db, BALANCE_FOR_CLICKING, BALANCE_FOR_REFERRAL, get_image
from bot.utils.message import text_editor
from bot.data.config import TEXT, bot
from bot.filters import AnyData
import bot.markups as nav

from asyncio import sleep, create_task
from aiogram import types, Router

router = Router()

# Ф-ция начисление баланса, после таймера
async def click(user_id: int, call: types.CallbackQuery):
    await text_editor(text=TEXT.delay_message,
                      event=call)
    await sleep(5)
    balance = await db.client.get(user_id, "balance")
    await db.client.update(user_id, balance=balance+BALANCE_FOR_CLICKING)
    await text_editor(text=TEXT.earn_currency.format(balance_for_click=BALANCE_FOR_CLICKING),
                      event=call,
                      reply_markup=nav.clicker_menu())

# Обработка основных инлайн-команд от пользователя
@router.callback_query(AnyData("profile", "start_earn", "start", "invite_friends", "clicker", "click"))
async def main_commands(call: types.CallbackQuery):
    action = call.data
    if action == "profile":
        balance = await db.client.get(call.from_user.id, "balance")
        referrals = await db.client.count_referrals(call.from_user.id)
        await text_editor(text=TEXT.profile.format(ID=call.from_user.id,
                                                   username=call.from_user.username,
                                                   balance=round(balance, 1),
                                                   referrer=referrals),
                          event=call,
                          photo=get_image.profile,
                          reply_markup=nav.back_button("main_menu"))

    if action == "start":
        await text_editor(text=TEXT.main_menu,
                          event=call,
                          photo=get_image.welcome,
                          reply_markup=nav.main_menu(call.from_user.id))

    if action == "start_earn":
        await text_editor(text=TEXT.earn,
                          event=call,
                          reply_markup=nav.earn_keyboard())

    if action == "invite_friends":
        me = await bot.get_me()
        link = f"https://t.me/{me.username}?start={call.from_user.id}"
        await text_editor(text=TEXT.invitation.format(link=link,
                                                      balance_for_referral=BALANCE_FOR_REFERRAL),
                          event=call,
                          reply_markup=nav.back_button("earn_menu"))

    if action == "clicker":
        await text_editor(text=TEXT.clicker,
                          event=call,
                          reply_markup=nav.clicker_menu())

    if action == "click":
        await create_task(click(call.from_user.id, call))
