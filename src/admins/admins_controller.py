from abc import ABC

from aiogram.types import Message

from src.admins.admins_service import AdminsService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class AdminsController(Controller, ABC):
    def __init__(self):
        super().__init__()

        self.admins_service: AdminsService = AdminsService()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def get_started(self, msg: Message) -> None:
        admin = await self.admins_service.get_admin_full_name_by_chat_id(chat_id=msg.from_user.id)
        full_name = None

        for row in admin:
            full_name = row["full_name"]

        await msg.answer(self.replicas["admin"]["greeting"] + full_name)
