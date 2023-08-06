from __future__ import annotations

from typing import  TYPE_CHECKING, Optional, Iterable, Union, TypeVar, List, Dict, Any, Type, Callable

from json import loads

from requests import Response

from pyrestsdk.request import BaseRequest
from pyrestsdk.type.model import QueryOption, HeaderOption

from pyjamf.types.pro.exceptions import ServiceException
from pyjamf.types.classic.models import JAMFEntity
from pyjamf.types import RequestType

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

B = TypeVar("B", bound="BaseJamfEntryRequest")
E = TypeVar("E", bound="JAMFEntity")


class BaseJamfEntryRequest(BaseRequest[E]):
    
    __request_type__ = RequestType.Single
    __results_key__ = ""

    def __init__(self, request_url: str, client, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        super().__init__(request_url, client, options)
        
        self.header_options.append(HeaderOption("accept","application/json"))

    def parse_response(
        self: B, _response: Optional[Response]
    ) -> Optional[Union[List[E], E]]:
        """Parses response into expected return type, list of generic type,
        single generic type or None"""

        if _response is None:
            return None

        _json_text = _response.text
        _json = loads(_json_text)
        
        results = _json[self.__results_key__]
        
        if self.__request_type__ == RequestType.Single:
            return self.parse_result(self._generic_type, results, self.Client)
        return self.parse_results(self._generic_type, results, self.Client)

    def parse_exception(self, response: Response):
        
        _json_text = response.text
        print(_json_text)
        _json = loads(_json_text)

        raise ServiceException.from_json(_json)
    
    def parse_results(self, obj_type: E, results: List[Dict[str, Any]], client: JamfServiceClient) -> List[E]:
        """Parses return into list of expected return type

        Args:
            obj_type (E): _description_
            results (Dict[str, Any]): JSON result from request
            client (JamfServiceClient): _description_

        Returns:
            E: The serialized object list
        """
        
        return [obj_type.from_json(raw_result, client) for raw_result in results]
    
    def parse_result(self, obj_type: E, result: Dict[str, Any], client: JamfServiceClient) -> E:
        """Parses return into expected return type

        Args:
            obj_type (E): _description_
            result (Dict[str, Any]): JSON result from request
            client (JamfServiceClient): _description_

        Returns:
            E: The serialized object
        """

        return obj_type.from_json(result, client)