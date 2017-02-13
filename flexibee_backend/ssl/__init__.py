import ssl
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class Ssl3HttpAdapter(HTTPAdapter):
    """"
    Transport adapter" that allows us to use SSLv3.
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block)  # ssl_version=ssl.PROTOCOL_SSLv3 - temoporary removed


sslrequests = requests.Session()
sslrequests.mount('https:', Ssl3HttpAdapter())
