import sys
import urllib.request
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthCheck")

HEALTH_URL = "http://localhost:8000/health"

def check_health():
    try:
        logger.info(f"Pinging health check endpoint: {HEALTH_URL}")
        req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "HealthCheckBot"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                logger.info(f"Health check passed successfully: {data}")
                sys.exit(0)
            else:
                logger.error(f"Health check failed with HTTP status: {response.status}")
                sys.exit(1)
    except Exception as e:
        logger.error(f"Health check connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_health()