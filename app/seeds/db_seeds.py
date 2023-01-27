from flask_seeder import Seeder

from app.repositories.models import Ingredient, Size, Beverage
from app.seeds.generate_functions import Generate


path_clients = "app/seeds/files/client_name.json"
path_sizes = "app/seeds/files/sizes.json"
path_beverages = "app/seeds/files/beverages.json"
path_ingredients = "app/seeds/files/ingredients.json"
total_orders = 100


class DbSeeder(Seeder):

    def run(self):
        ingredients = Generate.generate_size_ingredient_and_beverage(Ingredient, path_ingredients)
        sizes = Generate.generate_size_ingredient_and_beverage(Size, path_sizes)
        beverages = Generate.generate_size_ingredient_and_beverage(Beverage, path_beverages)

        # Add ingredients, sizes and beverage to db
        self.add_items_db(ingredients)
        self.add_items_db(sizes)
        self.add_items_db(beverages)

        orders, order_beverage, order_ingredient = Generate.generate_orders(
            total_orders, path_clients
        )
        self.add_items_db(orders)
        self.add_items_orders_db(order_beverage)
        self.add_items_orders_db(order_ingredient)

    def add_items_db(self, fake_data):
        for item in fake_data:
            self.db.session.add(item)

    def add_items_orders_db(self, fake_data):
        for item in fake_data:
            for _item in item:
                self.db.session.add(_item)
