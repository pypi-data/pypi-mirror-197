"""Source market event."""

from __future__ import annotations

from typing import Dict, List, Union
from service.ext.testing import faker

from ..common_types import (
    PersonType,
    PersonTypeSource,
    TypeOptionalListImages,
    SizedSourceMarketImage,
    IdNameSchema,
    builtins,
)

from .helpers import any_list_image_webp, any_list_image_png


class SourcePerson(builtins.TypeSource):
    """Source person."""

    id: int
    slug: str
    name: str
    description: str
    position: str
    parent: Union[IdNameSchema, None]

    person_type: PersonTypeSource

    main_image: Union[SizedSourceMarketImage, None]
    cover: Union[SizedSourceMarketImage, None]
    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages

    tags: Union[List[Dict], None]

    updated: Union[str, None]
    created: Union[str, None]

    __i18n__ = ['name', 'description', 'position']

    @classmethod
    def example(
        cls,
        pk: int,
        slug: str,
        name: str,
        description: str,
        parent_pk: int = None,
        position: str = 'position text',
        person_type: PersonTypeSource = PersonTypeSource.ARTIST,
        lang: str = 'ru',
        tags: List[Dict] = None,
        **kwargs,
    ) -> SourcePerson:
        """Example."""

        return SourcePerson(
            id=pk,
            slug=slug,
            name=name,
            description=description,
            position=position,
            person_type=person_type,
            parent={'id': parent_pk, 'name': 'fake'} if parent_pk else None,
            tags=tags,
            cover=SizedSourceMarketImage.example(),
            main_image=SizedSourceMarketImage.example(),
            gallery=any_list_image_png(alias='gallery'),
            gallery_webp=any_list_image_webp(alias='gallery'),
            updated=str(faker.any_dt_day_ago()),
            created=str(faker.any_dt_day_ago()),
        )

    def _read_person_type(self) -> PersonType:
        """Read person type."""

        _ptypes = {
            PersonTypeSource.ARTIST: PersonType.artist,
            PersonTypeSource.SPORTSMAN: PersonType.sportsman,
        }

        return _ptypes[self.person_type]

    def _read_tags(self) -> Union[List[int], None]:
        """Read person tags."""
        if bool(self.tags) and len(self.tags) > 0:
            return [_t['id'] for _t in self.tags if _t.get('id')]

    def read_media(self) -> Dict:
        """Read media."""

        if self.main_image:
            main_sized = self.main_image.to_sized_image()
        else:
            main_sized = None

        if self.cover:
            cover_sized = self.cover.to_sized_image()
        else:
            cover_sized = None

        if self.gallery:
            gallery = self.gallery
        else:
            gallery = None

        if self.gallery_webp:
            gallery_webp = self.gallery_webp
        else:
            gallery_webp = None

        return {
            'main': main_sized,
            'cover': cover_sized,
            'gallery': gallery,
            'gallery_webp': gallery_webp,
        }

    def clean(self) -> Dict:
        """Clean person source."""

        return {
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'parent_pk': self.parent.id if self.parent else None,
            'position': self.position,
            'person_type': self._read_person_type(),
            'media': self.read_media(),
            'tags': self._read_tags(),
        }
