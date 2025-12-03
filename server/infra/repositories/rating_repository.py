from abc import ABC, abstractmethod
from domain.rating import Rating


class RatingRepository(ABC):
    """
    Interface (contrato) para repositórios de Avaliações.
    """

    @abstractmethod
    def save(self, rating: Rating) -> Rating:
        """Salva uma nova avaliação."""
        pass

    @abstractmethod
    def list_by_bar_id(self, bar_id: int) -> list[Rating]:
        """Lista todas as avaliações de um bar específico."""
        pass