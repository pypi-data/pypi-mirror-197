"""Source market event."""

from __future__ import annotations

from typing import Dict, List, Union

from service.ext import fn
from service.ext.testing import faker

from ..common_types import (
    IdNameSchema,
    HallLayout,
    QNA,
    Restriction,
    ShortEventPlace,
    ShortPersonSchema,
    SizedSourceMarketImage,
    TypeSchema,
    builtins,
)

from .helpers import event_date_time


class SourceEventMarketCategory(IdNameSchema):
    """Event market category."""

    breadcrumbs: List[Dict]


class Children(TypeSchema):
    """Children event."""

    id: int
    parent_id: int

    date_start: str
    time_start: str
    date_finish: str
    time_finish: str

    top: Union[bool, None] = False
    is_top: Union[bool, None] = False
    is_global: Union[bool, None] = False
    is_fan_id: Union[bool, None] = False
    is_premiere: Union[bool, None] = False
    is_rejected: Union[bool, None] = False
    is_star_cast: Union[bool, None] = False
    has_open_date: Union[bool, None] = False
    is_full_house: Union[bool, None] = False
    is_rescheduled: Union[bool, None] = False

    @classmethod
    def example(
        cls,
        pk: int,
        parent_pk: int = None,
        outdated: bool = False,
        **kwargs,
    ) -> Children:
        """Example."""

        _context = {
            'id': pk,
            'parent_id': parent_pk,
            'is_global': bool(kwargs.get('is_global')),
            'is_fan_id': bool(kwargs.get('is_fan_id')),
            'is_premiere': bool(kwargs.get('is_premiere')),
            'is_rejected': bool(kwargs.get('is_rejected')),
            'is_star_cast': bool(kwargs.get('is_star_cast')),
            'is_full_house': bool(kwargs.get('is_full_house')),
            'is_rescheduled': bool(kwargs.get('is_rescheduled')),
            'has_open_date': bool(kwargs.get('has_open_date')),
        }

        _top = any([bool(kwargs.get('top')), bool(kwargs.get('is_top'))])
        _context.update({'top': _top, 'is_top': _top})

        days = faker.any_int_pos()
        if outdated:
            (ds, ts, df, tf) = event_date_time(days=days, future=False)
        else:
            (ds, ts, df, tf) = event_date_time(days=days, future=True)

        _context.update({
            'date_start': ds,
            'time_start': ts,
            'date_finish': df,
            'time_finish': tf,
        })

        return Children(**_context)


class HallLayoutSafe(TypeSchema):
    """Hall layout safe schema."""

    id: Union[int, None]
    name: Union[str, None]
    hall_id: Union[int, None]


class SourceMarketEvent(builtins.TypeSource):
    """Source market event."""

    id: int

    slug: str
    old_slug: Union[str, None]

    title: str
    is_periodical: bool

    date: Union[str, None]
    description: Union[str, None]
    annotation: Union[str, None]
    short_reference: Union[str, None]

    date_start: Union[str, None]
    time_start: Union[str, None]
    date_finish: Union[str, None]
    time_finish: Union[str, None]

    top: bool
    has_open_date: bool
    is_global: bool
    is_rejected: bool
    is_rescheduled: bool
    is_premiere: bool
    is_full_house: bool
    is_top: bool
    is_fan_id: bool
    is_pushkin: bool

    is_filled: bool
    is_star_cast: bool
    is_show_hint: bool
    is_certificate_event: bool
    fill_by_template: bool

    restriction: Restriction

    hint_text: Union[str, None]

    children: Union[List[Children], None]
    event_category: Union[SourceEventMarketCategory, None]
    hall_layout: Union[HallLayoutSafe, None]
    persons: Union[List[ShortPersonSchema], None]
    place: Union[ShortEventPlace, None]

    country: Union[IdNameSchema, None]
    tags: Union[List[IdNameSchema], None]

    qna: Union[List[QNA], None]

    cover: Union[SizedSourceMarketImage, None]
    preview: Union[SizedSourceMarketImage, None]

    manager: Union[Dict, None]
    widget: Union[Dict, None]

    ticket_cover: Union[str, None]
    seo_place: Union[str, None]
    seo_dates: Union[str, None]
    seo_duration: Union[str, None]
    seo_base_names: Union[str, None]
    seo_place_accusative: Union[str, None]
    seo_place_prepositional: Union[str, None]
    seo_categories_with_preposition: Union[str, None]
    seo_short_name_with_preposition: Union[str, None]
    seo_event_name_with_preposition: Union[str, None]

    __i18n__ = [
        'title',
        'description',
        'annotation',
        'short_reference',
    ]

    @classmethod
    def example(
        cls,
        pk: int,
        title: str,
        description: str,
        slug: str,
        outdated: bool = False,
        future_pk: List[int] = None,
        outdated_pk: List[int] = None,
        annotation: str = 'annotation',
        short_reference: str = 'short_reference',
        widget: Dict = None,
        linked_category: Union[Dict, None] = None,
        linked_place: Union[Dict, None] = None,
        linked_persons: List[Dict] = None,
        linked_tags: List[Dict] = None,
        lang: str = 'ru',
        **kwargs,
    ) -> SourceMarketEvent:
        """Example."""

        children = list()
        (ds, ts, df, tf) = (None, None, None, None)

        is_periodical = any([bool(future_pk), bool(outdated_pk)])

        if is_periodical:

            if future_pk:
                for f_pk in future_pk:

                    _obj = Children.example(
                        pk=f_pk,
                        parent_pk=pk,
                        outdated=False,
                    )
                    children.append(_obj.dict())

            if outdated_pk:
                for o_pk in outdated_pk:
                    _obj = Children.example(
                        pk=o_pk,
                        parent_pk=pk,
                        outdated=True,
                    )
                    children.append(_obj.dict())
        else:

            days = faker.any_int_pos()
            if outdated:
                (ds, ts, df, tf) = event_date_time(days=days, future=False)
            else:
                (ds, ts, df, tf) = event_date_time(days=days, future=True)

        return SourceMarketEvent(
            id=pk,
            slug=slug,
            old_slug=f'{slug} old',
            title=title,
            description=description,
            annotation=annotation,
            short_reference=short_reference,
            event_category=linked_category,
            place=linked_place,
            persons=linked_persons,
            tags=linked_tags,
            hint_text=kwargs.get('hint_text', 'Hint text'),
            restriction=Restriction.TWELVE.value,
            hall_layout=kwargs.get('hall_layout'),
            country=kwargs.get('country'),
            qna=kwargs.get('qna'),
            cover=SizedSourceMarketImage.example(),
            preview=SizedSourceMarketImage.example(),
            is_periodical=is_periodical,
            is_global=kwargs.get('is_global', False),
            is_rejected=kwargs.get('is_rejected', False),
            is_rescheduled=kwargs.get('is_rescheduled', False),
            is_premiere=kwargs.get('is_premiere', False),
            is_pushkin=kwargs.get('is_pushkin', False),
            is_full_house=kwargs.get('is_full_house', False),
            is_top=kwargs.get('is_top', False),
            is_filled=kwargs.get('is_filled', False),
            is_star_cast=kwargs.get('is_star_cast', False),
            is_fan_id=kwargs.get('is_fan_id', False),
            is_certificate_event=kwargs.get('is_certificate_event', False),
            is_show_hint=kwargs.get('is_show_hint', False),
            fill_by_template=kwargs.get('fill_by_template', False),
            top=kwargs.get('top', False),
            has_open_date=kwargs.get('has_open_date', False),
            date_start=ds,
            time_start=ts,
            date_finish=df,
            time_finish=tf,
            children=children if bool(children) else None,
            date=kwargs.get('date'),
            ticket_cover=kwargs.get('ticket_cover'),
            widget=widget,
            manager=kwargs.get('manager'),
            seo_place=kwargs.get('seo_place', 'seo_place'),
            seo_dates=kwargs.get('seo_dates', 'seo_dates'),
            seo_duration=kwargs.get('seo_duration', 'seo_duration'),
            seo_base_names=kwargs.get('seo_base_names', 'seo_base_names'),
            seo_place_accusative=kwargs.get(
                'seo_place_accusative',
                'seo_place_accusative',
            ),
            seo_place_prepositional=kwargs.get(
                'seo_place_prepositional',
                'seo_place_prepositional',
            ),
            seo_categories_with_preposition=kwargs.get(
                'seo_categories_with_preposition',
                'seo_categories_with_preposition',
            ),
            seo_short_name_with_preposition=kwargs.get(
                'seo_short_name_with_preposition',
                'seo_short_name_with_preposition',
            ),
            seo_event_name_with_preposition=kwargs.get(
                'seo_event_name_with_preposition',
                'seo_event_name_with_preposition',
            ),
        )

    def _read_start(self) -> Union[int, None]:
        """Read start stamp."""

        if self.date_start and self.time_start:
            return fn.timestamp(fn.dt_join(self.date_start, self.time_start))

    def _read_finish(self) -> Union[int, None]:
        """Read finish stamp."""

        if self.date_finish and self.time_finish:
            return fn.timestamp(fn.dt_join(self.date_finish, self.time_finish))

    def _read_children_item(self, item: Children) -> Dict:
        """Read children item."""

        _start, _finish = None, None

        _properties = {
            'is_periodical': self.is_periodical,
            'is_top': any([item.is_top, item.top]),
            'is_global': item.is_global,
            'is_rejected': item.is_rejected,
            'is_rescheduled': item.is_rescheduled,
            'is_open_date': item.has_open_date,
            'is_premiere': item.is_premiere,
            'is_fan_id': item.is_fan_id,
            'is_star_cast': item.is_star_cast,
            'is_full_house': item.is_full_house,
        }

        if item.date_start and item.time_start:
            _start = fn.timestamp(
                fn.dt_join(item.date_start, item.time_start),
            )

        if item.date_finish and item.time_finish:
            _finish = fn.timestamp(
                fn.dt_join(item.date_finish, item.time_finish),
            )

        return {
            'pk': item.id,
            'properties': _properties,
            'start': _start,
            'finish': _finish,
            'widget': self.widget.get('id') if self.widget else None,
        }

    def _read_children(self) -> Union[List[Dict], None]:
        """Read children."""

        if not self.children or len(self.children) <= 0:
            return

        buff = list()
        for _child in self.children:
            buff.append(self._read_children_item(item=_child))

        return buff

    def _read_max_date(self) -> Union[int, None]:
        """Max timestamp include children or empty."""

        if not self.is_periodical:
            return self._read_finish()

        if self.children and len(self.children) > 0:

            buff = list()
            for _e in self.children:
                _ts = fn.timestamp(fn.dt_join(_e.date_finish, _e.time_finish))
                if _ts:
                    buff.append(_ts)

            return max(buff)

    def clean(self) -> Dict:
        """Overrides."""  # noqa

        layout_pk = None
        if self.hall_layout and self.hall_layout.id:
            layout_pk = self.hall_layout.id

        category_pk = self.event_category.id if self.event_category else None
        place_pk = self.place.id if self.place else None
        restriction = Restriction(self.restriction)
        tags = [_t.id for _t in self.tags] if self.tags else None
        persons = [_p.id for _p in self.persons] if self.persons else None

        if self.cover:
            cover = self.cover.to_sized_image()
        else:
            cover = None

        if self.preview:
            preview = self.preview.to_sized_image()
        else:
            preview = None

        return {
            'title': self.title,
            'description': self.description,
            'annotation': self.annotation,
            'short_reference': self.short_reference,
            'slug': self.slug,
            'restriction': restriction,
            'place_pk': place_pk,
            'layout_pk': layout_pk,
            'category_pk': category_pk,
            'start': self._read_start(),
            'finish': self._read_finish(),
            'children': self._read_children(),
            'qna': self.qna,
            'persons': persons,
            'tags': tags,
            'widget': self.widget.get('id') if self.widget else None,
            'properties': {
                'is_periodical': self.is_periodical,
                'is_global': self.is_global,
                'is_top': any([self.top, self.is_top]),
                'is_premiere': self.is_premiere,
                'is_star_cast': self.is_star_cast,
                'is_rejected': self.is_rejected,
                'is_rescheduled': self.is_rescheduled,
                'is_fan_id': self.is_fan_id,
                'is_full_house': self.is_full_house,
                'is_open_date': self.has_open_date,
            },
            'media': {'cover': cover, 'preview': preview},
            'max_date': self._read_max_date(),
        }
