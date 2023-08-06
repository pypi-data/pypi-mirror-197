"""Houses Department Entry Collection Request Type
"""

from __future__ import annotations

from typing import  TYPE_CHECKING, Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption

from pyrestsdk.request.supports_types import SupportsGetMethod, SupportsInvokeCollectionRequest

from pyjamf.request.classic._base_jamf_request import BaseJamfEntryRequest

from pyjamf.types.classic.models import Department
from pyjamf.types import RequestType

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

class DepartmentEntryCollectionRequest(
    SupportsInvokeCollectionRequest,
    SupportsGetMethod,
    BaseJamfEntryRequest[Department]
):
    """Department Entry Collection Request Type
    """
    
    __request_type__ = RequestType.Multiple
    __results_key__ = "departments"

    def __init__(self, request_url: str, client: JamfServiceClient, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        super().__init__(request_url, client, options)