from decimal import Decimal
from datetime import datetime
import httpx
import xml.etree.ElementTree as ET
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from src.utils.logging import logger

from src.jobs.workers.abstractWorker import AbstractWorker
from src.repository import PlanRepository


class FeverUpWorker(AbstractWorker):
    URL = "https://provider.code-challenge.feverup.com/api/events"

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def fetch_raw_xml(self) -> str | None:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.URL)
                response.raise_for_status()
                return response.text
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 503:
                logger.error("Received 503 from server — will retry later")
                raise
            raise
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise

    def parse_plans(self, raw: str) -> list[dict]:
        if not raw:
            return []

        try:
            root = ET.fromstring(raw)
        except ET.ParseError as e:
            logger.error(f"Failed to parse XML: {e}")
            return []

        results = []
        for base_plan in root.findall(".//base_plan"):
            title = base_plan.attrib.get("title")
            sell_mode = base_plan.attrib.get("sell_mode")
            if sell_mode != "online":
                logger.info(
                    f"Event {title} found with sell_mode different than online, skipping"
                )
                continue
            for plan in base_plan.findall("./plan"):
                external_id = plan.attrib.get("plan_id")
                start_dt = plan.attrib.get("plan_start_date")
                end_dt = plan.attrib.get("plan_end_date")

                start_date, start_time = None, None
                end_date, end_time = None, None
                if start_dt:
                    try:
                        dt = datetime.fromisoformat(start_dt)
                        start_date = dt.date()
                        start_time = dt.time()
                    except:
                        logger.error(
                            f"Start date for plan {external_id} badly formatted"
                        )
                if end_dt:
                    try:
                        dt = datetime.fromisoformat(end_dt)
                        end_date = dt.date()
                        end_time = dt.time()
                    except:
                        logger.error(f"End date for plan {external_id} badly formatted")

                prices = []
                for zone in plan.findall("./zone"):
                    price = zone.attrib.get("price")
                    if price:
                        prices.append(Decimal(price))
                min_price = min(prices) if prices else None
                max_price = max(prices) if prices else None

                results.append(
                    {
                        "external_id": external_id,
                        "title": title,
                        "start_date": start_date,
                        "start_time": start_time,
                        "end_date": end_date,
                        "end_time": end_time,
                        "min_price": min_price,
                        "max_price": max_price,
                    }
                )

        return results

    def upsert_plans(self, plans: list[dict]):
        for p in plans:
            PlanRepository.upsertPlan(p)

    async def fetch_and_upsert(self, app):
        raw_xml = await self.fetch_raw_xml()
        plans = self.parse_plans(raw_xml)

        # DB operations inside app context
        with app.app_context():
            self.upsert_plans(plans)
