"""Raw location."""

from ..common_types import IdNameSchema, builtins


class TypeLocation(builtins.TypeRaw):
    """Raw type location."""

    name: str
    country: IdNameSchema
