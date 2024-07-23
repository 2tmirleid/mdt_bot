from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.middlewares.users_already_auth_middleware import UsersAlreadyAuthMiddleware
from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.users.users_controller import UsersController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersController = UsersController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAlreadyAuthMiddleware())
router.message.middleware(UsersAuthMiddleware())


@router.message(CommandStart())
async def process_users_get_started(msg: Message) -> None:
    await users_controller.users_get_started(msg)
