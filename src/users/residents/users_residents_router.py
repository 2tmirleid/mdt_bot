from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.states.users.users_search_residents_state import UsersSearchResidentsState
from src.users.residents.users_residents_controller import UsersResidentsController
from src.users.residents.users_residents_service import UsersResidentsService
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersResidentsController = UsersResidentsController()
users_service: UsersResidentsService = UsersResidentsService()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


@router.message(F.text == buttons['user']['main_panel']['residents'])
async def process_users_get_residents_property(msg: Message) -> None:
    await users_controller.users_get_residents_search_property(msg)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['user']['residents']['full_name'],
        callback_data['user']['residents']['resources'],
        callback_data['user']['residents']['city'],
        callback_data['user']['residents']['company'],
    ]
))
async def process_users_get_residents_value(clb_query: CallbackQuery, state: FSMContext) -> None:
    users_controller.property = str(clb_query.data.split("-")[1])

    await users_controller.users_get_residents_search_value(
        msg=clb_query.message,
        state=state,
        property=users_controller.property
    )


@router.message(StateFilter(
    UsersSearchResidentsState.value
), F.text)
async def process_users_get_resident(msg: Message, state: FSMContext) -> None:
    users_controller.value = msg.text

    await users_controller.users_get_residents(
        msg=msg,
        state=state
    )


@router.callback_query(lambda query: query.data.startswith("users_pagen_next_search"))
async def process_users_pagen_next_search(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) + 1

    await users_controller.users_get_residents(msg=clb_query.message,
                                               state=state,
                                               offset=offset,
                                               edit=True)


@router.callback_query(lambda query: query.data.startswith("users_pagen_backward_search"))
async def process_users_pagen_backward_search(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await users_controller.users_get_residents(msg=clb_query.message,
                                               state=state,
                                               offset=offset,
                                               edit=True)


@router.callback_query(lambda query: query.data.startswith("users_pagen_start_search"))
async def process_users_pagen_start_search(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = 0

    await users_controller.users_get_residents(msg=clb_query.message,
                                               state=state,
                                               offset=offset,
                                               edit=True)


@router.callback_query(lambda query: query.data.startswith("users_pagen_end_search"))
async def process_users_pagen_end_search(clb_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    property = users_controller.property
    value = users_controller.value

    residents_count = await users_service.get_residents(
        property=property,
        value=value
    )

    offset = residents_count[0]['count'] - 1

    await users_controller.users_get_residents(msg=clb_query.message,
                                               state=state,
                                               offset=offset,
                                               edit=True)
