"""Source category."""

from __future__ import annotations

from typing import Dict, List, Union
from service.ext.testing import faker
from service.ext import fn

from ..common_types import (
    BreadCrumbs,
    VisibleType,
    SizedSourceMarketImage,
    TypeSchema,
    builtins,
)


class ParentCategory(TypeSchema):
    """Parent category schema."""

    id: int
    slug: Union[str, None]
    name: Union[str, None]


class SourceCategory(builtins.TypeSource):
    """Source category."""

    id: int
    name: str
    parent: Union[int, None]

    is_actual: bool
    visible_type: VisibleType

    slug: str
    old_slug: Union[str, None]
    seo_text: Union[str, None]

    breadcrumbs: Union[List[BreadCrumbs], str, None]

    cover: SizedSourceMarketImage
    preview: SizedSourceMarketImage

    updated: str
    created: str

    __i18n__ = ['name']

    @classmethod
    def example(
        cls,
        pk: int,
        name: str,
        slug: str,
        is_actual: bool = True,
        seo_text: str = 'seo text',
        parent_pk: int = None,
        visible_type: VisibleType = VisibleType.simple,
    ) -> SourceCategory:
        """From values."""

        return SourceCategory(
            id=pk,
            name=name,
            slug=slug,
            parent=parent_pk,
            old_slug=f'{slug}_old',
            seo_text=seo_text,
            is_actual=is_actual,
            visible_type=visible_type,
            breadcrumbs=[{'title': name, 'slug': slug}],
            cover=SizedSourceMarketImage.example(),
            preview=SizedSourceMarketImage.example(),
            updated=str(faker.any_dt_day_ago()),
            created=str(faker.any_dt_day_ago()),
        )

    def clean(self) -> Dict:
        """Overrides."""

        _context = {
            'name': self.name,
            'slug': self.slug,
            'old_slug': self.old_slug,
            'parent_pk': self.parent if self.parent else None,
            'seo_text': self.seo_text,
            'is_actual': self.is_actual,
            'visible_type': self.visible_type,
            'updated': fn.date_str_to_timestamp(self.updated),
            'created': fn.date_str_to_timestamp(self.created),
        }

        _cover = self.cover.to_sized_image().dict()
        _preview = self.preview.to_sized_image().dict()

        _context['media'] = {'cover': _cover, 'preview': _preview}

        return _context
