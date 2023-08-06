"""layout examples."""

from typing import List, Tuple

from ..raws.layout import TypeLayout
from ...fn import digest_dict
from ...internals.builtins import Type18nDoc, TypeLang, Meta
from ...schemas.sources.layout import SourceLayout
from ...types import digest, fallback_digest


def layout_default() -> Tuple[int, Type18nDoc]:
    """Layout default."""

    pk, hall_pk = 1, 10
    name_en, name_ru = 'Схема по умолчанию', 'Default schema'

    return pk, {
        'ru': SourceLayout.example(
            pk=pk,
            name=name_ru,
            hall_id=hall_pk,
        ),
        'en': SourceLayout.example(
            pk=pk,
            name=name_en,
            hall_id=hall_pk,
        ),
    }


def layout_diff() -> Tuple[int, Type18nDoc]:
    """Layout different."""

    pk, hall_pk = 2, 20
    name_en, name_ru = 'Другая схема', 'Diff schema'

    return pk, {
        'ru': SourceLayout.example(
            pk=pk,
            name=name_ru,
            hall_id=hall_pk,
        ),
        'en': SourceLayout.example(
            pk=pk,
            name=name_en,
            hall_id=hall_pk,
        ),
    }


all_layouts = [
    layout_default(),
    layout_diff(),
]


def src_layouts():  # noqa
    """Src layouts."""

    return {l[0]: l[1] for l in all_layouts}


def raw_layouts(lang: TypeLang) -> List[TypeLayout]:
    """Raw layouts."""

    buff = list()

    for layout in all_layouts:
        pk, i18n = layout
        canonical = i18n[lang].clean()
        obj = TypeLayout.create_with_meta(
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
