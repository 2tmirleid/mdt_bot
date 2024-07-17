from abc import ABC

from aiogram.types import Message

from src.admins.forms.admins_forms_service import AdminsFormsService
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class AdminsFormsController(Controller, ABC):
    def __init__(self):
        super().__init__()

        self.admins_service: AdminsFormsService = AdminsFormsService()

        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def get_forms_admins_menu_panel(self, msg: Message) -> None:
        keyboard = await self.admins_reply_keyboards.forms_admins_menu_panel_keyboard()

        await msg.answer(self.replicas['admin']['other']['option'],
                         reply_markup=keyboard)
