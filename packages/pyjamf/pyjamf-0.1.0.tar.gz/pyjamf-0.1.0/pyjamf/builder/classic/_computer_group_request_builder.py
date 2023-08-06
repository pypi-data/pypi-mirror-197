"""Houses Computer Group Request Builder Type"""
from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import ComputerGroupEntryCollectionRequest
from pyjamf.builder.classic._computer_group_id_request_builder import ComputerGroupIdRequestBuilder

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class ComputerGroupRequestBuilder(EntityRequestBuilder[ComputerGroupEntryCollectionRequest]):
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
    def request(self) -> ComputerGroupEntryCollectionRequest:
        """Constructs a Computer Group Entry Collection Request without options

        Returns:
            ComputerGroupEntryCollectionRequest: The Computer Group Entry Collection Request
        """

        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> ComputerGroupEntryCollectionRequest:
        """Constructs a Computer Group Entry Collection Request with options

        Args:
            options (Optional[Iterable[Union[QueryOption, HeaderOption]]]):
            query or header options to include in the request

        Returns:
            ComputerGroupEntryCollectionRequest: The Computer Group Entry Collection Request
        """

        return ComputerGroupEntryCollectionRequest(self.request_url, self.request_client, options)

    def request_by_id(self, id: str) -> ComputerGroupIdRequestBuilder:
        """Constructs a Computer Group Id Request Builder

        Args:
            id (str): id of the device

        Returns:
            ComputerGroupIdRequestBuilder: The Computer Group Id Request Builder
        """

        return ComputerGroupIdRequestBuilder(self.append_segment_to_request_url(f"/id/{id}"), self.request_client)
