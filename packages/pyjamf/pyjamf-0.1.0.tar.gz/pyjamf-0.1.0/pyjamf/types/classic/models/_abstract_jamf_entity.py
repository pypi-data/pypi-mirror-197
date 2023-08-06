from typing import TypeVar, TYPE_CHECKING, Type, Dict

from abc import abstractmethod

from pyrestsdk.type.model._abstract_entity import AbstractEntity

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="AbstractJAMFEntity")
J = TypeVar("J", bound = "JamfServiceClient")

class AbstractJAMFEntity(AbstractEntity):
    
    def __init__(self: E, client: J) -> None:        
        super().__init__(client)
    
    @classmethod
    @abstractmethod
    def from_json(cls: Type[E], entry: Dict, client: J) -> E:
        """Converts provided dict entry to Abstract JAMF Entity

        Args:
            cls (Type[E]): The Abstract JAMF Entity class
            entry (Dict): The dictionary to unmarshal
            client (J): The request client

        Returns:
            E: The Abstract JAMF Entity
        """