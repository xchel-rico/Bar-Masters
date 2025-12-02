from unittest.mock import Mock
import pytest
from domain.rating import Rating
from domain.bar import Bar
from domain.user import User
from use_cases.rate_bar_use_case import RateBarUseCase

class TestRateBarUseCase:
    
    @pytest.fixture
    def mocks(self):
        return Mock(), Mock(), Mock() # bar_repo, user_repo, rating_repo

    def test_rate_bar_success(self, mocks):
        bar_repo, user_repo, rating_repo = mocks
        
        # Stubs
        bar_repo.get_by_id.return_value = Bar(10, "Bar", "End", "Desc", 1, "date")
        user_repo.get_by_id.return_value = User(5, "User", "email", "hash", "date")
        rating_repo.save.side_effect = lambda r: Rating(100, r.bar_id, r.user_id, r.score, r.comment, r.created_at)

        use_case = RateBarUseCase(bar_repo, user_repo, rating_repo)

        # Act
        result = use_case.execute(bar_id=10, user_id=5, score=5, comment="Excelente!")

        # Assert
        assert result.id == 100
        assert result.score == 5
        rating_repo.save.assert_called_once()

    def test_rate_bar_invalid_score(self, mocks):
        bar_repo, user_repo, rating_repo = mocks
        
        bar_repo.get_by_id.return_value = Bar(10, "Bar", "End", "Desc", 1, "date")
        user_repo.get_by_id.return_value = User(5, "User", "email", "hash", "date")

        use_case = RateBarUseCase(bar_repo, user_repo, rating_repo)

        # Score > 5
        with pytest.raises(ValueError, match="Score deve ser entre 1 e 5"):
            use_case.execute(10, 5, 6, "Ruim")

        # Score < 1
        with pytest.raises(ValueError, match="Score deve ser entre 1 e 5"):
            use_case.execute(10, 5, 0, "Ruim")

    def test_rate_bar_not_found(self, mocks):
        bar_repo, user_repo, rating_repo = mocks
        bar_repo.get_by_id.return_value = None # Bar não existe

        use_case = RateBarUseCase(bar_repo, user_repo, rating_repo)

        with pytest.raises(ValueError, match="Bar não encontrado"):
            use_case.execute(10, 5, 5, "")