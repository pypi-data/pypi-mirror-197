from typing import  TYPE_CHECKING, Optional, Iterable, Union, TypeVar, List, Dict, Any, Type, Callable

import json

from pyrestsdk.request import BaseRequest
from pyrestsdk.type.model import QueryOption, HeaderOption

from pyjamf.types.pro.exceptions import ServiceException, Error
from requests import Response

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

B = TypeVar("B", bound="BaseJamfEntryRequest")
J = TypeVar("J", bound="JamfServiceClient")


class BaseJamfEntryRequest(BaseRequest[J]):

    def __init__(self, request_url: str, client, options: Optional[Iterable[Union[QueryOption, HeaderOption]]]) -> None:
        super().__init__(request_url, client, options)

    def parse_response(
        self: B, _response: Optional[Response]
    ) -> Optional[Union[List[J], J]]:
        """Parses response into expected return type, list of generic type,
        single generic type or None"""

        if _response is None:
            return None

        _json_text = _response.text
        _json = json.loads(_json_text)

        try:
            _response.raise_for_status()
        except Exception as e:
            self.parse_exception(_json)
        else:
            _result = _json["results"]

        return self.parse_result(self._generic_type, _result, self.Client)

    def parse_exception(self, json: Dict[str, Any]):

        raise ServiceException.from_json(json)
    
    def parse_result(self, obj_type, result: Union[Dict[str, Any], List[Dict[str, Any]]], client) -> Union[List[J], J]:
        """parses return into expected return type"""

        _operation_dict: Dict[
            Type, Callable[[Union[Dict, List], JamfServiceClient], Union[List[J], J]]
        ] = {
            dict: lambda x, y: obj_type.from_json(x, y),  # type: ignore
            list: lambda x, y: [obj_type.from_json(raw_result, y) for raw_result in x],
        }

        if (_func := _operation_dict.get(type(result), None)) is None:
            raise Exception(f"unexpected type: {type(result)}")

        return _func(result, client)