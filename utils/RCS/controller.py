from abc import ABC

from utils.RCS.pagen import Pagen


class Controller(Pagen, ABC):
    def __init__(self):
        super().__init__()

