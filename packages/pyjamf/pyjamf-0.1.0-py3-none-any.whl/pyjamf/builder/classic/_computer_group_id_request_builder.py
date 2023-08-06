"""Houses Computer Group Id Request Builder Type"""

from typing import Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import ComputerGroupEntryRequest


class ComputerGroupIdRequestBuilder(EntityRequestBuilder):
    """Computer Group Id Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new ComputerGroupIdRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def request(self) -> ComputerGroupEntryRequest:
        
        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> ComputerGroupEntryRequest:
        
        return ComputerGroupEntryRequest(self.request_url, self.request_client, options)
    
    def request_by_subset(self, subset: str):
        
        raise NotImplementedError("request_by_subset is not implemented")