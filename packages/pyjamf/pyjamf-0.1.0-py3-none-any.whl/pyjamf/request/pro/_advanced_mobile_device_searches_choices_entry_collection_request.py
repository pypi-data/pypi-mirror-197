from typing import Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption

from pyrestsdk.request.supports_types import SupportsGetMethod, SupportsInvokeCollectionRequest

from pyjamf.request.pro._base_jamf_request import BaseJamfEntryRequest

class AdvancedMobileDeviceSearchesChoicesEntryCollectionRequest(
    SupportsInvokeCollectionRequest,
    SupportsGetMethod,
    BaseJamfEntryRequest[str]
):

    def __init__(self, request_url: str, client, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        super().__init__(request_url, client, options)
