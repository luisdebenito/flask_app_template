from src.models.model import MyModel
from src.mappers.abstractSerializer import AbstractSerializer


class ModelSerializer(AbstractSerializer):
    @staticmethod
    def serializeSingle(model: MyModel) -> dict:
        return {
            "id": model.id,
            "nombre": model.nombre,
        }
