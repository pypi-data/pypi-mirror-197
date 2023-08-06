"""Raw market event."""

from typing import Union, List

from ..common_types import TypeSchema, Restriction, SizedCloudImage, builtins


class EventMedia(TypeSchema):
    """Event media."""

    cover: Union[SizedCloudImage, None]
    preview: Union[SizedCloudImage, None]


class EventProperties(TypeSchema):
    """Event properties."""

    is_fan_id: bool
    is_periodical: bool
    is_top: bool
    is_global: bool
    is_premiere: bool
    is_star_cast: bool
    is_rejected: bool
    is_rescheduled: bool
    is_full_house: bool
    is_open_date: bool


class AnyEvent(TypeSchema):
    """Any event schema."""

    properties: EventProperties

    start: Union[int, None]
    finish: Union[int, None]

    widget: Union[str, None]


class ChildEvent(AnyEvent):
    """Child event."""

    pk: int


class QNA(TypeSchema):
    """QNA schema."""

    id: int
    answer: Union[str, None]
    question: Union[str, None]


class TypeMarketEvent(builtins.TypeRaw, AnyEvent):
    """Type market event.

    location_pk - subdomain link
    persons - list of persons links
    tags - list of tags links
    children - list of children events

    max_date - max($children.$finish)
    """

    slug: str
    old_slug: Union[str, None]

    restriction: Restriction

    title: str
    description: Union[str, None]
    annotation: Union[str, None]
    short_reference: Union[str, None]

    # Linked fields
    category_pk: Union[int, None]
    place_pk: Union[int, None]

    layout_pk: Union[int, None]
    persons: Union[List[int], None]
    tags: Union[List[int], None]
    qna: Union[List[QNA], None]

    # Calculated fields
    media: Union[EventMedia, None]
    children: Union[List[ChildEvent], None]
    max_date: Union[int, None]
