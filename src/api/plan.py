from flask import Blueprint, request
from datetime import datetime
from src.utils.response import success, error
from src.repository import PlanRepository
from src.serializers import PlanSerializer

Plan_b = Blueprint("api_plan", __name__)


@Plan_b.route("/search", methods=["GET"])
def getAll():
    """
    GET /search
    Description:
        Returns plans/events filtered by optional date range.

    Query Params:
        starts_at (ISO 8601, optional) filter start datetime
        ends_at   (ISO 8601, optional) filter end datetime

    Responses:
        200: { "events": [ ... ] }
        400: Invalid parameters
        500: Internal Error
    """
    starts_at = request.args.get("starts_at")
    ends_at = request.args.get("ends_at")

    try:
        starts_at = (
            datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
            if starts_at
            else None
        )
        ends_at = (
            datetime.fromisoformat(ends_at.replace("Z", "+00:00")) if ends_at else None
        )

        # I'd validate that starts_at is always older than ends_at
        # but it maybe does make sense to use it freely
    except Exception:
        return error("Invalid parameters", 400, 400)

    results = PlanRepository.search(
        starts_at=starts_at,
        ends_at=ends_at,
    )

    return success({"events": PlanSerializer.serializeList(results)})
