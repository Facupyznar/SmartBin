from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.routes.auth import auth_bp
from app.config import Config
from app.database import db
from app.models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar CSRF y DB
    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)

    # LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    # Registrar Blueprint de autenticación
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
