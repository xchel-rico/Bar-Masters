from datetime import datetime, timezone
from domain.bar import Bar
from infra.repositories.bar_repository import BarRepository
from infra.repositories.user_repository import UserRepository


class RegisterBarUseCase:
    """
    Caso de uso responsável pelo cadastro de novos bares.
    """

    def __init__(self, bar_repository: BarRepository, user_repository: UserRepository):
        self.bar_repository = bar_repository
        self.user_repository = user_repository

    def execute(self, name: str, address: str, description: str, owner_id: int) -> Bar:
        """
        Cadastra um bar validando se o usuário dono (owner_id) existe.
        """
        owner = self.user_repository.get_by_id(owner_id)
        if not owner:
            raise ValueError("Dono (user) não encontrado")

        now = datetime.now(timezone.utc).isoformat()
        bar = Bar(
            id=None,
            name=name,
            address=address,
            description=description,
            owner_id=owner_id,
            created_at=now,
        )
        return self.bar_repository.save(bar)