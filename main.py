from bot.data.config import BOT_USERNAME, dp, db, bot, logger, __version__
from bot.utils.bot_commands import set_commands
from bot.middleware import setup_middleware
from bot.handlers import routers

import asyncio
import sys
import os

label = """
███████╗███╗   ██╗ ██████╗███████╗██████╗
██╔════╝████╗  ██║██╔════╝██╔════╝██╔══██╗
█████╗  ██╔██╗ ██║██║     █████╗  ██████╔╝
██╔══╝  ██║╚██╗██║██║     ██╔══╝  ██╔══██╗
███████╗██║ ╚████║╚██████╗███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝  ╚═╝"""

# Запуск бота и базовых функций
async def main():
    await db.create_db()  # Проверка БД + создание при необходимости

    me = await bot.get_me()
    if me.username != BOT_USERNAME:
        logger.error("Bot Username doesn't match the one specified in the config!")

    await set_commands(bot)
    setup_middleware(dp)
    dp.include_routers(*routers())

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    print(label,
          "-_-_- Bot made by @Encer -_-_-",
          f"-_-_- Version: {__version__} -_-_-",
          "-_-_- Thanks for using -_-_-",
          sep="\n")
    try:
        # Исправление "RuntimeError: Event loop is closed" для Windows
        # if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win"):
        #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("-_-_- Bot was stopped -_-_-")
    finally:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
