from __future__ import annotations

from typing import Mapping, Optional, Sequence, TypedDict, Union

from ._discovery import DefaultMember

MeasureValue = Optional[Union[float, int, str, Sequence[Union[float, int]]]]


class CellSetHierarchy(TypedDict):
    dimension: str
    hierarchy: str


class CellSetMember(TypedDict):
    captionPath: Sequence[str]
    namePath: Sequence[str]


class CellSetAxis(TypedDict):
    hierarchies: Sequence[CellSetHierarchy]
    id: int
    positions: Sequence[Sequence[CellSetMember]]


class NormalizedCellSetAxis(CellSetAxis):
    maxLevelPerHierarchy: Sequence[int]
    """This property exists in CellSets returned by the WebSocket API but not in those returned by the REST API used by atoti.

    It is added when indexing the CellSet so that the logic to convert it to a table can be similar to the one used in ActiveUI.
    """


class CellSetCellProperties(TypedDict):
    BACK_COLOR: Optional[Union[int, str]]
    FONT_FLAGS: Optional[int]
    FONT_NAME: Optional[str]
    FONT_SIZE: Optional[int]
    FORE_COLOR: Optional[Union[int, str]]


class CellSetCell(TypedDict):
    formattedValue: str
    ordinal: int
    properties: CellSetCellProperties
    value: MeasureValue


class _CellSet(TypedDict):
    cube: str
    defaultMembers: Sequence[DefaultMember]


class CellSet(_CellSet):
    axes: Sequence[CellSetAxis]
    cells: Sequence[CellSetCell]


class IndexedCellSet(_CellSet):
    axes: Sequence[NormalizedCellSetAxis]
    cells: Mapping[int, CellSetCell]
