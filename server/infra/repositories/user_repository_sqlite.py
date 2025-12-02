import sqlite3
from domain.user import User
from infra.repositories.user_repository import UserRepository


class UserRepositorySQLite(UserRepository):
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory

    def _get_connection(self) -> sqlite3.Connection:
        return self.connection_factory()

    def save(self, user: User) -> User:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            if user.id is None:
                cursor.execute(
                    """
                    INSERT INTO users (name, email, password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user.name, user.email, user.password_hash, user.created_at),
                )
                conn.commit()
                user.id = cursor.lastrowid
            else:
                cursor.execute(
                    """
                    UPDATE users
                    SET name = ?, email = ?, password_hash = ?
                    WHERE id = ?
                    """,
                    (user.name, user.email, user.password_hash, user.id),
                )
                conn.commit()

            return user
        finally:
            conn.close()

    def get_by_email(self, email: str) -> User | None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, password_hash, created_at
                FROM users
                WHERE email = ?
                """,
                (email,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            return self._row_to_user(row)
        finally:
            conn.close()

    def get_by_id(self, user_id: int) -> User | None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, password_hash, created_at
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            return self._row_to_user(row)
        finally:
            conn.close()

    def _row_to_user(self, row) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )
