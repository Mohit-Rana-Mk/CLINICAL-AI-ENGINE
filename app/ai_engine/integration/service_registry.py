import logging

logger = logging.getLogger(__name__)

class ServiceRegistry:
    """
    Registry for managing internal AI pipeline components and microservice status.
    """
    def __init__(self):
        self._services = {}
        logger.info("Service Registry initialized.")

    def register(self, service_name: str, instance: any):
        self._services[service_name] = instance
        logger.info(f"Registered service: {service_name}")

    def get(self, service_name: str):
        return self._services.get(service_name)

    def list_services(self) -> list[str]:
        return list(self._services.keys())