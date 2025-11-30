from flask import Blueprint, request, jsonify
from use_cases.register_user_use_case import RegisterUserUseCase

bp = Blueprint("users_api", __name__, url_prefix="/api/users")

_register_user_uc: RegisterUserUseCase | None = None


def register_user_routes(app, register_user_uc: RegisterUserUseCase):
    global _register_user_uc
    _register_user_uc = register_user_uc

    app.register_blueprint(bp)


@bp.route("", methods=["POST"])
def api_register_user():
    global _register_user_uc

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    try:
        user = _register_user_uc.execute(name=name, email=email, password=password)

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
