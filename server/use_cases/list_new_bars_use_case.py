from infra.repositories.bar_repository import BarRepository
from domain.bar import Bar


class ListNewBarsUseCase:
    """
    Caso de uso para listar os bares mais recentes.
    """

    def __init__(self, bar_repository: BarRepository):
        self.bar_repository = bar_repository

    def execute(self, limit: int = 5) -> list[Bar]:
        """
        Retorna uma lista com os 'limit' últimos bares cadastrados.
        """
        return self.bar_repository.list_recent(limit)