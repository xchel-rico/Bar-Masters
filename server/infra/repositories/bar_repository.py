from abc import ABC, abstractmethod
from domain.bar import Bar


class BarRepository(ABC):

    @abstractmethod
    def save(self, bar: Bar) -> Bar:
        pass

    @abstractmethod
    def get_by_id(self, bar_id: int) -> Bar | None:
        pass

    @abstractmethod
    def get_random(self) -> Bar | None:
        pass

    @abstractmethod
    def search(self, text: str) -> list[Bar]:
        """Busca por nome, descrição, etc."""
        pass

    @abstractmethod
    def list_recent(self, limit: int = 5) -> list[Bar]:
        """Lista os bares mais recentes."""
        pass
