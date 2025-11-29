from flask import Blueprint, request, render_template_string
from use_cases.register_bar_use_case import RegisterBarUseCase
from use_cases.recommend_bar_use_case import RecommendBarUseCase
from use_cases.search_bars_use_case import SearchBarsUseCase
from use_cases.list_new_bars_use_case import ListNewBarsUseCase

bp = Blueprint("bars", __name__, url_prefix="/bars")

_register_bar_uc: RegisterBarUseCase | None = None
_recommend_bar_uc: RecommendBarUseCase | None = None
_search_bars_uc: SearchBarsUseCase | None = None
_list_new_bars_uc: ListNewBarsUseCase | None = None


def register_bar_routes(
    app,
    register_bar_uc: RegisterBarUseCase,
    recommend_bar_uc: RecommendBarUseCase,
    search_bars_uc: SearchBarsUseCase,
    list_new_bars_uc: ListNewBarsUseCase,
):
    global _register_bar_uc, _recommend_bar_uc, _search_bars_uc, _list_new_bars_uc
    _register_bar_uc = register_bar_uc
    _recommend_bar_uc = recommend_bar_uc
    _search_bars_uc = search_bars_uc
    _list_new_bars_uc = list_new_bars_uc

    app.register_blueprint(bp)


@bp.route("/register", methods=["GET", "POST"])
def register_bar():
    global _register_bar_uc

    if request.method == "GET":
        html = """
        <h2>Cadastrar bar</h2>
        <form method="post">
          Nome do bar: <input type="text" name="name"><br>
          Endereço: <input type="text" name="address"><br>
          Descrição: <input type="text" name="description"><br>
          ID do dono (user_id): <input type="number" name="owner_id"><br>
          <button type="submit">Salvar</button>
        </form>
        <p>Obs: crie primeiro o usuário dono e use o ID dele aqui.</p>
        """
        return render_template_string(html)

    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    description = request.form.get("description", "").strip()
    owner_id = request.form.get("owner_id")

    try:
        owner_id_int = int(owner_id)
    except (TypeError, ValueError):
        return "owner_id inválido", 400

    try:
        bar = _register_bar_uc.execute(
            name=name,
            address=address,
            description=description,
            owner_id=owner_id_int,
        )
        return render_template_string(
            """
            <h2>Bar cadastrado com sucesso!</h2>
            <p>ID: {{ bar.id }}</p>
            <p>Nome: {{ bar.name }}</p>
            <p>Endereço: {{ bar.address }}</p>
            <p>Descrição: {{ bar.description }}</p>
            <p>Owner ID: {{ bar.owner_id }}</p>
            <a href="/">Voltar</a>
            """,
            bar=bar,
        )
    except ValueError as e:
        return render_template_string(
            """
            <h2>Erro ao cadastrar bar</h2>
            <p>{{ error }}</p>
            <a href="/bars/register">Tentar novamente</a>
            """,
            error=str(e),
        ), 400


@bp.route("/random", methods=["GET"])
def random_bar():
    global _recommend_bar_uc
    bar = _recommend_bar_uc.execute()

    if not bar:
        return "<h2>Nenhum bar cadastrado ainda.</h2><a href='/'>Voltar</a>"

    return render_template_string(
        """
        <h2>Bar recomendado</h2>
        <p><strong>{{ bar.name }}</strong></p>
        <p>{{ bar.address }}</p>
        <p>{{ bar.description }}</p>
        <a href="/">Voltar</a>
        """,
        bar=bar,
    )


@bp.route("/search", methods=["GET"])
def search_bars():
    global _search_bars_uc
    q = request.args.get("q", "").strip()
    bars = _search_bars_uc.execute(q) if q else []

    return render_template_string(
        """
        <h2>Pesquisar bares</h2>
        <form method="get">
          Buscar: <input type="text" name="q" value="{{ q }}">
          <button type="submit">Buscar</button>
        </form>
        {% if q %}
          <h3>Resultados para "{{ q }}":</h3>
          {% if bars %}
            <ul>
            {% for bar in bars %}
              <li><strong>{{ bar.name }}</strong> - {{ bar.address }}</li>
            {% endfor %}
            </ul>
          {% else %}
            <p>Nenhum bar encontrado.</p>
          {% endif %}
        {% endif %}
        <a href="/">Voltar</a>
        """,
        q=q,
        bars=bars,
    )


@bp.route("/newest", methods=["GET"])
def newest_bars():
    global _list_new_bars_uc
    limit_param = request.args.get("limit")
    try:
        limit = int(limit_param) if limit_param else 5
    except ValueError:
        limit = 5

    bars = _list_new_bars_uc.execute(limit=limit)

    return render_template_string(
        """
        <h2>Novos bares (limite {{ limit }})</h2>
        {% if bars %}
          <ul>
          {% for bar in bars %}
            <li>
              <strong>{{ bar.name }}</strong> - {{ bar.address }}
              (owner_id: {{ bar.owner_id }})
            </li>
          {% endfor %}
          </ul>
        {% else %}
          <p>Nenhum bar cadastrado ainda.</p>
        {% endif %}
        <a href="/">Voltar</a>
        """,
        bars=bars,
        limit=limit,
    )
