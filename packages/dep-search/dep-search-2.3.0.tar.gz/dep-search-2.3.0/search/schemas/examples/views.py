"""Example view."""

from typing import List
from ...types import ViewMeta, BreadCrumbs, digest
from ..views import ViewCategory


def raw_category_view(lang: str) -> List[ViewCategory]:
    """Raw category view."""

    return [
        ViewCategory(
            pk=1,
            name='Классика',
            meta=ViewMeta(commit=digest, lang=lang),
            level=0,
            visible_type='hockey',
            seo_text='seo_text',
            is_actual=True,
            breadcrumbs=[BreadCrumbs(slug='slug', title='title')],
            slug='box',
            old_slug='box_old',
            parent=None,
            cover=None,
            preview=None,
            lookup_pk=[1],
            lookup_slug=['box'],
            lookup_tag_pk=[20],
            lookup_tag_slug=['slug_20'],
        ),
        ViewCategory(
            pk=56,
            parent=None,
            name='Classics',
            is_actual=True,
            meta=ViewMeta(commit=digest, lang=lang),
            breadcrumbs=[BreadCrumbs(slug='slug', title='title')],
            level=1,
            visible_type='hockey',
            seo_text='seo_text',
            slug='classical',
            old_slug='box_old',
            cover=None,
            preview=None,
            lookup_pk=[10, 56],
            lookup_slug=['classical', 'music'],
            lookup_tag_pk=[20],
            lookup_tag_slug=['slug_20'],
        ),
    ]
