from aiogram import Router, F
from aiogram.types import Message

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.users.about.users_about_controller import UsersAboutController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersAboutController = UsersAboutController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


@router.message(F.text == buttons['user']['main_panel']['about'])
async def process_users_get_about_mdt(msg: Message) -> None:
    await users_controller.users_get_about_mdt(msg)
