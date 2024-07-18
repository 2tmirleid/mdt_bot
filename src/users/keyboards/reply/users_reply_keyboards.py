from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class UsersReplyKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")

    async def users_start_command_reply_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.buttons['user']['start'])]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
