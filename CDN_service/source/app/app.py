from services.CDN_settings import *
from shared.schemas.CDN import *
from fastapi import APIRouter, Depends, status
from app.CDN_settings import router as api_router
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(title="CDN", root_path="/")  # noqa
app.include_router(api_router)


@app.get("/")
async def root(
        params: params.GetVideo = Depends(),
        service: CDNSettingsService = Depends(),
):
    url = await service.get_redirect(params.video)
    return RedirectResponse(url, status_code=301)