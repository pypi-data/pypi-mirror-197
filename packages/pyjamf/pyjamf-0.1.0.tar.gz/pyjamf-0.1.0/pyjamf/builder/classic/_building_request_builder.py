"""Houses Building Request Builder Type"""

from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import BuildingEntryCollectionRequest, BuildingEntryRequest

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class BuildingRequestBuilder(EntityRequestBuilder):
    """Building Request Builder Type
    """

    def __init__(self, request_url: str, client: JamfServiceClient) -> None:
        """intializes a new ComputerGroupIdRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (JamfServiceClient): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def request(self) -> BuildingEntryCollectionRequest:
        """Creates a Building Entry Collection Request without options

        Returns:
            BuildingEntryCollectionRequest: The Building Entry Collection Request
        """
        
        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> BuildingEntryCollectionRequest:
        """Creates a Building Entry Collection Request with options

        Args:
            options (Optional[Iterable[Union[QueryOption, HeaderOption]]]): Query and Header options to add to request

        Returns:
            BuildingEntryCollectionRequest: The Building Entry Collection Request
        """
        
        return BuildingEntryCollectionRequest(self.request_url, self.request_client, options)
    
    def request_by_id(self, id: str) -> BuildingEntryRequest:
        """Creates a Building Entry Request by the id of the building

        Args:
            id (str): id of the building

        Returns:
            BuildingEntryRequest: The Building Entry Request
        """
        
        return BuildingEntryRequest(self.append_segment_to_request_url(f"/id/{id}"), self.request_client, None)
    
    def request_by_name(self, name: str) -> BuildingEntryRequest:
        """Creates a Building Entry Request by the name of the building

        Args:
            name (str): Name of the building

        Returns:
            BuildingEntryRequest: The Building Entry Request
        """
        
        return BuildingEntryRequest(self.append_segment_to_request_url(f"/name/{name}"), self.request_client, None)