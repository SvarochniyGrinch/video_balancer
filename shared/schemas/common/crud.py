from .models import CamelModel


class CRUDResponse[T](CamelModel):
    item: T


__all__ = [
    "CRUDResponse",
]
