from .common import CDNsettings
from shared.schemas.common import CRUDResponse, ListResponse


Create = CRUDResponse[CDNsettings]
Read = CRUDResponse[CDNsettings]
Update = CRUDResponse[CDNsettings]
List = ListResponse[CDNsettings]
Get = CRUDResponse[CDNsettings]


__all__ = [
    "Create",
    "Read",
    "Update",
    "List",
    "Get",
]
