from ..manager import OrderManager, BaseManager,\
    OrderIngredientManager, OrderBeverageManager


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
