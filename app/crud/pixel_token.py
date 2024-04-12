from app.crud.base import CRUDBase
from app.models.activity_log import PixelToken


class CRUDPixelToken(CRUDBase):
    pass


pixel_token_crud = CRUDPixelToken(PixelToken)
