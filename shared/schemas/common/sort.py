from .models import CamelModel
from pydantic import Field
from enum import Enum


class SortOrder(str, Enum):
    Asc = "asc"
    Desc = "desc"


class SortParams(CamelModel):
    sort_by: str | None = Field(None, validation_alias="sortBy")
    sort_order: SortOrder = Field(SortOrder.Asc, validation_alias="sortOrder")

    def __bool__(self):
        return self.sort_by is not None


__all__ = [
    "SortOrder",
    "SortParams",
]
