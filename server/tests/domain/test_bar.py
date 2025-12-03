from domain.bar import Bar

class TestBarEntity:
    """
    Suite de testes para a entidade Bar (Domínio).
    Garante a integridade dos dados do estabelecimento.
    """

    def test_bar_creation(self):
        """
        Deve criar um objeto Bar e garantir que o owner_id e outros campos
        sejam atribuídos corretamente.
        """
        bar = Bar(
            id=10,
            name="Bar do Zé",
            address="Rua X",
            description="Melhor bar",
            owner_id=5,
            created_at="2025-11-30T12:00:00"
        )

        assert bar.id == 10
        assert bar.name == "Bar do Zé"
        assert bar.address == "Rua X"
        assert bar.owner_id == 5
        assert str(bar) == "<Bar id=10 name=Bar do Zé>"