"""Houses Building Entry Request Type
"""

from typing import Optional, Iterable, Union, TYPE_CHECKING, Optional, Iterable, Union, List, Dict, Any

from pyrestsdk.type.model import QueryOption, HeaderOption
from pyrestsdk.request.supports_types import SupportsGetMethod, SupportsInvokeRequest, SupportsDeleteMethod, SupportsPutMethod, SupportsPostMethod

from pyjamf.request.classic._base_jamf_request import BaseJamfEntryRequest
from pyjamf.types.classic.models import Computer
from pyjamf.types import RequestType

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class ComputerEntryRequest(
    SupportsInvokeRequest,
    SupportsGetMethod,
    SupportsDeleteMethod,
    SupportsPutMethod,
    SupportsPostMethod,
    BaseJamfEntryRequest[Computer]
):
    """Computer Entry Request Type
    """
    
    __request_type__ = RequestType.Single
    __results_key__ = "computer"

    def __init__(self, request_url: str, client: "JamfServiceClient", options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        print(request_url)
        super().__init__(request_url, client, options)
