from sqlalchemy.orm import mapped_column, Mapped

from core.models import Base


class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str]
    is_done: Mapped[bool] = mapped_column(default=False)
