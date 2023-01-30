from ..manager import BaseManager
from ..models import Size
from ..serializer import SizeSerializer


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer
