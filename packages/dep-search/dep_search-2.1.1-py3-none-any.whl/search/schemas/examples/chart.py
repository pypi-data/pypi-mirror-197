"""Chart examples."""

from typing import List, Tuple

from service.ext.testing import faker

from ..raws.chart import TypeChart
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...fn import digest_dict
from ...types import digest, fallback_digest
from ...schemas.sources.chart import SourceChart


from .category import (
    category_classic,
    category_viola,
    category_guitar,
    category_box,
    category_rock,
)

from .market_event import event_kipelov_with_classical, event_aria
from .market_event import event_vanessa_mae, event_sergey_radnev
from .market_event import event_emelianenko_vs_tayson

pk_category_classic, i18n_category_classic = category_classic()
pk_category_viola, i18n_category_viola = category_viola()
pk_category_guitar, i18n_category_guitar = category_guitar()
pk_category_box, i18n_category_box = category_box()
pk_category_rock, i18n_category_rock = category_rock()

pk_aria, i18n_aria = event_aria()
pk_mma_fight, i18n_mma_fight = event_emelianenko_vs_tayson()
pk_kipelov_with_classical, i18n_kipelov = event_kipelov_with_classical()

pk_mae, i18n_mae = event_vanessa_mae()
pk_radnev, i18n_radnev = event_sergey_radnev()


def chart_classical() -> Tuple[int, Type18nDoc]:
    """Chart classical."""

    pk, slug = 1, 'chart_classical'

    return pk, {
        'ru': SourceChart.example(
            pk=pk,
            slug=slug,
            name='Классика',
            description='Подборка классической музыки',
            start=faker.any_dt_day_ago(days=20),
            finish=faker.any_dt_future_day(days=20),
            linked_events=[i18n_mae['ru'], i18n_radnev['ru']],
            linked_categories=[
                i18n_category_classic['ru'],
                i18n_category_guitar['ru'],
                i18n_category_viola['ru'],
            ],
            lang='ru',
        ),
        'en': SourceChart.example(
            pk=pk,
            slug=slug,
            name='Classic',
            description='Chart with classic music',
            start=faker.any_dt_day_ago(days=20),
            finish=faker.any_dt_future_day(days=20),
            linked_events=[i18n_mae['en'], i18n_radnev['en']],
            linked_categories=[
                i18n_category_classic['en'],
                i18n_category_guitar['en'],
                i18n_category_viola['en'],
            ],
            lang='en',
        ),
    }


def chart_rock() -> Tuple[int, Type18nDoc]:
    """Chart rock."""

    pk, slug = 2, 'chart_rock'

    return pk, {
        'ru': SourceChart.example(
            pk=pk,
            slug=slug,
            name='Рок музыка',
            description='Подборка рок музыки',
            start=faker.any_dt_day_ago(days=90),
            finish=faker.any_dt_future_day(days=90),
            linked_events=[i18n_aria['ru'], i18n_kipelov['ru']],
            linked_categories=[
                i18n_category_rock['ru'],
            ],
            lang='ru',
        ),
        'en': SourceChart.example(
            pk=pk,
            slug=slug,
            name='Rock music',
            description='Chart with rock music',
            start=faker.any_dt_day_ago(days=20),
            finish=faker.any_dt_future_day(days=20),
            linked_events=[i18n_aria['en'], i18n_kipelov['en']],
            linked_categories=[
                i18n_category_rock['en'],
            ],
            lang='en',
        ),
    }


def chart_box() -> Tuple[int, Type18nDoc]:
    """Chart box."""

    pk, slug = 3, 'chart_fights'

    return pk, {
        'ru': SourceChart.example(
            pk=pk,
            slug=slug,
            name='Предстоящие бои',
            description='Подборка предстоящих боев',
            start=faker.any_dt_day_ago(days=90),
            finish=faker.any_dt_future_day(days=90),
            linked_events=[i18n_mma_fight['ru']],
            linked_categories=[
                i18n_category_box['ru'],
            ],
            lang='ru',
        ),
        'en': SourceChart.example(
            pk=pk,
            slug=slug,
            name='Future fights',
            description='Chart with future fight events',
            start=faker.any_dt_day_ago(days=10),
            finish=faker.any_dt_future_day(days=10),
            linked_events=[i18n_mma_fight['en']],
            linked_categories=[
                i18n_category_box['en'],
            ],
            lang='en',
        ),
    }


all_charts = [
    chart_classical(),
    chart_rock(),
    chart_box(),
]


def src_charts():  # noqa
    """Src charts."""

    return {C[0]: C[1] for C in all_charts}


def raw_charts(lang: TypeLang) -> List[TypeChart]:
    """Raw charts."""

    buff = list()

    for chart in all_charts:
        pk, i18n = chart
        canonical = i18n[lang].clean()
        obj = TypeChart.create_with_meta(
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
