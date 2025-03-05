from services.CDN_settings import *
from shared.schemas.CDN import *
from fastapi import APIRouter, Depends, status
from app.api import router as api_router
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(title="CDN", root_path="/")  # noqa
app.include_router(api_router)



router = APIRouter(tags=["CDN",],)


@router.put(
    path="/create_setting",
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
    path="/get_setting",
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
    path="/update_setting",
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


@router.get(
    path="/get_all",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Read},
    },
)
async def list(
    params: params.List = Depends(),
    service: CDNSettingsService = Depends(),
):
    return await service.list(params)


@app.get("/")
async def root(
        params: params.GetVideo = Depends(),
        service: CDNSettingsService = Depends(),
):
    url = await service.get_redirect(params.video)
    return RedirectResponse(url, status_code=301)