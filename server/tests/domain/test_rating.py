from domain.rating import Rating

class TestRatingEntity:
    """
    Suite de testes para a entidade Rating (Domínio).
    Valida a estrutura de dados de uma avaliação.
    """

    def test_rating_creation(self):
        """
        Deve criar uma avaliação vinculando corretamente o usuário e o bar,
        além da nota (score) e comentário.
        """
        rating = Rating(
            id=100,
            bar_id=10,
            user_id=1,
            score=5,
            comment="Muito bom!",
            created_at="2025-11-30T14:00:00"
        )

        assert rating.id == 100
        assert rating.bar_id == 10
        assert rating.user_id == 1
        assert rating.score == 5
        assert rating.comment == "Muito bom!"
        assert str(rating) == "<Rating id=100 bar_id=10 user_id=1 score=5>"