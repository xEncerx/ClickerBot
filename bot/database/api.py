from aiosqlite import IntegrityError
import aiosqlite

from bot.database import models

from typing import Union, Optional, Any
from datetime import datetime
import os


class DBApi:
	def __init__(self, db_path: str):
		self.db_path = db_path
		self.client = _Client(self)
		self.promocode = _Promocode(self)
		self.task = _Task(self)

	@staticmethod
	def _dict_factory(cursor, row) -> dict:
		return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

	async def db_request(self, query: str, param: tuple = (), fetchone: bool = False, fetchall: bool = False,
						 use_factory: bool = False) -> Any:
		async with aiosqlite.connect(self.db_path) as connection:
			if any([fetchone, fetchall]) and use_factory:
				connection.row_factory = self._dict_factory

			async with connection.execute(query, param) as cursor:
				await connection.commit()
				if fetchone:
					return await cursor.fetchone()
				elif fetchall:
					return await cursor.fetchall()

	# Проверка и создание таблиц в БД
	async def create_db(self) -> None:
		if not os.path.exists(self.db_path):
			print("- DB  wasn't found | Creating...")
			with open(self.db_path, "w") as _: ...
		else:
			print("+ DB found | Checking...")

		client_len = len(await self.db_request("PRAGMA table_info(client)", fetchall=True))
		act_promo_len = len(await self.db_request("PRAGMA table_info(activated_promo)", fetchall=True))
		comp_tasks_len = len(await self.db_request("PRAGMA table_info(completed_task)", fetchall=True))
		promocodes_len = len(await self.db_request("PRAGMA table_info(promocodes)", fetchall=True))
		tasks_len = len(await self.db_request("PRAGMA table_info(tasks)", fetchall=True))

		if client_len == 6:
			print("+ Client Table was found(1/5)")
		else:
			print("- Table wasn't found(1/5) | Creating...")
			await self.db_request(models.table_client)

		if act_promo_len == 2:
			print("+ Activated_promo Table was found(2/5)")
		else:
			print("- Table wasn't found(2/5) | Creating...")
			await self.db_request(models.table_activated_promo)

		if comp_tasks_len == 2:
			print("+ Completed_task Table was found(3/5)")
		else:
			print("- Table wasn't found(3/5) | Creating...")
			await self.db_request(models.table_completed_task)

		if promocodes_len == 2:
			print("+ Promocodes Table was found(4/5)")
		else:
			print("- Table wasn't found(4/5) | Creating...")
			await self.db_request(models.table_promocodes)

		if tasks_len == 5:
			print("+ Tasks Table was found(5/5)")
		else:
			print("- Table wasn't found(5/5) | Creating...")
			await self.db_request(models.table_tasks)


class _Promocode:
	def __init__(self, parent: DBApi):
		self._parent = parent

	async def add(self, promo: str, reward: int) -> bool:
		try:
			await self._parent.db_request("INSERT INTO promocodes VALUES (?, ?)",
										  (promo, reward))
			return True
		except IntegrityError: return False

	async def delete(self,
					 promo: str) -> None:
		await self._parent.db_request("DELETE FROM promocodes WHERE promo = ?", (promo,))

	async def exists(self, promo: str) -> bool:
		result = await self._parent.db_request("SELECT 1 FROM promocodes WHERE promo = ?", (promo,), fetchone=True)
		return bool(result)

	async def is_used(self, user_id: int, promo: str) -> bool:
		result = await self._parent.db_request("SELECT 1 FROM activated_promo WHERE user_id = ? AND promo = ?",
											   (user_id, promo,),
											   fetchone=True)
		return bool(result)

	async def get_reward(self, promo: str) -> int:
		result = await self._parent.db_request("SELECT reward FROM promocodes WHERE promo = ?", (promo,),
											   fetchone=True)
		return result[0]

	async def set_used(self, user_id: int, promo: str) -> None:
		await self._parent.db_request("INSERT INTO activated_promo VALUES(?,?)", (user_id, promo))

	async def get_all(self) -> list:
		result = await self._parent.db_request("SELECT * FROM promocodes", fetchall=True)
		return result

class _Task:
	def __init__(self, parent: DBApi):
		self._parent = parent

	async def get(self, task_id: Optional[int] = None, completed_task: Optional[list] = None) -> dict:
		if task_id:
			result = await self._parent.db_request("SELECT * FROM tasks WHERE task_id = ?",
												   (task_id,), fetchone=True, use_factory=True)
		elif completed_task:
			placeholders = ','.join(map(str, completed_task))
			result = await self._parent.db_request(f"SELECT * FROM tasks WHERE task_id NOT IN ({placeholders})",
												   fetchall=True, use_factory=True)
		else:
			result = await self._parent.db_request("SELECT * FROM tasks", fetchall=True, use_factory=True)

		return result

	async def add(self,
				  description: str,
				  reward: int,
				  channel_id: Optional[int],
				  file_id: Optional[tuple]
				  ) -> None:
		if isinstance(file_id, (tuple, list)):
			file_id = f"{file_id}"

		await self._parent.db_request("INSERT INTO tasks (description, reward, channel_id, file_id) VALUES (?, ?, ?, ?)",
									  (description, reward, channel_id, file_id))

	async def delete(self, task_id: int) -> None:
		async with aiosqlite.connect(self._parent.db_path) as connection:
			await connection.execute("BEGIN")
			await connection.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
			await connection.execute("DELETE FROM completed_task WHERE task_id = ?", (task_id,))
			await connection.execute("UPDATE completed_task SET task_id = task_id - 1 WHERE task_id >= ?", (task_id,))
			await connection.execute("UPDATE tasks SET task_id = task_id - 1 WHERE task_id > ?", (task_id,))
			await connection.commit()

	async def exists(self, task_id: int) -> bool:
		result = await self._parent.db_request("SELECT 1 FROM tasks WHERE task_id = ?", (task_id,), fetchone=True)
		return bool(result)

	async def get_completed_tasks(self, user_id: int) -> list:
		result = await self._parent.db_request("SELECT task_id FROM completed_task WHERE user_id = ?", (user_id,), fetchall=True)
		return [i[0] for i in result]

	async def add_completed_tasks(self, user_id: int, task_id: int) -> None:
		try:
			await self._parent.db_request("INSERT INTO completed_task VALUES(?, ?)", (user_id, task_id,))
		except aiosqlite.IntegrityError:
			pass


class _Client:
	def __init__(self, parent: DBApi):
		self._parent = parent

	async def add(self,
				  user_id: int,
				  referrer_id: Optional[int] = None,
				  username: Optional[str] = None,
				  balance: int = 0,
				  register_time: Optional[Union[str, datetime]] = None,
				  status: str = "active"
				  ) -> None:

		if not register_time:
			register_time = datetime.now().strftime("%H:%M %d.%m.%Y")

		try:
			await self._parent.db_request("INSERT INTO client VALUES(?, ?, ?, ?, ?, ?)",
										  (user_id, balance, referrer_id, register_time, username, status))
		except IntegrityError:
			pass

	async def get(self,
				  user_id: int,
				  data: Union[str, tuple],
				  use_factory: bool = False
				  ) -> Union[str, dict]:

		if isinstance(data, tuple):
			use_factory = True
			data = ", ".join(data)

		result = await self._parent.db_request(f"SELECT {data} FROM client WHERE user_id = ?", (user_id,),
											   use_factory=use_factory,
											   fetchone=True)
		if isinstance(result, dict): return result
		return result[0]

	async def get_all(self, data: Union[str, tuple] = "user_id") -> list[int]:
		if isinstance(data, tuple):
			data = ", ".join(data)

		data = await self._parent.db_request(f"SELECT {data} FROM client", fetchall=True)
		return [temp[0] if len(temp) == 1 else temp for temp in data]

	async def update(self, user_id: int, **kwargs) -> None:
		if not kwargs: return

		data = ", ".join([f"{row}='{value}'" for row, value in kwargs.items()])
		await self._parent.db_request(f"UPDATE client SET {data} WHERE user_id =?", (user_id,))

	async def exists(self, user_id: int) -> bool:
		result = await self._parent.db_request("SELECT 1 FROM client WHERE user_id = ?", (user_id,), fetchone=True)
		return bool(result)

	async def count_referrals(self, referrer_id: int) -> int:
		result = await self._parent.db_request("SELECT COUNT(user_id) as count FROM client WHERE referrer_id = ?",
											   (referrer_id,),
											   fetchone=True)
		return result[0]

	async def add_completed_task(self, user_id: int, task_id: int) -> None:
		try:
			await self._parent.db_request("INSERT INTO completed_tasks VALUES(?,?)", (user_id, task_id))
		except IntegrityError:
			pass

	async def add_activated_promo(self, user_id: int, promo: int) -> None:
		try:
			await self._parent.db_request("INSERT INTO activated_promo VALUES(?,?)", (user_id, promo))
		except IntegrityError:
			pass

	async def is_active_promo(self, user_id: int, promo: str) -> bool:
		result = await self._parent.db_request("SELECT 1 FROM activated_promo WHERE user_id = ? AND promo = ?",
											   (user_id, promo),
											   fetchone=True)
		return bool(result)

	async def is_completed_task(self, user_id: int, task_id: int) -> bool:
		result = await self._parent.db_request("SELECT 1 FROM completed_task WHERE user_id =? AND task_id =?",
											   (user_id, task_id),
											   fetchone=True)
		return bool(result)
