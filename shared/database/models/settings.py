from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class CDNSettings(Base):
    __tablename__ = "cdn_settings"

    cdn_host: Mapped[str] = mapped_column(default="cdn.example.com")
    period: Mapped[int] = mapped_column(default=1)
