import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.jobs.workers.feverUpWorker import FeverUpWorker


@pytest.mark.asyncio
async def test_fetch_raw_xml_success():
    worker = FeverUpWorker()

    # Mock httpx.AsyncClient.get to return a successful response
    mock_response = MagicMock()  # Changed from AsyncMock to MagicMock
    mock_response.text = "<xml></xml>"
    mock_response.raise_for_status = MagicMock()  # Explicitly make it a MagicMock

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = mock_client_cls.return_value.__aenter__.return_value
        mock_client.get = AsyncMock(return_value=mock_response)  # Only get() is async

        result = await worker.fetch_raw_xml()
        assert result == "<xml></xml>"
        mock_response.raise_for_status.assert_called_once()


def test_parse_plans_empty_input():
    worker = FeverUpWorker()
    result = worker.parse_plans(None)
    assert result == []


def test_parse_plans_invalid_xml():
    worker = FeverUpWorker()
    invalid_xml = "<xml><unclosed_tag></xml>"
    result = worker.parse_plans(invalid_xml)
    assert result == []


def test_parse_plans_valid_xml():
    worker = FeverUpWorker()
    sample_xml = """
    <root>
        <base_plan title="Test Plan" sell_mode="online">
            <plan plan_id="123" plan_start_date="2025-12-22T10:00:00" plan_end_date="2025-12-22T12:00:00">
                <zone price="10.5"/>
                <zone price="15.0"/>
            </plan>
        </base_plan>
    </root>
    """
    result = worker.parse_plans(sample_xml)
    assert len(result) == 1
    plan = result[0]
    assert plan["external_id"] == "123"
    assert plan["title"] == "Test Plan"
    assert plan["start_date"] == datetime.fromisoformat("2025-12-22T10:00:00").date()
    assert plan["start_time"] == datetime.fromisoformat("2025-12-22T10:00:00").time()
    assert plan["min_price"] == Decimal("10.5")
    assert plan["max_price"] == Decimal("15.0")


def test_parse_plans_invalid_offline_xml():
    worker = FeverUpWorker()
    sample_xml = """
    <root>
        <base_plan title="Test Plan" sell_mode="offline">
            <plan plan_id="123" plan_start_date="2025-12-22T10:00:00" plan_end_date="2025-12-22T12:00:00">
                <zone price="10.5"/>
                <zone price="15.0"/>
            </plan>
        </base_plan>
    </root>
    """
    result = worker.parse_plans(sample_xml)
    assert len(result) == 0


def test_upsert_plans_calls_repository():
    worker = FeverUpWorker()
    plans = [{"external_id": "123"}]

    with patch(
        "src.jobs.workers.feverUpWorker.PlanRepository.upsertPlan"
    ) as mock_upsert:
        worker.upsert_plans(plans)
        mock_upsert.assert_called_once_with(plans[0])


@pytest.mark.asyncio
async def test_fetch_and_upsert_calls_all_methods():
    worker = FeverUpWorker()
    raw_xml = "<root></root>"
    plans = [{"external_id": "123"}]

    # Mock fetch_raw_xml and parse_plans
    worker.fetch_raw_xml = AsyncMock(return_value=raw_xml)
    worker.parse_plans = MagicMock(return_value=plans)
    worker.upsert_plans = MagicMock()

    # Mock app context manager
    mock_app = MagicMock()
    mock_app.app_context.return_value.__enter__.return_value = None

    await worker.fetch_and_upsert(mock_app)
    worker.fetch_raw_xml.assert_awaited_once()
    worker.parse_plans.assert_called_once_with(raw_xml)
    worker.upsert_plans.assert_called_once_with(plans)
