from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .routes.webhook import webhook_bp
    from .routes.dashboard import dashboard_bp
    
    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app
