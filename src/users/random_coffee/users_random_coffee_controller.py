from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.validator import Validator


class UsersRandomCoffeeController(Controller):
    def __init__(self):
        super().__init__()

        self.users_service: UsersService = UsersService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()
        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.validator: Validator = Validator()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

