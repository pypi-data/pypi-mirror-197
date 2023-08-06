from __future__ import annotations

from typing import Callable, Iterable, Mapping, Optional, TypeVar, Union, overload

from ._discovery import (
    Discovery,
    DiscoveryCatalog,
    DiscoveryCube,
    DiscoveryDimension,
    DiscoveryHierarchy,
    IndexedDiscovery,
    IndexedDiscoveryCatalog,
    IndexedDiscoveryCube,
    IndexedDiscoveryDimension,
    IndexedDiscoveryHierarchy,
)
from ._named import Named

_IndexableT = TypeVar("_IndexableT", bound=Named, covariant=True)
_TransformedT = TypeVar("_TransformedT")


@overload
def _index(iterable: Iterable[_IndexableT], /) -> Mapping[str, _IndexableT]:
    ...


@overload
def _index(
    iterable: Iterable[_IndexableT],
    /,
    *,
    transform: Callable[[_IndexableT], _TransformedT],
) -> Mapping[str, _TransformedT]:
    ...


def _index(
    iterable: Iterable[_IndexableT],
    /,
    *,
    transform: Optional[Callable[[_IndexableT], _TransformedT]] = None,
) -> Mapping[str, Union[_IndexableT, _TransformedT]]:
    return {
        element["name"]: transform(element) if transform else element
        for element in iterable
    }


def _index_hierarchy(hierarchy: DiscoveryHierarchy, /) -> IndexedDiscoveryHierarchy:
    return {
        "caption": hierarchy["caption"],
        "levels": _index(hierarchy["levels"]),
        "name": hierarchy["name"],
        "slicing": hierarchy["slicing"],
    }


def _index_dimension(dimension: DiscoveryDimension, /) -> IndexedDiscoveryDimension:
    return {
        "caption": dimension["caption"],
        "hierarchies": _index(dimension["hierarchies"], transform=_index_hierarchy),
        "name": dimension["name"],
        "type": dimension["type"],
    }


def _index_cube(cube: DiscoveryCube, /) -> IndexedDiscoveryCube:
    return {
        "defaultMembers": cube["defaultMembers"],
        "dimensions": _index(cube["dimensions"], transform=_index_dimension),
        "measures": _index(cube["measures"]),
        "name": cube["name"],
    }


def _index_catalog(catalog: DiscoveryCatalog, /) -> IndexedDiscoveryCatalog:
    return {
        "cubes": _index(catalog["cubes"], transform=_index_cube),
        "name": catalog["name"],
    }


def index_discovery(discovery: Discovery, /) -> IndexedDiscovery:
    """Index the discovery by name to provide faster access to its elements."""
    return {
        "catalogs": _index(discovery["catalogs"], transform=_index_catalog),
    }
