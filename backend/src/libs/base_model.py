from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Basic SqlAlchemy Model

    :param id: int
    :param created_at: timestamp - static
    :param updated_at: timestamp - dynamic

    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
