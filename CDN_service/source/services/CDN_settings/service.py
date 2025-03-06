from shared.database.repos import CDNSettingsRepo
from shared.schemas.CDN import *
from fastapi import Depends, HTTPException, status
from typing import TYPE_CHECKING

COUNTER = 0

if TYPE_CHECKING:
    from shared.database.models import CDNSettings as CDNModel


class CDNSettingsService:
    def __init__(
        self,
        repo: CDNSettingsRepo = Depends(),
    ):
        self.repo = repo

    async def create(self, body: bodies.Create) -> responses.Create:
        obj = await self.repo.new(**body.model_dump(mode="json"),)
        if obj is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Some conflicts caused")  # noqa
        return responses.Create(item=CDNsettings.model_validate(obj, from_attributes=True))

    async def read(self, params: params.Read) -> responses.Read:
        obj = await self._get_object(1)
        return responses.Read(item=CDNsettings.model_validate(obj, from_attributes=True))

    async def _get_object(self, id: int) -> "CDNModel":
        obj = await self.repo.get(id=id)
        if obj is None:
            return None
            # raise HTTPException(status.HTTP_404_NOT_FOUND, "Setting not found")  # noqa
        return obj

    async def update(self, params: params.Update, body: bodies.Update) -> responses.Update:
        obj = await self._get_object(1)
        if obj is None:
            new_data = body.model_dump(exclude_none=True, exclude={'id'})
            new_data['id'] = 1  # Фиксируем id=1
            new_obj = await self.repo.new(**new_data,)
            obj = await self.repo.create(new_obj)
            if obj is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create CDN settings")
        else:
            obj = await self.repo.update(obj, **body.model_dump(exclude_none=True),)
            if obj is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Some conflicts caused")  # noqa
        return responses.Update(item=CDNsettings.model_validate(obj, from_attributes=True))

    async def list(self, params: params.List) -> responses.List:
        items, total = await self.repo.list(params, **params.filters.model_dump(exclude_none=True),)
        return responses.List(
            items=[CDNsettings.model_validate(
                item, from_attributes=True) for item in items],
            total=total,
        )
    
    def _get_host(self, url: str):
        host = url.split("/")[2]
        return host

    def _get_bucket_name(self, host: str):
        bucket_name = host.split(".")[0]
        return bucket_name

    def _get_video_path(self, url: str):
        video_path = "/".join(url.split("/")[3:])
        return video_path

    async def _redirect_in_cdn(self, url: str):
        config = await self.repo.get_or_create()
        video_path = self._get_video_path(url)
        host = self._get_host(url)
        bucket_name = self._get_bucket_name(host)
        url = f"https://{config.cdn_host}/{bucket_name}/{video_path}"
        return url

    async def get_redirect(self, url: str):
        global COUNTER
        config = await self.repo.get_or_create()

        COUNTER+= 1

        if config.period <= 0 or COUNTER % config.period == 0:
            COUNTER = 0
            return url
        return await self._redirect_in_cdn(url)
    
    # http://localhost:8000/?video=http://s1.origin-cluster/video/1488/xcg2djHckad.m3u8
