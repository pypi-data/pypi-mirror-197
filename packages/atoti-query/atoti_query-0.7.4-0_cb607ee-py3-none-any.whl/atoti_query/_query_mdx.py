from datetime import timedelta
from typing import Any, Literal, Protocol

import pandas as pd
from atoti_core import EMPTY_MAPPING, Context


class QueryMdx(Protocol):
    def __call__(
        self,
        mdx: str,
        *,
        context: Context = EMPTY_MAPPING,
        keep_totals: bool = False,
        mode: Literal["pretty", "raw"] = "pretty",
        timeout: timedelta = timedelta(seconds=30),
        **kwargs: Any,
    ) -> pd.DataFrame:
        ...
