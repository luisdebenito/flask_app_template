from src.utils.database import db


class AbstractBaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)

    def serialize(self) -> dict:
        raise NotImplementedError
