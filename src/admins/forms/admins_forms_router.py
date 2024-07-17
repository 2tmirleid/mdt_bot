from aiogram import Router, F
from aiogram.types import Message

from src.admins.forms.admins_forms_controller import AdminsFormsController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

# Подключение middleware для защиты от несанкцианированного доступа в админку
router.message.middleware(AdminsMiddleware())
router.callback_query.middleware(AdminsMiddleware())

admins_controller: AdminsFormsController = AdminsFormsController()


lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


# Обработка нажатия кнопки "Анкеты"
@router.message(F.text == buttons['admin']['main_panel']['forms']['main'])
async def process_admins_get_forms_menu_panel(msg: Message) -> None:
    await admins_controller.get_forms_admins_menu_panel(msg)
