import calendar
from typing import Any, List, Optional, Sequence
from sqlalchemy.sql import text, column
from sqlalchemy import func, desc

from .models import Ingredient, Order, OrderIngredient, Size, Beverage, OrderBeverage, db
from .serializers import (IngredientSerializer, OrderBeverageSerializer, OrderIngredientSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        serializer = cls.serializer(many=True)
        _objects = cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        result = serializer.dump(_objects)
        return result


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        serializer = cls.serializer(many=True)
        _objects = cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        result = serializer.dump(_objects)
        return result


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
        most_requested_size={}
        item = cls.session.query(Size.name, func.count(cls.model.size_id).label('times')).\
        join(cls.model).\
        group_by(Size.name).\
        order_by(desc('times')).\
        first()

        if item is not None:
            most_requested_size = {
                "size": item.name,
                "times": item.times
            }
            
        return most_requested_size
    
    @classmethod
    def get_month_with_more_revenue(cls) -> list:
        month_with_more_revenue = {}
        order = cls.session.query(func.strftime('%m', cls.model.date).label('month'), func.sum(cls.model.total_price).label('total_revenue')).\
        group_by('month').\
        order_by(desc('total_revenue')).\
        first()

        if order is not None:
            month_with_more_revenue = {
                "month": calendar.month_name[int(order.month)],
                "total_sales": order.total_revenue 
            }
            
        return month_with_more_revenue
    
    @classmethod
    def get_more_orders_customers(cls) -> list:
        customers = []
        orders = cls.session.query(cls.model.client_name, func.count(cls.model.client_name).label('orders_count')).\
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
        orders = cls.session.query(cls.model.client_name, func.sum(cls.model.total_price).label('total_sales')).\
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


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class OrderIngredientManager(BaseManager):
    serializer = OrderIngredientSerializer
    model = OrderIngredient

    @classmethod
    def get_most_request_ingredient(cls) -> list:
        most_requested_ingredient={}
        item = cls.session.query(Ingredient.name, func.count(cls.model.ingredient_id).label('times')).\
        join(cls.model).\
        group_by(Ingredient.name).\
        order_by(desc('times')).\
        first()

        if item is not None:
            most_requested_ingredient = {
                "ingredient": item.name,
                "times": item.times,
            }
            
        return most_requested_ingredient


class OrderBeverageManager(BaseManager):
    serializer = OrderBeverageSerializer
    model = OrderBeverage

    @classmethod
    def get_most_request_beverage(cls) -> list:
        most_requested_beverage = {}
        item = cls.session.query(Beverage.name, func.count(cls.model.beverage_id).label('times')).\
        join(cls.model).\
        group_by(Beverage.name).\
        order_by(desc('times')).\
        first()
        
        if item is not None:
            most_requested_beverage = {
                "beverage": item.name,
                "times": item.times, 
            }
            
        return most_requested_beverage


class ReportManager(BaseManager):

    @classmethod
    def get_all_report(cls):
        result = {
            "most_popular_ingredient": OrderIngredientManager.get_most_request_ingredient(),
            "most_popular_beverage": OrderBeverageManager.get_most_request_beverage(),
            "most_popular_size": OrderManager.get_most_request_size(),
            "best_month": OrderManager.get_month_with_more_revenue(),
            "more_orders_customers": OrderManager.get_more_orders_customers(),
            "more_purchases_customers": OrderManager.get_more_purchases_customers()
        }
        return result
