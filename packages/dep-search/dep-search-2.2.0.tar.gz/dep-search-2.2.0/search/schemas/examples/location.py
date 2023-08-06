"""Location examples."""

from typing import List, Tuple

from ..raws.location import TypeLocation
from ...fn import digest_dict
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.location import SourceLocation
from ...types import digest, fallback_digest


country = {
    'ru': {'id': 1, 'name': 'Россия'},
    'en': {'id': 1, 'name': 'Russia'},
}


def location_msk() -> Tuple[int, Type18nDoc]:
    """Location msk."""

    pk = 1

    return pk, {
        'ru': SourceLocation.example(
            pk=pk,
            name='Москва',
            country=country['ru'],
        ),
        'en': SourceLocation.example(
            pk=pk,
            name='Moscow',
            country=country['en'],
        ),
    }


def location_spb() -> Tuple[int, Type18nDoc]:
    """Location spb."""

    pk = 2

    return pk, {
        'ru': SourceLocation.example(
            pk=pk,
            name='Санкт-Петербург',
            country=country['ru'],
        ),
        'en': SourceLocation.example(
            pk=pk,
            name='Saint-Petersburg',
            country=country['en'],
        ),
    }


all_locations = [
    location_msk(),
    location_spb(),
]


def src_locations():  # noqa
    """Src location."""

    return {l[0]: l[1] for l in all_locations}


def raw_locations(lang: TypeLang) -> List[TypeLocation]:
    """Raw locations."""

    buff = list()

    for location in all_locations:
        pk, i18n = location
        canonical = i18n[lang].clean()
        obj = TypeLocation.create_with_meta(
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
