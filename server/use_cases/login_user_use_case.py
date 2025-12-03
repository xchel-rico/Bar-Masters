import hashlib
from domain.user import User
from infra.repositories.user_repository import UserRepository

class LoginUserUseCase:
    """
    Caso de uso responsável por autenticar um usuário.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> User:
        """
        Autentica o usuário verificando e-mail e senha.
        
        1. Busca o usuário pelo e-mail.
        2. Gera o hash da senha fornecida.
        3. Compara com o hash salvo no banco.
        
        Retorna:
            User: O objeto do usuário se a autenticação for bem-sucedida.
            
        Lança:
            ValueError: Se o usuário não for encontrado ou a senha estiver incorreta.
        """
        user = self.user_repository.get_by_email(email)
        
        if not user:
            raise ValueError("Usuário ou senha inválidos")

        input_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        
        if input_hash != user.password_hash:
            raise ValueError("Usuário ou senha inválidos")

        return user