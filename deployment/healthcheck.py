import sys
import urllib.request
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthCheck")

HEALTH_URL = "http://localhost:8000/health"
MAX_RETRIES = 15
RETRY_DELAY = 3  # seconds between attempts

def check_health():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Pinging health check endpoint: {HEALTH_URL} (Attempt {attempt}/{MAX_RETRIES})")
            req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "HealthCheckBot"})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    logger.info(f"Health check passed successfully: {data}")
                    sys.exit(0)
                else:
                    logger.warning(f"Health check returned HTTP status: {response.status}, retrying...")
        except Exception as e:
            logger.warning(f"Connection attempt failed ({e}), container/models likely still initializing...")
        
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    logger.error("Health check failed: Max retries reached. Server or ML models failed to respond in time.")
    sys.exit(1)

if __name__ == "__main__":
    check_health()
