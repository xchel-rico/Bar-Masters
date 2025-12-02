from flask import Blueprint, request, jsonify
from use_cases.register_bar_use_case import RegisterBarUseCase
from use_cases.recommend_bar_use_case import RecommendBarUseCase
from use_cases.search_bars_use_case import SearchBarsUseCase
from use_cases.list_new_bars_use_case import ListNewBarsUseCase
from use_cases.rate_bar_use_case import RateBarUseCase

bp = Blueprint("bars_api", __name__, url_prefix="/api/bars")

_register_bar_uc: RegisterBarUseCase | None = None
_recommend_bar_uc: RecommendBarUseCase | None = None
_search_bars_uc: SearchBarsUseCase | None = None
_list_new_bars_uc: ListNewBarsUseCase | None = None
_rate_bar_uc: RateBarUseCase | None = None


def register_bar_routes(
    app,
    register_bar_uc: RegisterBarUseCase,
    recommend_bar_uc: RecommendBarUseCase,
    search_bars_uc: SearchBarsUseCase,
    list_new_bars_uc: ListNewBarsUseCase,
    rate_bar_uc: RateBarUseCase,
):
    global _register_bar_uc, _recommend_bar_uc, _search_bars_uc, _list_new_bars_uc, _rate_bar_uc

    _register_bar_uc = register_bar_uc
    _recommend_bar_uc = recommend_bar_uc
    _search_bars_uc = search_bars_uc
    _list_new_bars_uc = list_new_bars_uc
    _rate_bar_uc = rate_bar_uc

    app.register_blueprint(bp)


# --------------------------
# POST /api/bars
# --------------------------
@bp.route("", methods=["POST"])
def api_register_bar():
    global _register_bar_uc
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    name = data.get("name")
    address = data.get("address")
    description = data.get("description")
    owner_id = data.get("owner_id")

    if not name or not address or not owner_id:
        return jsonify({"error": "name, address and owner_id are required"}), 400

    try:
        bar = _register_bar_uc.execute(
            name=name,
            address=address,
            description=description,
            owner_id=int(owner_id),
        )

        return jsonify({
            "id": bar.id,
            "name": bar.name,
            "address": bar.address,
            "description": bar.description,
            "owner_id": bar.owner_id,
            "created_at": bar.created_at,
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# --------------------------
# GET /api/bars/random
# --------------------------
@bp.route("/random", methods=["GET"])
def api_random_bar():
    global _recommend_bar_uc

    bar = _recommend_bar_uc.execute()

    if not bar:
        return jsonify([]), 200

    return jsonify({
        "id": bar.id,
        "name": bar.name,
        "address": bar.address,
        "description": bar.description,
        "owner_id": bar.owner_id,
        "created_at": bar.created_at,
    })


# --------------------------
# GET /api/bars/search?q=...
# --------------------------
@bp.route("/search", methods=["GET"])
def api_search_bars():
    global _search_bars_uc

    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    bars = _search_bars_uc.execute(q)

    return jsonify([
        {
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "description": b.description,
            "owner_id": b.owner_id,
            "created_at": b.created_at,
        }
        for b in bars
    ])


# --------------------------
# GET /api/bars/newest
# --------------------------
@bp.route("/newest", methods=["GET"])
def api_newest_bars():
    global _list_new_bars_uc

    limit_param = request.args.get("limit")
    try:
        limit = int(limit_param) if limit_param else 5
    except ValueError:
        limit = 5

    bars = _list_new_bars_uc.execute(limit=limit)

    return jsonify([
        {
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "description": b.description,
            "owner_id": b.owner_id,
            "created_at": b.created_at,
        }
        for b in bars
    ])


# --------------------------
# POST /api/bars/<bar_id>/rate
# --------------------------
@bp.route("/<int:bar_id>/rate", methods=["POST"])
def api_rate_bar(bar_id: int):
    global _rate_bar_uc

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    user_id = data.get("user_id")
    score = data.get("score")
    comment = data.get("comment", "")

    if not user_id or not score:
        return jsonify({"error": "user_id and score required"}), 400

    try:
        rating = _rate_bar_uc.execute(
            bar_id=bar_id,
            user_id=int(user_id),
            score=int(score),
            comment=comment,
        )

        return jsonify({
            "id": rating.id,
            "bar_id": rating.bar_id,
            "user_id": rating.user_id,
            "score": rating.score,
            "comment": rating.comment,
            "created_at": rating.created_at,
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# --------------------------
# GET /api/bars/<id> (Detalhes do bar)
# --------------------------
@bp.route("/<int:bar_id>", methods=["GET"])
def api_get_bar(bar_id):
    from infra.repositories.bar_repository_sqlite import BarRepositorySQLite
    from infra.db.database import get_connection
    
    # Instanciamos o repo aqui rápido para não mudar a injeção de dependência global
    repo = BarRepositorySQLite(get_connection)
    bar = repo.get_by_id(bar_id)

    if not bar:
        return jsonify({"error": "Bar não encontrado"}), 404

    return jsonify({
        "id": bar.id,
        "name": bar.name,
        "address": bar.address,
        "description": bar.description,
        "owner_id": bar.owner_id,
        "created_at": bar.created_at,
    })