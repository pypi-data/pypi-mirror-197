"""Event examples."""

from typing import Tuple, List

from ..raws.market_event import TypeMarketEvent
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources import SourceMarketEvent
from ...fn import digest_dict
from ...types import digest, fallback_digest


from .category import (
    category_rock,
    category_classic,
    category_viola,
    category_guitar,
    category_box,
    category_football,
)

from .tag import (
    tag_rock,
    tag_classic,
    tag_viola,
    tag_guitar,
    tag_box,
    tag_football,
    tag_sport,
)

from .person import (
    person_kipelov,
    person_dubinin,
    person_mae,
    person_radnev,
    person_emelianenko,
    person_tayson,
    person_zenit,
    person_chelsea,
)

from .place import place_spb, place_msk

pk_category_box, i18n_category_box = category_box()
pk_category_rock, i18n_category_rock = category_rock()
pk_category_classic, i18n_category_classic = category_classic()
pk_category_viola, i18n_category_viola = category_viola()
pk_category_guitar, i18n_category_guitar = category_guitar()
pk_category_football, i18n_category_football = category_football()

pk_tag_classic, i18n_tag_classic = tag_classic()
pk_tag_box, i18n_tag_box = tag_box()
pk_tag_viola, i18n_tag_viola = tag_viola()
pk_tag_guitar, i18n_tag_guitar = tag_guitar()
pk_tag_rock, i18n_tag_rock = tag_rock()
pk_tag_sport, i18n_tag_sport = tag_sport()
pk_tag_football, i18n_tag_football = tag_football()

pk_person_kipelov, i18n_person_kipelov = person_kipelov()
pk_person_dubinin, i18n_person_dubinin = person_dubinin()
pk_person_mae, i18n_person_mae = person_mae()
pk_person_radnev, i18n_person_radnev = person_radnev()
pk_person_emelianenko, i18n_person_emelianenko = person_emelianenko()
pk_person_tayson, i18n_person_tayson = person_tayson()
pk_person_zenit, i18n_person_zenit = person_zenit()
pk_person_chelsea, i18n_person_chelsea = person_chelsea()

pk_place_msk, i18n_place_msk = place_msk()
pk_place_spb, i18n_place_spb = place_spb()


def event_aria() -> Tuple[int, Type18nDoc]:
    """Event aria."""

    pk, slug = 1, 'aria_group'

    event_ru = SourceMarketEvent.example(
        pk=pk,
        slug=slug,
        title='Ария',
        description='Ария',
        linked_category=i18n_category_rock['ru'],
        linked_place=i18n_place_msk['ru'],
        linked_persons=[
            i18n_person_kipelov['ru'],
            i18n_person_dubinin['ru'],
        ],
        linked_tags=[i18n_tag_rock['ru']],
        future_pk=[12, 13],
        outdated=False,
        lang='ru',
    )

    # translates only
    event_en = SourceMarketEvent(**event_ru.dict())
    event_en.title = 'The Aria'
    event_en.description = 'The Aria Group'

    return pk, {'ru': event_ru, 'en': event_en}


def event_kipelov_with_classical() -> Tuple[int, Type18nDoc]:
    """Event kipelov with classical orchestra."""

    pk, slug = 2, 'kipelov_with_classical'

    event_ru = SourceMarketEvent.example(
        pk=pk,
        slug=slug,
        title='Кипелов лучшее',
        description='Кипелов с классическим оркестром',
        linked_category=i18n_category_rock['ru'],
        linked_place=i18n_place_msk['ru'],
        linked_persons=[i18n_person_kipelov['ru']],
        linked_tags=[i18n_tag_rock['ru'], i18n_tag_classic['ru']],
        future_pk=[21, 22],
        outdated=False,
        lang='ru',
    )

    # translates only
    event_en = SourceMarketEvent(**event_ru.dict())
    event_en.title = 'The best of Kipelov'
    event_en.description = 'The Kipelov with a classical orchestra'

    return pk, {'ru': event_ru, 'en': event_en}


def event_vanessa_mae():
    """Event Vanessa Mae."""

    pk, slug = 3, 'mae_awesome'

    event_ru = SourceMarketEvent.example(
        pk=pk,
        slug=slug,
        title='Ванесса Мэй - сольный концерт',
        description='Ванесса Мэй - сольный концерт c лучшими композициями',
        linked_category=i18n_category_classic['ru'],
        linked_place=i18n_place_msk['ru'],
        linked_persons=[i18n_person_mae['ru']],
        linked_tags=[i18n_tag_classic['ru'], i18n_tag_viola['ru']],
        future_pk=[31, 32],
        outdated=False,
        lang='ru',
    )

    # translates only
    event_en = SourceMarketEvent(**event_ru.dict())
    event_en.title = 'Vanessa May - solo concert'
    event_en.description = 'Vanessa May - solo concert with best songs'

    return pk, {'ru': event_ru, 'en': event_en}


def event_sergey_radnev():
    """Event Sergey Radnev."""

    pk, slug = 4, 'sergey_radnev'

    event_ru = SourceMarketEvent.example(
        pk=pk,
        slug=slug,
        title='Сергей Раднев, классика',
        description='Классическая гитара в исполнении С. Раднева',
        linked_category=i18n_category_classic['ru'],
        linked_place=i18n_place_msk['ru'],
        linked_persons=[i18n_person_radnev['ru']],
        linked_tags=[i18n_tag_classic['ru'], i18n_tag_guitar['ru']],
        future_pk=[41, 42],
        outdated=False,
        lang='ru',
    )

    # translates only
    event_en = SourceMarketEvent(**event_ru.dict())
    event_en.title = 'Sergey Radnev, classical'
    event_en.description = 'Classical guitar with maestro S. Radnev'

    return pk, {'ru': event_ru, 'en': event_en}


def event_emelianenko_vs_tayson():
    """Event box with Emelianenko vs Mike Tayson."""

    pk, slug = 5, 'fight_olds'

    event_ru = SourceMarketEvent.example(
        pk=pk,
        slug=slug,
        title='Федор Емельяненко против Майка Тайсона',
        description='Тотальная стариковская заруба',
        linked_category=i18n_category_box['ru'],
        linked_place=i18n_place_msk['ru'],
        linked_persons=[
            i18n_person_emelianenko['ru'],
            i18n_person_tayson['ru'],
        ],
        linked_tags=[i18n_tag_box['ru']],
        outdated=False,
        lang='ru',
    )

    # translates only
    event_en = SourceMarketEvent(**event_ru.dict())
    event_en.title = 'F. Emelianenko vs Mike Tayson'
    event_en.description = 'Fight of olds'

    return pk, {'ru': event_ru, 'en': event_en}


def event_zenit_vs_chelsea():
    """Event football Zenit vs Chelsea."""

    pk, slug = 6, 'zenit_vs_chelsea'

    event_ru = SourceMarketEvent.example(
        pk=pk,
        slug=slug,
        title='Зенит против Челси',
        description='Нога мяч соревнования',
        linked_category=i18n_category_football['ru'],
        linked_place=i18n_place_spb['ru'],
        linked_persons=[
            i18n_person_zenit['ru'],
            i18n_person_chelsea['ru'],
        ],
        linked_tags=[i18n_tag_sport['ru'], i18n_tag_football['ru']],
        outdated=False,
        lang='ru',
    )

    # translates only
    event_en = SourceMarketEvent(**event_ru.dict())
    event_en.title = 'Zenit vs Chelsea'
    event_en.description = 'Football competition'

    return pk, {'ru': event_ru, 'en': event_en}


all_market_events = [  # noqa
    event_aria(),
    event_kipelov_with_classical(),
    event_vanessa_mae(),
    event_sergey_radnev(),
    event_emelianenko_vs_tayson(),
    event_zenit_vs_chelsea(),
]


def src_market_events():  # noqa
    """Src events."""

    return {event[0]: event[1] for event in all_market_events}


def raw_market_events(lang: TypeLang) -> List[TypeMarketEvent]:
    """Raw market events."""

    buff = list()

    for event in all_market_events:
        pk, i18n = event
        canonical = i18n[lang].clean()
        obj = TypeMarketEvent.create_with_meta(
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
