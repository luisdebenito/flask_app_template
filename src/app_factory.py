import os
from flask import Flask
from flask_migrate import Migrate

from src.utils.database import db
from src.api import blueprints


def create_app(test_config=None):
    """
    Factory to create a Flask app instance.
    :param test_config: Optional dict to override config for testing
    """
    app = Flask(__name__)

    # Default config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_URL", "sqlite:///db.sqlite"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override with test config if provided
    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
