from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        from . import models
        db.create_all()

    return app
