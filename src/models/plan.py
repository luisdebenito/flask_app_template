from src.models.abstractBaseModel import AbstractBaseModel
from src.utils.database import db
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class Plan(AbstractBaseModel):
    __tablename__ = "plan"

    uid = db.Column(db.String, nullable=False, unique=True)
    external_id = db.Column(db.String, nullable=False, unique=True)

    title = db.Column(db.String, nullable=False)

    start_date = db.Column(db.Date, nullable=True)
    start_time = db.Column(db.Time, nullable=True)

    end_date = db.Column(db.Date, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    min_price = db.Column(db.Numeric(10, 2), nullable=True)
    max_price = db.Column(db.Numeric(10, 2), nullable=True)

    @hybrid_property
    def start_datetime(self):
        """Get start datetime as Python datetime object"""
        if self.start_date and self.start_time:
            return datetime.combine(self.start_date, self.start_time)
        return None

    @start_datetime.expression
    def start_datetime(cls):
        """SQL expression for start datetime"""
        return func.datetime(cls.start_date, cls.start_time)

    @hybrid_property
    def end_datetime(self):
        """Get end datetime as Python datetime object"""
        if self.end_date and self.end_time:
            return datetime.combine(self.end_date, self.end_time)
        return None

    @end_datetime.expression
    def end_datetime(cls):
        """SQL expression for end datetime"""
        return func.datetime(cls.end_date, cls.end_time)
