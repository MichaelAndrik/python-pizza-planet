import calendar
from typing import List
from sqlalchemy import func, desc

from ..manager import BaseManager
from ..models import Order, Ingredient, OrderBeverage,\
    OrderIngredient, Size, Beverage
from ..serializer import OrderSerializer


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all(
            (
                OrderIngredient(
                    order_id=new_order._id,
                    ingredient_id=ingredient.get('_id'),
                    ingredient_price=ingredient.get('price')
                ) for ingredient in ingredients
            )
        )
        cls.session.add_all(
            (
                OrderBeverage(
                    order_id=new_order._id,
                    beverage_id=beverage.get('_id'),
                    beverage_price=beverage.get('price')
                ) for beverage in beverages
            )
        )
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')

    @classmethod
    def get_most_request_size(cls) -> list:
        item = cls.session.query(Size.name, func.count(cls.model.size_id).label('times')).\
            join(cls.model).\
            group_by(Size.name).\
            order_by(desc('times')).\
            first()

        most_requested_size = {
            "size": item.name,
            "times": item.times
        }

        return most_requested_size

    @classmethod
    def get_month_with_more_revenue(cls) -> list:
        order = cls.session.query(
            func.strftime('%m', cls.model.date).label('month'),
            func.sum(cls.model.total_price).label('total_revenue')
            ).\
            group_by('month').\
            order_by(desc('total_revenue')).\
            first()

        month_with_more_revenue = {
            "month": calendar.month_name[int(order.month)],
            "total_sales": order.total_revenue
        }

        return month_with_more_revenue

    @classmethod
    def get_more_orders_customers(cls) -> list:
        customers = []
        orders = cls.session.query(
            cls.model.client_name,
            func.count(cls.model.client_name).label('orders_count')
            ).\
            group_by(cls.model.client_name).\
            order_by(desc('orders_count')).\
            limit(3)

        if orders is not None:
            for order in orders:
                customers.append({
                    "orders": order.orders_count,
                    "client_name": order.client_name
                })

        return customers

    @classmethod
    def get_more_purchases_customers(cls) -> list:
        customers = []
        orders = cls.session.query(
            cls.model.client_name,
            func.sum(cls.model.total_price).label('total_sales')
            ).\
            group_by(cls.model.total_price).\
            order_by(desc('total_sales')).\
            limit(3)

        if orders is not None:
            for order in orders:
                customers.append({
                    "orders": order.total_sales,
                    "client_name": order.client_name
                })

        return customers
