from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.admins.admins_controller import AdminsController
from src.middlewares.admins_middleware import AdminsMiddleware

router: Router = Router()

# Подключение middleware для защиты от несанкцианированного доступа в админку
router.message.middleware(AdminsMiddleware())
router.callback_query.middleware(AdminsMiddleware())

admins_controller: AdminsController = AdminsController()


@router.message(Command("admin"))
async def process_admins_get_started(msg: Message) -> None:
    await msg.answer('work')
