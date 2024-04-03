from aiogram import types, Router

from bot.data.config import TEXT

router = Router()

# Обработка всех неизвестных команд
@router.message()
async def message_missed(message: types.Message):
	await message.answer(TEXT.error.message_missed)