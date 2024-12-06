from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.middlewares.users_auth_middleware import UsersAuthMiddleware
from src.middlewares.users_moderate_auth_middleware import UsersModerateAuthMiddleware
from src.users.random_coffee.users_random_coffee_controller import UsersRandomCoffeeController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

users_controller: UsersRandomCoffeeController = UsersRandomCoffeeController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

router.message.middleware(UsersAuthMiddleware())
router.message.middleware(UsersModerateAuthMiddleware())


# @router.message(F.text == buttons['user']['main_panel']['random_coffee'])
# async def process_users_get_random_coffee_info(msg: Message, state: FSMContext) -> None:
#     await state.clear()
#
#     await users_controller.users_get_random_coffee_info(msg)


@router.callback_query(lambda query: query.data.startswith("users_random_coffee_subscribe"))
async def process_users_subscribe_for_random_coffee(clb_query: CallbackQuery) -> None:
    user_id = str(clb_query.data.split("-")[1])

    await users_controller.users_subscribe_for_random_coffee(msg=clb_query.message,
                                                             user_id=user_id)


@router.callback_query(lambda query: query.data.startswith("users_random_coffee_unsubscribe"))
async def process_users_unsubscribe_for_random_coffee(clb_query: CallbackQuery) -> None:
    user_id = str(clb_query.data.split("-")[1])

    await users_controller.users_unsubscribe_for_random_coffee(msg=clb_query.message,
                                                               user_id=user_id)
