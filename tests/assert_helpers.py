from typing import Any, Dict

from sqlalchemy.sql import text
from sqlalchemy.orm import Session

class AssertHelpers():
    def __init__(self, db: Session) -> None:
        self.db = db

    def __find_any_in_db(self, table: str, expected: Dict[str, Any]):
        result = self.db.execute(text(f"SELECT * FROM {table}")).all()
        for row in result:
            data = row._asdict()
            matches = len(expected) > 0
            for key, value in expected.items():
                matches = matches and key in data and data[key] == value
            if matches:
                return True, row
        return False, [row._asdict() for row in result]

    def database_count(self, table_name: str, expected: int) -> None:
        result = self.db.execute(text(f"SELECT COUNT(*) as entries FROM {table_name}")).first()
        actual = result[0]
        assert expected == actual, (
            f"Failed asserting that table {table_name} has {expected} entries."
            f"\nActual: {actual}"
        )

    def database_has(self, table_name: str, expected: Dict[str, Any]) -> None:
        found, result = self.__find_any_in_db(table_name, expected)
        if not found:
            assert False, (
                f"Failed asserting that table {table_name} contains {str(expected)}."
                f"\nActual: {str(result)}"
            )
        assert True
