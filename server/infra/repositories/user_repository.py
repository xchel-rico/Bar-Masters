from abc import ABC, abstractmethod
from domain.user import User


class UserRepository(ABC):
    """
    Interface (contrato) para repositórios de Usuários.
    Define os métodos que qualquer implementação (SQLite, Postgres, Memory) deve ter.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """Salva ou atualiza um usuário."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo e-mail."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        """Busca um usuário pelo ID."""
        pass