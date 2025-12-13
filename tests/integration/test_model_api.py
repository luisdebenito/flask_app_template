import pytest
from main import app
from utils.database import db
from models.model import MyModel

@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_get_model_empty(client):
    response = client.get("/model")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "data": []}  # Adjust according to your Response.ok_query format

def test_get_model_with_data(client):
    with app.app_context():
        obj = MyModel(nombre="IntegrationTest")
        db.session.add(obj)
        db.session.commit()

    response = client.get("/model")
    assert response.status_code == 200
    assert len(response.json["data"]) == 1
    assert response.json["data"][0]["nombre"] == "IntegrationTest"
