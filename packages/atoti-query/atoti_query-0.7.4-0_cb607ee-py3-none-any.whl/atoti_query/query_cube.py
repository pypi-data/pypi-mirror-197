from __future__ import annotations

from datetime import timedelta
from typing import Any, Iterable, Literal, Optional

import pandas as pd
from atoti_core import (
    BASE_SCENARIO_NAME,
    EMPTY_MAPPING,
    QUERY_DOC,
    BaseCube,
    BaseLevel,
    BaseMeasure,
    Context,
    QueryFilter,
    doc,
    get_query_args_doc,
)

from ._discovery import IndexedDiscoveryCube
from ._execute_gaq import ExecuteGaq
from ._generate_mdx import generate_mdx
from ._query_mdx import QueryMdx
from ._query_private_parameters import QueryPrivateParameters
from ._widget_conversion_details import WidgetConversionDetails
from .query_hierarchies import QueryHierarchies
from .query_levels import QueryLevels
from .query_measures import QueryMeasures


class QueryCube(BaseCube[QueryHierarchies, QueryLevels, QueryMeasures]):
    def __init__(
        self,
        name: str,
        /,
        *,
        cube: IndexedDiscoveryCube,
        execute_gaq: Optional[ExecuteGaq],
        hierarchies: QueryHierarchies,
        measures: QueryMeasures,
        query_mdx: QueryMdx,
    ) -> None:
        super().__init__(name, hierarchies=hierarchies, measures=measures)

        self._cube = cube
        self._execute_gaq = execute_gaq
        self._query_mdx = query_mdx

    @property
    def levels(self) -> QueryLevels:
        """Levels of the cube."""
        return QueryLevels(hierarchies=self.hierarchies)

    @doc(QUERY_DOC, args=get_query_args_doc(is_query_session=True))
    def query(
        self,
        *measures: BaseMeasure,
        context: Context = EMPTY_MAPPING,
        filter: Optional[QueryFilter] = None,  # pylint: disable=redefined-builtin
        include_empty_rows: bool = False,
        include_totals: bool = False,
        levels: Iterable[BaseLevel] = (),
        mode: Literal["pretty", "raw"] = "pretty",
        scenario: str = BASE_SCENARIO_NAME,
        timeout: timedelta = timedelta(seconds=30),
        **kwargs: Any,
    ) -> pd.DataFrame:
        query_private_parameters = QueryPrivateParameters(**kwargs)
        filter = query_private_parameters.condition if filter is None else filter

        levels_coordinates = [level._coordinates for level in levels]
        measures_coordinates = [measure._coordinates for measure in measures]

        if mode == "raw" and self._execute_gaq and not context:
            return self._execute_gaq(
                cube_name=self.name,
                filter=filter,
                include_empty_rows=include_empty_rows,
                include_totals=include_totals,
                levels_coordinates=levels_coordinates,
                measures_coordinates=measures_coordinates,
                scenario=scenario,
                timeout=timeout,
            )

        mdx = generate_mdx(
            cube=self._cube,
            filter=filter,
            include_empty_rows=include_empty_rows,
            include_totals=include_totals,
            levels_coordinates=levels_coordinates,
            measures_coordinates=measures_coordinates,
            scenario=scenario,
        )

        query_result = self._query_mdx(
            mdx,
            context=context,
            get_level_data_types=query_private_parameters.get_level_data_types,
            keep_totals=include_totals,
            mode=mode,
            timeout=timeout,
        )

        # Always use an MDX including totals because ActiveUI 5 then relies on context values to show/hide totals.
        if not include_totals and query_result._atoti_widget_conversion_details:
            query_result._atoti_widget_conversion_details = WidgetConversionDetails(
                mdx=generate_mdx(
                    cube=self._cube,
                    filter=filter,
                    include_empty_rows=include_empty_rows,
                    include_totals=True,
                    levels_coordinates=levels_coordinates,
                    measures_coordinates=measures_coordinates,
                    scenario=scenario,
                ),
                session_id=query_result._atoti_widget_conversion_details.session_id,
                widget_creation_code=query_result._atoti_widget_conversion_details.widget_creation_code,
            )

        return query_result
