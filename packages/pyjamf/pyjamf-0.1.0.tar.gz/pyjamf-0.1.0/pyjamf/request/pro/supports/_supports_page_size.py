from typing import TypeVar

from pyrestsdk.request.supports_types import SupportsQueryOptions
from pyrestsdk.type.model import QueryOption

S = TypeVar("S", bound="SupportsPageSize")


class SupportsPageSize(SupportsQueryOptions):

    def page_size(self: S, page_size: int) -> S:

        self.query_options.append(QueryOption("page-size", page_size))

        return self
