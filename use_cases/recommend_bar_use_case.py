from infra.repositories.bar_repository import BarRepository
from domain.bar import Bar


class RecommendBarUseCase:
    def __init__(self, bar_repository: BarRepository):
        self.bar_repository = bar_repository

    def execute(self) -> Bar | None:
        return self.bar_repository.get_random()
