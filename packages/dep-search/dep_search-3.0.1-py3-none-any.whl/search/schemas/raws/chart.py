"""Raw chart."""

from typing import List, Union

from ..common_types import SizedCloudImage, builtins


class TypeChart(builtins.TypeRaw):
    """Raw type chart."""

    name: str
    description: str

    slug: str
    old_slug: Union[str, None]

    start: Union[int, None]
    finish: Union[int, None]

    events: Union[List[int], None]
    categories: Union[List[int], None]

    position: int
    on_main: bool

    preview: Union[SizedCloudImage, None]
    cover: Union[SizedCloudImage, None]

    seo_name: Union[str, None]
    seo_description: Union[str, None]
