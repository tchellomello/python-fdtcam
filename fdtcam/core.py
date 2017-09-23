"""Python FDT Camera module."""
import requests
from .const import DEFAULT_HTTP_PORT
from .exceptions import FDTException
from .helpers import myself


class FDTCam(object):
    """FDT IP Camera module."""

    def __init__(self, host, username, password, http_port=DEFAULT_HTTP_PORT):

        self._host = host
        self._username = username
        self._password = password
        self._http_port = http_port
        self.session = requests.Session()

    @property
    def baseurl(self):
        """Base URL used CGI API requests on FDT Camera."""
        return "http://" + self._host + "/cgi-bin/hi3510/param.cgi?cmd={}&-usr=" \
                + self._username + "&-pwd=" + self._password

    def query(self, cmd):
        """Generic abstraction to run query."""
        url = self.baseurl.format(cmd)
        req = self.session.get(url)
        if req.ok and req.status_code == 200:
            return req.text
        req.raise_for_status()

    def getservertime(self):
        """Return server time."""
        return self.query(myself())

    def getserverinfo(self):
        """Return camera attributes."""
        return self.query(myself())
