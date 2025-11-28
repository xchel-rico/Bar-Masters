import random
from domain.bar import Bar
from infra.repositories.bar_repository import BarRepository


class BarRepositorySQLite(BarRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, bar: Bar) -> Bar:
        cursor = self.conn.cursor()
        if bar.id is None:
            cursor.execute(
                """
                INSERT INTO bars (name, address, description, owner_id, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (bar.name, bar.address, bar.description, bar.owner_id, bar.created_at),
            )
            self.conn.commit()
            bar.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE bars
                SET name = ?, address = ?, description = ?, owner_id = ?
                WHERE id = ?
                """,
                (bar.name, bar.address, bar.description, bar.owner_id, bar.id),
            )
            self.conn.commit()
        return bar

    def get_by_id(self, bar_id: int) -> Bar | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bars WHERE id = ?", (bar_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_bar(row)

    def get_random(self) -> Bar | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bars")
        rows = cursor.fetchall()
        if not rows:
            return None
        row = random.choice(rows)
        return self._row_to_bar(row)

    def search(self, text: str) -> list[Bar]:
        cursor = self.conn.cursor()
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

    def list_recent(self, limit: int = 5) -> list[Bar]:
        cursor = self.conn.cursor()
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

    def _row_to_bar(self, row) -> Bar:
        return Bar(
            id=row["id"],
            name=row["name"],
            address=row["address"],
            description=row["description"],
            owner_id=row["owner_id"],
            created_at=row["created_at"],
        )
