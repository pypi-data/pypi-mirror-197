"""Houses Computer Group Type"""

from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, Type, Dict

from pyjamf.types.classic.models._computer import Computer
from pyjamf.types.classic.models._jamf_entity import JAMFEntity
from pyjamf.types.classic.models._abstract_computer_group import AbstractComputerGroup

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="ComputerGroup")

class ComputerGroup(JAMFEntity, AbstractComputerGroup):
    """ Computer Group Type
    """
    
    _id: int
    _name: str
    _is_smart: bool
    _site: dict
    _criteria: list
    _computers: list
    
    def __init__(self: E, client: JamfServiceClient) -> None:
        super().__init__(client)
        
        self._id = 0
        self._name = ""
        self._is_smart = False
        self._site = {}
        self._criteria = []
        self._computers = []
        
    @property
    def id(self) -> int:
        
        return self._id
    
    @property
    def name(self) -> str:
        
        return self._name
    
    @property
    def is_smart(self) -> bool:
        
        return self._is_smart
    
    @property
    def site(self) -> dict:
        
        return self._site
    
    @property
    def criteria(self) -> list:
        
        return self._criteria
    
    @property
    def computers(self) -> list:
        
        return self._computers
    
    @classmethod
    def from_json(cls: Type[E], entry: Dict, client: JamfServiceClient) -> E:
        
        _new = cls(client)
        
        _new._id = entry.get("id", 0)
        _new._name = entry.get("name", "")
        _new._is_smart = entry.get("is_smart", False)
        _new._site = entry.get("site", "")
        _new._criteria = entry.get("criteria", [])
        
        _new._computers = entry.get("computers", [])
        
        if len(_new._computers) > 0:
            _new._computers = [Computer.from_json(computer, _new.Client) for computer in _new._computers]
        
        return _new