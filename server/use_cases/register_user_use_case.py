from datetime import datetime, timezone
from domain.user import User
from infra.repositories.user_repository import UserRepository
import hashlib


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, name: str, email: str, password: str) -> User:
        # comprobar se j´a existe um usuário com o mesmo e-mail
        existing = self.user_repository.get_by_email(email)
        if existing:
            raise ValueError("E-mail já cadastrado")

        password_hash = self._hash_password(password)
        now = datetime.now(timezone.utc).isoformat()

        user = User(
            id=None,
            name=name,
            email=email,
            password_hash=password_hash,
            created_at=now,
        )
        return self.user_repository.save(user)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
