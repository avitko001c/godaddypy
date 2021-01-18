import os
import pathlib
from godaddypy.configloader import load_config

__all__ = ['Account']


class Account(object):
    """The GoDaddyPy Account.

    An account is used to provide authentication headers to the `godaddypy.Client`.
    """
    configfile = pathlib.Path(os.path.expanduser('~/.godaddy/credentials'))
    if configfile.exists():
        try:
            config = load_config(configfile)
            _api_key = config['profiles']['default']['api_key']
            _api_secret = config['profiles']['default']['api_secret']
        except:
            _api_key = None
            _api_secret = None
            pass

    _SSO_KEY_TEMPLATE = 'sso-key {api_key}:{api_secret}'

    def __init__(self, api_key=_api_key, api_secret=_api_secret, delegate=None):
        """Create a new `godadypy.Account` object.

        :type api_key: str or unicode
        :param api_key: The API_KEY provided by GoDaddy

        :type api_secret: str or unicode
        :param api_secret: The API_SECRET provided by GoDaddy
        """

        self._api_key = api_key
        self._api_secret = api_secret
        self._delegate = delegate

    def get_headers(self):
        headers = {
            'Authorization': self._SSO_KEY_TEMPLATE.format(api_key=self._api_key,
                                                           api_secret=self._api_secret)
        }

        if self._delegate is not None:
            headers['X-Shopper-Id'] = self._delegate

        return headers
