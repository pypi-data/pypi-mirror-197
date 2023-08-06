"""Houses Catagories Request Builder Type"""

from typing import Optional, Iterable, TypeVar

from pyrestsdk.type.model import QueryOption

from pyrestsdk.requestbuilder import EntityRequestBuilder

O = TypeVar("O", bound=QueryOption)

class ClientCheckInHistoryRequestBuilder(EntityRequestBuilder):
    """Catagories Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new CatagoriesRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """

        super().__init__(request_url, client)
        
    def request_with_options(self, options: Optional[Iterable[O]]):
        pass