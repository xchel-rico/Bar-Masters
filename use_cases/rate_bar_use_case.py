from datetime import datetime
from domain.rating import Rating
from infra.repositories.bar_repository import BarRepository
from infra.repositories.user_repository import UserRepository
from infra.repositories.rating_repository import RatingRepository


class RateBarUseCase:
    def __init__(
        self,
        bar_repository: BarRepository,
        user_repository: UserRepository,
        rating_repository: RatingRepository,
    ):
        self.bar_repository = bar_repository
        self.user_repository = user_repository
        self.rating_repository = rating_repository

    def execute(self, bar_id: int, user_id: int, score: int, comment: str) -> Rating:
        bar = self.bar_repository.get_by_id(bar_id)
        if not bar:
            raise ValueError("Bar não encontrado")

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        if score < 1 or score > 5:
            raise ValueError("Score deve ser entre 1 e 5")

        now = datetime.utcnow().isoformat()
        rating = Rating(
            id=None,
            bar_id=bar_id,
            user_id=user_id,
            score=score,
            comment=comment,
            created_at=now,
        )
        return self.rating_repository.save(rating)
