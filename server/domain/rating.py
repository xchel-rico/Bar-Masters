class Rating:
    """
    Entidade que representa uma Avaliação feita por um usuário a um bar.
    """

    def __init__(self, id, bar_id, user_id, score, comment, created_at):
        self.id = id
        self.bar_id = bar_id        # referência ao Bar
        self.user_id = user_id      # referência ao User que avaliou
        self.score = score          # Nota de 1 a 5
        self.comment = comment
        self.created_at = created_at

    def __repr__(self):
        return f"<Rating id={self.id} bar_id={self.bar_id} user_id={self.user_id} score={self.score}>"