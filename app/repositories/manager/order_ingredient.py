from sqlalchemy import func, desc

from .base import BaseManager
from ..models import OrderIngredient, Ingredient
from ..serializer import OrderIngredientSerializer


class OrderIngredientManager(BaseManager):
    serializer = OrderIngredientSerializer
    model = OrderIngredient

    @classmethod
    def get_most_request_ingredient(cls) -> list:
        item = cls.session.query(
            Ingredient.name,
            func.count(cls.model.ingredient_id).label('times')
            ).\
            join(cls.model).\
            group_by(Ingredient.name).\
            order_by(desc('times')).\
            first()

        most_requested_ingredient = {
            "ingredient": item.name,
            "times": item.times,
        }

        return most_requested_ingredient
