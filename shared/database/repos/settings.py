from .base import BaseRepo
from shared.database.models import CDNSettings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CDNSettingsRepo(BaseRepo[CDNSettings]):
    model = CDNSettings

    async def _create(self):
        cdn = CDNSettings(cdn_host="cdn.example.com", period=5)
        self.session.add(cdn)
        return cdn

    async def get_or_create(self):
        prompt = select(CDNSettings).limit(1)
        result = await self.session.execute(prompt)
        cdn: CDNSettings = result.scalars().one_or_none()
        if cdn is None:
            cdn = await self._create()
        await self.session.commit()
        return cdn