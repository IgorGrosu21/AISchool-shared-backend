from shared_backend.utils.exceptions import NotFound

from .service import Service

class ServiceStorage:
  _debug: bool
  _services: dict[str, Service]

  def __init__(self, config: dict[str, dict[str, str]], client_id: str, debug: bool):
    self._debug = debug
    self._services = {}

    for service_id, service_config in config.items():
      if service_id == client_id:
        continue
      self._services[service_id] = self.serialize_service({'id': service_id, **service_config})

  def serialize_service(self, service_config: dict[str, str]) -> Service:
    return Service(service_config, self._debug)

  def get_service(self, service_id: str) -> Service | None:
    return self._services.get(service_id)

  def get_service_url(self, service_id: str) -> str:
    service = self.get_service(service_id)
    if not service:
      raise NotFound(f'Service {service_id} not found in service storage')
    return service.get_url()