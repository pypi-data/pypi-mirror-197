"""Person examples."""

from typing import Tuple, List

from ..raws.person import TypePerson
from ...internals.builtins import Type18nDoc, Meta, TypeLang
from ...fn import digest_dict
from ...types import digest, fallback_digest
from ...schemas.sources.person import SourcePerson, PersonTypeSource

from .tag import (
    tag_rock,
    tag_concert,
    tag_football,
    tag_box,
    tag_viola,
    tag_guitar,
)

pk_tag_rock, i18n_tag_rock = tag_rock()
pk_tag_concert, i18n_tag_concert = tag_concert()
pk_tag_viola, i18n_tag_viola = tag_viola()
pk_tag_guitar, i18n_tag_guitar = tag_guitar()
pk_tag_football, i18n_tag_football = tag_football()
pk_tag_box, i18n_tag_box = tag_box()


def person_kipelov() -> Tuple[int, Type18nDoc]:
    """Person Kipelov."""

    pk, slug = 1, 'v_kipelov'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Валерий Кипелов',
            position='Вокалист, фронт-мен группы Ария',
            description='Кипелов лучший',
            tags=[i18n_tag_rock['ru'], i18n_tag_concert['ru']],
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Valeriy Kipelov',
            description='Kipelov best',
            position='Vocal, Aria group front-man',
            tags=[i18n_tag_rock['en'], i18n_tag_concert['en']],
        ),
    }


def person_dubinin() -> Tuple[int, Type18nDoc]:
    """Person dubinin."""

    pk, slug = 11, 'v_dubinin'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Виталий Дубинин',
            position='Вокалист, бас гитара',
            description='Тоже отличный музыкант, участник гр. Ария',
            tags=[i18n_tag_rock['ru'], i18n_tag_concert['ru']],
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Vitaliy Dubinin',
            description='Nice musicant too, member of Aria gr',
            position='Vocal, bas guitar',
            tags=[i18n_tag_rock['en'], i18n_tag_concert['en']],
        ),
    }


def person_mae() -> Tuple[int, Type18nDoc]:
    """Person Mae."""

    pk, slug = 2, 'v_mae'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Ванесса Мей',
            description='Инфо про Мэй',
            position='Скрипач',
            tags=[i18n_tag_concert['ru'], i18n_tag_viola['ru']],
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Vanessa Mae',
            description='Info about Mae',
            position='Violinist',
            tags=[i18n_tag_concert['en'], i18n_tag_viola['en']],
        ),
    }


def person_radnev() -> Tuple[int, Type18nDoc]:
    """Person Radnev."""

    pk, slug = 3, 's_radnev'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Сергей Раднев',
            description='Сергей Раднев - классическая гитара',
            position='Гитарист',
            tags=[i18n_tag_concert['ru'], i18n_tag_guitar['ru']],
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Sergey Radnev',
            description='Sergey Radnev - classic guitar',
            position='Guitarist',
            tags=[i18n_tag_concert['en'], i18n_tag_guitar['en']],
        ),
    }


def person_emelianenko() -> Tuple[int, Type18nDoc]:
    """Person emelianenko."""

    pk, slug = 4, 'emelianenko'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Федор Емельяненко',
            description='Русский боец',
            tags=[i18n_tag_box['ru']],
            position='MMA Боец',
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Fedor Emelianenko',
            description='RUSSIAN Boxer',
            position='MMA Fighter',
            tags=[i18n_tag_box['en']],
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


def person_tayson() -> Tuple[int, Type18nDoc]:
    """Person tayson."""

    pk, slug = 5, 'tayson'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Майк Тайсон',
            description='Америкосный боец',
            position='Боксер',
            tags=[i18n_tag_box['ru']],
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Mike Tayson',
            description='USA Boxer',
            tags=[i18n_tag_box['en']],
            position='Boxer',
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


def person_zenit() -> Tuple[int, Type18nDoc]:
    """Person zenit team parent."""

    pk, slug = 6, 'zenit_team'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='ФК Зенит',
            description='Футбольный клуб Зенит',
            position='Вы о чем вообще?',
            tags=[i18n_tag_football['ru']],
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Zenit',
            description='The football team Zenit',
            position='What about you?',
            tags=[i18n_tag_football['en']],
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


def person_chelsea() -> Tuple[int, Type18nDoc]:
    """Person chelsea team parent."""

    pk, slug = 7, 'chelsea_team'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='ФК Челси',
            description='Футбольный клуб Челси',
            position='Под вопросом',
            tags=[i18n_tag_football['ru']],
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Chelsea team',
            description='The football team Chelsea',
            position='Need a time for answer',
            tags=[i18n_tag_football['en']],
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


def person_kerjakov() -> Tuple[int, Type18nDoc]:
    """Person zenit kerjakov."""

    pk, slug = 61, 'zenit_kerjakov'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Михаил Кержаков',
            description='Игрок Зенита',
            position='Игрок ногой',
            tags=[i18n_tag_football['ru']],
            person_type=PersonTypeSource.SPORTSMAN,
            parent_pk=6,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Mikhail Kerjakov',
            description='Player of Zenit',
            position='Foot player',
            tags=[i18n_tag_football['en']],
            person_type=PersonTypeSource.SPORTSMAN,
            parent_pk=6,
        ),
    }


def person_mostovoy() -> Tuple[int, Type18nDoc]:
    """Person zenit mostovoy."""

    pk, slug = 62, 'zenit_mostovoy'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Андрей Мостовой',
            description='Игрок Зенита',
            position='Игрок ногой',
            tags=[i18n_tag_football['ru']],
            parent_pk=6,
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Andrey Mostovoy',
            description='Player of Zenit',
            position='Foot player',
            tags=[i18n_tag_football['en']],
            parent_pk=6,
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


def person_haverz() -> Tuple[int, Type18nDoc]:
    """Person chelsea haverz."""

    pk, slug = 71, 'chelsea_haverz'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Кай Хаверц',
            description='Игрок Челси',
            position='Игрок ногой',
            tags=[i18n_tag_football['ru']],
            parent_pk=7,
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Kay Haverz',
            description='Player of Chelsea',
            position='Foot player',
            tags=[i18n_tag_football['en']],
            parent_pk=7,
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


def person_silva() -> Tuple[int, Type18nDoc]:
    """Person chelsea silva."""

    pk, slug = 72, 'chelsea_silva'

    return pk, {
        'ru': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Тиагу Силва',
            description='Игрок Челси',
            position='Игрок ногой',
            tags=[i18n_tag_football['ru']],
            parent_pk=7,
            person_type=PersonTypeSource.SPORTSMAN,
        ),
        'en': SourcePerson.example(
            pk=pk,
            slug=slug,
            name='Tiagu Silva',
            description='Player of Chelsea',
            position='Foot player',
            tags=[i18n_tag_football['en']],
            parent_pk=7,
            person_type=PersonTypeSource.SPORTSMAN,
        ),
    }


all_persons = [  # noqa
    person_kipelov(),
    person_mae(),
    person_radnev(),
    person_emelianenko(),
    person_tayson(),
    person_zenit(),
    person_kerjakov(),
    person_mostovoy(),
    person_chelsea(),
    person_silva(),
    person_haverz(),
]


def src_persons():  # noqa
    """Src persons."""

    return {p[0]: p[1] for p in all_persons}


def raw_persons(lang: TypeLang) -> List[TypePerson]:
    """Raw persons."""

    buff = list()

    for person in all_persons:
        pk, i18n = person
        canonical = i18n[lang].clean()
        obj = TypePerson.create_with_meta(
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
