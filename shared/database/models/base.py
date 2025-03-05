from sqlalchemy.orm import declarative_base, Mapped, mapped_column

SQLBase = declarative_base()


class Base(SQLBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(primary_key=True)


