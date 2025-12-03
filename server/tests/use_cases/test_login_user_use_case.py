import hashlib
from unittest.mock import Mock
import pytest
from domain.user import User
from use_cases.login_user_use_case import LoginUserUseCase

class TestLoginUserUseCase:
    """
    Suite de testes para o caso de uso de Login.
    Verifica a autenticação correta e o tratamento de credenciais inválidas.
    """

    def test_login_success(self):
        """
        Deve retornar o usuário quando o e-mail e a senha (hash) conferem.
        """
        # Arrange
        mock_repo = Mock()
        
        # Cria um hash real para simular o que estaria no banco
        correct_password = "minha_senha_secreta"
        expected_hash = hashlib.sha256(correct_password.encode("utf-8")).hexdigest()
        
        # Simula usuário encontrado no banco
        user_in_db = User(1, "Carlos", "carlos@test.com", expected_hash, "date")
        mock_repo.get_by_email.return_value = user_in_db

        use_case = LoginUserUseCase(mock_repo)

        # Act
        result = use_case.execute("carlos@test.com", correct_password)

        # Assert
        assert result.id == 1
        assert result.name == "Carlos"
        mock_repo.get_by_email.assert_called_with("carlos@test.com")

    def test_login_user_not_found(self):
        """
        Deve lançar erro quando o e-mail não existe no banco.
        """
        # Arrange
        mock_repo = Mock()
        # Simula que não achou ninguém
        mock_repo.get_by_email.return_value = None

        use_case = LoginUserUseCase(mock_repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Usuário ou senha inválidos"):
            use_case.execute("naoexiste@test.com", "123456")

    def test_login_wrong_password(self):
        """
        Deve lançar erro quando o e-mail existe, mas a senha não confere.
        """
        # Arrange
        mock_repo = Mock()
        
        # Senha correta no banco
        expected_hash = hashlib.sha256("senha_correta".encode("utf-8")).hexdigest()
        user_in_db = User(1, "Carlos", "carlos@test.com", expected_hash, "date")
        
        mock_repo.get_by_email.return_value = user_in_db

        use_case = LoginUserUseCase(mock_repo)

        # Act & Assert (Tentando logar com senha ERRADA)
        with pytest.raises(ValueError, match="Usuário ou senha inválidos"):
            use_case.execute("carlos@test.com", "senha_errada")