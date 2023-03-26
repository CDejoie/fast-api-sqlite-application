from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.assert_helpers import AssertHelpers
from tests.test_configuration import client, db, db_engine
from tests.factories.task_factory import TaskFactory


class TestBrowseTasks:
    GET_URL = "/api/v1/tasks"

    def test_get_tasks_when_no_task_then_return_empty_array(self, client: TestClient):
        response = client.get(self.GET_URL)

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_get_tasks_when_tasks_then_return_tasks(
        self, client: TestClient, db: Session
    ):
        TaskFactory(db).count(3).create()

        response = client.get(self.GET_URL)

        assert response.status_code == 200
        assert len(response.json()) == 3


class TestCreateTask:
    CREATE_URL = "/api/v1/tasks"
    TABLE_NAME = "tasks"

    def test_create_task_when_given_no_name_then_raise_422(
        self, client: TestClient, db: Session
    ):
        response = client.post(self.CREATE_URL, json={"name": None})

        assert response.status_code == 422
        AssertHelpers(db).database_count(self.TABLE_NAME, 0)

    def test_create_task_when_given_name_then_create_task(
        self, client: TestClient, db: Session
    ):
        given_name = "foo"

        response = client.post(self.CREATE_URL, json={"name": given_name})

        assert response.status_code == 200
        AssertHelpers(db).database_count(self.TABLE_NAME, 1)
        AssertHelpers(db).database_has(self.TABLE_NAME, {"name": given_name})


class TestUpdateTask:
    UPDATE_URL = "/api/v1/tasks"
    TABLE_NAME = "tasks"

    def test_update_task_when_given_not_existing_id_then_raise_404(
        self, client: TestClient
    ):
        response = client.put(f"{self.UPDATE_URL}/{42}", json={"name": "foo"})

        assert response.status_code == 404

    def test_update_task_when_given_existing_id_but_no_update_then_raise_422(
        self, client: TestClient, db: Session
    ):
        task = TaskFactory(db).create()

        response = client.put(f"{self.UPDATE_URL}/{task.id}", json={})

        assert response.status_code == 422

    def test_update_task_when_given_existing_id_then_update_task(
        self, client: TestClient, db: Session
    ):
        initial_name = "foo"
        intial_status = False
        task = TaskFactory(db).create({"name": initial_name, "is_done": intial_status})
        AssertHelpers(db).database_has(
            self.TABLE_NAME,
            {"id": task.id, "name": initial_name, "is_done": intial_status},
        )

        update_name = "bar"
        update_status = True

        response = client.put(
            f"{self.UPDATE_URL}/{task.id}",
            json={"name": update_name, "is_done": update_status},
        )

        assert response.status_code == 200
        AssertHelpers(db).database_count(self.TABLE_NAME, 1)
        AssertHelpers(db).database_has(
            self.TABLE_NAME,
            {"id": task.id, "name": update_name, "is_done": update_status},
        )


class TestDeleteTask:
    DELETE_URL = "/api/v1/tasks"
    TABLE_NAME = "tasks"

    def test_delete_task_when_given_not_existing_id_then_raise_404(
        self, client: TestClient
    ):
        response = client.delete(f"{self.DELETE_URL}/{42}")

        assert response.status_code == 404

    def test_delete_task_when_given_existing_id_then_delete_task(
        self, client: TestClient, db: Session
    ):
        task = TaskFactory(db).create()
        AssertHelpers(db).database_has(self.TABLE_NAME, {"id": task.id})

        response = client.delete(f"{self.DELETE_URL}/{task.id}")

        assert response.status_code == 200
        AssertHelpers(db).database_count(self.TABLE_NAME, 0)
