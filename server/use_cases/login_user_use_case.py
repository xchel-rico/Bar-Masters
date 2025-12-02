import hashlib
from domain.user import User
from infra.repositories.user_repository import UserRepository

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email)
        
        # Verifica se usuário existe
        if not user:
            raise ValueError("Usuário ou senha inválidos")

        # Verifica se a senha bate com o hash salvo
        input_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        
        if input_hash != user.password_hash:
            raise ValueError("Usuário ou senha inválidos")

        return user