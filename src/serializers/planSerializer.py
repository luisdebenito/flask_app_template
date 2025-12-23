from src.models import Plan
from src.serializers.abstractSerializer import AbstractSerializer


class PlanSerializer(AbstractSerializer):
    @staticmethod
    def serializeSingle(plan: Plan) -> dict:
        return {
            "id": plan.uid,
            "title": plan.title,
            "start_date": plan.start_date.isoformat() if plan.start_date else None,
            "start_time": plan.start_time.isoformat() if plan.start_time else None,
            "end_date": plan.end_date.isoformat() if plan.end_date else None,
            "end_time": plan.end_time.isoformat() if plan.end_time else None,
            "min_price": float(plan.min_price) if plan.min_price is not None else None,
            "max_price": float(plan.max_price) if plan.max_price is not None else None,
        }
