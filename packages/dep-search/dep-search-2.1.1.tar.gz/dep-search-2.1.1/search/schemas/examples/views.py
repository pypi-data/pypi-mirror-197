"""Example view."""

from typing import List
from ...types import ViewMeta, BreadCrumbs, digest
from ..views import ViewCategory


def raw_category_view(lang: str) -> List[ViewCategory]:
    """Raw category view."""

    return [
        ViewCategory(
            pk=1,
            meta=ViewMeta(commit= digest, lang=lang),
            level=0,
            breadcrumbs=[BreadCrumbs(slug='slug', title='title')],
            slug='box',
            parent_pk=None,
            lookup_pk=[1],
            lookup_slug=['box'],
            lookup_tag_pk=[20],
            lookup_tag_slug=['slug_20'],
        ),
        ViewCategory(
            pk=56,
            parent_pk=1,
            meta=ViewMeta(commit=digest, lang=lang),
            breadcrumbs=[BreadCrumbs(slug='slug', title='title')],
            level=1,
            slug='classical',
            lookup_pk=[10, 56],
            lookup_slug=['classical', 'music'],
            lookup_tag_pk=[20],
            lookup_tag_slug=['slug_20'],
        ),
    ]
