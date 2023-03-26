from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, cast

from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.models import Base


class ModelFactory(ABC):
    model: Base
    items_count: int = 1

    def __init__(self, db: Session):
        self.faker = Faker()
        self.db = db

    def count(self, items: int) -> ModelFactory:
        self.items_count = items
        return self

    def raw(
        self, overrides: Dict[str, Any] | None = None
    ) -> Dict[str, Any] | List[Base]:
        if overrides is None:
            overrides = {}

        items = []
        for _ in range(self.items_count):
            attrs: Dict[str, Any] = self.definitions()
            attrs.update(jsonable_encoder(overrides))
            items.append(attrs)

        return items if self.items_count > 1 else items[0]

    def create_item(self, **kwargs) -> Base:
        row = self.model(**kwargs)

        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)

        return row

    def create(self, overrides: Dict[str, Any] | None = None) -> Base | List[Base]:
        items = self.raw(overrides=overrides)
        if self.items_count == 1:
            return self.create_item(**cast(Dict, items))

        return [self.create_item(**item) for item in items]

    @abstractmethod
    def definitions(self) -> Dict[str, Any]:
        raise NotImplementedError()
