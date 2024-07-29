from aiogram import Router

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