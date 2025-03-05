from .settings import *
from services.CDN_settings import CDNSettingsService
from shared.schemas.CDN import *
from fastapi import APIRouter, Depends, status


router = APIRouter(tags=["CDN",], prefix=PREFIX)


@router.put(
    path=Paths.Create,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.Create},
        status.HTTP_400_BAD_REQUEST: {},
    },
)
async def create(
    body: bodies.Create,
    service: CDNSettingsService = Depends(),
):
    return await service.create(body)


@router.get(
    path=Paths.Read,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Read},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def read(
    params: params.Read = Depends(),
    service: CDNSettingsService = Depends(),
):
    return await service.read(params)


@router.patch(
    path=Paths.Update,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Update},
        status.HTTP_400_BAD_REQUEST: {},
        status.HTTP_404_NOT_FOUND: {},
    },
)
async def update(
    body: bodies.Update,
    params: params.Update = Depends(),
    service: CDNSettingsService = Depends(),
):
    return await service.update(params, body)


# @router.get(
#     path=Paths.List,
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_200_OK: {"model": responses.Read},
#     },
# )
# async def list(
#     params: params.List = Depends(),
#     service: CDNSettingsService = Depends(),
# ):
#     return await service.list(params)
