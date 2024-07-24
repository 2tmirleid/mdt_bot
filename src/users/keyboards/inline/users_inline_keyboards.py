from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class UsersInlineKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def users_dynamic_entity_to_main_menu_panel_keyboard(
            self, markup: bool = False
    ) -> list or InlineKeyboardMarkup:

        back_to_main_menu_btn = self.buttons['user']['to_main_panel']
        back_to_main_menu_clb_data = self.callback_data['user']['to_main_panel']

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

    async def users_profile_inline_keyboard(self, profile_id) -> list:
        return [
            InlineKeyboardButton(text=self.buttons['user']['profile']['edit']['main'],
                                 callback_data=self.callback_data['user']['profile']['edit']['main'] + f"-{profile_id}")
        ]

    async def users_edit_profile_inline_keyboard(self) -> list:
        photo_btn_text =      self.buttons['user']['profile']['edit']['photo']
        # phone_btn_text =      self.buttons['user']['profile']['edit']['phone']
        full_name_btn_text =  self.buttons['user']['profile']['edit']['full_name']

        birth_date_btn_text = self.buttons['user']['profile']['edit']['birth_date']
        city_btn_text =       self.buttons['user']['profile']['edit']['city']
        company_btn_text =    self.buttons['user']['profile']['edit']['company']

        position_btn_text =   self.buttons['user']['profile']['edit']['position']
        rm_status_btn_text =  self.buttons['user']['profile']['edit']['rm_status']
        hobbies_btn_text =    self.buttons['user']['profile']['edit']['hobbies']

        resources_btn_text =  self.buttons['user']['profile']['edit']['resources']
        expertise_btn_text =  self.buttons['user']['profile']['edit']['expertise']

        #  Callback_data_btns
        photo_btn_clb_data =      self.callback_data['user']['profile']['edit']['photo']
        # phone_btn_clb_data =      self.callback_data['user']['profile']['edit']['phone']
        full_name_btn_clb_data =  self.callback_data['user']['profile']['edit']['full_name']

        birth_date_btn_clb_data = self.callback_data['user']['profile']['edit']['birth_date']
        city_btn_clb_data =       self.callback_data['user']['profile']['edit']['city']
        company_btn_clb_data =    self.callback_data['user']['profile']['edit']['company']

        position_btn_clb_data =   self.callback_data['user']['profile']['edit']['position']
        rm_status_btn_clb_data =  self.callback_data['user']['profile']['edit']['rm_status']
        hobbies_btn_clb_data =    self.callback_data['user']['profile']['edit']['hobbies']

        resources_btn_clb_data =  self.callback_data['user']['profile']['edit']['resources']
        expertise_btn_clb_data =  self.callback_data['user']['profile']['edit']['expertise']

        return [
            [
                InlineKeyboardButton(text=photo_btn_text, callback_data=photo_btn_clb_data),
                # InlineKeyboardButton(text=phone_btn_text, callback_data=phone_btn_clb_data),
                InlineKeyboardButton(text=full_name_btn_text, callback_data=full_name_btn_clb_data)
            ],
            [
                InlineKeyboardButton(text=birth_date_btn_text, callback_data=birth_date_btn_clb_data),
                InlineKeyboardButton(text=city_btn_text, callback_data=city_btn_clb_data),
                InlineKeyboardButton(text=company_btn_text, callback_data=company_btn_clb_data)
            ],
            [
                InlineKeyboardButton(text=position_btn_text, callback_data=position_btn_clb_data),
                InlineKeyboardButton(text=rm_status_btn_text, callback_data=rm_status_btn_clb_data),
                InlineKeyboardButton(text=hobbies_btn_text, callback_data=hobbies_btn_clb_data)
            ],
            [
                InlineKeyboardButton(text=resources_btn_text, callback_data=resources_btn_clb_data),
                InlineKeyboardButton(text=expertise_btn_text, callback_data=expertise_btn_clb_data)
            ]
        ]

    async def users_get_search_property(self) -> list:
        full_name_btn_text = self.buttons['user']['residents']['full_name']
        resources_btn_text = self.buttons['user']['residents']['resources']
        city_btn_text = self.buttons['user']['residents']['city']
        company_btn_text = self.buttons['user']['residents']['company']

        full_name_btn_clb_data = self.callback_data['user']['residents']['full_name']
        resources_btn_clb_data = self.callback_data['user']['residents']['resources']
        city_btn_clb_data = self.callback_data['user']['residents']['city']
        company_btn_clb_data = self.callback_data['user']['residents']['company']

        return [
            [
                InlineKeyboardButton(text=full_name_btn_text, callback_data=full_name_btn_clb_data),
                InlineKeyboardButton(text=resources_btn_text, callback_data=resources_btn_clb_data)
            ],
            [
                InlineKeyboardButton(text=city_btn_text, callback_data=city_btn_clb_data),
                InlineKeyboardButton(text=company_btn_text, callback_data=company_btn_clb_data)
            ]
        ]
