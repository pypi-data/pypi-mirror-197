"""Raw layout."""

from typing import Dict, Union

from ..common_types import builtins


class TypeLayout(builtins.TypeRaw):
    """Raw type layout."""

    name: str
    properties: Union[Dict, None]
    hall_pk: Union[int, None]
