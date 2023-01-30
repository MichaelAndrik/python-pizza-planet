from ..repositories.manager import IngredientManager
from .base import BaseController


class IngredientController(BaseController):
    manager = IngredientManager
