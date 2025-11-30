from flask import Blueprint, request, render_template_string
from use_cases.register_user_use_case import RegisterUserUseCase

bp = Blueprint("users", __name__, url_prefix="/users")

_register_user_uc: RegisterUserUseCase | None = None


def register_user_routes(app, register_user_uc: RegisterUserUseCase):
    global _register_user_uc
    _register_user_uc = register_user_uc
    app.register_blueprint(bp)


@bp.route("/register", methods=["GET", "POST"])
def register_user():
    global _register_user_uc

    if request.method == "GET":
        # Formulário simples em HTML
        html = """
        <h2>Registrar usuário</h2>
        <form method="post">
          Nome: <input type="text" name="name"><br>
          E-mail: <input type="email" name="email"><br>
          Senha: <input type="password" name="password"><br>
          <button type="submit">Registrar</button>
        </form>
        """
        return render_template_string(html)

    # POST
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    try:
        user = _register_user_uc.execute(name=name, email=email, password=password)
        return render_template_string(
            """
            <h2>Usuário registrado com sucesso!</h2>
            <p>ID: {{ user.id }}</p>
            <p>Nome: {{ user.name }}</p>
            <p>E-mail: {{ user.email }}</p>
            <a href="/">Voltar</a>
            """,
            user=user,
        )
    except ValueError as e:
        return render_template_string(
            """
            <h2>Erro ao registrar usuário</h2>
            <p>{{ error }}</p>
            <a href="/users/register">Tentar novamente</a>
            """,
            error=str(e),
        ), 400
