from src.models.abstractBaseModel import AbstractBaseModel
from src.utils.database import db


class MyModel(AbstractBaseModel):
    __tablename = "my_model"

    nombre = db.Column(db.String)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
