from typing import TypeVar

from pyrestsdk.request.supports_types import SupportsQueryOptions
from pyrestsdk.type.model import QueryOption

S = TypeVar("S", bound="SupportsPage")


class SupportsPage(SupportsQueryOptions):

    def page(self: S, page: int) -> S:

        self.query_options.append(QueryOption("page", page))

        return self
