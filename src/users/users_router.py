from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.states.users.users_edit_profile_state import UsersEditProfileState
from src.users.users_controller import UsersController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersController = UsersController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


@router.message(CommandStart())
async def process_users_get_started(msg: Message) -> None:
    await users_controller.users_get_started(msg)


@router.callback_query(F.data == callback_data['user']['to_main_panel'])
@router.message(F.text == buttons['user']['to_main_panel'])
async def process_users_get_main_menu_panel(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    if isinstance(event, Message):
        await users_controller.users_get_main_menu_panel(event)

    if isinstance(event, CallbackQuery):
        await users_controller.users_get_main_menu_panel(event.message)


@router.message(F.text == buttons['user']['main_panel']['profile'])
async def process_users_get_profile(msg: Message) -> None:
    await users_controller.users_get_profile(msg)


@router.callback_query(lambda query: query.data.startswith("users_edit_profile"))
async def process_users_edit_profile(clb_query: CallbackQuery, state: FSMContext) -> None:
    chat_id = str(clb_query.data.split("-")[1])

    await users_controller.users_edit_profile(
        msg=clb_query.message,
        state=state,
        chat_id=chat_id
    )


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['user']['profile']['edit']['photo'],
        callback_data['user']['profile']['edit']['phone'],
        callback_data['user']['profile']['edit']['full_name'],
        callback_data['user']['profile']['edit']['birth_date'],
        callback_data['user']['profile']['edit']['city'],
        callback_data['user']['profile']['edit']['company'],
        callback_data['user']['profile']['edit']['position'],
        callback_data['user']['profile']['edit']['rm_status'],
        callback_data['user']['profile']['edit']['hobbies'],
        callback_data['user']['profile']['edit']['resources'],
        callback_data['user']['profile']['edit']['expertise'],
    ]
))
async def process_users_edit_profile_property(clb_query: CallbackQuery, state: FSMContext) -> None:
    property = str(clb_query.data.split("-")[1])

    await users_controller.users_get_edit_profile_property(
        msg=clb_query.message,
        state=state,
        property=property
    )


@router.message(StateFilter(
    UsersEditProfileState.value
), F.text)
async def process_users_edit_profile_value(msg: Message, state: FSMContext) -> None:
    await users_controller.users_get_edit_profile_value(msg, state)
