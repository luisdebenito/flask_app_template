from abc import ABC, abstractmethod
import asyncio


class AbstractWorker(ABC):
    """
    Abstract base worker.
    All workers must implement `fetch_and_upsert`.
    """

    @abstractmethod
    async def fetch_and_upsert(self, app):
        pass

    def run(self, app):
        """
        Entry point to run the worker asynchronously.
        """
        asyncio.run(self.fetch_and_upsert(app))
