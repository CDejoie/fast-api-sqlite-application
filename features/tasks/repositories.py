from fastapi import Depends

from app.db import get_db
from core.repositories import ModelRepository
from features.tasks.models import Task


class TaskRepository(ModelRepository):
    model = Task

    def __init__(self, db=Depends(get_db)) -> None:
        super().__init__(db=db, model=self.model)
