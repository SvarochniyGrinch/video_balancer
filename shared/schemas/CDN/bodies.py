from shared.schemas.common import CamelModel
from typing import Any


class Create(CamelModel):
    cdn_host: str
    period: int


class Update(CamelModel):
    cdn_host: str | None = None
    period: int | None = None


class Get(CamelModel):
    ...


__all__ = [
    "Create",
    "Update",
    "Get",
]
