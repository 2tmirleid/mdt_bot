from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.states.admins.events.admins_choose_events_city import AdminsChooseEventsCity
from src.states.users.users_choose_events_city import UsersChooseEventsCity
from src.users.calendar.users_calendar_controller import UsersCalendarController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersCalendarController = UsersCalendarController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


@router.message(F.text == buttons['user']['main_panel']['calendar'])
async def process_users_get_events_city(msg: Message, state: FSMContext) -> None:
    users_controller.chat_id = msg.from_user.id

    await users_controller.users_choose_city(msg, state)


@router.message(StateFilter(UsersChooseEventsCity.city), F.text)
async def process_users_get_events(msg: Message, state: FSMContext) -> None:
    users_controller.city = msg.text

    # Обработка вывода мероприятий с выбранным городом
    await users_controller.users_get_events(msg=msg, state=state)


# Обработка кнопки пагинации >> для мероприятий
@router.callback_query(lambda query: query.data.startswith("users_pagen_next_events"))
async def process_users_pagen_next_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await users_controller.users_get_events(msg=clb_query.message,
                                            state=state,
                                            offset=offset,
                                            edit=True)


# Обработка кнопки пагинации << для мероприятий
@router.callback_query(lambda query: query.data.startswith("users_pagen_backward_events"))
async def process_users_pagen_backward_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await users_controller.users_get_events(msg=clb_query.message,
                                            state=state,
                                            offset=offset,
                                            edit=True)


# Обработка кнопки пагинации "В начало" для мероприятий
@router.callback_query(lambda query: query.data.startswith("users_pagen_start_events"))
async def process_users_pagen_start_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = 0

    await users_controller.users_get_events(msg=clb_query.message,
                                            state=state,
                                            offset=offset,
                                            edit=True)


# Обработка кнопки пагинации "В конец" для мероприятий
@router.callback_query(lambda query: query.data.startswith("users_pagen_end_events"))
async def process_users_pagen_end_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    city = users_controller.city

    offset = await users_controller.users_get_events_count(city=city) - 1

    await users_controller.users_get_events(msg=clb_query.message,
                                            state=state,
                                            offset=offset,
                                            edit=True)


@router.callback_query(lambda query: query.data.startswith("user_register_for_event"))
async def process_users_register_for_event(clb_query: CallbackQuery, state: FSMContext) -> None:
    user_id = str(clb_query.data.split("-")[1])
    event_id = str(clb_query.data.split("-")[2])
    offset = str(clb_query.data.split("-")[3])

    await users_controller.register_user_for_event(
        msg=clb_query.message,
        state=state,
        offset=int(offset),
        user_id=user_id,
        event_id=event_id
    )


@router.callback_query(lambda query: query.data.startswith("user_unregister_for_event"))
async def process_users_unregister_for_event(clb_query: CallbackQuery, state: FSMContext) -> None:
    user_id = str(clb_query.data.split("-")[1])
    event_id = str(clb_query.data.split("-")[2])
    offset = str(clb_query.data.split("-")[3])

    await users_controller.unregister_user_for_event(
        msg=clb_query.message,
        state=state,
        offset=int(offset),
        user_id=user_id,
        event_id=event_id
    )
