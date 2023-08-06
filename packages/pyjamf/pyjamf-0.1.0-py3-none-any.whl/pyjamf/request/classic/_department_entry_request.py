
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Iterable, Union

from pyrestsdk.type.model import QueryOption, HeaderOption

from pyrestsdk.request.supports_types import SupportsGetMethod, SupportsInvokeRequest, SupportsDeleteMethod, SupportsPutMethod

from pyjamf.request.classic._base_jamf_request import BaseJamfEntryRequest

from pyjamf.types.classic.models import Department
from pyjamf.types import RequestType

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient


class DepartmentEntryRequest(
    SupportsInvokeRequest,
    SupportsGetMethod,
    SupportsDeleteMethod,
    SupportsPutMethod,
    BaseJamfEntryRequest[Department]
):

    __request_type__ = RequestType.Single
    __results_key__ = "department"

    def __init__(self, request_url: str, client: JamfServiceClient, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        super().__init__(request_url, client, options)
