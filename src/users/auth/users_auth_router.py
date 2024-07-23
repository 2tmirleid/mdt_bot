from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.middlewares.users_already_auth_middleware import UsersAlreadyAuthMiddleware
from src.states.users.auth.users_auth_state import UsersAuthState
from src.users.auth.users_auth_controller import UsersAuthController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_auth_controller: UsersAuthController = UsersAuthController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAlreadyAuthMiddleware())


@router.message(F.text == buttons['user']['register']['start'])
async def process_users_get_phone(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_phone(msg, state)


@router.message(StateFilter(
    UsersAuthState.phone
), F.text | F.contact)
async def process_users_get_photo(msg: Message, state: FSMContext) -> None:
    if msg.text:
        await users_auth_controller.users_get_phone(msg, state)

        return

    if msg.contact.phone_number:
        phone = msg.contact.phone_number

        user = await users_auth_controller.check_if_user_phone_registered(phone)

        if not user:
            await users_auth_controller.users_get_photo(msg=msg, state=state, phone=phone)
        else:
            await users_auth_controller.users_save_tg_chat_id_and_tg_username(msg, phone)


@router.message(StateFilter(
    UsersAuthState.full_name
), F.text)
@router.message(StateFilter(
    UsersAuthState.photo
), F.photo)
async def process_users_get_full_name(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_full_name(msg, state)


@router.message(StateFilter(
    UsersAuthState.birth_date
), F.text)
async def process_users_get_city(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_city(msg, state)


@router.message(StateFilter(
    UsersAuthState.city
), F.text)
async def process_users_get_company(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_company(msg, state)


@router.message(StateFilter(
    UsersAuthState.company
), F.text)
async def process_users_get_position(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_position(msg, state)


@router.message(StateFilter(
    UsersAuthState.position
), F.text)
async def process_users_get_rm_status(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_rm_status(msg, state)


@router.message(StateFilter(
    UsersAuthState.rm_status
), F.text)
async def process_users_get_hobbies(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_hobbies(msg, state)


@router.message(StateFilter(
    UsersAuthState.hobbies
), F.text)
async def process_users_get_resources(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_resources(msg, state)


@router.message(StateFilter(
    UsersAuthState.resources
), F.text)
async def process_users_get_expertise(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_get_expertise(msg, state)


@router.message(StateFilter(
    UsersAuthState.expertise
), F.text)
async def process_users_auth_finish(msg: Message, state: FSMContext) -> None:
    await users_auth_controller.users_auth_finish(msg, state)
