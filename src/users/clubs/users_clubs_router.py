from aiogram import Router, F
from aiogram.types import Message

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.users.clubs.users_clubs_controller import UsersClubsController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersClubsController = UsersClubsController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


@router.message(F.text == buttons['user']['main_panel']['clubs']['main'])
async def process_users_get_clubs_info(msg: Message) -> None:
    await users_controller.users_get_clubs_info(msg)


@router.message(F.text == buttons['user']['clubs']['mdt_it'])
async def process_users_get_clubs_mdt_it(msg: Message) -> None:
    await users_controller.users_get_clubs_mdt_it(msg)


@router.message(F.text == buttons['user']['clubs']['mdt_woman'])
async def process_users_get_clubs_mdt_it(msg: Message) -> None:
    await users_controller.users_get_clubs_mdt_woman(msg)
