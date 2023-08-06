from typing import Optional

from atoti_core import BaseLevels, raise_multiple_levels_with_same_name_error

from .query_hierarchies import QueryHierarchies
from .query_level import QueryLevel


class QueryLevels(BaseLevels[QueryHierarchies, QueryLevel]):
    """Flat representation of all the levels in the cube."""

    def _find_level(
        self,
        level_name: str,
        *,
        dimension_name: Optional[str] = None,
        hierarchy_name: Optional[str] = None,
    ) -> QueryLevel:
        if dimension_name is None:
            if hierarchy_name is None:
                level = self._flatten()[level_name]
                if level is not None:
                    return level
                hierarchies = [
                    hierarchy
                    for ((_, lvl_name), hierarchy) in self._hierarchies.items()
                    if level_name == lvl_name
                ]
                raise_multiple_levels_with_same_name_error(
                    level_name,
                    hierarchies=hierarchies,
                )

            return self._hierarchies[hierarchy_name][level_name]

        return self._hierarchies[(dimension_name, hierarchy_name)][level_name]  # type: ignore
