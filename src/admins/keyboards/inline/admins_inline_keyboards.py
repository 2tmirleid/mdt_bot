from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class AdminsInlineKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def admins_dynamic_entity_to_main_menu_panel_keyboard(
            self, markup: bool = False
    ) -> list or InlineKeyboardMarkup:

        back_to_main_menu_btn = self.buttons['admin']['to_main_panel']
        back_to_main_menu_clb_data = self.callback_data['admin']['to_main_panel']

        if markup:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=back_to_main_menu_btn, callback_data=back_to_main_menu_clb_data)]
                ]
            )
        else:
            return [
                InlineKeyboardButton(text=back_to_main_menu_btn, callback_data=back_to_main_menu_clb_data)
            ]

    async def admins_new_forms_inline_keyboards(self, callback_data: str) -> list:
        accept_btn_text = self.buttons['admin']['forms']['accept']
        reject_btn_text = self.buttons['admin']['forms']['reject']

        accept_btn_clb_data = self.callback_data['admin']['forms']['accept'] + callback_data
        reject_btn_clb_data = self.callback_data['admin']['forms']['reject'] + callback_data

        return [
            [InlineKeyboardButton(text=accept_btn_text, callback_data=accept_btn_clb_data),
             InlineKeyboardButton(text=reject_btn_text, callback_data=reject_btn_clb_data)]
        ]

    async def admins_dynamic_entity_keyboard(self, callback_data: str) -> list:
        add_btn_text = self.buttons['admin']['general']['add']
        edit_btn_text = self.buttons['admin']['general']['edit']['main']
        delete_btn_text = self.buttons['admin']['general']['delete']

        add_btn_clb_data = self.callback_data['admin']['general']['add'] + callback_data.rsplit("-", 1)[0]
        edit_btn_clb_data = self.callback_data['admin']['general']['edit']['main'] + callback_data
        delete_btn_clb_data = self.callback_data['admin']['general']['delete'] + callback_data

        return [
            InlineKeyboardButton(text=add_btn_text, callback_data=add_btn_clb_data),
            InlineKeyboardButton(text=edit_btn_text, callback_data=edit_btn_clb_data),
            InlineKeyboardButton(text=delete_btn_text, callback_data=delete_btn_clb_data)
        ]
