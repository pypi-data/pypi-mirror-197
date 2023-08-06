"""Tag examples."""

from typing import Tuple, List

from ..raws.tag import TypeTag
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...fn import digest_dict
from ...schemas.sources.tag import SourceTag
from ...types import digest, fallback_digest

from .category import (
    category_concert,
    category_theatre,
    category_opera,
    category_rock,
    category_classic,
    category_guitar,
    category_viola,
    category_show,
    category_kids,
    category_standup,
    category_sport,
    category_box,
    category_football,
)

pk_concert, i18n_concert = category_concert()
pk_theatre, i18n_theatre = category_theatre()
pk_opera, i18n_opera = category_opera()
pk_rock, i18n_rock = category_rock()
pk_classic, i18n_classic = category_classic()
pk_guitar, i18n_guitar = category_guitar()
pk_viola, i18n_viola = category_viola()
pk_show, i18n_show = category_show()
pk_kids, i18n_kids = category_kids()
pk_standup, i18n_standup = category_standup()
pk_sport, i18n_sport = category_sport()
pk_box, i18n_box = category_box()
pk_football, i18n_football = category_football()


def tag_concert() -> Tuple[int, Type18nDoc]:
    """Tag concert."""

    pk, slug = 1, 'tag_concert'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Концерты',
            event_category=i18n_concert['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Concerts',
            event_category=i18n_concert['en'],
            lang='en',
        ),
    }


def tag_theatre() -> Tuple[int, Type18nDoc]:
    """Tag theatre."""

    pk, slug = 2, 'tag_theatre'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Театральные представления',
            event_category=i18n_theatre['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Theatre shows',
            event_category=i18n_theatre['en'],
            lang='en',
        ),
    }


def tag_opera() -> Tuple[int, Type18nDoc]:
    """Tag opera."""

    pk, slug = 3, 'tag_opera'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Ёперные представления',
            event_category=i18n_opera['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Opera shows',
            event_category=i18n_opera['en'],
            lang='en',
        ),
    }


def tag_rock() -> Tuple[int, Type18nDoc]:
    """Tag rock."""

    pk, slug = 4, 'tag_rock'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Рок музыка',
            event_category=i18n_rock['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Rock music',
            event_category=i18n_rock['en'],
            lang='en',
        ),
    }


def tag_classic() -> Tuple[int, Type18nDoc]:
    """Tag classic."""

    pk, slug = 5, 'tag_classic'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Классическая музыка',
            event_category=i18n_classic['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Classic music',
            event_category=i18n_classic['en'],
            lang='en',
        ),
    }


def tag_viola() -> Tuple[int, Type18nDoc]:
    """Tag viola."""

    pk, slug = 6, 'tag_viola'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Скрипичная музыка',
            event_category=i18n_viola['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Viola music',
            event_category=i18n_viola['en'],
            lang='en',
        ),
    }


def tag_guitar() -> Tuple[int, Type18nDoc]:
    """Tag guitar."""

    pk, slug = 7, 'tag_guitar'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Классическая гитара',
            event_category=i18n_guitar['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Classic guitar',
            event_category=i18n_guitar['en'],
            lang='en',
        ),
    }


def tag_show() -> Tuple[int, Type18nDoc]:
    """Tag show."""

    pk, slug = 8, 'tag_shows'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Представления',
            event_category=i18n_show['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Shows',
            event_category=i18n_show['en'],
            lang='en',
        ),
    }


def tag_kids() -> Tuple[int, Type18nDoc]:
    """Tag kids."""

    pk, slug = 9, 'tag_kids'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Детские представления',
            event_category=i18n_kids['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Kids shows',
            event_category=i18n_kids['en'],
            lang='en',
        ),
    }


def tag_standup() -> Tuple[int, Type18nDoc]:
    """Tag standup."""

    pk, slug = 10, 'tag_standup'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Стендап представления',
            event_category=i18n_standup['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Standup shows',
            event_category=i18n_standup['en'],
            lang='en',
        ),
    }


def tag_sport() -> Tuple[int, Type18nDoc]:
    """Tag sport."""

    pk, slug = 11, 'tag_sport'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Спортивные матчи',
            event_category=i18n_sport['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Sports events',
            event_category=i18n_sport['en'],
            lang='en',
        ),
    }


def tag_box() -> Tuple[int, Type18nDoc]:
    """Tag box."""

    pk, slug = 12, 'tag_box'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Боксерские поединки',
            event_category=i18n_box['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Box fight',
            event_category=i18n_box['en'],
            lang='en',
        ),
    }


def tag_football() -> Tuple[int, Type18nDoc]:
    """Tag football."""

    pk, slug = 13, 'tag_football'

    return pk, {
        'ru': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Футбольные события',
            event_category=i18n_football['ru'],
            lang='ru',
        ),
        'en': SourceTag.example(
            pk=pk,
            slug=slug,
            name='Football events',
            event_category=i18n_football['en'],
            lang='en',
        ),
    }


all_tags = [  # noqa
    tag_concert(),
    tag_theatre(),
    tag_opera(),
    tag_rock(),
    tag_classic(),
    tag_viola(),
    tag_guitar(),
    tag_show(),
    tag_kids(),
    tag_standup(),
    tag_sport(),
    tag_box(),
    tag_football(),
]


def src_tags():  # noqa
    """Src tags."""

    return {tag[0]: tag[1] for tag in all_tags}


def raw_tags(lang: TypeLang) -> List[TypeTag]:
    """Raw tags."""

    buff = list()

    for domain in all_tags:
        pk, i18n = domain
        canonical = i18n[lang].clean()
        obj = TypeTag.create_with_meta(
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
