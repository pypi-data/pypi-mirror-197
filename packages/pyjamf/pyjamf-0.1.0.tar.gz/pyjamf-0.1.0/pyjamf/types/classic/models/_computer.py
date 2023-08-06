"""Houses Computer Type"""

from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, Type, Dict

from pyjamf.types.classic.models._jamf_entity import JAMFEntity
from pyjamf.types.classic.models._abstract_computer import AbstractComputer

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="Computer")

class Computer(JAMFEntity, AbstractComputer):
    """Computer Type
    """
    
    _id: int
    _name: str
    _mac_address: str
    _alt_mac_address: str
    _serial_number: str
    
    def __init__(self: E, client: JamfServiceClient) -> None:
        super().__init__(client)
        
        self._id = 0
        self._name = ""
        self._mac_address = ""
        self._alt_mac_address = ""
        self._serial_number = ""
    
    @property
    def id(self) -> int:
        return self._id
    @property
    def name(self) -> str:
        return self._name
    @property
    def mac_address(self) -> str:
        return self._mac_address
    @property
    def alt_mac_address(self) -> str:
        return self._alt_mac_address
    @property
    def serial_number(self) -> str:
        return self._serial_number
    
    @classmethod
    def from_json(cls: Type[E], entry: Dict, client: JamfServiceClient) -> E:
        
        _new = cls(client)
        
        _new._id = entry.get("id", 0)
        _new._name = entry.get("name", "")
        _new._mac_address = entry.get("mac_adress", "")
        _new._alt_mac_address = entry.get("alt_mac_address", "")
        _new._serial_number = entry.get("serial_number", "")
        
        return _new