from shared.schemas.common import CamelModel

class CDNsettings(CamelModel):
    id: int
    cdn_host: str
    period: int


__all__ = [
    "CDNsettings",
]
