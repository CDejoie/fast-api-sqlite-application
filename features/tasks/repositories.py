from fastapi import Depends

from app.db import get_db
from core.repositories import ModelRepository
from features.tasks.models import Task


class TaskRepository(ModelRepository):
    def __init__(self, db=Depends(get_db)) -> None:
        super().__init__(db=db, model=Task)
