from infra.repositories.bar_repository import BarRepository
from domain.bar import Bar


class SearchBarsUseCase:
    """
    Caso de uso para buscar bares por texto.
    """

    def __init__(self, bar_repository: BarRepository):
        self.bar_repository = bar_repository

    def execute(self, text: str) -> list[Bar]:
        """
        Busca bares cujo nome, endereço ou descrição contenham o texto fornecido.
        """
        return self.bar_repository.search(text)