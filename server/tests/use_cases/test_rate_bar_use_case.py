from unittest.mock import Mock
import pytest
from domain.rating import Rating
from domain.bar import Bar
from domain.user import User
from use_cases.rate_bar_use_case import RateBarUseCase

class TestRateBarUseCase:
    """
    Suite de testes para Avaliação de Bares.
    Valida as regras de existência de entidades e limites de nota (1-5).
    """
    
    @pytest.fixture
    def mocks(self):
        """Fixture do Pytest para criar mocks limpos antes de cada teste."""
        return Mock(), Mock(), Mock() # bar_repo, user_repo, rating_repo

    def test_rate_bar_success(self, mocks):
        """
        Deve registrar uma avaliação com sucesso quando todos os dados são válidos.
        """
        bar_repo, user_repo, rating_repo = mocks
        
        # Stubs (Comportamentos simulados)
        bar_repo.get_by_id.return_value = Bar(10, "Bar", "End", "Desc", 1, "date")
        user_repo.get_by_id.return_value = User(5, "User", "email", "hash", "date")
        # Simula o save retornando a avaliação com ID
        rating_repo.save.side_effect = lambda r: Rating(100, r.bar_id, r.user_id, r.score, r.comment, r.created_at)

        use_case = RateBarUseCase(bar_repo, user_repo, rating_repo)

        # Act
        result = use_case.execute(bar_id=10, user_id=5, score=5, comment="Excelente!")

        # Assert
        assert result.id == 100
        assert result.score == 5
        rating_repo.save.assert_called_once()

    def test_rate_bar_invalid_score(self, mocks):
        """
        Deve lançar erro se a nota (score) for menor que 1 ou maior que 5.
        """
        bar_repo, user_repo, rating_repo = mocks
        
        # As entidades existem
        bar_repo.get_by_id.return_value = Bar(10, "Bar", "End", "Desc", 1, "date")
        user_repo.get_by_id.return_value = User(5, "User", "email", "hash", "date")

        use_case = RateBarUseCase(bar_repo, user_repo, rating_repo)

        # Teste 1: Nota maior que 5
        with pytest.raises(ValueError, match="Score deve ser entre 1 e 5"):
            use_case.execute(10, 5, 6, "Ruim")

        # Teste 2: Nota menor que 1
        with pytest.raises(ValueError, match="Score deve ser entre 1 e 5"):
            use_case.execute(10, 5, 0, "Ruim")

    def test_rate_bar_not_found(self, mocks):
        """
        Deve falhar se tentar avaliar um bar que não existe.
        """
        bar_repo, user_repo, rating_repo = mocks
        
        # Simula Bar inexistente
        bar_repo.get_by_id.return_value = None 

        use_case = RateBarUseCase(bar_repo, user_repo, rating_repo)

        with pytest.raises(ValueError, match="Bar não encontrado"):
            use_case.execute(10, 5, 5, "")