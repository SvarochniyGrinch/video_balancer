from .models import CamelModel
from pydantic import Field


class PaginationParams(CamelModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100, validation_alias="perPage")


__all__ = [
    "PaginationParams",
]
