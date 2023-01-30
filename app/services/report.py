from app.common.http_methods import GET
from flask import Blueprint

from app.services.base import BaseService

from ..controllers import ReportController

report = Blueprint('report', __name__)
service = BaseService(ReportController)


@report.route('/', methods=GET)
def get_report():
    return service.get_all()
