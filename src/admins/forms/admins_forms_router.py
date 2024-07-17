from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.admins.forms.admins_forms_controller import AdminsFormsController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

# Подключение middleware для защиты от несанкцианированного доступа в админку
router.message.middleware(AdminsMiddleware())
# router.callback_query.middleware(AdminsMiddleware())

admins_controller: AdminsFormsController = AdminsFormsController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


# Обработка нажатия кнопки "Анкеты"
@router.message(F.text == buttons['admin']['main_panel']['forms']['main'])
async def process_admins_get_forms_menu_panel(msg: Message) -> None:
    await admins_controller.get_forms_admins_menu_panel(msg)


# Обработка нажатия кнопки "Новые анкеты"
@router.message(F.text == buttons['admin']['main_panel']['forms']['new'])
async def process_admins_get_new_forms(msg: Message) -> None:
    await admins_controller.get_forms_admins_new(msg)


# Обработка кнопки пагинации >> для новых анкет
@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_forms"))
async def process_admins_pagen_next_forms(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_controller.get_forms_admins_new(msg=clb_query.message,
                                                 offset=offset,
                                                 edit=True)


# Обработка кнопки пагинации << для новых анкет
@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_forms"))
async def process_admins_pagen_backward_forms(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_controller.get_forms_admins_new(msg=clb_query.message,
                                                 offset=offset,
                                                 edit=True)


# Обработка подтверждения новой анкеты
@router.callback_query(lambda query: query.data.startswith("admins_forms_accept"))
async def process_admins_accept_new_form(clb_query: CallbackQuery) -> None:
    form_id = str(clb_query.data.split("-")[1])

    await admins_controller.admins_accept_new_form(msg=clb_query.message, form_id=form_id)
