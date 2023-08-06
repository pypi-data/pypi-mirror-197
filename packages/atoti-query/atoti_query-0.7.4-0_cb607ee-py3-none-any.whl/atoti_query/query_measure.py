from typing import Optional

from atoti_core import BaseMeasure


class QueryMeasure(BaseMeasure):
    def __init__(
        self,
        name: str,
        /,
        *,
        description: Optional[str],
        folder: Optional[str],
        formatter: Optional[str],
        visible: bool,
    ) -> None:
        super().__init__(name)

        self._description = description
        self._folder = folder
        self._formatter = formatter
        self._visible = visible

    @property
    def folder(self) -> Optional[str]:
        """Folder of the measure."""
        return self._folder

    @property
    def visible(self) -> bool:
        """Whether the measure is visible or not."""
        return self._visible

    @property
    def description(self) -> Optional[str]:
        """Description of the measure."""
        return self._description

    @property
    def formatter(self) -> Optional[str]:
        """Formatter of the measure."""
        return self._formatter
