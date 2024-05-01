from app.crud.base import CRUDBase
from app.models.activity_log import FlowParams


class CRUDFlowParams(CRUDBase):
    pass


flow_params_crud = CRUDFlowParams(FlowParams)
