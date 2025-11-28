from abc import ABC, abstractmethod
from domain.rating import Rating


class RatingRepository(ABC):

    @abstractmethod
    def save(self, rating: Rating) -> Rating:
        pass

    @abstractmethod
    def get_by_bar_id(self, bar_id: int) -> list[Rating]:
        pass
