import pytest
from datetime import datetime, timedelta, timezone
from src.models.plan import Plan
from src.utils.database import db


# Static base date for all tests
BASE_DATE = datetime(2021, 7, 15, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def seed_plans(test_client):
    """Seed some plans for testing using the test DB."""
    plans = [
        Plan(
            external_id="1111",
            uid="Fakeuid1",
            title="First Event starting at 1pm, ending next day at 2pm",
            start_date=BASE_DATE.date(),  # 2021-07-15
            start_time=(BASE_DATE + timedelta(hours=1)).time(),  # 13:00
            end_date=(BASE_DATE + timedelta(days=1)).date(),  # 2021-07-16
            end_time=(
                BASE_DATE + timedelta(days=1, hours=2)
            ).time(),  # 14:00 (26 hours from BASE_DATE)
            min_price=10.0,
            max_price=50.0,
            active=True,
        ),
        Plan(
            external_id="2222",
            uid="Fakeuid2",
            title="Second Event starting at 5pm, ending next day at 10pm",
            start_date=BASE_DATE.date(),  # 2021-07-15
            start_time=(BASE_DATE + timedelta(hours=5)).time(),  # 17:00
            end_date=(BASE_DATE + timedelta(days=1)).date(),  # 2021-07-16
            end_time=(
                BASE_DATE + timedelta(days=1, hours=10)
            ).time(),  # 22:00 (34 hours from BASE_DATE)
            min_price=20.0,
            max_price=60.0,
            active=True,
        ),
    ]

    db.session.bulk_save_objects(plans)
    db.session.commit()
    yield

    # Cleanup
    db.session.query(Plan).delete()
    db.session.commit()


def test_search_no_params(test_client, seed_plans):
    """All active plans should be returned if no params"""
    response = test_client.get("/search")
    assert response.status_code == 200
    data = response.json["data"]["events"]
    assert len(data) == 2
    assert all(plan["id"] in ["Fakeuid1", "Fakeuid2"] for plan in data)


def test_search_starts_at(test_client, seed_plans):
    """Filter by starts_at - should only return events starting after 2pm"""
    # Event1 starts at 1pm, Event2 starts at 5pm
    # Filter at 2pm should only return Event2
    starts_at = (BASE_DATE + timedelta(hours=2)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )  # 2021-07-15T14:00:00Z
    response = test_client.get(f"/search?starts_at={starts_at}")
    assert response.status_code == 200
    data = response.json["data"]["events"]
    assert len(data) == 1
    assert data[0]["id"] == "Fakeuid2"


def test_search_ends_at(test_client, seed_plans):
    """Filter by ends_at - should only return events ending before 5pm next day"""
    # Event1 ends at 2pm next day (26 hours), Event2 ends at 10pm next day (34 hours)
    # Filter at 5pm next day (29 hours) should only return Event1
    ends_at = (BASE_DATE + timedelta(days=1, hours=5)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )  # 2021-07-16T17:00:00Z
    response = test_client.get(f"/search?ends_at={ends_at}")
    assert response.status_code == 200
    data = response.json["data"]["events"]
    assert len(data) == 1
    assert data[0]["id"] == "Fakeuid1"


def test_search_starts_and_ends_at(test_client, seed_plans):
    """Filter by both starts_at and ends_at"""
    # Event1: starts 1pm, ends 2pm next day
    # Event2: starts 5pm, ends 10pm next day
    # Filter: starts >= 12pm, ends <= 6pm next day
    # Should only return Event1 (starts at 1pm, ends at 2pm next day)
    starts_at = BASE_DATE.strftime("%Y-%m-%dT%H:%M:%SZ")  # 2021-07-15T12:00:00Z
    ends_at = (BASE_DATE + timedelta(days=1, hours=6)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )  # 2021-07-16T18:00:00Z
    response = test_client.get(f"/search?starts_at={starts_at}&ends_at={ends_at}")
    assert response.status_code == 200
    data = response.json["data"]["events"]
    assert len(data) == 1
    assert data[0]["id"] == "Fakeuid1"


def test_error_starts_at_bad_format(test_client, seed_plans):
    """Badly formatted date throws 400 error"""
    starts_at = "2021-07-41T17%3A32%3A28Z"  # Invalid day (41)
    response = test_client.get(f"/search?starts_at={starts_at}")
    assert response.status_code == 400
    data = response.json["error"]
    assert data.get("code") == 400
    assert data.get("message") == "Invalid parameters"
