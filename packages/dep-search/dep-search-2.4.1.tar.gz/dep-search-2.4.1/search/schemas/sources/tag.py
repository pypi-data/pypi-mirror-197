"""Source tag."""

from __future__ import annotations

from typing import Dict, List, Union
from service.ext import fn
from service.ext.testing import faker

from ..common_types import IdNameSchema, builtins


class SourceEventCategory(IdNameSchema):
    """Tag event category."""

    breadcrumbs: List[Dict]


class SourceTag(builtins.TypeSource):
    """Source tag."""

    id: int
    name: str
    slug: str
    old_slug: Union[str, None]

    event_category: Union[SourceEventCategory, None]

    created: str
    updated: str

    __i18n__ = ['name']

    @classmethod
    def example(
        cls,
        pk: int,
        name: str,
        slug: str,
        lang: str = 'ru',
        **kwargs,
    ) -> SourceTag:
        """Example."""

        return SourceTag(
            id=pk,
            name=f'{name} [{lang.upper()}]',
            slug=slug,
            old_slug=f'{slug}_old',
            event_category=kwargs.get('event_category'),
            created=str(faker.any_dt_day_ago(days=5)),
            updated=str(faker.any_dt_day_ago(days=2)),
        )

    def clean(self) -> Dict:
        """Overrides."""

        cleaned = {
            'name': self.name,
            'slug': self.slug,
            'old_slug': self.old_slug,
            'created': fn.date_str_to_timestamp(self.created),
            'updated': fn.date_str_to_timestamp(self.updated),
        }

        if self.event_category and self.event_category.id:
            cleaned.update({'category_pk': self.event_category.id})

        return cleaned
