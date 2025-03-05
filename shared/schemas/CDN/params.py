from shared.schemas.common import CamelModel, ListParams
from fastapi import Depends, Path


class Read(CamelModel):
    id: int = Path()


class Update(CamelModel):
    id: int = Path()


class List(ListParams):
    ...


class GetVideo(CamelModel):
    video: str = Path()
    


__all__ = [
    "Read",
    "Update",
    "List",
    "GetVideo",
]
