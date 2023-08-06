from datetime import timedelta
from typing import Iterable, Optional, Protocol

import pandas as pd
from atoti_core import LevelCoordinates, MeasureCoordinates, QueryFilter


class ExecuteGaq(Protocol):
    def __call__(
        self,
        *,
        cube_name: str,
        filter: Optional[QueryFilter] = None,  # pylint: disable=redefined-builtin
        include_empty_rows: bool,
        include_totals: bool,
        levels_coordinates: Iterable[LevelCoordinates],
        measures_coordinates: Iterable[MeasureCoordinates],
        scenario: str,
        timeout: timedelta,
    ) -> pd.DataFrame:
        ...
