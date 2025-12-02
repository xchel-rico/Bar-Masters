from unittest.mock import Mock
import pytest
from domain.bar import Bar
from domain.user import User
from use_cases.register_bar_use_case import RegisterBarUseCase


class TestRegisterBarUseCase:

    def test_register_bar_success(self):
        # Arrange
        mock_bar_repo = Mock()
        mock_user_repo = Mock()

        # Simula que o dono do bar existe
        mock_user_repo.get_by_id.return_value = User(
            1, "Dono", "dono@test.com", "hash", "date")

        # Mock do save retornando o bar com ID
        mock_bar_repo.save.side_effect = lambda b: Bar(
            10, b.name, b.address, b.description, b.owner_id, b.created_at)

        use_case = RegisterBarUseCase(mock_bar_repo, mock_user_repo)

        # Act
        result = use_case.execute("Bar Legal", "Rua A", "Desc", 1)

        # Assert
        assert result.id == 10
        assert result.name == "Bar Legal"
        assert result.owner_id == 1
        mock_bar_repo.save.assert_called_once()

    def test_register_bar_owner_not_found(self):
        # Arrange
        mock_bar_repo = Mock()
        mock_user_repo = Mock()

        # Simula que o dono NÃO existe
        mock_user_repo.get_by_id.return_value = None

        use_case = RegisterBarUseCase(mock_bar_repo, mock_user_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Dono \(user\) não encontrado"):
            use_case.execute("Bar", "Rua", "Desc", 999)

        mock_bar_repo.save.assert_not_called()
