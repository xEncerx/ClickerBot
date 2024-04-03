from bot.data.config import db, MIN_WITHDRAW, MIN_REFERRAL_WITHDRAW, REDIRECT_LINK, TEXT, get_image
from bot.utils.message import text_editor
import bot.markups as nav

from aiogram import types, Router, F

router = Router()

# Кнопка - Вывести + проверка возможно ли это сделать
@router.callback_query(F.data == "withdraw")
async def withdraw(call: types.CallbackQuery):
    balance = await db.client.get(call.from_user.id, "balance")
    referrals = await db.client.count_referrals(call.from_user.id)
    if balance < MIN_WITHDRAW:
        await call.answer(TEXT.error.no_money.format(min_withdraw=MIN_WITHDRAW),
                          show_alert=True)
        return
    if referrals < MIN_REFERRAL_WITHDRAW:
        await call.answer(TEXT.error.no_referrals.format(referral=MIN_REFERRAL_WITHDRAW),
                          show_alert=True)
        return

    await text_editor(text=TEXT.withdraw.format(link=REDIRECT_LINK),
                      event=call,
                      photo=get_image.withdraw,
                      reply_markup=nav.back_button("main_menu"))
