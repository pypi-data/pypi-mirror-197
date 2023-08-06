""" Houses Category Type
"""

from typing import TypeVar, TYPE_CHECKING, Type, Dict

from abc import abstractmethod

from pyrestsdk.type.model import Entity

from pyjamf.types.classic.models._abstract_category import AbstractCategory

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="Category")
J = TypeVar("J", bound="JamfServiceClient")


class Category(Entity, AbstractCategory):
    """Category Type
    """

    _id: int
    _name: str

    @abstractmethod
    def __init__(self: E, client: J) -> None:
        super().__init__(client)

    @property
    def id(self) -> int:
        
        return self._id

    @property
    def name(self) -> str:
        
        return self._name

    @classmethod
    def from_json(cls: Type[E], entry: Dict, client: J) -> E:
        
        _new = cls(client)

        _new._id = entry.get("id", 0)
        _new._name = entry.get("name", "")

        return _new
