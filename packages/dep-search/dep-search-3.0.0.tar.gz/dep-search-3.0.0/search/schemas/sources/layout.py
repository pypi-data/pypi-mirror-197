"""Source layout."""

from __future__ import annotations

from typing import Dict, Union
from service.ext.testing import faker

from ..common_types import builtins


class SourceLayout(builtins.TypeSource):
    """Source layout."""

    id: int
    name: str
    hall_id: int

    meta: Union[Dict, None]

    __i18n__ = ['name']

    @classmethod
    def example(
        cls,
        pk: int,
        name: str,
        hall_id: int = None,
    ) -> SourceLayout:
        """Example."""

        cover_langs = ('ru', 'en', 'ar', 'es', 'zh', 'de', 'fr', 'kk', 'ja')
        background = {lang: faker.any_image_url() for lang in cover_langs}

        meta = {
            'width': faker.any_int_pos(),
            'height': faker.any_int_pos(),
            'background': background,
        }

        return SourceLayout(
            id=pk,
            name=name,
            hall_id=hall_id,
            meta=meta,
        )

    def clean(self) -> Dict:
        """Overrides."""

        return {
            'name': self.name,
            'hall_pk': self.hall_id,
            'properties': self.meta,
        }
