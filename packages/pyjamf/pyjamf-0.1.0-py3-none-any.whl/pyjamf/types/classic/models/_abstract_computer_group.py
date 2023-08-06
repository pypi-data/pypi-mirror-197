
from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, Type, Dict

from abc import abstractmethod

from pyjamf.types.classic.models._abstract_jamf_entity import AbstractJAMFEntity

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="AbstractComputerGroup")

class AbstractComputerGroup(AbstractJAMFEntity):
    
    _id: int
    _name: str
    _is_smart: bool
    _site: dict
    _criteria: list
    _computers: list
    
    @abstractmethod
    def __init__(self: E, client: JamfServiceClient) -> None:
        super().__init__(client)
        
    @property
    @abstractmethod
    def id(self) -> int: ...
    
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @property
    @abstractmethod
    def is_smart(self) -> bool: ...
    
    @property
    @abstractmethod
    def site(self) -> dict: ...
    
    @property
    @abstractmethod
    def criteria(self) -> list: ...
    
    @property
    @abstractmethod
    def computers(self) -> list: ...
    
    @classmethod
    @abstractmethod
    def from_json(cls: Type[E], entry: Dict, client: JamfServiceClient) -> E:...