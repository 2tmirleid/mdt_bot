from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.admins.admins_service import AdminsService
from utils.errors.admins.admins_errors_formatter import AdminsErrorsFormatter


class AdminsMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.admins_errors: AdminsErrorsFormatter = AdminsErrorsFormatter()

        self.admins_service: AdminsService = AdminsService()

        super().__init__()

    async def on_pre_process_message(
            self,
            msg: Message,
            data: Dict[str, Any]
    ) -> None:
        chat_id = msg.from_user.id

        is_admin = await self.admins_service.am_i_admin(chat_id)

        if not is_admin:
            error_msg = await self.admins_errors.forbidden_access(chat_id)
            raise CancelHandler(error_msg)

    async def on_pre_process_callback_query(
            self,
            query: CallbackQuery,
            data: Dict[str, Any]
    ) -> None:
        chat_id = query.message.from_user.id

        is_admin = await self.admins_service.am_i_admin(chat_id)

        if not is_admin:
            error_msg = await self.admins_errors.forbidden_access(chat_id)
            raise CancelHandler(error_msg)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            await self.on_pre_process_message(event, data)

        if isinstance(event, CallbackQuery):
            await self.on_pre_process_callback_query(event, data)

        return await handler(event, data)
