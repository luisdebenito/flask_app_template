from abc import abstractmethod
from src.models.abstractBaseModel import AbstractBaseModel
from typing import List


class AbstractSerializer:
    @abstractmethod
    def serializeSingle(model: AbstractBaseModel) -> dict:
        raise Exception("Method not implemented")

    @staticmethod
    def serializeList(models: List[AbstractBaseModel]) -> List[dict]:
        return [c.serializeSingle() for c in models]
