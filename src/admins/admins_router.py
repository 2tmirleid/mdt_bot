from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.admins.admins_controller import AdminsController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

# Подключение middleware для защиты от несанкцианированного доступа в админку
router.message.middleware(AdminsMiddleware())
router.callback_query.middleware(AdminsMiddleware())

admins_controller: AdminsController = AdminsController()


lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


# Обработка команды /admin
@router.message(Command("admin"))
async def process_admins_get_started(msg: Message) -> None:
    await admins_controller.get_started(msg)


# Обработка сообщений и callback_query, которые относятся к возврату или переходу в главное меню админки
@router.callback_query(F.data == callback_data['admin']['backward'])
@router.callback_query(F.data == callback_data['admin']['to_main_panel'])
@router.message(F.text == buttons['admin']['backward'])
@router.message(F.text == buttons['admin']['to_main_panel'])
async def process_admins_get_backward(msg: Message) -> None:
    await admins_controller.get_main_admin_panel(msg)