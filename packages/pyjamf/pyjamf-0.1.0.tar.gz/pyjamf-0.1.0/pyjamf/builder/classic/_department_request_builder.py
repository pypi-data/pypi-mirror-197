"""Houses Department Request Builder Type"""

from __future__ import annotations

from typing import Optional, Iterable, Union, TYPE_CHECKING

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.request.classic import DepartmentEntryCollectionRequest, DepartmentEntryRequest

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class DepartmentRequestBuilder(EntityRequestBuilder):
    """Department Request Builder Type
    """

    def __init__(self, request_url: str, client: JamfServiceClient) -> None:
        """intializes a new Department Request Builder

        Args:
            request_url (str): the url to make the request to
            client (JamfServiceClient): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def request(self) -> DepartmentEntryCollectionRequest:
        """Creates a Department Entry Collection Request without options

        Returns:
            DepartmentEntryCollectionRequest: The Department Entry Collection Request
        """
        
        return self.request_with_options(None)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> DepartmentEntryCollectionRequest:
        """Creates a Department Entry Collection Request with options

        Args:
            options (Optional[Iterable[Union[QueryOption, HeaderOption]]]): Query and Header options to add to request

        Returns:
            DepartmentEntryCollectionRequest: The Department Entry Collection Request
        """
        
        return DepartmentEntryCollectionRequest(self.request_url, self.request_client, options)
    
    def request_by_id(self, id: str) -> DepartmentEntryRequest:
        """Creates a Department Entry Request by id

        Args:
            id (str): Id of department

        Returns:
            DepartmentEntryRequest: The Department Entry Request
        """
        
        return DepartmentEntryRequest(self.append_segment_to_request_url(f"id/{id}"), self.request_client, None)
    
    def request_by_name(self, name: str) -> DepartmentEntryRequest:
        """Creates a Department Entry Request by name

        Args:
            name (str): Name of department

        Returns:
            DepartmentEntryRequest: The Department Entry Request
        """
        
        return DepartmentEntryRequest(self.append_segment_to_request_url(f"name/{name}"), self.request_client, None)