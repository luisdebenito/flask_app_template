from abc import ABC, abstractmethod
from src.models.abstractBaseModel import AbstractBaseModel
from typing import List


class AbstractSerializer(ABC):
    @staticmethod
    @abstractmethod
    def serializeSingle(model: AbstractBaseModel) -> dict:
        """Serialize a single model"""
        raise NotImplementedError("Method not implemented")

    @classmethod
    def serializeList(cls, models: List[AbstractBaseModel]) -> List[dict]:
        """Serialize a list of models using the subclass implementation"""
        return [cls.serializeSingle(m) for m in models]
