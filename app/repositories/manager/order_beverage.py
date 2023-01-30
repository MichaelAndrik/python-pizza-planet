from sqlalchemy import func, desc

from ..manager import BaseManager
from ..models import OrderBeverage, Beverage
from ..serializer import OrderBeverageSerializer


class OrderBeverageManager(BaseManager):
    serializer = OrderBeverageSerializer
    model = OrderBeverage

    @classmethod
    def get_most_request_beverage(cls) -> list:
        item = cls.session.query(
            Beverage.name,
            func.count(cls.model.beverage_id).label('times')
            ).\
            join(cls.model).\
            group_by(Beverage.name).\
            order_by(desc('times')).\
            first()

        most_requested_beverage = {
            "beverage": item.name,
            "times": item.times
        }

        return most_requested_beverage
