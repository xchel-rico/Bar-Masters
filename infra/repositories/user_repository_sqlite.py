from domain.user import User
from infra.repositories.user_repository import UserRepository

class UserRepositorySQLite(UserRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, user: User) -> User:
        cursor = self.conn.cursor()
        if user.id is None:
            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user.name, user.email, user.password_hash, user.created_at),
            )
            self.conn.commit()
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
            self.conn.commit()
        return user

    def get_by_email(self, email: str) -> User | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )

    def get_by_id(self, user_id: int) -> User | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            created_at=row["created_at"],
        )
