"""Source chart."""

from __future__ import annotations

from typing import Dict, List, Union
from datetime import datetime

from service.ext import fn

from ..common_types import (
    IdNameSchema,
    SizedSourceMarketImage,
    TypeSchema,
    builtins,
)


class ChartSchedule(TypeSchema):
    """Chart schedule."""

    date_start: str
    time_finish: str
    time_start: str
    date_finish: str


class ChartEvent(TypeSchema):
    """Chart event schema."""

    id: int
    is_parent: Union[bool, None]
    title: Union[str, None]


class SourceChart(builtins.TypeSource):
    """Source chart."""

    id: int
    name: str
    description: Union[str, None]

    slug: str
    old_slug: Union[str, None]

    position: int
    on_main: bool

    events: Union[List[ChartEvent], None]

    preview: Union[SizedSourceMarketImage, None]
    cover: Union[SizedSourceMarketImage, None]

    category: Union[List[IdNameSchema], None]
    schedule: Union[ChartSchedule, None]

    seo_title: Union[str, None]
    seo_description: Union[str, None]

    __i18n__ = ['name', 'description', 'seo_title', 'seo_description']

    @classmethod
    def example(
        cls,
        pk: int,
        slug: str,
        name: str,
        description: str,
        start: datetime,
        finish: datetime,
        linked_events: Union[List[Dict], None] = None,
        linked_categories: Union[List[Dict], None] = None,
        on_main: bool = True,
        position: int = 1,
        lang: str = 'ru',
        **kwargs,
    ) -> SourceChart:
        """Example."""

        date_start, time_start = fn.dt_split(start)
        date_finish, time_finish = fn.dt_split(finish)

        schedule = ChartSchedule(
            date_start=str(date_start),
            time_finish=str(time_start),
            time_start=str(date_finish),
            date_finish=str(time_finish),
        )

        return SourceChart(
            id=pk,
            slug=slug,
            old_slug=f'{slug}_old',
            name=f'{name} [{lang.upper()}]',
            description=f'{description} [{lang.upper()}]',
            seo_title=f'seo title [{lang.upper()}]',
            seo_description=f'seo description [{lang.upper()}]',
            position=position,
            cover=SizedSourceMarketImage.example(),
            preview=SizedSourceMarketImage.example(),
            on_main=on_main,
            events=linked_events,
            category=linked_categories,
            schedule=schedule,
        )

    def clean(self) -> Dict:
        """Overrides."""

        _context = {
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'old_slug': self.old_slug,
            'position': self.position,
            'on_main': self.on_main,
            'seo_name': self.seo_title,
            'seo_description': self.seo_description,
        }

        if self.events:
            _context.update({'events': [e.id for e in self.events]})

        if self.cover:
            _context.update({'cover': self.cover.to_sized_image()})

        if self.preview:
            _context.update({'preview': self.preview.to_sized_image()})

        if self.category:
            _context.update({
                'categories': [category.id for category in self.category],
            })

        if self.schedule:

            ds = fn.timestamp(
                fn.dt_join(
                    self.schedule.date_start,
                    self.schedule.time_start,
                ),
            )

            df = fn.timestamp(
                fn.dt_join(
                    self.schedule.date_finish,
                    self.schedule.time_finish,
                ),
            )

            if ds and df:
                _context.update({'start': ds, 'finish': df})

        return _context
