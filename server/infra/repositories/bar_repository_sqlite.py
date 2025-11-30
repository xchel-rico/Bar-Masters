import random
import sqlite3
from domain.bar import Bar
from infra.repositories.bar_repository import BarRepository


class BarRepositorySQLite(BarRepository):
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory

    def _get_connection(self) -> sqlite3.Connection:
        return self.connection_factory()

    def save(self, bar: Bar) -> Bar:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if bar.id is None:
                cursor.execute(
                    """
                    INSERT INTO bars (name, address, description, owner_id, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        bar.name,
                        bar.address,
                        bar.description,
                        bar.owner_id,
                        bar.created_at,
                    ),
                )
                conn.commit()
                bar.id = cursor.lastrowid
            else:
                cursor.execute(
                    """
                    UPDATE bars
                    SET name = ?, address = ?, description = ?, owner_id = ?
                    WHERE id = ?
                    """,
                    (
                        bar.name,
                        bar.address,
                        bar.description,
                        bar.owner_id,
                        bar.id,
                    ),
                )
                conn.commit()
            return bar
        finally:
            conn.close()

    def get_by_id(self, bar_id: int) -> Bar | None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bars WHERE id = ?", (bar_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_bar(row)
        finally:
            conn.close()

    def get_random(self) -> Bar | None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bars")
            rows = cursor.fetchall()
            if not rows:
                return None
            row = random.choice(rows)
            return self._row_to_bar(row)
        finally:
            conn.close()

    def search(self, text: str) -> list[Bar]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            like = f"%{text}%"
            cursor.execute(
                """
                SELECT * FROM bars
                WHERE name LIKE ? OR address LIKE ? OR description LIKE ?
                """,
                (like, like, like),
            )
            rows = cursor.fetchall()
            return [self._row_to_bar(r) for r in rows]
        finally:
            conn.close()

    def list_recent(self, limit: int = 5) -> list[Bar]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM bars
                ORDER BY datetime(created_at) DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [self._row_to_bar(r) for r in rows]
        finally:
            conn.close()

    def _row_to_bar(self, row) -> Bar:
        return Bar(
            id=row["id"],
            name=row["name"],
            address=row["address"],
            description=row["description"],
            owner_id=row["owner_id"],
            created_at=row["created_at"],
        )
