import time
from src.jobs.workers import FeverUpWorker
from src.app_factory import create_app
from src.utils.logging import logger

WORKERS = [FeverUpWorker()]

# I've thought about doing it through a cron, but
# I don't see much difference between a cron and an interval in this file
INTERVAL = 60  # seconds


def run_all_workers(app):
    for worker in WORKERS:
        logger.info(f"Running {worker.__class__.__name__}")
        worker.run(app)


if __name__ == "__main__":
    app = create_app()

    while True:
        logger.info("Starting workers run...")
        try:
            run_all_workers(app)
        except Exception as e:
            logger.info(f"Error running workers: {e}")
        logger.info(f"Sleeping for {INTERVAL} seconds...\n")
        time.sleep(INTERVAL)
