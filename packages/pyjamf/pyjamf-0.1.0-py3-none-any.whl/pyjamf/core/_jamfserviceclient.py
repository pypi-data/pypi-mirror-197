"""Houses JAMF Service Client Type
"""

from requests import Session

from pyrestsdk import AbstractServiceClient

from pyjamf.core._client_factory import HTTPClientFactory

from pyjamf.builder.pro import JamfProRequestBuilder
from pyjamf.builder.classic import JamfClassicRequestBuilder


class JamfServiceClient(AbstractServiceClient):
    """JAMF Service Client Type
    """

    def __init__(self, credentials, hostname) -> None:
        self.jamf_session = self._get_session(credentials, hostname)

    @property
    def pro_api(self) -> JamfProRequestBuilder:
        """Creates JAMF Pro Request Builder

        Returns:
            JamfProRequestBuilder: The JAMF Pro Request Builder
        """

        return JamfProRequestBuilder(self.jamf_session.base_url+"/api", self)

    @property
    def classic_api(self) -> JamfClassicRequestBuilder:
        """Creates JAMF Classic Request Builder

        Returns:
            JamfClassicRequestBuilder: The JAMF Classic Request Builder
        """

        return JamfClassicRequestBuilder(self.jamf_session.base_url+"/JSSResource", self)

    def get(self, url: str, **kwargs):
        """Sends a GET request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return self.jamf_session.get(self._instance_url(url), **kwargs)

    def options(self, url, **kwargs):
        """Sends a OPTIONS request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.jamf_session.options(self._instance_url(url), **kwargs)

    def head(self, url, **kwargs):
        """Sends a HEAD request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.jamf_session.head(self._instance_url(url), **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """Sends a POST request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return self.jamf_session.post(self._instance_url(url), data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """Sends a PUT request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.jamf_session.put(self._instance_url(url), data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """Sends a PATCH request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return self.jamf_session.patch(self._instance_url(url), data=data, **kwargs)

    def delete(self, url, **kwargs):
        """Sends a DELETE request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return self.jamf_session.delete(self._instance_url(url), **kwargs)

    def _instance_url(self, url: str) -> str:
        """Appends BASE_URL to user provided path
        :param url: user provided path
        :return: graph_url
        """
        return self.jamf_session.base_url + url if (url[0] == '/') else url  # type: ignore

    @staticmethod
    def _get_session(credential, hostname: str) -> Session:
        """Gets JAMF session

        Args:
            credential (_type_): Credentials used for auth
            hostname (str): The hostname for JAMF Cloud

        Returns:
            Session: The JAMF Session
        """
        

        return HTTPClientFactory(hostname).create_with_default_middleware(credential)
