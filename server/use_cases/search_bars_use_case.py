from infra.repositories.bar_repository import BarRepository
from domain.bar import Bar


class SearchBarsUseCase:
    def __init__(self, bar_repository: BarRepository):
        self.bar_repository = bar_repository

    def execute(self, text: str) -> list[Bar]:
        return self.bar_repository.search(text)
