"""Houses Computer Request Builder Type"""

from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import ComputerEntryRequest

from pyjamf.types.classic.enums import SubSet

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class ComputerIdRequestBuilder(EntityRequestBuilder):
    """Computer Request Builder Type
    """

    def __init__(self, request_url: str, client: JamfServiceClient) -> None:
        """intializes a new Computer Request Builder

        Args:
            request_url (str): the url to make the request to
            client (JamfServiceClient): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def request(self) -> ComputerEntryRequest:
        """Creates a Computer Entry Collection Request without options

        Returns:
            ComputerEntryRequest: The Computer Entry Collection Request
        """
        
        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> ComputerEntryRequest:
        """Creates a Computer Entry Collection Request with options

        Args:
            options (Optional[Iterable[Union[QueryOption, HeaderOption]]]): Query and Header options to add to request

        Returns:
            ComputerEntryRequest: The Computer Entry Request
        """
        
        return ComputerEntryRequest(self.request_url, self.request_client, options)
    
    def request_with_subset(self, subset: SubSet) -> ComputerEntryRequest:
        """Creates a Computer Entry Collection Request with subset

        Args:
            subset (SubSet): The subset

        Returns:
            ComputerEntryRequest: The Computer Entry Request
        """
        
        
        return ComputerEntryRequest(self.append_segment_to_request_url(f"subset/{subset.value}"), self.request_client, None)