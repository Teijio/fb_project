from app.crud.base import CRUDBase
from app.models.activity_log import Application


class CRUDApplication(CRUDBase):
    pass


application_crud = CRUDApplication(Application)
