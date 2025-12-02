from unittest.mock import Mock
import pytest
from domain.user import User
from use_cases.register_user_use_case import RegisterUserUseCase


class TestRegisterUserUseCase:

    def test_register_user_success(self):
        # Arrange (Preparação)
        mock_repo = Mock()
        # Simula que não existe usuário com esse email
        mock_repo.get_by_email.return_value = None
        # Simula o retorno do save (com ID gerado)
        mock_repo.save.side_effect = lambda u: User(
            1, u.name, u.email, u.password_hash, u.created_at)

        use_case = RegisterUserUseCase(mock_repo)

        # Act (Ação)
        result = use_case.execute("Carlos", "carlos@test.com", "123456")

        # Assert (Verificação)
        assert result.id == 1
        assert result.name == "Carlos"
        assert result.email == "carlos@test.com"
        # Verifica se o método save foi chamado
        mock_repo.save.assert_called_once()

    def test_register_user_email_already_exists(self):
        # Arrange
        mock_repo = Mock()
        # Simula que JÁ existe um usuário
        mock_repo.get_by_email.return_value = User(
            1, "Existing", "carlos@test.com", "hash", "date")

        use_case = RegisterUserUseCase(mock_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="E-mail já cadastrado"):
            use_case.execute("Carlos", "carlos@test.com", "123456")

        # Garante que NÃO tentou salvar
        mock_repo.save.assert_not_called()
