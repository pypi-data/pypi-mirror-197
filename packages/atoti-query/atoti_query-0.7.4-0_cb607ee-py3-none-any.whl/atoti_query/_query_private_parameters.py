from dataclasses import dataclass
from typing import Optional

from atoti_core import QueryFilter, deprecated, keyword_only_dataclass

from ._get_level_data_types import GetLevelDataTypes


@keyword_only_dataclass
@dataclass(frozen=True)
class QueryPrivateParameters:
    condition: Optional[QueryFilter] = None
    get_level_data_types: Optional[GetLevelDataTypes] = None

    def __post_init__(self) -> None:
        if self.condition is not None:
            deprecated(
                "The `condition` parameter is deprecated: it has been renamed `filter`."
            )
