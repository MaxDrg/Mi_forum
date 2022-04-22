import urllib.parse as urlparse
from urllib.parse import urlencode
from config import Config
cfg = Config()

class Web:
    def __init__(self, user_id: int):
        self.__telegr_id = user_id

    def forum_url(self, passwd):
        params = {
            'telegr_id': self.__telegr_id,
            'passwd': passwd 
        }
        url_parts = list(urlparse.urlparse(cfg.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query) 
        return urlparse.urlunparse(url_parts)

    def forum_url(self, passwd):
        params = {
            'telegr_id': self.__telegr_id,
            'passwd': passwd 
        }
        url_parts = list(urlparse.urlparse(cfg.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query) 
        return urlparse.urlunparse(url_parts)