"""Houses Computer Request Builder Type"""

from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.builder.classic._computer_id_request_builder import ComputerIdRequestBuilder

from pyjamf.request.classic import ComputerEntryCollectionRequest, ComputerEntryRequest

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class ComputerRequestBuilder(EntityRequestBuilder):
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
    def request(self) -> ComputerEntryCollectionRequest:
        """Creates a Computer Entry Collection Request without options

        Returns:
            ComputerEntryCollectionRequest: The Computer Entry Collection Request
        """
        
        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> ComputerEntryCollectionRequest:
        """Creates a Computer Entry Collection Request with options

        Args:
            options (Optional[Iterable[Union[QueryOption, HeaderOption]]]): Query and Header options to add to request

        Returns:
            ComputerEntryCollectionRequest: The Computer Entry Collection Request
        """
        
        return ComputerEntryCollectionRequest(self.request_url, self.request_client, options)
    
    def request_by_id(self, id: str) -> ComputerIdRequestBuilder:
        """Creates a Computer Entry Request by the id of the Computer

        Args:
            id (str): id of the Computer

        Returns:
            ComputerIdRequestBuilder: The Computer Entry Request Builder
        """
        
        return ComputerIdRequestBuilder(self.append_segment_to_request_url(f"/id/{id}"), self.request_client)
    
    def request_by_name(self, name: str) -> ComputerEntryRequest:
        """Creates a Computer Entry Request by the name of the Computer

        Args:
            name (str): Name of the Computer

        Returns:
            ComputerEntryRequest: The Computer Entry Request
        """
        
        return ComputerEntryRequest(self.append_segment_to_request_url(f"/name/{name}"), self.request_client, None)
    
    def request_by_mac_address(self, mac_address: str) -> ComputerEntryRequest:
        """Creates a Computer Entry Request by the mac address of the Computer

        Args:
            mac_address (str): Mac address of the Computer

        Returns:
            ComputerEntryRequest: The Computer Entry Request
        """
        
        return ComputerEntryRequest(self.append_segment_to_request_url(f"/macaddress/{mac_address}"), self.request_client, None)
    
    def request_by_serial(self, serial: str) -> ComputerEntryRequest:
        """Creates a Computer Entry Request by the serial of the Computer

        Args:
            serial (str): Serial of the Computer

        Returns:
            ComputerEntryRequest: The Computer Entry Request
        """
        
        return ComputerEntryRequest(self.append_segment_to_request_url(f"/serialnumber/{serial}"), self.request_client, None)
    
    def request_by_udid(self, udid: str) -> ComputerEntryRequest:
        """Creates a Computer Entry Request by the udid of the Computer

        Args:
            udid (str): Udid of the Computer

        Returns:
            ComputerEntryRequest: The Computer Entry Request
        """
        
        return ComputerEntryRequest(self.append_segment_to_request_url(f"/udid/{udid}"), self.request_client, None)
    
    @property
    def request_subset_basic(self) -> ComputerEntryCollectionRequest:
        """Creates a Computer Entry Collection Request for subset basic

        Returns:
            ComputerEntryCollectionRequest: The Computer Entry Collection Request
        """
        
        return ComputerEntryCollectionRequest(self.append_segment_to_request_url("subset/basic"), self.request_client, None)