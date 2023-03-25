from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(sa.Identity(start=1, cycle=True), primary_key=True, index=True,)
    created_at: Mapped[datetime] = mapped_column(default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(default=sa.func.now(), onupdate=sa.func.now())
