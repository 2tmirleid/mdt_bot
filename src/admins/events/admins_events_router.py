from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.events.admins_events_controller import AdminsEventsController
from src.middlewares.admins_middleware import AdminsMiddleware
from src.states.admins.events.admins_choose_events_city import AdminsChooseEventsCity
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

# Подключение middleware для защиты от несанкцианированного доступа в админку
router.message.middleware(AdminsMiddleware())
# router.callback_query.middleware(AdminsMiddleware())

admins_controller: AdminsEventsController = AdminsEventsController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


# Обработка нажатия кнопки "Мероприятия" в панели админа
@router.message(F.text == buttons['admin']['main_panel']['events']['main'])
async def process_admins_choose_events_city(msg: Message, state: FSMContext) -> None:
    await admins_controller.choose_city(msg=msg, state=state)


# Обработка выбора города админом
@router.message(StateFilter(AdminsChooseEventsCity.city), F.text)
async def process_admins_get_events(msg: Message, state: FSMContext) -> None:
    admins_controller.city = msg.text

    # Обработка вывода мероприятий с выбранным городом
    await admins_controller.admins_get_events(msg=msg, state=state)


# Обработка кнопки пагинации >> для мероприятий
@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_events"))
async def process_admins_pagen_next_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_controller.admins_get_events(msg=clb_query.message,
                                              state=state,
                                              offset=offset,
                                              edit=True)


# Обработка кнопки пагинации << для мероприятий
@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_events"))
async def process_admins_pagen_backward_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_controller.admins_get_events(msg=clb_query.message,
                                              state=state,
                                              offset=offset,
                                              edit=True)
