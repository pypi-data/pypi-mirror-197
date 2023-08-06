"""Source location."""

from __future__ import annotations

from typing import Dict

from ..common_types import IdNameSchema, builtins


class SourceLocation(builtins.TypeSource):
    """Source location."""

    id: int
    name: str
    country: IdNameSchema

    __i18n__ = ['name']

    @classmethod
    def example(
        cls,
        pk: int,
        name: str,
        country: Dict,
    ) -> SourceLocation:
        """Example."""

        return SourceLocation(id=pk, name=name, country=country)

    def clean(self) -> Dict:
        """Overrides."""

        return {'name': self.name, 'country': self.country}
