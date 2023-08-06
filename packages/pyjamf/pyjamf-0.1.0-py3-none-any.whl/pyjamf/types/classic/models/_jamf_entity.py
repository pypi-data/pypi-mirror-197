from typing import TypeVar, TYPE_CHECKING, Type, Dict

from pyrestsdk.type.model import Entity

from pyjamf.types.classic.models._abstract_jamf_entity import AbstractJAMFEntity

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="JAMFEntity")
J = TypeVar("J", bound = "JamfServiceClient")

class JAMFEntity(Entity, AbstractJAMFEntity):
    
    def __init__(self: E, client: J) -> None:
        super().__init__(client)