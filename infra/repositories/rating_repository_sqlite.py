import sqlite3
from domain.rating import Rating
from infra.repositories.rating_repository import RatingRepository

class RatingRepositorySQLite(RatingRepository):
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory
    
    def _get_connection(self)-> sqlite3.Connection:
        return self.connection_factory()

    def save(self, rating: Rating) -> Rating:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if rating.id is None:
                cursor.execute(
                    """
                    INSERT INTO ratings (bar_id, user_id, score, comment, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        rating.bar_id,
                        rating.user_id,
                        rating.score,
                        rating.comment,
                        rating.created_at,
                    ),
                )
                conn.commit()
                rating.id = cursor.lastrowid
            else:
                cursor.execute(
                    """
                    UPDATE ratings
                    SET score = ?, comment = ?
                    WHERE id = ?
                    """,
                    (
                        rating.score,
                        rating.comment,
                        rating.id,
                    ),
                )
                conn.commit()

            return rating
        finally:
            conn.close()

    def list_by_bar_id(self, bar_id: int) -> list[Rating]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM ratings
                WHERE bar_id = ?
                ORDER BY datetime(created_at) DESC
                """,
                (bar_id,),
            )
            rows = cursor.fetchall()

            return [
                Rating(
                    id=row["id"],
                    bar_id=row["bar_id"],
                    user_id=row["user_id"],
                    score=row["score"],
                    comment=row["comment"],
                    created_at=row["created_at"],
                )
                for row in rows
            ]

        finally:
            conn.close()