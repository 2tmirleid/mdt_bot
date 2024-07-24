from abc import abstractmethod

from aiogram.types import InlineKeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class Pagen:
    def __init__(self):
        self.lexicon = load_lexicon()

        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def build_admins_pagen(self, pages: int, callback_data: str, offset=0) -> list:
        if pages > 0:
            buttons = []

            backward_btn_text = self.buttons['pagen']['backward']
            next_btn_text = self.buttons['pagen']['next']

            start_btn_text = self.buttons['pagen']['start']
            end_btn_text = self.buttons['pagen']['end']

            backward_clb_data = self.callback_data['admin']['pagen']['backward'] + callback_data
            next_clb_data = self.callback_data['admin']['pagen']['next'] + callback_data

            start_clb_data = self.callback_data['admin']['pagen']['start'] + callback_data
            end_clb_data = self.callback_data['admin']['pagen']['end'] + callback_data

            if offset > 0:
                buttons.append(InlineKeyboardButton(text=start_btn_text,
                                                    callback_data=start_clb_data))
                buttons.append(InlineKeyboardButton(text=backward_btn_text,
                                                    callback_data=backward_clb_data))
            if pages > offset + 1:
                buttons.append(InlineKeyboardButton(text=next_btn_text,
                                                    callback_data=next_clb_data))
                buttons.append(InlineKeyboardButton(text=end_btn_text,
                                                    callback_data=end_clb_data))

            return buttons

    async def build_users_pagen(self, pages: int, callback_data: str, offset=0) -> list:
        if pages > 0:
            buttons = []

            backward_btn_text = self.buttons['pagen']['backward']
            next_btn_text = self.buttons['pagen']['next']

            start_btn_text = self.buttons['pagen']['start']
            end_btn_text = self.buttons['pagen']['end']

            backward_clb_data = self.callback_data['user']['pagen']['backward'] + callback_data
            next_clb_data = self.callback_data['user']['pagen']['next'] + callback_data

            start_clb_data = self.callback_data['user']['pagen']['start'] + callback_data
            end_clb_data = self.callback_data['user']['pagen']['end'] + callback_data

            if offset > 0:
                buttons.append(InlineKeyboardButton(text=start_btn_text,
                                                    callback_data=start_clb_data))
                buttons.append(InlineKeyboardButton(text=backward_btn_text,
                                                    callback_data=backward_clb_data))
            if pages > offset + 1:
                buttons.append(InlineKeyboardButton(text=next_btn_text,
                                                    callback_data=next_clb_data))
                buttons.append(InlineKeyboardButton(text=end_btn_text,
                                                    callback_data=end_clb_data))

            return buttons
