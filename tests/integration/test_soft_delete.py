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

def test_soft_delete_filter(client):
    from main import db

    with app.app_context():
        # Add active and inactive entries
        active_model = MyModel(nombre="Active")
        inactive_model = MyModel(nombre="Inactive", active=False)
        db.session.add_all([active_model, inactive_model])
        db.session.commit()

        # Query using repository
        from repository.modelRepository import ModelRepository
        results = ModelRepository.getAll()
        
        # Only active model should be returned
        assert len(results) == 1
        assert results[0].nombre == "Active"

def test_api_respects_soft_delete(client):
    with app.app_context():
        # Add active and inactive entries
        active_model = MyModel(nombre="ActiveAPI")
        inactive_model = MyModel(nombre="InactiveAPI", active=False)
        db.session.add_all([active_model, inactive_model])
        db.session.commit()

    # Call the endpoint
    response = client.get("/model")
    assert response.status_code == 200
    data = response.json["data"]  # Adjust based on Response.ok_query structure
    assert len(data) == 1
    assert data[0]["nombre"] == "ActiveAPI"
