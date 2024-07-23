from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class UsersReplyKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")

    async def users_to_main_panel_reply_keyboard(self, markup=False) -> ReplyKeyboardMarkup or list:
        if markup:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=self.buttons['user']['to_main_panel'])]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        else:
            return [
                KeyboardButton(text=self.buttons['user']['to_main_panel'])
            ]

    async def users_start_command_reply_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.buttons['user']['start'])]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def users_start_register_reply_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.buttons['user']['register']['start'])]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def users_send_phone_number_reply_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.buttons['user']['register']['phone'],
                                request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def users_main_menu_panel_reply_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.buttons['user']['main_panel']['profile']),
                    KeyboardButton(text=self.buttons['user']['main_panel']['residents']),
                ],
                [
                    KeyboardButton(text=self.buttons['user']['main_panel']['about']),
                    KeyboardButton(text=self.buttons['user']['main_panel']['contacts']),
                ],
                [
                    KeyboardButton(text=self.buttons['user']['main_panel']['calendar'])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def users_contacts_reply_keyboard(self) -> list:
        return [
                 KeyboardButton(text=self.buttons['user']['contacts']['ceo']),
                 KeyboardButton(text=self.buttons['user']['contacts']['moderator'])
            ]
