from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import TelegramObject, Message, CallbackQuery

from src.users.auth.users_auth_controller import UsersAuthController
from src.users.users_service import UsersService


class UsersModerateAuthMiddleware(BaseMiddleware):
    def __init__(self):
        self.users_service: UsersService = UsersService()
        self.users_auth_controller: UsersAuthController = UsersAuthController()

        super().__init__()

    async def on_pre_process_message(
            self,
            msg: Message,
            data: Dict[str, Any]
    ) -> None:
        chat_id = msg.from_user.id

        is_auth = await self.users_service.get_user_by_chat_id(chat_id)

        if len(is_auth) > 0:
            if is_auth[0]['is_rejected']:
                await self.users_auth_controller.users_form_rejected(msg)
                raise CancelHandler()
            elif not is_auth[0]['is_approved']:
                await self.users_auth_controller.users_form_moderate(msg)
                raise CancelHandler()

    async def on_pre_process_callback_query(
            self,
            query: CallbackQuery,
            data: Dict[str, Any]
    ) -> None:
        chat_id = query.message.from_user.id

        is_auth = await self.users_service.get_user_by_chat_id(chat_id)

        if len(is_auth) > 0:
            if is_auth[0]['is_rejected']:
                await self.users_auth_controller.users_form_rejected(query.message)
                raise CancelHandler()
            elif not is_auth[0]['is_approved']:
                await self.users_auth_controller.users_form_moderate(query.message)
                raise CancelHandler()

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
