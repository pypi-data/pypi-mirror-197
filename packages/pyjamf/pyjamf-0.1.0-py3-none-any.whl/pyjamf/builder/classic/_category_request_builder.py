"""Houses Category Request Builder Type"""

from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import CategoryEntryCollectionRequest, CategoryEntryRequest

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class CategoryRequestBuilder(EntityRequestBuilder):
    """Category Request Builder Type
    """

    def __init__(self, request_url: str, client: JamfServiceClient) -> None:
        """intializes a new ComputerGroupIdRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (JamfServiceClient): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def request(self) -> CategoryEntryCollectionRequest:
        """Creates a Category Entry Collection Request without options

        Returns:
            CategoryEntryCollectionRequest: The Category Entry Collection Request
        """
        
        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> CategoryEntryCollectionRequest:
        """Creates a Category Entry Collection Request with options

        Args:
            options (Optional[Iterable[Union[QueryOption, HeaderOption]]]): Query and Header options to add to request

        Returns:
            CategoryEntryCollectionRequest: The Category Entry Collection Request
        """
        
        return CategoryEntryCollectionRequest(self.request_url, self.request_client, options)
    
    def request_by_id(self, id: str) -> CategoryEntryRequest:
        """Creates a Category Entry Request by the id of the Category

        Args:
            id (str): id of the Category

        Returns:
            CategoryEntryRequest: The Category Entry Request
        """
        
        return CategoryEntryRequest(self.append_segment_to_request_url(f"/id/{id}"), self.request_client, None)
    
    def request_by_name(self, name: str) -> CategoryEntryRequest:
        """Creates a Category Entry Request by the name of the Category

        Args:
            name (str): Name of the Category

        Returns:
            CategoryEntryRequest: The Category Entry Request
        """
        
        return CategoryEntryRequest(self.append_segment_to_request_url(f"/name/{name}"), self.request_client, None)