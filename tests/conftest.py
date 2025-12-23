from src.app_factory import create_app
from src.utils.database import db
import pytest


@pytest.fixture
def test_client():
    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with test_app.app_context():
        db.create_all()
        yield test_app.test_client()
        db.drop_all()
