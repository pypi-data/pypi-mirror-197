"""Place examples."""

from typing import Tuple, List

from ..raws.place import TypePlace
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.place import SourcePlace
from ...fn import digest_dict
from ...types import digest, fallback_digest


def place_msk() -> Tuple[int, Type18nDoc]:
    """Place msk."""

    pk, slug = 1, 'msk_luxury_appart'
    return pk, {
        'ru': SourcePlace.example(
            pk=pk,
            slug=slug,
            name='Москоу Лухари аппартментс',

        ),
        'en': SourcePlace.example(
            pk=pk,
            slug=slug,
            name='Moscow luxury appartments',
        ),
    }


def place_spb() -> Tuple[int, Type18nDoc]:
    """Domain spb."""

    pk, slug = 2, 'spb_lounge'

    return pk, {
        'ru': SourcePlace.example(
            pk=pk,
            slug=slug,
            name='Рубик',
            lang='ru',
        ),
        'en': SourcePlace.example(
            pk=pk,
            slug=slug,
            name='Ribic',
            lang='en',
        ),
    }


all_places = [
    place_msk(),
    place_spb(),
]


def src_places():  # noqa
    """Src places."""

    return {p[0]: p[1] for p in all_places}


def raw_places(lang: TypeLang) -> List[TypePlace]:
    """Raw places."""

    buff = list()

    for place in all_places:
        pk, i18n = place
        canonical = i18n[lang].clean()
        obj = TypePlace.create_with_meta(
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
