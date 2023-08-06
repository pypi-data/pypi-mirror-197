from __future__ import annotations

from atoti_core import BaseLevel, ReprJson


class QueryLevel(BaseLevel):
    def __init__(self, name: str, /, *, dimension: str, hierarchy: str) -> None:
        super().__init__(name)

        self._dimension = dimension
        self._hierarchy = hierarchy

    @property
    def dimension(self) -> str:
        """Dimension of the level."""
        return self._dimension

    @property
    def hierarchy(self) -> str:
        """Hierarchy of the level."""
        return self._hierarchy

    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
        }
        return (
            data,
            {"expanded": True, "root": self.name},
        )
