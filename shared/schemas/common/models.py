from shared.utils import to_camel_case, to_pascal_case
from pydantic import BaseModel, ConfigDict


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )


class PascalModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_pascal_case,
        populate_by_name=True,
    )


__all__ = [
    "CamelModel",
    "PascalModel",
]
