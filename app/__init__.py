from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/cybersec.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    # ✅ Import all blueprints
    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.module_routes import module_bp
    from .routes.quiz_routes import quiz_bp
    from .routes.leaderboard_routes import leaderboard_bp
    from .routes.admin_routes import admin_bp
    from .routes.main_routes import main_bp

    # ✅ Register them
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(module_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)


    

    with app.app_context():
        db.create_all()

    return app
