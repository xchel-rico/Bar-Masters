from flask import Flask
from flask_cors import CORS
from infra.db.database import init_db, get_connection

from infra.repositories.user_repository_sqlite import UserRepositorySQLite
from infra.repositories.bar_repository_sqlite import BarRepositorySQLite
from infra.repositories.rating_repository_sqlite import RatingRepositorySQLite

from use_cases.register_user_use_case import RegisterUserUseCase
from use_cases.register_bar_use_case import RegisterBarUseCase
from use_cases.recommend_bar_use_case import RecommendBarUseCase
from use_cases.search_bars_use_case import SearchBarsUseCase
from use_cases.list_new_bars_use_case import ListNewBarsUseCase
from use_cases.rate_bar_use_case import RateBarUseCase

from app.routes.user_routes import register_user_routes
from app.routes.bar_routes import register_bar_routes


def create_app():
    app = Flask(__name__)

    CORS(app)

    # Inicializa BD
    init_db()

    # Repositórios
    user_repo = UserRepositorySQLite(get_connection)
    bar_repo = BarRepositorySQLite(get_connection)
    rating_repo = RatingRepositorySQLite(get_connection)

    # Use cases
    register_user_uc = RegisterUserUseCase(user_repo)
    register_bar_uc = RegisterBarUseCase(bar_repo, user_repo)
    recommend_bar_uc = RecommendBarUseCase(bar_repo)
    search_bars_uc = SearchBarsUseCase(bar_repo)
    list_new_bars_uc = ListNewBarsUseCase(bar_repo)
    rate_bar_uc = RateBarUseCase(bar_repo, user_repo, rating_repo)

    # Registrar rotas da API
    register_user_routes(app, register_user_uc)
    register_bar_routes(
        app,
        register_bar_uc,
        recommend_bar_uc,
        search_bars_uc,
        list_new_bars_uc,
        rate_bar_uc
    )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
