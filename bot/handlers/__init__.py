from .client import start, main_menu, withdraw, promocode, tasks

from .admin import admin_commands, mailing, statistic
from .admin import promocode as admin_promo
from .admin import tasks as admin_tasks

from .back_button import router as back_router
from .missed import router as missed_router

from aiogram import Router

def routers() -> list[Router]:
    data = [
        start.router,
        main_menu.router,
        withdraw.router,
        promocode.router,
        tasks.router,
        admin_commands.router,
        mailing.router,
        statistic.router,
        admin_promo.router,
        admin_tasks.router,
        back_router,
        missed_router
    ]
    return data
