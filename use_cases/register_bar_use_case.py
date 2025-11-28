from datetime import datetime
from domain.bar import Bar
from infra.repositories.bar_repository import BarRepository
from infra.repositories.user_repository import UserRepository


class RegisterBarUseCase:
    def __init__(self, bar_repository: BarRepository, user_repository: UserRepository):
        self.bar_repository = bar_repository
        self.user_repository = user_repository

    def execute(self, name: str, address: str, description: str, owner_id: int) -> Bar:
        owner = self.user_repository.get_by_id(owner_id)
        if not owner:
            raise ValueError("Dono (user) não encontrado")

        now = datetime.utcnow().isoformat()
        bar = Bar(
            id=None,
            name=name,
            address=address,
            description=description,
            owner_id=owner_id,
            created_at=now,
        )
        return self.bar_repository.save(bar)
