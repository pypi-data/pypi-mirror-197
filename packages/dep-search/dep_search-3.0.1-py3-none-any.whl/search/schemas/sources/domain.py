"""Source tag."""

from __future__ import annotations

from typing import Dict, List, Union
from service.ext.testing import faker

from ..common_types import IdNameSchema, builtins


class SourceDomain(builtins.TypeSource):
    """Source domain."""

    id: int
    name: str

    subdivision_codes: Union[str, None] = None
    locations: Union[List[IdNameSchema], None] = None

    sort_order: Union[int, None] = 1
    sub_domain: Union[str, None]

    display_in_cities_list: Union[bool, None] = False
    is_active: Union[bool, None] = False
    country_code: Union[str, None] = None

    __i18n__ = ['name']

    @classmethod
    def example(
        cls,
        pk: int,
        name: str,
        sub_domain: str,
        is_visible: bool = True,
        is_active: bool = True,
        country_code: str = 'ru',
        subdivision_codes: str = None,
        sort_order: int = 1,
    ) -> SourceDomain:
        """Example."""

        return SourceDomain(
            id=pk,
            name=name,
            subdivision_codes=subdivision_codes,
            sort_order=sort_order,
            sub_domain=sub_domain,
            display_in_cities_list=is_visible,
            is_active=is_active,
            country_code=country_code,
            locations=[
                {
                    'id': faker.any_int_pos(),
                    'name': faker.any_address(),
                },
            ],
        )

    def clean(self) -> Dict:
        """Overrides."""

        _context = {
            'name': self.name,
            'domain': self.sub_domain,
            'ordering': self.sort_order,
            'is_active': self.is_active,
            'is_visible': self.display_in_cities_list,
            'country': self.country_code,
            'locations': None,
            'sub_divisions': None,
        }

        if self.locations:
            _context['locations'] = [_l.id for _l in self.locations]

        if self.subdivision_codes:
            _context['sub_divisions'] = str(self.subdivision_codes).split(',')

        return _context
