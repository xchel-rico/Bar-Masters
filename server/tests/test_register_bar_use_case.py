from unittest.mock import Mock
import pytest
from domain.bar import Bar
from domain.user import User
from use_cases.register_bar_use_case import RegisterBarUseCase

class TestRegisterBarUseCase:
    """
    Suite de testes para o cadastro de Bares.
    Garante que a associação com o dono (owner) seja validada.
    """

    def test_register_bar_success(self):
        """
        Deve cadastrar um bar com sucesso quando o dono (owner_id) é válido.
        """
        # Arrange
        mock_bar_repo = Mock()
        mock_user_repo = Mock()

        # Simula que o usuário dono existe no banco
        mock_user_repo.get_by_id.return_value = User(1, "Dono", "dono@test.com", "hash", "date")
        
        # Mock do save retornando o bar persistido com ID 10
        mock_bar_repo.save.side_effect = lambda b: Bar(10, b.name, b.address, b.description, b.owner_id, b.created_at)

        use_case = RegisterBarUseCase(mock_bar_repo, mock_user_repo)

        # Act
        result = use_case.execute("Bar Legal", "Rua A", "Desc", 1)

        # Assert
        assert result.id == 10
        assert result.name == "Bar Legal"
        assert result.owner_id == 1
        mock_bar_repo.save.assert_called_once()

    def test_register_bar_owner_not_found(self):
        """
        Deve impedir o cadastro se o ID do dono informado não existir.
        """
        # Arrange
        mock_bar_repo = Mock()
        mock_user_repo = Mock()

        # Simula que o usuário NÃO foi encontrado (None)
        mock_user_repo.get_by_id.return_value = None

        use_case = RegisterBarUseCase(mock_bar_repo, mock_user_repo)

        # Act & Assert
        # Usamos 'raw string' (r"") para evitar warnings de escape sequence
        with pytest.raises(ValueError, match=r"Dono \(user\) não encontrado"):
            use_case.execute("Bar", "Rua", "Desc", 999)
        
        # Garante que o método save do bar nunca foi chamado
        mock_bar_repo.save.assert_not_called()