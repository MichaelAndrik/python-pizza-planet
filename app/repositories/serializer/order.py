from app.plugins import ma

from .size import SizeSerializer
from .order_beverage import OrderBeverageSerializer
from .order_ingredient import OrderIngredientSerializer
from ..models import Order


class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    order_ingredient = ma.Nested(OrderIngredientSerializer, many=True)
    order_beverage = ma.Nested(OrderBeverageSerializer, many=True)

    class Meta:
        model = Order
        load_instance = True
        fields = (
            '_id',
            'client_name',
            'client_dni',
            'client_address',
            'client_phone',
            'date',
            'total_price',
            'size',
            'order_ingredient',
            'order_beverage'
        )
