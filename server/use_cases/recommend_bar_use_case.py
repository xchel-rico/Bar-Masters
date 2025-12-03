from infra.repositories.bar_repository import BarRepository
from domain.bar import Bar


class RecommendBarUseCase:
    """
    Caso de uso para recomendar um bar aleatório ao usuário.
    """

    def __init__(self, bar_repository: BarRepository):
        self.bar_repository = bar_repository

    def execute(self) -> Bar | None:
        """
        Retorna um único bar aleatório do banco de dados, ou None se não houver bares.
        """
        return self.bar_repository.get_random()