from domain.user import User

class TestUserEntity:
    """
    Suite de testes para a entidade User (Domínio).
    Verifica se a classe de modelo está armazenando os dados corretamente.
    """

    def test_user_creation(self):
        """
        Deve instanciar um objeto User com todos os atributos corretos.
        """
        user = User(
            id=1,
            name="Teste Silva",
            email="teste@email.com",
            password_hash="hash123",
            created_at="2025-11-30T10:00:00"
        )

        assert user.id == 1
        assert user.name == "Teste Silva"
        assert user.email == "teste@email.com"
        assert user.password_hash == "hash123"
        # Verifica a representação em string (__repr__) para logs
        assert str(user) == "<User id=1 email=teste@email.com>"