"""Houses Advanced Mobile Device Searches Choices Request Builder Type"""

from typing import Optional, Iterable

from pyrestsdk.requestbuilder import EntityRequestBuilder


class BuildingsRequestBuilder(EntityRequestBuilder):
    """Advanced Mobile Device Searches Choices Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)
        
    def request_with_options(self, options: Optional[Iterable[O]]):
        pass