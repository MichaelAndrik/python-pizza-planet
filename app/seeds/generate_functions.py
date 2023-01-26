import json
import random
from faker import Faker
from datetime import datetime

from app.repositories.models import Order, OrderBeverage, OrderIngredient
from app.controllers import BeverageController, SizeController,\
    IngredientController, OrderController


class Generate():

    @classmethod
    def generate_size_ingredient_and_beverage(cls, model, path_data: str) -> list:
        fake = []
        items = cls.get_data(path_data)
        for item in items:
            fake.append(
                model(
                    name=item["name"],
                    price=item["price"]
                )
            )
        return fake

    @classmethod
    def generate_orders(cls, total_orders: int, path_data: str) -> list:
        fake_order = []
        fake_order_ingredient = []
        fake_order_beverage = []
        sizes, error = SizeController.get_all()
        all_ingredients, error = IngredientController.get_all()
        all_beverages, error = BeverageController.get_all()

        for order_count in range(1, total_orders + 1):
            size = sizes[random.randint(0, len(sizes)-1)]
            ingredients = cls.get_random_ingredients_beverages(all_ingredients)
            beverages = cls.get_random_ingredients_beverages(all_beverages)

            fake_order.append(
                Order(
                    _id=order_count,
                    client_name=cls.get_name(path_data),
                    client_dni="DNI",
                    client_address=Faker().address(),
                    client_phone=Faker().phone_number(),
                    date=cls.get_date(),
                    total_price=OrderController.calculate_order_price(
                        size.get('price'),
                        ingredients,
                        beverages
                    ),
                    size_id=size.get('_id')
                )
            )

            fake_order_ingredient.append([
                OrderIngredient(
                    order_id=order_count,
                    ingredient_id=ingredient.get('_id'),
                    ingredient_price=ingredient.get('price')
                ) for ingredient in ingredients
            ])

            fake_order_beverage.append([
                OrderBeverage(
                    order_id=order_count,
                    beverage_id=beverage.get('_id'),
                    beverage_price=beverage.get('price')
                ) for beverage in beverages
            ])

        return fake_order, fake_order_beverage, fake_order_ingredient

    @staticmethod
    def get_random_ingredients_beverages(items: list) -> list:
        items_count = random.randint(1, len(items)-1)
        items_random = random.sample(items, k=items_count)
        return items_random

    @staticmethod
    def get_name(path_data: str) -> str:
        with open(path_data) as file:
            _file = json.load(file).get('names')
            return _file[Faker().pyint(max_value=len(_file)-1)]

    @staticmethod
    def get_date() -> datetime:
        date_random = Faker().date_time_between(
            start_date=datetime(2022, 1, 1),
            end_date=datetime(2022, 12, 12)
        )
        return date_random

    @staticmethod
    def get_data(path_data: str) -> list:
        with open(path_data) as file:
            return json.load(file).get('data')
