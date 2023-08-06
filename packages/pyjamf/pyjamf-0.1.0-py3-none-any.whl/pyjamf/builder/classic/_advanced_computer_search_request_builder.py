"""Houses Computer Group Request Builder Type"""
from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import AdvancedComputerSearchEntryRequest

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class AdvancedComputerSearchesRequestBuilder(EntityRequestBuilder):
    """Computer Group Request Builder Type
    """

    def __init__(self, request_url: str, client: JamfServiceClient) -> None:
        """intializes a new ComputerGroupRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (JamfServiceClient): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def request(self):

        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]):
        
        raise NotImplementedError("request_with_options is not implemented yet")

    def request_by_id(self, id: str) -> AdvancedComputerSearchEntryRequest:
        """Constructs a Computer Group Id Request Builder

        Args:
            id (str): id of the device

        Returns:
            ComputerGroupIdRequestBuilder: The Computer Group Id Request Builder
        """

        return AdvancedComputerSearchEntryRequest(self.append_segment_to_request_url(f"/id/{id}"), self.request_client, None)
