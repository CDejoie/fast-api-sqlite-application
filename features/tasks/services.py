from typing import Any, Dict

from fastapi import Depends

from features.tasks.repositories import TaskRepository
from features.tasks.schemas import Task, TaskUpdate


class TaskServices:
    def __init__(self, task_repository: TaskRepository = Depends()) -> None:
        self.task_repository = task_repository

    def update(self, task_id: int, given_task: TaskUpdate) -> Task:
        self.task_repository.find_or_fail(id=task_id)

        task_to_update_fields = self.__get_task_fields_to_update(given_task)

        return self.task_repository.update(task_id, task_to_update_fields)

    def delete(self, task_id: int) -> None:
        self.task_repository.find_or_fail(id=task_id)

        self.task_repository.delete(task_id)

    @staticmethod
    def __get_task_fields_to_update(task_to_update: TaskUpdate) -> Dict[str, Any]:
        return {
            key: value
            for key, value in task_to_update.dict().items()
            if value is not None
        }
