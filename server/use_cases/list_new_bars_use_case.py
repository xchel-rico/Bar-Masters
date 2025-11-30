from infra.repositories.bar_repository import BarRepository
from domain.bar import Bar


class ListNewBarsUseCase:
    def __init__(self, bar_repository: BarRepository):
        self.bar_repository = bar_repository

    def execute(self, limit: int = 5) -> list[Bar]:
        return self.bar_repository.list_recent(limit)
