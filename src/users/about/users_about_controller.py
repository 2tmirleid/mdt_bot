import os

from aiogram.types import Message, FSInputFile

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class UsersAboutController(Controller):
    def __init__(self):
        super().__init__()

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def users_get_about_mdt(self, msg: Message) -> None:
        back_to_main_menu_button = await (self.users_inline_keyboards.
                                          users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'static', 'МДТ 2024.pdf')

        document = FSInputFile(file_path)

        await msg.answer_document(document=document,
                                  caption=self.replicas['general']['about_mdt'],
                                  reply_markup=back_to_main_menu_button)

