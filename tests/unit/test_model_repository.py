import pytest
from models.model import MyModel
from repository.modelRepository import ModelRepository

# Mocking a database session using SQLAlchemy in-memory
from utils.database import db
from main import app

@pytest.fixture(scope="module")
def test_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_get_all_empty(test_app):
    # No data yet
    with test_app.app_context():
        results = ModelRepository.getAll()
        assert results == []

def test_get_all_with_data(test_app):
    with test_app.app_context():
        obj1 = MyModel(nombre="Test1")
        obj2 = MyModel(nombre="Test2")
        db.session.add_all([obj1, obj2])
        db.session.commit()

        results = ModelRepository.getAll()
        assert len(results) == 2
        assert results[0].nombre == "Test1"
