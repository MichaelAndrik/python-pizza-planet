from ..repositories.manager import SizeManager
from .base import BaseController


class SizeController(BaseController):
    manager = SizeManager
