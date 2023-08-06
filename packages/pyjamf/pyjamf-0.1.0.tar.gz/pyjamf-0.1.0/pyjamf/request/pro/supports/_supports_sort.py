from typing import TypeVar

from pyrestsdk.request.supports_types import SupportsQueryOptions
from pyrestsdk.type.model import QueryOption

S = TypeVar("S", bound="SupportsPage")


class SupportsPage(SupportsQueryOptions):

    def sort(self: S, field: str, direction: str) -> S:

        self.query_options.append(QueryOption(
            "page-size", f"{field}:{direction}"))

        return self
