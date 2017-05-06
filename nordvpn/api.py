import requests

from urllib.parse import urlparse
from urllib.request import urljoin

__all__ = 'Config', 'Nord'

class Config(object):
    """
    Nord Configuration Client
    """
    base = 'https://api.nordvpn.com'
    endpoints = {
        'address': '/user/address',
        'config': '/files/zipv2',
        'nameserver': '/dns/smart',
        'server': '/server',
        'stats': '/server/stats',
        'user': '/user/databytoken'
    }
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        if username and password:
            self.endpoints['oath'] = '/token/token/{username}'.format(
                username=username
            )

    def __repr__(self):
        username = self.username if self.username else 'anonymous'
        name = self.__class__.__name__
        return '<{name} [{username}]>'.format(
            name=name,
            username=username
        )

    @property
    def headers(self):
        base = urlparse(self.base)
        return {
            'User-Agent': '{app}/{version}'.format(
                app='NordVPN Client',
                version='0.0.1',
            ),
            'Host': base.netloc,
            'Connection': 'Close'
        }

class Nord(Config):
    """
    A Nord Clienht that interacts with the api.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        if name in self.api:
            return self.request(name)
        else:
            return super(self.__class__, self).__getattribute__(name)

    @property
    def api(self):
        return {
            k: urljoin(self.base, v) for k,v in self.endpoints.items()
        }

    def request(self, endpoint):
        return requests.get(self.api[endpoint], headers=self.headers)
