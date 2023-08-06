"""Domain examples."""

from typing import List, Tuple

from ..raws.domain import TypeDomain
from ...fn import digest_dict
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.domain import SourceDomain
from ...types import digest, fallback_digest


def domain_spb() -> Tuple[int, Type18nDoc]:
    """Domain spb."""

    pk, domain = 1, 'spb'

    return pk, {
        'ru': SourceDomain.example(
            pk=pk,
            name='Питер',
            sub_domain=domain,
            subdivision_codes='spb',
        ),
        'en': SourceDomain.example(
            pk=pk,
            name='Saint Petersburg',
            sub_domain=domain,
            subdivision_codes='spb',
        )
    }


def domain_msk() -> Tuple[int, Type18nDoc]:
    """Domain msk."""

    pk, domain = 2, 'msk'

    return pk, {
        'ru': SourceDomain.example(
            pk=pk,
            name='Москва',
            sub_domain=domain,
            subdivision_codes='mos, mow',
        ),
        'en': SourceDomain.example(
            pk=pk,
            name='Moscow',
            sub_domain=domain,
            subdivision_codes='mos, mow',
        )
    }


def domain_vrn() -> Tuple[int, Type18nDoc]:
    """Domain vrn."""

    pk, domain = 3, 'vrn'

    return pk, {
        'ru': SourceDomain.example(
            pk=pk,
            name='Воронеж',
            sub_domain=domain,
        ),
        'en': SourceDomain.example(
            pk=pk,
            name='Voronezh',
            sub_domain=domain,
        )
    }


def domain_lip() -> Tuple[int, Type18nDoc]:
    """Domain lip."""

    pk, domain = 4, 'lip'

    return pk, {
        'ru': SourceDomain.example(
            pk=pk,
            name='Липецк',
            sub_domain=domain,
        ),
        'en': SourceDomain.example(
            pk=pk,
            name='Lipetsk',
            sub_domain=domain,
        )
    }


all_domains = [
    domain_spb(),
    domain_msk(),
    domain_vrn(),
    domain_lip(),
]


def src_domains():  # noqa
    """Src domains."""

    return {d[0]: d[1] for d in all_domains}


def raw_domains(lang: TypeLang) -> List[TypeDomain]:
    """Raw domains."""

    buff = list()

    for domain in all_domains:
        pk, i18n = domain
        canonical = i18n[lang].clean()
        obj = TypeDomain.create_with_meta(
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
