from src.app_factory import create_app
from src.utils.response import success, error
from src.utils.database import db
from src.api import blueprints


app = create_app()


@app.errorhandler(404)
def api_404_error(wargs=None):
    return error("Page not found", 404, 404)


@app.errorhandler(500)
def api_500_error(wargs=None):
    return error("Internal error", 500, 500)


@app.route("/health", methods=["GET"])
def healthcheck():
    db_ok = False
    try:
        db.session.execute(db.text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    bps = list(app.blueprints.keys())
    bps_ok = len(bps) == len(blueprints)

    return success("OK") if db_ok and bps_ok else error("NOT OK", 503, 503)
