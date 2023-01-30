import pytest

from app.controllers import ReportController, OrderController


def test_report_get_all(app, order):
    _, error_order = OrderController.create(order)
    report, error = ReportController.get_report()
    pytest.assume(error is None)
    pytest.assume(error_order is None)
    pytest.assume(report.get('most_popular_ingredient'))
    pytest.assume(report.get('most_popular_beverage'))
    pytest.assume(report.get('most_popular_size'))
    pytest.assume(report.get('best_month'))
    pytest.assume(report.get('more_orders_customers'))
    pytest.assume(report.get('more_purchases_customers'))


def test_get_report_AttributeError_when_db_is_empty(app):
    controller = ReportController()
    _, error = controller.get_report()
    pytest.assume(error is not None)
