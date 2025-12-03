class User:
    """
    Entidade que representa um Usuário no sistema.
    """

    def __init__(self, id, name, email, password_hash, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"