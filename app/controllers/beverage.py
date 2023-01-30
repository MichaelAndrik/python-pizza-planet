from ..repositories.manager import BeverageManager
from .base import BaseController


class BeverageController(BaseController):
    manager = BeverageManager
