from typing import List

from fastapi import APIRouter, Depends

from features.tasks.repositories import TaskRepository
from features.tasks.schemas import Task, TaskCreate, TaskUpdate
from features.tasks.services import TaskServices

router = APIRouter(tags=["tasks"])


@router.get("", response_model=List[Task])
def list_tasks(repository: TaskRepository = Depends()):
    return repository.all()


@router.post("", response_model=Task)
def create_task(task: TaskCreate, repository: TaskRepository = Depends()):
    return repository.find_or_create(task.dict())


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, service: TaskServices = Depends()):
    return service.update(task_id, task)

@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskServices = Depends()):
    service.delete(task_id)
