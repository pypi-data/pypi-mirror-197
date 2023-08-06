"""Houses Departments Request Builder Type"""

from typing import Optional, Iterable

from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.pro import DepartmentsCollectionRequest


class DepartmentsRequestBuilder(EntityRequestBuilder):
    """Departments Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    def request_with_options(self, options: Optional[Iterable[O]]) -> DepartmentsCollectionRequest:

        return DepartmentsCollectionRequest(self.request_url, self.request_client, options)
