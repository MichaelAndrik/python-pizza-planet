from typing import Sequence

from ..manager import BaseManager
from ..models import Beverage
from ..serializer import BeverageSerializer


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        serializer = cls.serializer(many=True)
        _objects = cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        result = serializer.dump(_objects)
        return result
