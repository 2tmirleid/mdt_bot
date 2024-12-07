from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class AdminsReplyKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")

    async def to_main_admins_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.buttons['admin']['to_main_panel'])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def main_admins_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.buttons['admin']['main_panel']['forms']['main']),
                    KeyboardButton(text=self.buttons['admin']['main_panel']['events']['main'])
                ],
                [
                    # KeyboardButton(text=self.buttons['admin']['main_panel']['random_coffee']['main'])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def forms_admins_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.buttons['admin']['main_panel']['forms']['new'])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def admins_events_city_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.buttons['admin']['main_panel']['events']['city']['saransk']),
                 KeyboardButton(text=self.buttons['admin']['main_panel']['events']['city']['moscow'])],
                [KeyboardButton(text=self.buttons['admin']['to_main_panel'])]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def admins_random_coffee_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.buttons['admin']['main_panel']['random_coffee']['subscribed']),
                    KeyboardButton(text=self.buttons['admin']['main_panel']['random_coffee']['unsubscribed'])
                ],
                [
                    KeyboardButton(text=self.buttons['admin']['to_main_panel'])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

