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

    async def admins_dynamic_create_inline_keyboard(self, callback_data: str) -> list:
        add_btn_text = self.buttons['admin']['general']['add']
        add_btn_clb_data = self.callback_data['admin']['general']['add'] + callback_data.rsplit("-", 1)[0]

        return [
            InlineKeyboardButton(text=add_btn_text, callback_data=add_btn_clb_data)
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

    async def admins_events_add_city_inline_keyboard(self) -> list:
        saransk_btn_text = self.buttons['admin']['main_panel']['events']['city']['saransk']
        moscow_btn_text = self.buttons['admin']['main_panel']['events']['city']['moscow']

        saransk_btn_clb_data = self.callback_data['admin']['main_panel']['events']['city']['add']['saransk']
        moscow_btn_clb_data = self.callback_data['admin']['main_panel']['events']['city']['add']['moscow']

        return [
            [InlineKeyboardButton(text=saransk_btn_text, callback_data=saransk_btn_clb_data),
             InlineKeyboardButton(text=moscow_btn_text, callback_data=moscow_btn_clb_data)]
        ]
 
    async def admins_events_edit_city_inline_keyboard(self) -> list:
        saransk_btn_text = self.buttons['admin']['main_panel']['events']['city']['saransk']
        moscow_btn_text = self.buttons['admin']['main_panel']['events']['city']['moscow']

        saransk_btn_clb_data = self.callback_data['admin']['main_panel']['events']['city']['edit']['saransk']
        moscow_btn_clb_data = self.callback_data['admin']['main_panel']['events']['city']['edit']['moscow']

        return [
            [InlineKeyboardButton(text=saransk_btn_text, callback_data=saransk_btn_clb_data),
             InlineKeyboardButton(text=moscow_btn_text, callback_data=moscow_btn_clb_data)]
        ]

    async def admins_export_event_inline_keyboard(self, callback_data: str) -> list:
        export_btn_text = self.buttons['admin']['general']['export']

        export_btn_clb_data = self.callback_data['admin']['general']['export'] + callback_data

        return [
            InlineKeyboardButton(text=export_btn_text, callback_data=export_btn_clb_data)
        ]

    async def admins_edit_events_inline_keyboard(self) -> list:
        photo_btn_text = self.buttons['admin']['main_panel']['edit']['events']['photo']
        title_btn_text = self.buttons['admin']['main_panel']['edit']['events']['title']
        city_btn_text = self.buttons['admin']['main_panel']['edit']['events']['city']
        description_btn_text = self.buttons['admin']['main_panel']['edit']['events']['description']
        event_date_btn_text = self.buttons['admin']['main_panel']['edit']['events']['event_date']
        activity_btn_text = self.buttons['admin']['main_panel']['edit']['events']['is_active']

        photo_btn_clb_data = self.callback_data['admin']['main_panel']['edit']['events']['photo']
        title_btn_clb_data = self.callback_data['admin']['main_panel']['edit']['events']['title']
        city_btn_clb_data = self.callback_data['admin']['main_panel']['edit']['events']['city']
        description_btn_clb_data = self.callback_data['admin']['main_panel']['edit']['events']['description']
        event_date_btn_clb_data = self.callback_data['admin']['main_panel']['edit']['events']['event_date']
        activity_btn_clb_data = self.callback_data['admin']['main_panel']['edit']['events']['is_active']

        return [
            [InlineKeyboardButton(text=photo_btn_text, callback_data=photo_btn_clb_data),
             InlineKeyboardButton(text=title_btn_text, callback_data=title_btn_clb_data),
             InlineKeyboardButton(text=city_btn_text, callback_data=city_btn_clb_data)],
            [InlineKeyboardButton(text=description_btn_text, callback_data=description_btn_clb_data),
             InlineKeyboardButton(text=event_date_btn_text, callback_data=event_date_btn_clb_data),
             InlineKeyboardButton(text=activity_btn_text, callback_data=activity_btn_clb_data)]
        ]
