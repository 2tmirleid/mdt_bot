from aiogram import Router, F
from aiogram.types import Message

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.users.contacts.users_contacts_controller import UsersContactsController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersContactsController = UsersContactsController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


@router.message(F.text == buttons['user']['main_panel']['contacts'])
async def process_users_get_contacts(msg: Message) -> None:
    await users_controller.users_get_contacts(msg)


@router.message(F.text == buttons['user']['contacts']['ceo'])
async def process_users_get_ceo(msg: Message) -> None:
    await users_controller.users_get_ceo(msg)


@router.message(F.text == buttons['user']['contacts']['moderator'])
async def process_users_get_moderator(msg: Message) -> None:
    await users_controller.users_get_moderator(msg)
