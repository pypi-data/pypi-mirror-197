from typing import Mapping

from atoti_core import BaseHierarchy

from .query_level import QueryLevel


class QueryHierarchy(BaseHierarchy[QueryLevel]):
    def __init__(
        self,
        name: str,
        /,
        *,
        dimension: str,
        levels: Mapping[str, QueryLevel],
        slicing: bool,
    ) -> None:
        super().__init__(name, dimension=dimension)

        self._levels = levels
        self._slicing = slicing

    @property
    def levels(self) -> Mapping[str, QueryLevel]:
        """Levels of the hierarchy."""
        return self._levels

    @property
    def dimension(self) -> str:
        """Dimension of the hierarchy."""
        return self._dimension

    @property
    def slicing(self) -> bool:
        """Whether the hierarchy is slicing or not."""
        return self._slicing

    @property
    def name(self) -> str:
        """Name of the hierarchy."""
        return self._name

    def __getitem__(self, key: str, /) -> QueryLevel:
        return self.levels[key]
