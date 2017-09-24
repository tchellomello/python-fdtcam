"""Python FDT Camera module."""
import requests
from .const import (
    DEFAULT_HTTP_PORT, DEFAULT_USERNAME, DEFAULT_PASSWORD)


class FDTCam(object):
    """FDT IP Camera module."""

    def __init__(self,
                 host,
                 username=DEFAULT_USERNAME,
                 password=DEFAULT_PASSWORD,
                 http_port=DEFAULT_HTTP_PORT):
        """Initialize FDT IP Camera module."""
        self._host = host
        self._username = username
        self._password = password
        self._http_port = http_port
        self.session = requests.Session()

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self._host)

    @property
    def __baseurl(self):
        """Base URL used CGI API requests on FDT Camera."""
        return "http://" + self._host \
                + "/cgi-bin/hi3510/param.cgi?cmd={}&-usr=" \
                + self._username + "&-pwd=" + self._password

    @property
    def __command_url(self):
        """Base command URL used by CGI API requests."""
        return "http://" + self._host \
                + "/cgi-bin/hi3510/{}&-usr=" \
                + self._username + "&-pwd=" + self._password

    def __to_dict(self, response):
        """Format response to dict."""
        if not isinstance(response, str):
            raise

        # dict to return
        rdict = {}

        # remove single quotes and semi-collon characters
        response = response.replace('\'', '').replace(';', '')

        # eliminate 'var ' from response and create a list
        rlist = [l.split('var ', 1)[1] for l in response.splitlines()]

        # for each member of the list, remove the double quotes
        # and populate dictionary
        for item in rlist:
            key, value = item.replace('"', '').strip().split('=')
            rdict[key] = value

        return rdict

    def query(self, cmd):
        """Generic abstraction to run query."""
        url = self.__baseurl.format(cmd)
        req = self.session.get(url)
        if req.ok and req.status_code == 200:
            try:
                return self.__to_dict(req.text)
            except:
                return req.text
        req.raise_for_status()

    @property
    def device_type(self):
        """Return device type."""
        return self.query('getdevtype').get('devtype')

    def get_server_time(self):
        """Return server time."""
        return self.query('getservertime')

    def get_server_info(self):
        """Return camera attributes."""
        return self.query('getserverinfo')

    @property
    def current_users(self):
        """Return number of online users."""
        return self.query('getstreamnum').get('stream_num')

    def get_ntp_info(self):
        """Return NTP info."""
        return self.query('getntpattr')

    def get_snapshot(self, filename=None):
        """Return camera snapshot."""
        url = self.__command_url.format('web/tmpfs/auto.jpg')

        req = self.session.get(url)
        if req.ok:
            if filename is None:
                return req.content

            with open(filename, 'wb') as fd:
                fd.write(req.content)
        return

    @property
    def factory_reset(self):
        """Restore factory settings."""
        url = self.__command_url.format('sysreset.cgi')
        return self.session.get(url)

    @property
    def reboot(self):
        """Reboot camera."""
        url = self.__command_url.format('sysreboot.cgi')
        return self.session.get(url)
