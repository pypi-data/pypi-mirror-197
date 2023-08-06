"""Houses Advanced Mobile Device Searches Delete Multiple Request Builder Type"""

from typing import Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption


from pyrestsdk.requestbuilder import EntityRequestBuilder


class AdvancedMobileDeviceSearchesDeleteMultipleRequestBuilder(EntityRequestBuilder):
    """Advanced Mobile Device Searches Delete Multiple Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    def request_with_options(self, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]):
        pass