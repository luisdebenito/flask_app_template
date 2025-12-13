from models.model import MyModel
from typing import List

class ModelRepository:
    @staticmethod
    def getAll() -> List[MyModel]:
        return MyModel.query.order_by(MyModel.nombre.desc()).all()



