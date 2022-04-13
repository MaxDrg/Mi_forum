import urllib.parse as urlparse
from urllib.parse import urlencode
from config import Config
cfg = Config()

class Web:
    def __init__(self, user_id: int, passwd: str):
        self.__telegr_id = user_id
        self.__passwd = passwd

        params = {
            'telegr_id': self.__telegr_id,
            'passwd': self.__passwd 
        }

        url_parts = list(urlparse.urlparse(cfg.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query) 
        self.url = urlparse.urlunparse(url_parts)