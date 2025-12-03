from abc import ABC, abstractmethod
from domain.bar import Bar


class BarRepository(ABC):
    """
    Interface (contrato) para repositórios de Bares.
    """

    @abstractmethod
    def save(self, bar: Bar) -> Bar:
        """Salva ou atualiza um bar."""
        pass

    @abstractmethod
    def get_by_id(self, bar_id: int) -> Bar | None:
        """Busca um bar pelo ID."""
        pass

    @abstractmethod
    def get_random(self) -> Bar | None:
        """Retorna um bar aleatório."""
        pass

    @abstractmethod
    def search(self, text: str) -> list[Bar]:
        """Busca bares por nome, descrição, etc."""
        pass

    @abstractmethod
    def list_recent(self, limit: int = 5) -> list[Bar]:
        """Lista os bares mais recentes."""
        pass