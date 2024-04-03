from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State

from typing import Iterable, Any, Iterator, Callable, Coroutine, Union, Optional, List
from itertools import islice

from bot.filters import StartsWith

# Создания списка из кнопок с возможностью листать
class Paginator:
    def __init__(
            self,
            data: Union[
                InlineKeyboardMarkup,
                Iterable[InlineKeyboardButton],
                InlineKeyboardBuilder
            ],
            state: State = None,
            callback_startswith: str = 'page_',
            size: int = 8,
            page_separator: str = '/',
            dp: Optional[Union[Dispatcher, Router]] = None,
            extra_buttons: Optional[List[InlineKeyboardButton]] = None
    ):
        self.dp = dp
        self.page_separator = page_separator
        self._state = state
        self._size = size
        self._startswith = callback_startswith
        self._extra_buttons = extra_buttons

        if isinstance(data, InlineKeyboardMarkup):
            it = data.inline_keyboard
        elif isinstance(data, Iterable):
            it = data
        elif isinstance(data, InlineKeyboardBuilder):
            it = data.export()
        else:
            raise ValueError(f'{data} is not valid data')

        self._list_kb = list(
            self._chunk(
                it=it,
                size=self._size
            )
        )

    def __call__(
            self,
            current_page=0,
            *args,
            **kwargs
    ) -> InlineKeyboardMarkup:
        _list_current_page = self._list_kb[current_page]

        paginations = self._get_paginator(
            counts=len(self._list_kb),
            page=current_page,
            page_separator=self.page_separator,
            startswith=self._startswith
        )
        buttons = [*_list_current_page, paginations]
        if self._extra_buttons:
            buttons.append(self._extra_buttons)

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        if self.dp:
            self.paginator_handler()

        return keyboard

    @staticmethod
    def _get_page(call: types.CallbackQuery) -> int:
        return int(call.data[-1])

    @staticmethod
    def _chunk(it, size) -> Iterator[tuple[Any, ...]]:
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    def _get_paginator(
            self,
            counts: int,
            page: int,
            page_separator: str = '/',
            startswith: str = 'page_'
    ) -> list[InlineKeyboardButton]:
        counts -= 1
        paginations = []

        if page > 0:
            paginations.append(
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data=f'{startswith}{page - 1}'
                ),
            )
        paginations.append(
            InlineKeyboardButton(
                text=f'{page + 1}{page_separator}{counts + 1}',
                callback_data='pass'
            ),
        )
        if counts > page:
            paginations.append(
                InlineKeyboardButton(
                    text='➡️',
                    callback_data=f'{startswith}{page + 1}'
                )
            )

        return paginations

    def paginator_handler(self) -> Callable[[CallbackQuery, FSMContext], Coroutine[Any, Any, None]]:
        async def _page(call: types.CallbackQuery, state: FSMContext):
            page = self._get_page(call)

            await call.message.edit_reply_markup(
                reply_markup=self.__call__(
                    current_page=page
                )
            )
            await state.update_data({f'last_page_{self._startswith}': page})

        if not self.dp:
            return _page, StartsWith(self._startswith)
        else:
            self.dp.callback_query.register(
                _page,
                StartsWith(self._startswith),
            )