"""Views."""

from typing import Dict, List, Union
from pydantic import Field as SchemaField
from spec.types import Spec
from service.ext import fn
from .raws.market_event import ChildEvent, EventProperties
from .common_types import (
    BreadCrumbs,
    QNA,
    HallLayout,
    Restriction,
    TypeSchema,
    TypeOptionalImage,
    TypeOptionalListImages,
    SizedSourceMarketImage,
    IdNameSchema,
    builtins,
)


class ViewCategory(builtins.TypeView):
    """View category."""

    pk: int
    slug: str

    level: int
    parent_pk: Union[int, None]

    breadcrumbs: List[BreadCrumbs]

    lookup_pk: List[int]
    lookup_slug: List[str]

    lookup_tag_pk: List[int]
    lookup_tag_slug: List[str]


class EventCategory(TypeSchema):
    """Event category."""

    id: int
    parent_id: Union[int, None]

    slug: str
    name: str

    visible_type: str

    breadcrumbs: List[BreadCrumbs]

    old_slug: Union[str, None]
    seo_text: Union[str, None]


class PlaceLocation(TypeSchema):
    """Place location."""

    id: int
    name: str
    subdomain: Union[int, None]
    country: Union[IdNameSchema, None]


class EventPlace(TypeSchema):
    """Event place."""

    id: int
    name: str

    slug: str

    cover: SizedSourceMarketImage
    preview: SizedSourceMarketImage

    description: str
    address: str
    how_to_get: Union[str, None]

    location: Union[PlaceLocation, None]

    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages

    url: Union[str, None]
    schema_title: Union[str, None]
    schema_webp: TypeOptionalImage
    schemas_webp: TypeOptionalListImages

    schema_url: TypeOptionalImage = SchemaField(
        alias='schema',
        default=None,
    )

    schemas_urls: TypeOptionalListImages = SchemaField(
        alias='schemas',
        default=None,
    )

    cover: Union[SizedSourceMarketImage, None]
    preview: Union[SizedSourceMarketImage, None]

    updated: Union[str, None]
    created: Union[str, None]


class EventParentPerson(IdNameSchema):
    """Event parent position."""

    position: Union[str, None]


class EventPerson(TypeSchema):
    """Event person."""

    id: int
    name: str
    slug: str
    parent: Union[EventParentPerson, None]


class MarketChildEvent(TypeSchema):
    """Market child event."""

    id: int
    parent_id: int

    is_fan_id: bool
    is_periodical: bool
    is_top: bool
    is_global: bool
    is_premiere: bool
    is_star_cast: bool
    is_rejected: bool
    is_rescheduled: bool
    is_full_house: bool
    has_open_date: bool

    date_start: Union[str, None]
    time_start: Union[str, None]
    date_finish: Union[str, None]
    time_finish: Union[str, None]

    widget: str


class MarketEvent(TypeSchema):
    """Market event."""

    id: int
    slug: str
    old_slug: Union[str, None]

    title: str
    description: str
    annotation: Union[str, None]
    short_reference: Union[str, None]

    restriction: Restriction

    date_start: Union[str, None]
    time_start: Union[str, None]
    date_finish: Union[str, None]
    time_finish: Union[str, None]

    is_fan_id: bool
    is_periodical: bool
    is_top: bool
    is_global: bool
    is_premiere: bool
    is_star_cast: bool
    is_rejected: bool
    is_rescheduled: bool
    is_full_house: bool
    has_open_date: bool

    dates: Union[List[MarketChildEvent], None]
    post_dates: Union[List[MarketChildEvent], None]

    subdomain: Union[str, None]
    event_category: EventCategory
    hall_layout: Union[HallLayout, None]
    place: Union[EventPlace, None]
    persons: Union[List[EventPerson], None]
    cover: SizedSourceMarketImage
    preview: SizedSourceMarketImage
    qna: Union[List[QNA], None]
    widget: Union[str, None]


class ViewEvent(builtins.TypeView):
    """View market event."""

    # Market event schema

    pk: int
    slug: str
    old_slug: Union[str, None]

    title: str
    description: str
    annotation: Union[str, None]
    short_reference: Union[str, None]

    restriction: Restriction

    start: Union[int, None]
    finish: Union[int, None]

    properties: EventProperties

    subdomain: Union[str, None]

    event_category: EventCategory

    children: Union[List[ChildEvent], None]
    max_date: Union[int, None]

    hall_layout: Union[HallLayout, None]
    place: Union[EventPlace, None]
    persons: Union[List[EventPerson], None]

    cover: SizedSourceMarketImage
    preview: SizedSourceMarketImage

    qna: Union[List[QNA], None]

    widget: Union[str, None]

    # Lookup view fields

    lookup_tag_pk: List[int]
    lookup_tag_slug: List[str]

    lookup_category_pk: List[int]
    lookup_category_slug: List[str]

    def _get_dates(self, spec: Spec, outdated: bool) -> List[MarketChildEvent]:
        """Get dates for market event."""

        ts_now = fn.current_stamp()

        if not self.children:
            return list()

        buff = list()

        for child in self.children:

            if outdated:
                if child.finish > ts_now:
                    continue
            else:
                if child.finish < ts_now:
                    continue

            date_start, time_start = fn.ts_split(ts=child.start, spec=spec)
            date_finish, time_finish = fn.ts_split(ts=child.finish, spec=spec)

            market_event = MarketChildEvent(
                id=child.pk,
                parent_id=self.pk,
                date_start=str(date_start),
                time_start=str(time_start),
                date_finish=str(date_finish),
                time_finish=str(time_finish),
                is_fan_id=child.properties.is_fan_id,
                is_periodical=child.properties.is_periodical,
                is_top=child.properties.is_top,
                is_global=child.properties.is_global,
                is_premiere=child.properties.is_premiere,
                is_star_cast=child.properties.is_star_cast,
                is_rejected=child.properties.is_rejected,
                is_rescheduled=child.properties.is_rescheduled,
                is_full_house=child.properties.is_full_house,
                has_open_date=child.properties.is_open_date,
                widget=self.widget,  # todo fix
            )

            buff.append(market_event)

        return buff

    def as_market_event(self, spec: Spec) -> MarketEvent:
        """As market event."""

        date_start, time_start = fn.ts_split(ts=self.start, spec=spec)
        date_finish, time_finish = fn.ts_split(ts=self.finish, spec=spec)

        current_dates = self._get_dates(spec=spec, outdated=False)
        post_dates = self._get_dates(spec=spec, outdated=True)

        return MarketEvent(
            id=self.pk,
            slug=self.slug,
            old_slug=self.old_slug,
            title=self.title,
            description=self.description,
            annotation=self.annotation,
            short_reference=self.short_reference,
            restriction=self.restriction,
            date_start=str(date_start),
            time_start=str(time_start),
            date_finish=str(date_finish),
            time_finish=str(time_finish),
            is_star_cast=self.properties.is_star_cast,
            is_premiere=self.properties.is_premiere,
            is_fan_id=self.properties.is_fan_id,
            is_rejected=self.properties.is_rejected,
            is_rescheduled=self.properties.is_rescheduled,
            is_full_house=self.properties.is_full_house,
            is_periodical=self.properties.is_periodical,
            is_top=self.properties.is_top,
            is_global=self.properties.is_global,
            has_open_date=self.properties.is_open_date,
            dates=current_dates,
            post_dates=post_dates,
            subdomain=self.subdomain,
            event_category=self.event_category,
            hall_layout=self.hall_layout,
            place=self.place,
            persons=self.persons,
            cover=self.cover,
            preview=self.preview,
            widget=self.widget,
            qna=self.qna,
        )
