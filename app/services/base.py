from typing import Optional
from flask import jsonify

from ..controllers.base import BaseController


class BaseService:

    def __init__(self, controller):
        self.controller: Optional[BaseController] = controller

    def service_response(self, result, error):
        response = result if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code

    def get_all(self):
        result, error = self.controller.get_all()
        return self.service_response(result, error)

    def get_by_id(self, _id):
        result, error = self.controller.get_by_id(_id)
        return self.service_response(result, error)

    def create(self, request):
        result, error = self.controller.create(request)
        return self.service_response(result, error)

    def update(self, request):
        result, error = self.controller.update(request)
        return self.service_response(result, error)
