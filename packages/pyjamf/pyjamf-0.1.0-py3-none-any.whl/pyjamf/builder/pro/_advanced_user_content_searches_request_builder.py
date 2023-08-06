"""Houses Advanced Mobile Device Searches Choices Request Builder Type"""

from typing import Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.pro import AdvancedUserContentSearchesEntryRequest, AdvancedUserContentSearchesEntryCollectionRequest


class AdvancedUserContentSearchesRequestBuilder(EntityRequestBuilder):
    """Advanced Mobile Device Searches Choices Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> AdvancedUserContentSearchesEntryCollectionRequest:
        
        return AdvancedUserContentSearchesEntryCollectionRequest(self.request_url, self.request_client, options)
    
    def id(self, id: str) -> AdvancedUserContentSearchesEntryRequest:
        
        return AdvancedUserContentSearchesEntryRequest(self.append_segment_to_request_url(id), self.request_client, None)