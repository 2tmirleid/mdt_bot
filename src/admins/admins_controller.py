from abc import ABC

from utils.RCS.controller import Controller


class AdminsController(Controller, ABC):
    def __init__(self):
        super().__init__()


