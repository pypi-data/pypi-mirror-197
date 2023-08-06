"""Houses Department Type"""

from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, Type, Dict

from pyjamf.types.classic.models._abstract_deparment import AbstractDepartment
from pyjamf.types.classic.models._jamf_entity import JAMFEntity

if TYPE_CHECKING:
    from pyjamf.core import JamfServiceClient

E = TypeVar("E", bound="Department")


class Department(JAMFEntity, AbstractDepartment):
    """Department Type
    """

    _id: int
    _name: str

    def __init__(self: E, client: JamfServiceClient) -> None:
        super().__init__(client)

        self._id = 0
        self._name = ""

    @property
    def id(self) -> int:

        return self._id

    @property
    def name(self) -> str:

        return self._name

    @classmethod
    def from_json(cls: Type[E], entry: Dict, client: JamfServiceClient) -> E:

        _new = cls(client)

        _new._id = entry.get("id", 0)
        _new._name = entry.get("name", "")

        return _new
