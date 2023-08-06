"""Category examples.

Category tree:

+ [1] concert
    + [11] theatre
    + [12] opera
    + [13] rock
    + [14] classic
        + [141] viola
        + [142] guitar
+ [2] show
    + [21] standup
    + [22] kids
+ [3] sport
    + [31] box
    + [32] football

"""

from typing import Tuple, List

from ..raws.category import TypeCategory
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.category import SourceCategory
from ...fn import digest_dict
from ...types import digest, fallback_digest


def category_concert() -> Tuple[int, Type18nDoc]:
    """Category concert."""

    pk, slug = 1, 'concerts'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Концерты',
            slug=slug,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='The Concerts',
            slug=slug,
        )
    }


def category_theatre() -> Tuple[int, Type18nDoc]:
    """Category theatre."""

    pk, slug = 11, 'theatre'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Театр',
            slug=slug,
            parent_pk=1,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Theatre',
            slug=slug,
            parent_pk=1,
        ),
    }


def category_opera() -> Tuple[int, Type18nDoc]:
    """Category opera."""

    pk, slug = 12, 'opera'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Опера',
            slug=slug,
            parent_pk=1,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Opera',
            slug=slug,
            parent_pk=1,
        ),
    }


def category_rock() -> Tuple[int, Type18nDoc]:
    """Category rock."""

    pk, slug = 13, 'rock'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Рок',
            slug=slug,
            parent_pk=1,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Rock',
            slug=slug,
            parent_pk=1,
        ),
    }


def category_classic() -> Tuple[int, Type18nDoc]:
    """Category classic."""

    pk, slug = 14, 'classic'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Классика',
            slug=slug,
            parent_pk=1,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Classic',
            slug=slug,
            parent_pk=1,
        ),
    }


def category_viola() -> Tuple[int, Type18nDoc]:
    """Category viola."""

    pk, slug = 141, 'viola'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Скрипка',
            slug=slug,
            parent_pk=14,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Viola',
            slug=slug,
            parent_pk=14,
        ),
    }


def category_guitar() -> Tuple[int, Type18nDoc]:
    """Category guitar."""

    pk, slug = 142, 'guitar'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Гитара',
            slug=slug,
            parent_pk=14,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Guitar',
            slug=slug,
            parent_pk=14,
        ),
    }


def category_show() -> Tuple[int, Type18nDoc]:
    """Category show."""

    pk, slug = 2, 'shows'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Представления',
            slug=slug,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='The shows',
            slug=slug,
        ),
    }


def category_standup() -> Tuple[int, Type18nDoc]:
    """Category standup."""

    pk, slug = 21, 'standup'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Стендап',
            slug=slug,
            parent_pk=2,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='The standup',
            slug=slug,
            parent_pk=2,
        ),
    }


def category_kids() -> Tuple[int, Type18nDoc]:
    """Category kids."""

    pk, slug = 22, 'kids'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Детские представления',
            slug=slug,
            parent_pk=2,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='The kid shows',
            slug=slug,
            parent_pk=2,
        ),
    }


def category_sport() -> Tuple[int, Type18nDoc]:
    """Category sport."""

    pk, slug = 3, 'sport'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Спортивные события',
            slug=slug,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Sport events',
            slug=slug,
        ),
    }


def category_box() -> Tuple[int, Type18nDoc]:
    """Category box."""

    pk, slug = 31, 'box'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Бокс',
            slug=slug,
            parent_pk=3,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='The box',
            slug=slug,
            parent_pk=3,
        ),
    }


def category_football() -> Tuple[int, Type18nDoc]:
    """Category football."""

    pk, slug = 32, 'football'

    return pk, {
        'ru': SourceCategory.example(
            pk=pk,
            name='Футбол',
            slug=slug,
            parent_pk=3,
        ),
        'en': SourceCategory.example(
            pk=pk,
            name='Football',
            slug=slug,
            parent_pk=3,
        ),
    }


all_categories = [  # noqa
    category_concert(),
    category_theatre(),
    category_opera(),
    category_rock(),
    category_classic(),
    category_viola(),
    category_guitar(),
    category_show(),
    category_kids(),
    category_standup(),
    category_sport(),
    category_box(),
    category_football(),
]


def src_categories():  # noqa
    """Src categories."""

    return {c[0]: c[1] for c in all_categories}


def raw_categories(lang: TypeLang) -> List[TypeCategory]:
    """Raw categories."""

    buff = list()

    for category in all_categories:
        pk, i18n = category
        canonical = i18n[lang].clean()
        obj = TypeCategory.create_with_meta(
            normalized_doc=canonical,
            meta=Meta(
                pk=str(pk),
                lang=lang,
                checksum=digest_dict(canonical),
                commit=fallback_digest,
                branch=digest,
            ),
        )
        buff.append(obj)

    return buff
