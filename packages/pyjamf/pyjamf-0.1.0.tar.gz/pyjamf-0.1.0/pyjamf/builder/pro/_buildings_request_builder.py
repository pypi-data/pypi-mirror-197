"""Houses Advanced Mobile Device Searches Choices Request Builder Type"""

from typing import Optional, Iterable

from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.builder.pro._buildings_delete_multiple_request_builder import BuildingsDeleteMultipleRequestBuilder
from pyjamf.builder.pro._buildings_export_request_builder import BuildingsExportRequestBuilder
from pyjamf.builder.pro._buildings_history_request_builder import BuildingsHistoryRequestBuilder


class BuildingsRequestBuilder(EntityRequestBuilder):
    """Advanced Mobile Device Searches Choices Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)
        
    @property
    def delete_multiple(self) -> BuildingsDeleteMultipleRequestBuilder:
        
        return BuildingsDeleteMultipleRequestBuilder(self.append_segment_to_request_url("delete-multiple"), self.request_client)
    
    @property
    def export(self) -> BuildingsExportRequestBuilder:
        
        return BuildingsExportRequestBuilder(self.append_segment_to_request_url("export"), self.request_client)
    
    @property
    def history(self) -> BuildingsHistoryRequestBuilder:
        
        return BuildingsHistoryRequestBuilder(self.append_segment_to_request_url("history"), self.request_client)
    
    def request_with_options(self, options: Optional[Iterable[O]]):
        pass
    
    def id(self, id: str):
        pass