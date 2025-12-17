import os
from flask import Flask
from dotenv import load_dotenv
from src.utils.response import Response
from src.utils.database import db
from flask_migrate import Migrate
from src.api import blueprints

load_dotenv()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL", "sqlite:///db.sqlite")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.errorhandler(404)
def basic_pages(wargs=None):
    # whatever custom things come here
    return Response.error("Page not found", 404)


@app.route("/health", methods=["GET"])
def healthcheck():
    db_ok = False
    try:
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    # Check blueprints
    bps = list(app.blueprints.keys())
    bps_ok = len(bps) == len(blueprints)
    return Response.success("OK") if db_ok and bps_ok else Response.error("NOT OK", 503)
