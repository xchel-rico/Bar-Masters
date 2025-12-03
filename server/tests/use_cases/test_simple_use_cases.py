from unittest.mock import Mock
from domain.bar import Bar
from use_cases.search_bars_use_case import SearchBarsUseCase
from use_cases.recommend_bar_use_case import RecommendBarUseCase
from use_cases.list_new_bars_use_case import ListNewBarsUseCase

class TestSimpleReadUseCases:
    """
    Testes para casos de uso de leitura (Busca, Recomendação e Listagem).
    Verifica se os use cases estão delegando corretamente para os repositórios.
    """

    def test_search_bars(self):
        """
        O caso de uso deve chamar o método 'search' do repositório com o texto correto.
        """
        mock_repo = Mock()
        expected_bars = [Bar(1, "Bar A", "End", "Desc", 1, "date")]
        mock_repo.search.return_value = expected_bars
        
        use_case = SearchBarsUseCase(mock_repo)
        result = use_case.execute("query")

        assert result == expected_bars
        mock_repo.search.assert_called_with("query")

    def test_recommend_bar(self):
        """
        O caso de uso deve retornar o bar aleatório fornecido pelo repositório.
        """
        mock_repo = Mock()
        expected_bar = Bar(1, "Random", "End", "Desc", 1, "date")
        mock_repo.get_random.return_value = expected_bar

        use_case = RecommendBarUseCase(mock_repo)
        result = use_case.execute()

        assert result == expected_bar
        mock_repo.get_random.assert_called_once()

    def test_list_new_bars(self):
        """
        O caso de uso deve solicitar a lista de bares recentes respeitando o limite.
        """
        mock_repo = Mock()
        expected_list = [Bar(1, "New", "End", "Desc", 1, "date")]
        mock_repo.list_recent.return_value = expected_list

        use_case = ListNewBarsUseCase(mock_repo)
        result = use_case.execute(limit=10)

        assert len(result) == 1
        mock_repo.list_recent.assert_called_with(10)