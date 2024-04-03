from aiogram.types.input_file import FSInputFile, URLInputFile

from typing import Optional, Generator
from pathlib import Path
import json
import os

# Моды для парсинга
class Mode:
    DICT: str = "DICT"
    PATH: str = "PATH"

# Парсим изображения
class GetImage:
    PATH = os.getcwd()
    ImagesPath = os.path.join(PATH, "images")
    Available_names = ["welcome", "promocode", "tasks", "withdraw", "admin_menu", "profile"]
    Available_suffixes = [".png", ".jpg", ".jpeg"]

    def __init__(self, mode: str = Mode.DICT, data: Optional[dict] = None):
        """
        :param mode: Mode.PATH - парс из папки | Mode.DICT - парс ссылок или file_id
        :param data: Словарь с ссылками | словарь с file_id

        Лучше всего использовать file_id. Для получения введите в бота /file_id (работает только в боте, в котором был создан)

        Examples:

        func = GetImage(Mode.PATH)

        func.welcome -> FSInputFile

        ---

        func = GetImage(Mode.DICT, data={"welcome": "link",
                                        "admin_menu": "file_id})

        func.welcome -> URLInputFile

        func.admin_menu -> str (id файла)

        Available keys:

        ["welcome", "promocode", "tasks", "withdraw", "admin_menu", "profile"]
        """

        self._data = data

        self.welcome = None
        self.promocode = None
        self.tasks = None
        self.withdraw = None
        self.admin_menu = None
        self.profile = None

        if not data and mode == Mode.PATH:
            self._parse_path()
        elif data and mode == Mode.DICT:
            self._parse_url()

    def _parse_path(self) -> None:
        if not os.path.exists(self.ImagesPath):
            os.makedirs(self.ImagesPath)

        for name in os.listdir(self.ImagesPath):
            path = os.path.join(self.ImagesPath, name)
            suffix = Path(path).suffix
            if suffix not in self.Available_suffixes:
                continue

            filename = name.split(".")[0]
            if filename in self.Available_names:
                self.__setattr__(filename, FSInputFile(path))

    def _parse_url(self) -> None:
        for name, link in self._data.items():
            if name in self.Available_names:
                if not link:
                    continue

                if link.startswith("http"):
                    self.__setattr__(name, URLInputFile(link))
                else:
                    self.__setattr__(name, link)

# Разделение входного списка на более мелкие
def spliter(L: list, chunk: int = 30) -> Generator:
    return (L[i:i+chunk] for i in range(0, len(L), chunk))

# Превращение строки формата json в dict. И обратно.
class JSON:
    @staticmethod
    def to_dict(data: str) -> Optional[dict]:
        try:
            data = data.replace("'", "\"")
            data = json.loads(data)
            return data
        except json.decoder.JSONDecodeError:
            return None

    @staticmethod
    def to_string(data: dict) -> str:
        return json.dumps(data, sort_keys=True)
