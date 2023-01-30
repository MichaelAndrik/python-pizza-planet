from app.plugins import ma

from ..models import OrderIngredient
from ..serializer import IngredientSerializer


class OrderIngredientSerializer(ma.SQLAlchemyAutoSchema):

    ingredient = ma.Nested(IngredientSerializer)

    class Meta:
        model = OrderIngredient
        load_instance = True
        fields = (
            'ingredient_price',
            'ingredient'
        )
