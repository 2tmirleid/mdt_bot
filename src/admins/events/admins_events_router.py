from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.events.admins_events_controller import AdminsEventsController
from src.middlewares.admins_middleware import AdminsMiddleware
from src.states.admins.events.admins_choose_events_city import AdminsChooseEventsCity
from src.states.admins.events.create_events_state import CreateEventsState
from src.states.admins.events.edit_events_state import EditEventsState
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


# Обработка кнопки пагинации "В начало" для мероприятий
@router.callback_query(lambda query: query.data.startswith("admins_pagen_start_events"))
async def process_admins_pagen_start_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = 0

    await admins_controller.admins_get_events(msg=clb_query.message,
                                              state=state,
                                              offset=offset,
                                              edit=True)


# Обработка кнопки пагинации "В конец" для мероприятий
@router.callback_query(lambda query: query.data.startswith("admins_pagen_end_events"))
async def process_admins_pagen_end_events(clb_query: CallbackQuery, state: FSMContext) -> None:
    city = admins_controller.city

    offset = await admins_controller.admins_get_events_count(city=city) - 1

    print(offset)

    await admins_controller.admins_get_events(msg=clb_query.message,
                                              state=state,
                                              offset=offset,
                                              edit=True)


@router.callback_query(F.data == callback_data['admin']['general']['add'] + "_events")
async def process_admins_add_event_photo(clb_query: CallbackQuery, state: FSMContext) -> None:
    await admins_controller.admins_add_event_photo(msg=clb_query.message, state=state)


@router.message(StateFilter(CreateEventsState.photo), F.photo)
async def process_admins_add_event_title(msg: Message, state: FSMContext) -> None:
    await admins_controller.admins_add_event_title(msg=msg, state=state)


@router.message(StateFilter(CreateEventsState.title), F.text)
async def process_admins_add_event_description(msg: Message, state: FSMContext) -> None:
    await admins_controller.admins_add_event_description(msg=msg, state=state)


@router.message(StateFilter(CreateEventsState.description), F.text)
async def process_admins_add_event_date(msg: Message, state: FSMContext) -> None:
    await admins_controller.admins_add_event_date(msg=msg, state=state)


@router.message(StateFilter(CreateEventsState.event_date), F.text)
async def process_admins_add_event_city(msg: Message, state: FSMContext) -> None:
    await admins_controller.admins_add_event_city(msg=msg, state=state)


@router.callback_query(lambda query: any(
    city in query.data for city in [
        callback_data['admin']['main_panel']['events']['city']['add']['saransk'],
        callback_data['admin']['main_panel']['events']['city']['add']['moscow'],
    ]
))
@router.message(StateFilter(CreateEventsState.city), F.text)
async def process_admins_add_event_finish(msg: Message | CallbackQuery, state: FSMContext) -> None:
    if isinstance(msg, Message):
        city = msg.text

        await admins_controller.admins_add_event_finish(msg=msg, state=state, city=city)
    if isinstance(msg, CallbackQuery):
        temp_city = str(msg.data.split("-")[1])

        city = "Саранск" if temp_city == "saransk" else "Москва"

        await admins_controller.admins_add_event_finish(msg=msg.message, state=state, city=city)


@router.callback_query(lambda query: query.data.startswith("admins_export_users_for_events"))
async def process_admins_export_events(clb_query: CallbackQuery) -> None:
    event_id = str(clb_query.data.split("-")[1])

    admins_controller.event_id = event_id

    await admins_controller.admins_export_events(msg=clb_query.message, event_id=event_id)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_users_for_events"))
async def process_admins_pagen_next_events(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) + 1

    event_id = admins_controller.event_id

    await admins_controller.admins_export_events(msg=clb_query.message,
                                                 event_id=event_id,
                                                 offset=offset,
                                                 edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_users_for_events"))
async def process_admins_pagen_backward_events(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    event_id = admins_controller.event_id

    await admins_controller.admins_export_events(msg=clb_query.message,
                                                 event_id=event_id,
                                                 offset=offset,
                                                 edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_start_users_for_events"))
async def process_admins_pagen_start_events(clb_query: CallbackQuery) -> None:
    offset = 0

    event_id = admins_controller.event_id

    await admins_controller.admins_export_events(msg=clb_query.message,
                                                 event_id=event_id,
                                                 offset=offset,
                                                 edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_end_users_for_events"))
async def process_admins_pagen_end_events(clb_query: CallbackQuery) -> None:
    event_id = admins_controller.event_id

    offset = await admins_controller.admins_get_users_count_for_events(event_id=event_id) - 1

    await admins_controller.admins_export_events(msg=clb_query.message,
                                                 event_id=event_id,
                                                 offset=offset,
                                                 edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_delete_events"))
async def process_admins_delete_event(clb_query: CallbackQuery, state: FSMContext) -> None:
    event_id = str(clb_query.data.split("-")[1])

    await admins_controller.admins_delete_event(clb_query.message, state, event_id)


@router.callback_query(lambda query: query.data.startswith("admins_edit_events"))
async def process_admins_edit_event(clb_query: CallbackQuery, state: FSMContext) -> None:
    event_id = str(clb_query.data.split("-")[1])

    await admins_controller.admins_edit_event(
        msg=clb_query.message,
        state=state,
        event_id=event_id
    )


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['main_panel']['edit']['events']['photo'],
        callback_data['admin']['main_panel']['edit']['events']['title'],
        callback_data['admin']['main_panel']['edit']['events']['description'],
        callback_data['admin']['main_panel']['edit']['events']['event_date'],
        callback_data['admin']['main_panel']['edit']['events']['city'],
        callback_data['admin']['main_panel']['edit']['events']['is_active']
    ]
))
async def process_admins_edit_event_property(clb_query: CallbackQuery, state: FSMContext) -> None:
    property = str(clb_query.data.split("-")[1])

    await admins_controller.admins_edit_event_property(
        msg=clb_query.message,
        state=state,
        property=property
    )


# @router.callback_query(lambda query: any(
#     edit_action in query.data for edit_action in [
#         callback_data['admin']['main_panel']['events']['city']['edit']['saransk'],
#         callback_data['admin']['main_panel']['events']['city']['edit']['moscow']
#     ]
# ))
# async def process_admins_edit_event_city(clb_query: CallbackQuery, state: FSMContext) -> None:
#     clb_data = str(clb_query.data.split("-")[1])
#
#     city = "Саранск" if clb_data == "saransk" else "Москва"
#
#     await state.update_data(value=city)
#
#     await admins_controller.admins_edit_event_value(msg=clb_query.message, state=state)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['main_panel']['events']['city']['edit']['saransk'],
        callback_data['admin']['main_panel']['events']['city']['edit']['moscow']
    ]
))
@router.message(StateFilter(
    EditEventsState.value
), F.photo | F.text)
async def process_admins_edit_event_value(event: Message | CallbackQuery, state: FSMContext) -> None:
    if isinstance(event, Message):
        await admins_controller.admins_edit_event_value(msg=event, state=state)

    if isinstance(event, CallbackQuery):
        clb_data = str(event.data.split("-")[1])

        city = "Саранск" if clb_data == "saransk" else "Москва"

        await state.update_data(value=city)

        await admins_controller.admins_edit_event_value(msg=event.message, state=state)
