class Bar:
    def __init__(self, id, name, address, description, owner_id, created_at):
        self.id = id
        self.name = name
        self.address = address
        self.description = description
        self.owner_id = owner_id  # referência ao User dono do bar
        self.created_at = created_at

    def __repr__(self):
        return f"<Bar id={self.id} name={self.name}>"
