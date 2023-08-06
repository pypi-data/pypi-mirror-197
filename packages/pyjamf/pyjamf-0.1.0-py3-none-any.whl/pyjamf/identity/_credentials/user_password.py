from requests import Session
import base64


class UsernamePasswordCredential():
    """Authenticates a user with a username and password."""
    
    def __init__(self, hostname, username, password) -> None:
        
        self._base_url = self.get_base_url(hostname)
        self._username = username
        self._password = password
        self._jamf_sesion = Session()
        
    def _request_token(self, **kwargs):
        app = self._get_app(**kwargs)
        return app.acquire_token_by_username_password(
            username=self._username,
            password=self._password
        )
        
    def get_base_url(self, hostname: str) -> str:
        return f"https://{hostname}.jamfcloud.com/api"
    
    def get_token(self):
        
        url = self.AppendSegmentToRequestUrl("auth/tokens")
        
        _encode_string = f"{self._username}:{self._password}".encode("ascii")
        _base64_string = base64.b64encode(_encode_string)
        _decode_base64_string = _base64_string.decode("ascii")
        
        headers = {"Authorization": f"Basic {_decode_base64_string}"}
        
        return self.post(url, headers=headers).get("token")
    
    def post(self, url, params=None, data=None, headers=None):
        return self._jamf_sesion.post(
            url=url,
            data=data,
            params=params,
            headers=headers
        ).json()
        
    def AppendSegmentToRequestUrl(self, url_segment:str) -> str:
        """Gets a URL that is the request builder's request URL with the segment appended.

        Args:
            url_segment (str): The segment to append to the request URL.

        Returns:
            str: A URL that is the request builder's request URL with the segment appended.
        """
        
        if not url_segment.startswith("/"):
            # Checks if url segment starts with /
            # Appends it if it does not
            url_segment = "/{0}".format(url_segment)
        
        return "{0}{1}".format(self._base_url, url_segment)