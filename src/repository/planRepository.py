from src.models.plan import Plan, db
from typing import List
from datetime import datetime
import uuid


class PlanRepository:
    @staticmethod
    def search(starts_at: datetime | None, ends_at: datetime | None) -> List[Plan]:
        query = Plan.query

        # SQLAlchemy combines multiple .filter() calls with AND by default.
        # If both starts_at and ends_at are provided, both filters are applied
        if starts_at:
            query = query.filter(Plan.start_datetime >= starts_at)
        if ends_at:
            query = query.filter(Plan.end_datetime <= ends_at)

        return query.order_by(Plan.start_date.asc()).all()

    @staticmethod
    def getOneByExternalId(external_id: str) -> Plan | None:
        return Plan.query.filter_by(external_id=external_id).first()

    @classmethod
    def upsertPlan(cls, plan_dict: dict) -> None:
        if not plan_dict["external_id"]:
            return
        existing = cls.getOneByExternalId(plan_dict["external_id"])
        if existing:
            # Update
            existing.title = plan_dict["title"]
            existing.start_date = plan_dict["start_date"]
            existing.start_time = plan_dict["start_time"]
            existing.end_date = plan_dict["end_date"]
            existing.end_time = plan_dict["end_time"]
            existing.min_price = plan_dict["min_price"]
            existing.max_price = plan_dict["max_price"]
        else:
            # Insert new
            new_plan = Plan(
                uid=str(uuid.uuid4()),
                external_id=plan_dict["external_id"],
                title=plan_dict["title"],
                start_date=plan_dict["start_date"],
                start_time=plan_dict["start_time"],
                end_date=plan_dict["end_date"],
                end_time=plan_dict["end_time"],
                min_price=plan_dict["min_price"],
                max_price=plan_dict["max_price"],
            )
            db.session.add(new_plan)

        db.session.commit()
