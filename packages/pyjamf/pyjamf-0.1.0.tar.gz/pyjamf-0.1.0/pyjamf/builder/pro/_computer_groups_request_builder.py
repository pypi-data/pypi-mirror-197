"""Houses Computer Groups Request Builder Type"""

from typing import Optional, Iterable, TypeVar

from pyrestsdk.type.model import QueryOption

from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.builder.pro._client_check_in_history_request_builder import ClientCheckInHistoryRequestBuilder

O = TypeVar("O", bound=QueryOption)

class ComputerGroupsRequestBuilder(EntityRequestBuilder):
    """Computer Groups Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new CatagoriesRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """

        super().__init__(request_url, client)
        
    def request(self):
        return self.request_with_options(None)
        
    def request_with_options(self, options: Optional[Iterable[O]]):
        return super().request_with_options(options)
    
    def request_by_id(self, id: str):
        raise NotImplementedError("request_by_id has not been implemented yet")