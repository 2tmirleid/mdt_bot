from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.states.users.auth.users_auth_state import UsersAuthState
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.users_service import UsersService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class UsersController(Controller):
    def __init__(self):
        super().__init__()

        self.users_service: UsersService = UsersService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def users_get_started(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.users_to_main_panel_reply_keyboard()

        await msg.answer(self.replicas['user']['greeting'],
                         reply_markup=keyboard)
