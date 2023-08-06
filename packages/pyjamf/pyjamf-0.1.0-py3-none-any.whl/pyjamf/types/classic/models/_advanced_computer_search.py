from typing import TypeVar, TYPE_CHECKING, Type, Dict, List

from pyrestsdk.type.model import Entity

from pyjamf.types.classic.models._computer import Computer

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="AdvancedComputerSearch")
J = TypeVar("J", bound="JamfServiceClient")


class AdvancedComputerSearch(Entity):
    """Advanced Computer Search Type
    """
    
    _name: str
    _computers: list

    def __init__(self: E, client: J) -> None:
        super().__init__(client)

        self._computers = []

    @classmethod
    def from_json(cls: Type[E], entry: Dict, client: J) -> E:

        _new = cls(client)
        
        _new._name = entry.get("name", "")

        display_fields = entry["display_fields"]

        for computer in entry.get("computers", []):

            _computer = {
                "name": computer.get("name"),
                "udid": computer.get("udid"),
                "id": computer.get("id")
            }

            for disply_field in display_fields:
                
                key_name = disply_field["name"].replace(" ","_").replace("-","_")
                
                _computer[key_name] = computer.get(key_name)
                
            _new._computers.append(_computer)

        return _new
