from aiogram.fsm.state import StatesGroup, State

# State для Админа
class Admin(StatesGroup):
	class AddTask(StatesGroup):
		data = State()

	class DeleteTask(StatesGroup):
		task_id = State()

	class AddPromo(StatesGroup):
		data = State()

	class DeletePromo(StatesGroup):
		get_promo = State()

	class Mailing(StatesGroup):
		get_data = State()
		confirm = State()

	class FileId(StatesGroup):
		get_id = State()

# State для Клиента
class Client(StatesGroup):
	class Promo(StatesGroup):
		get_promo = State()
