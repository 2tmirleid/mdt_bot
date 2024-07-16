from abc import abstractmethod

from utils.lexicon.load_lexicon import load_lexicon


class Pagen:
    def __init__(self):
        self.lexicon = load_lexicon()

        # self.buttons = self.lexicon.get("buttons")
        # self.buttons = self.lexicon.get("callback_data")

    @abstractmethod
    async def build_admins_pagen(self) -> list:
        pass

    @abstractmethod
    async def build_users_pagen(self) -> list:
        pass
