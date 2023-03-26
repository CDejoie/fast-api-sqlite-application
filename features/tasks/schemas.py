from typing import Optional

from pydantic import BaseModel, root_validator


class Task(BaseModel):
    id: int
    name: str
    is_done: bool

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    name: str


class TaskUpdate(BaseModel):
    name: Optional[str]
    is_done: Optional[bool]

    @root_validator
    @classmethod
    def any_of(cls, parameter):
        if len([value for value in parameter.values() if value != None]) == 0:
            raise ValueError("You must update at least one value")
        return parameter
