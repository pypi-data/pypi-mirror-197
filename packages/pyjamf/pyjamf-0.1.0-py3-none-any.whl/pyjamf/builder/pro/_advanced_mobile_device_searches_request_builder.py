"""Houses Advanced Mobile Device Searches Request Builder Type"""

from typing import Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder

from pyjamf.builder.pro._advanced_mobile_device_searches_choices_request_builder import AdvancedMobileDeviceSearchesChoicesRequestBuilder
from pyjamf.builder.pro._advanced_mobile_device_searches_delete_multiple_request_builder import AdvancedMobileDeviceSearchesDeleteMultipleRequestBuilder

from pyjamf.request.pro import AdvancedMobileDeviceSearchesEntryRequest, AdvancedMobileDeviceSearchesEntryCollectionRequest


class AdvancedMobileDeviceSearchesRequestBuilder(EntityRequestBuilder):
    """Advanced Mobile Device Searches Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def choices(self) -> AdvancedMobileDeviceSearchesChoicesRequestBuilder:

        return AdvancedMobileDeviceSearchesChoicesRequestBuilder(self.append_segment_to_request_url("choices"), self.request_client)

    @property
    def delete_multiple(self) -> AdvancedMobileDeviceSearchesDeleteMultipleRequestBuilder:

        return AdvancedMobileDeviceSearchesDeleteMultipleRequestBuilder(self.append_segment_to_request_url("delete-multiple"), self.request_client)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> AdvancedMobileDeviceSearchesEntryCollectionRequest:

        return AdvancedMobileDeviceSearchesEntryCollectionRequest(self.request_url, self.request_client, options)

    def id(self, sys_id: str) -> AdvancedMobileDeviceSearchesEntryRequest:

        return AdvancedMobileDeviceSearchesEntryRequest(self.append_segment_to_request_url(sys_id), self.request_client, None)
