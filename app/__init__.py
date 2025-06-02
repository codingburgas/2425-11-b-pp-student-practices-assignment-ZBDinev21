from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from app.extensions import db
from sqlalchemy.dialects.mysql import pyodbc
from app.routes.Main import main_bp


# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(main_bp=None):
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Secret key for session management
    app.register_blueprint(main_bp)
    
    # Config setup
    db_config = '/config.py'

    def get_db_connection():
        connection_string = (
            f"DRIVER={db_config['driver']};"
            f"SERVER={db_config['server']};"
            f"PORT=1433;"
            f"DATABASE={db_config['database']};"
            f"UID={db_config['username']};"
            f"PWD={db_config['password']}"
        )
        return pyodbc.connect(connection_string)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.Auth import auth_bp
    from app.routes.Main import main_bp
    from app.routes.Admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    return app

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404