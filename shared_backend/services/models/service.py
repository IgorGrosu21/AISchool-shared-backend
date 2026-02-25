class Service:
  _id: str
  _dev_url: str
  _prod_url: str
  _debug: bool

  is_authenticated = True # For JWTServiceAuthentication

  def __init__(self, config: dict[str, str], debug: bool):
    self._id = config['id']
    self._dev_url = config['dev_url']
    self._prod_url = config['prod_url']
    self._debug = debug

  def get_id(self) -> str:
    return self._id.replace('-service', '')

  def get_url(self) -> str:
    return self._dev_url if self._debug else self._prod_url