from features.tasks.models import Task
from tests.factories.model_factory import ModelFactory


class TaskFactory(ModelFactory):
    model = Task

    def definitions(self) -> dict:
        return {
            "name": self.faker.name(),
            "is_done": False,
        }
