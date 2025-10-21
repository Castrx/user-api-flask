from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

swagger_template = {
    "swagger": "2.0",
    "info": {"title": "User API", "version": "1.0.0"},
    "basePath": "/"
}

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///local.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    Swagger(app, template=swagger_template)

    # Importa e registra os blueprints
    from .routes.auth import bp as auth_bp
    from .routes.users import bp as users_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")

    # 🔹 Cria as tabelas automaticamente na inicialização (se não existirem)
    with app.app_context():
        from .models.user import User  # ajuste conforme o nome real do seu arquivo de modelo
        db.create_all()

    # Endpoint de verificação
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
