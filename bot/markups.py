from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from bot.data.config import ADMIN_ID, FEEDBACK_LINK

# Клавиатура - /start
def welcome_menu(user_id: int) -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="🖥 Начать", callback_data="start")
		]
	]

	if user_id in ADMIN_ID:
		buttons.append(
			[
				InlineKeyboardButton(text="👤 Admin Menu", callback_data="admin_menu")
			]
		)

	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура - главное меню
def main_menu(user_id: int) -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="💸 Заработать", callback_data="start_earn")
		],
		[
			InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
			InlineKeyboardButton(text="💳 Вывести", callback_data="withdraw")
		],
		[
			InlineKeyboardButton(text="🎟 Промокод", callback_data="enter_promocode")
		]
	]
	if FEEDBACK_LINK:
		buttons.append(
			[
				InlineKeyboardButton(text="👉 Наши отзывы ⭐️", url=FEEDBACK_LINK)
			]
		)
	if user_id in ADMIN_ID:
		buttons.append(
			[
				InlineKeyboardButton(text="👤 Admin Menu", callback_data="admin_menu")
			]
		)

	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Кнопка назад
def back_button(value: str) -> InlineKeyboardMarkup:
	button = [
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data=f"back|{value}")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=button)

# Клавиатура - заработок баланса
def earn_keyboard() -> InlineKeyboardMarkup:
	buttons = [
			[
				InlineKeyboardButton(text="💥 Кликер", callback_data="clicker")
			],
			[
				InlineKeyboardButton(text="💰 Задания", callback_data="tasks")
			],
			[
				InlineKeyboardButton(text="👥 Пригласить друзей", callback_data="invite_friends")
			],
			[
				InlineKeyboardButton(text="🔙 Назад", callback_data="back|main_menu")
			]
	]
	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура - кликер
def clicker_menu() -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="💥 Клик", callback_data="click")
		],
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data="back|earn_menu")
		]
	]

	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура - админ меню
def admin_menu() -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="🖋 Создать рассылку", callback_data="mailing_menu")
		],
		[
			InlineKeyboardButton(text="➕ Задание", callback_data="add_task"),
			InlineKeyboardButton(text="➖ Задание", callback_data="delete_task")
		],
		[
			InlineKeyboardButton(text="➕ Промокод", callback_data="create_promo"),
			InlineKeyboardButton(text="➖ Промокод", callback_data="delete_promo"),
		],
		[
			InlineKeyboardButton(text="📃 Распечатать промокоды", callback_data="print_all_promo")
		],
		[
			InlineKeyboardButton(text="📃 Статистика", callback_data="statistic")
		],
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data="back|main_menu")
		]
	]

	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура - подтверждение рассылки
def confirm_menu() -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")
		],
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data="back|admin_menu")
		]
	]

	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура - создание промокода
def create_promo_menu() -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="🎟 Промокод", callback_data="enter_promo")
		],
		[
			InlineKeyboardButton(text="💵 Вознаграждение", callback_data="enter_reward")
		],
		[
			InlineKeyboardButton(text="📤 Опубликовать промокод", callback_data="publish_promo")
		],
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data="back|admin_menu")
		]
	]

	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура добавления заданий
def add_task() -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="📃 Описание", callback_data="change_task_description"),
			InlineKeyboardButton(text="💵 Вознаграждение", callback_data="change_task_reward")
		],
		[
			InlineKeyboardButton(text="🆔 Канала", callback_data="change_channel_id"),
			InlineKeyboardButton(text="➕ Файл", callback_data="change_file_id")
		],
		[
			InlineKeyboardButton(text="📤 Опубликовать задание", callback_data="publish_task")
		],
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data="back|admin_menu")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура проверки выполнения заданий
def complete_task(task_id: int) -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="✅ Проверить", callback_data=f"check_task|{task_id}")
		],
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data="back|earn_menu")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=buttons)