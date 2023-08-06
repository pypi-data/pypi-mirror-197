from __future__ import annotations

import math
from typing import (
    TYPE_CHECKING,
    Any,
    Collection,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import pandas as pd
from atoti_core import (
    Context,
    DataType,
    HierarchyCoordinates,
    LevelCoordinates,
    convert_to_pandas,
)

from ._cellset import (
    CellSetAxis,
    CellSetCellProperties,
    CellSetHierarchy,
    CellSetMember,
    IndexedCellSet,
    MeasureValue,
    NormalizedCellSetAxis,
)
from ._discovery import DefaultMember, IndexedDiscovery, IndexedDiscoveryCube
from ._get_cube import get_cube
from ._get_level_data_types import GetLevelDataTypes
from .query_result import QueryResult

if TYPE_CHECKING:
    # This requires pandas' optional dependency jinja2.
    from pandas.io.formats.style import Styler  # pylint: disable=nested-import


_MEASURES_HIERARCHY: CellSetHierarchy = {
    "dimension": "Measures",
    "hierarchy": "Measures",
}
_MEASURES_HIERARCHY_COORDINATES = HierarchyCoordinates(
    _MEASURES_HIERARCHY["dimension"],
    _MEASURES_HIERARCHY["hierarchy"],
)

_GRAND_TOTAL_CAPTION = "Total"


def _is_slicer(axis: CellSetAxis, /) -> bool:
    return axis["id"] == -1


def _get_default_measure(
    default_members: Iterable[DefaultMember], /
) -> Optional[CellSetMember]:
    return next(
        (
            CellSetMember(captionPath=member["captionPath"], namePath=member["path"])
            for member in default_members
            if member["dimension"] == _MEASURES_HIERARCHY["dimension"]
            and member["hierarchy"] == _MEASURES_HIERARCHY["hierarchy"]
        ),
        None,
    )


def _get_measure_names_and_captions(
    axes: Iterable[CellSetAxis], /, *, default_measure: Optional[CellSetMember] = None
) -> Tuple[Sequence[str], Sequence[str]]:
    if not axes:
        # When there are no axes at all, there is only one cell:
        # the value of the default measure aggregated at the top.
        return (
            ([default_measure["namePath"][0]], [default_measure["captionPath"][0]])
            if default_measure
            else ([], [])
        )

    # While looping on all the positions related to the Measures axis, the name of the same measure will come up repeatedly.
    # Only one occurrence of each measure name should be kept and the order of the occurrences must be preserved.
    name_to_caption = {
        position[hierarchy_index]["namePath"][0]: position[hierarchy_index][
            "captionPath"
        ][0]
        for axis in axes
        if not _is_slicer(axis)
        for hierarchy_index, hierarchy in enumerate(axis["hierarchies"])
        if hierarchy == _MEASURES_HIERARCHY
        for position in axis["positions"]
    }

    return tuple(name_to_caption), tuple(name_to_caption.values())


def _get_levels_coordinates(
    axes: Iterable[NormalizedCellSetAxis],
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> List[LevelCoordinates]:
    return [
        LevelCoordinates(hierarchy["dimension"], hierarchy["hierarchy"], level["name"])
        for axis in axes
        if not _is_slicer(axis)
        for hierarchy_index, hierarchy in enumerate(axis["hierarchies"])
        if hierarchy != _MEASURES_HIERARCHY
        for level_index, level in enumerate(
            cube["dimensions"][hierarchy["dimension"]]["hierarchies"][
                hierarchy["hierarchy"]
            ]["levels"].values()
        )
        if level_index < axis["maxLevelPerHierarchy"][hierarchy_index]
        and level["type"] != "ALL"
    ]


# See https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-fore-color-and-back-color-contents.
# Improved over from https://github.com/activeviam/activeui/blob/ba42f1891cd6908de618fdbbab34580a6fe3ee58/packages/activeui-sdk/src/widgets/tabular/cell/MdxCellStyle.tsx#L29-L48.
def _cell_color_to_css_value(color: Union[int, str], /) -> str:
    if isinstance(color, str):
        return "transparent" if color == '"transparent"' else color
    rest, red = divmod(color, 256)
    rest, green = divmod(rest, 256)
    rest, blue = divmod(rest, 256)
    return f"rgb({red}, {green}, {blue})"


# See https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-using-cell-properties.
def _cell_font_flags_to_styles(font_flags: int, /) -> List[str]:
    styles = []
    text_decorations = []

    if font_flags & 1 == 1:
        styles.append("font-weight: bold")
    if font_flags & 2 == 2:
        styles.append("font-style: italic")
    if font_flags & 4 == 4:
        text_decorations.append("underline")
    if font_flags & 8 == 8:
        text_decorations.append("line-through")

    if text_decorations:
        styles.append(f"""text-decoration: {" ".join(text_decorations)}""")

    return styles


def _cell_properties_to_style(properties: CellSetCellProperties, /) -> str:
    styles = []

    back_color = properties.get("BACK_COLOR")
    if back_color is not None:
        styles.append(f"background-color: {_cell_color_to_css_value(back_color)}")

    font_flags = properties.get("FONT_FLAGS")
    if font_flags is not None:
        styles.extend(_cell_font_flags_to_styles(font_flags))

    font_name = properties.get("FONT_NAME")
    if font_name is not None:
        styles.append(f"font-family: {font_name}")

    font_size = properties.get("FONT_SIZE")
    if font_size is not None:
        styles.append(f"font-size: {font_size}px")

    fore_color = properties.get("FORE_COLOR")
    if fore_color is not None:
        styles.append(f"color: {_cell_color_to_css_value(fore_color)}")

    return "; ".join(styles)


def _get_pythonic_formatted_value(formatted_value: str, /) -> str:
    lower_formatted_value = formatted_value.lower()

    if lower_formatted_value == "true":
        return "True"

    if lower_formatted_value == "false":
        return "False"

    return formatted_value


CellMembers = Dict[HierarchyCoordinates, CellSetMember]


def _get_cell_members_and_is_total(
    ordinal: int,
    /,
    *,
    axes: Iterable[NormalizedCellSetAxis],
    cube: IndexedDiscoveryCube,
    keep_totals: bool,
) -> Tuple[CellMembers, bool]:
    cell_members: CellMembers = {}
    is_total = False

    for axis in axes:
        if _is_slicer(axis):
            continue

        ordinal, position_index = divmod(ordinal, len(axis["positions"]))
        for hierarchy_index, hierarchy in enumerate(axis["hierarchies"]):
            hierarchy_coordinates = HierarchyCoordinates(
                hierarchy["dimension"], hierarchy["hierarchy"]
            )
            member = axis["positions"][position_index][hierarchy_index]

            is_total |= (
                len(member["namePath"]) != axis["maxLevelPerHierarchy"][hierarchy_index]
            )

            if not keep_totals and is_total:
                return {}, True

            cell_members[hierarchy_coordinates] = (
                member
                if hierarchy_coordinates == _MEASURES_HIERARCHY_COORDINATES
                or cube["dimensions"][hierarchy_coordinates.dimension_name][
                    "hierarchies"
                ][hierarchy_coordinates.hierarchy_name]["slicing"]
                else {
                    "captionPath": member["captionPath"][1:],
                    "namePath": member["namePath"][1:],
                }
            )

    return cell_members, is_total


def _get_member_name_index(
    levels_coordinates: Collection[LevelCoordinates],
    /,
    *,
    cube_name: str,
    get_level_data_types: Optional[GetLevelDataTypes] = None,
    members: Iterable[Tuple[Optional[str], ...]],
) -> Optional[pd.Index]:
    if not levels_coordinates:
        return None

    level_names = tuple(
        level_coordinates.level_name for level_coordinates in levels_coordinates
    )
    index_dataframe = pd.DataFrame(
        members,
        columns=level_names,
    )
    object_java_type: DataType = "Object"
    level_data_types: Mapping[LevelCoordinates, DataType] = (
        get_level_data_types(levels_coordinates, cube_name=cube_name)
        if get_level_data_types
        else {
            level_coordinates: object_java_type
            for level_coordinates in levels_coordinates
        }
    )
    for level_coordinates in levels_coordinates:
        index_dataframe[level_coordinates.level_name] = convert_to_pandas(
            index_dataframe[level_coordinates.level_name],
            data_type=level_data_types[level_coordinates],
        )

    if len(levels_coordinates) == 1:
        return pd.Index(index_dataframe.iloc[:, 0])

    return pd.MultiIndex.from_frame(index_dataframe)  # type: ignore[no-any-return]


def _get_member_caption_index(
    levels_coordinates: Collection[LevelCoordinates],
    /,
    *,
    cube: IndexedDiscoveryCube,
    members: Iterable[Tuple[Optional[str], ...]],
) -> Optional[pd.Index]:
    if not levels_coordinates:
        return None

    level_captions = tuple(
        next(
            level["caption"]
            for level_name, level in cube["dimensions"][
                level_coordinates.dimension_name
            ]["hierarchies"][level_coordinates.hierarchy_name]["levels"].items()
            if level_name == level_coordinates.level_name
        )
        for level_coordinates in levels_coordinates
    )

    members_with_grand_total_caption = (
        (_GRAND_TOTAL_CAPTION,)
        if all(element == None for element in member)
        else member
        for member in members
    )

    index_dataframe = pd.DataFrame(
        members_with_grand_total_caption,
        columns=level_captions,
        dtype="string",
    ).fillna("")

    if len(levels_coordinates) == 1:
        return pd.Index(index_dataframe.iloc[:, 0])

    return pd.MultiIndex.from_frame(index_dataframe)  # type: ignore[no-any-return]


def _create_measure_collection(
    measure_values: Iterable[Mapping[str, Any]],
    /,
    *,
    index: Optional[pd.Index],
    measure_name: str,
) -> Union[List[MeasureValue], pd.Series]:
    values: List[MeasureValue] = [values.get(measure_name) for values in measure_values]
    return (
        pd.Series(
            values,
            # Forcing `object` dtypes when some measure values are ``None`` to prevent pandas from inferring a numerical type and ending up with NaNs.
            dtype="object",
            index=index,
        )
        if None in values
        else values
    )


def _get_members_path(
    members: Iterable[CellSetMember],
    /,
    *,
    property_name: Literal["captionPath", "namePath"],
) -> Tuple[Optional[str], ...]:
    return tuple(
        name
        for member in members
        for name in member[property_name]
        # Replacing empty collection with `None` so that the member is still taken into account.
        or cast(  # mypy raises a `list-item` issue without the widening to `Optional[str]`.
            Iterable[Optional[str]], [None]
        )
    )


def _get_data_values(
    measure_values: Iterable[Mapping[str, Any]],
    /,
    *,
    index: Optional[pd.Index],
    measure_names: Collection[str],
) -> Dict[str, Union[List[MeasureValue], pd.Series]]:
    """Return a mapping of measure name to collection with a dtype of ``object`` when some measure values are ``None``."""
    return {
        measure_name: _create_measure_collection(
            measure_values, index=index, measure_name=measure_name
        )
        for measure_name in measure_names
    }


def cellset_to_query_result(
    cellset: IndexedCellSet,
    /,
    *,
    context: Optional[Context] = None,
    discovery: IndexedDiscovery,
    get_level_data_types: Optional[GetLevelDataTypes] = None,
    keep_totals: bool,
) -> QueryResult:
    """Convert an MDX CellSet to a pandas DataFrame."""
    default_measure = _get_default_measure(cellset["defaultMembers"])
    cube = get_cube(cellset["cube"], discovery=discovery)

    has_some_style = any(
        cell for cell in cellset["cells"].values() if cell["properties"]
    )

    member_captions_to_measure_formatted_values: Dict[
        Tuple[Optional[str], ...], Dict[str, str]
    ] = {}
    member_captions_to_measure_styles: Dict[
        Tuple[Optional[str], ...], Dict[str, str]
    ] = {}
    member_names_to_measure_values: Dict[Tuple[Optional[str], ...], Dict[str, Any]] = {}

    has_some_cells_or_any_non_measures_hierarchy = cellset["cells"] or any(
        hierarchy != _MEASURES_HIERARCHY
        for axis in cellset["axes"]
        for hierarchy in axis["hierarchies"]
    )
    cell_count = (
        # The received CellSet is sparse (i.e. empty cells are omitted) so it is important to loop over all the possible ordinals.
        math.prod([len(axis["positions"]) for axis in cellset["axes"]])
        if has_some_cells_or_any_non_measures_hierarchy
        else 0
    )

    for ordinal in range(0, cell_count):
        cell = cellset["cells"].get(ordinal)

        cell_members, is_total = _get_cell_members_and_is_total(
            ordinal,
            axes=cellset["axes"],
            cube=cube,
            keep_totals=keep_totals,
        )

        if keep_totals or not is_total:
            if not default_measure:
                raise RuntimeError(
                    "Expected a default member for measures but found none."
                )

            measure = cell_members.setdefault(
                _MEASURES_HIERARCHY_COORDINATES,
                default_measure,
            )

            non_measure_cell_members = tuple(
                cell_member
                for hierarchy, cell_member in cell_members.items()
                if hierarchy != _MEASURES_HIERARCHY_COORDINATES
            )

            member_names = _get_members_path(
                non_measure_cell_members, property_name="namePath"
            )
            member_captions = _get_members_path(
                non_measure_cell_members, property_name="captionPath"
            )

            member_names_to_measure_values.setdefault(member_names, {})[
                measure["namePath"][0]
            ] = (None if cell is None else cell["value"])
            member_captions_to_measure_formatted_values.setdefault(member_captions, {})[
                measure["captionPath"][0]
            ] = (
                ""
                if cell is None
                else _get_pythonic_formatted_value(cell["formattedValue"])
            )

            if has_some_style:
                member_captions_to_measure_styles.setdefault(member_captions, {})[
                    measure["captionPath"][0]
                ] = (
                    ""
                    if cell is None
                    else _cell_properties_to_style(cell["properties"])
                )

    levels_coordinates = _get_levels_coordinates(
        cellset["axes"],
        cube=cube,
    )

    member_name_index = _get_member_name_index(
        levels_coordinates,
        cube_name=cellset["cube"],
        get_level_data_types=get_level_data_types,
        members=member_names_to_measure_values.keys(),
    )

    member_caption_index = _get_member_caption_index(
        levels_coordinates,
        cube=cube,
        members=member_captions_to_measure_formatted_values.keys(),
    )

    measure_names, measure_captions = _get_measure_names_and_captions(
        cellset["axes"], default_measure=default_measure
    )

    formatted_values_dataframe = pd.DataFrame(
        member_captions_to_measure_formatted_values.values(),
        columns=measure_captions,
        dtype="string",
        index=member_caption_index,
    ).fillna("")

    def _get_styler() -> Styler:
        styler = formatted_values_dataframe.style

        if has_some_style:

            def apply_style(_: pd.DataFrame) -> pd.DataFrame:
                return pd.DataFrame(
                    member_captions_to_measure_styles.values(),
                    columns=measure_captions,
                    index=member_caption_index,
                )

            styler = styler.apply(
                apply_style,
                # `None` is documented as a valid argument value but pandas-stubs does not support it.
                axis=None,  # type: ignore
            )

        return styler

    data_values = _get_data_values(
        member_names_to_measure_values.values(),
        index=member_name_index,
        measure_names=measure_names,
    )

    return QueryResult(
        data_values,
        context=context,
        formatted_values=formatted_values_dataframe,
        get_styler=_get_styler,
        index=member_name_index,
    )
