
from typing import Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption

from pyrestsdk.request.supports_types import SupportsGetMethod, SupportsInvokeRequest

from pyjamf.request.pro._base_jamf_request import BaseJamfEntryRequest

from pyjamf.types.pro.models import MobileDevice


class MobileDeviceEntryRequest(
    SupportsInvokeRequest,
    SupportsGetMethod,
    BaseJamfEntryRequest[MobileDevice]
):

    def __init__(self, request_url: str, client, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        super().__init__(request_url, client, options)
