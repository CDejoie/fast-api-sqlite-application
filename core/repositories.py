import abc
from functools import wraps
from types import FunctionType
from typing import Dict

from fastapi import HTTPException
from sqlalchemy.orm import Query, Session

from core.models import Base


def wrapper(mcs):
    @wraps(mcs)
    def wrapped(*args, **kwargs):
        try:
            res = mcs(*args, **kwargs)
        except Exception as exc:
            if len(args) > 0 and hasattr(args[0], "db"):
                args[0].db.rollback()
            raise exc
        return res

    return wrapped


class WrappedModelRepository(type, metaclass=abc.ABCMeta):
    def __new__(mcs, class_name, bases, namespace, **kwargs):
        super().__new__(mcs, class_name, bases, namespace, **kwargs)
        class_dict = {}
        for attribute_name, attribute in namespace.items():
            if isinstance(attribute, FunctionType):
                attribute = wrapper(attribute)
            class_dict[attribute_name] = attribute
        return type.__new__(mcs, class_name, bases, class_dict)


class ModelRepository(metaclass=WrappedModelRepository):
    def __init__(self, model: Base, db: Session):
        self.model = model
        self.db = db

    def new_query(self) -> Query:
        return self.db.query(self.model)

    def all(self):
        return self.new_query().all()

    def find_or_fail(self, **kwargs):
        result = self.new_query().filter_by(**kwargs).first()
        if result is None:
            raise HTTPException(
                status_code=404, detail=f"No {self.model} for the given params {kwargs}"
            )

        return result

    def create(self, **kwargs) -> Base:
        row = self.model(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def find_or_create(self, find: Dict) -> Base:
        row = self.new_query().filter_by(**find).count()
        if row > 0:
            self.db.commit()
            return self.new_query().filter_by(**find).first()

        return self.create(**find)

    def update(self, id: int, update: Dict) -> Base:
        row = self.new_query().filter(self.model.id == id)
        row.update(update)
        self.db.commit()

        return row.first()

    def delete(self, id: int) -> None:
        query = self.new_query().filter(self.model.id == id)
        query.delete(synchronize_session=False)
        self.db.commit()
