"""Houses Computer Type"""

from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, Type, Dict

from abc import abstractmethod

from pyjamf.types.classic.models._abstract_jamf_entity import AbstractJAMFEntity

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="AbstractComputer")

class AbstractComputer(AbstractJAMFEntity):
    """Abstract Computer Type
    """
    
    _id: int
    _name: str
    _mac_address: str
    _alt_mac_address: str
    _serial_number: str
    
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
    def mac_address(self) -> str: ...

    @property
    @abstractmethod
    def alt_mac_address(self) -> str: ...

    @property
    @abstractmethod
    def serial_number(self) -> str: ...

    
    @classmethod
    @abstractmethod
    def from_json(cls: Type[E], entry: Dict, client: JamfServiceClient) -> E: ...
