"""Source tag."""

from __future__ import annotations

from typing import Any, Dict, Union
from service.ext.testing import faker

from ..common_types import (
    IdNameSchema,
    LocationSchema,
    SchemaField,
    SizedSourceMarketImage,
    TypeOptionalImage,
    TypeOptionalListImages,
    builtins,
)

from .helpers import (
    any_list_image_webp,
    any_list_image_png,
    any_image_png,
    any_image_webp,
)


class SourcePlace(builtins.TypeSource):
    """Source place."""

    id: int
    slug: str
    name: str
    description: str
    address: str

    location_id: Union[int, None]
    place_type: IdNameSchema

    popularity: Union[int, None]
    count: Union[int, None]
    how_to_get: Union[str, None]

    parent: Union[Any, None]

    url: TypeOptionalImage

    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages

    schema_title: Union[str, None]
    schema_webp: TypeOptionalImage
    schemas_webp: TypeOptionalListImages

    schema_url: TypeOptionalImage = SchemaField(
        alias='schema',
        default=None,
    )
    schemas_urls: TypeOptionalListImages = SchemaField(
        alias='schemas',
        default=None,
    )

    cover: Union[SizedSourceMarketImage, None]
    preview: Union[SizedSourceMarketImage, None]

    updated: Union[str, None]
    created: Union[str, None]

    __i18n__ = [
        'name',
        'address',
        'description',
        'how_to_get',
        'schema_title',
    ]

    @classmethod
    def example(
        cls,
        pk: int,
        slug: str,
        name: str,
        parent: int = None,
        lang: str = 'ru'
    ) -> SourcePlace:
        """Example."""

        return SourcePlace(
            id=pk,
            slug=slug,
            name=name,
            description=faker.any_sentence(lang=lang),
            address=faker.any_address(lang=lang),
            parent=parent,
            popularity=faker.any_int_pos(),
            count=faker.any_int_pos(),
            how_to_get='how to get',
            url=faker.any_image_url(),
            schema_title='schema title',
            schema=any_image_png(name='schema'),
            schema_webp=any_image_webp(name='schema'),
            schemas=any_list_image_png(alias='schemas'),
            schemas_webp=any_list_image_webp(alias='schemas'),
            gallery=any_list_image_png(alias='gallery'),
            gallery_webp=any_list_image_png(alias='gallery'),
            place_type={'id': faker.any_int_pos(), 'name': faker.any_word()},
            location_id=faker.any_int_pos(),
            updated=str(faker.any_dt_day_ago()),
            created=str(faker.any_dt_day_ago()),
            cover=SizedSourceMarketImage.example(),
            preview=SizedSourceMarketImage.example(),
        )

    def clean(self) -> Dict:
        """Overrides."""  # noqa

        return {
            'slug': self.slug,
            'location_pk': self.location_id,
            'info': {
                'name': self.name,
                'description': self.description,
                'address': self.address,
                'count': self.count,
                'popularity': self.popularity,
                'url': self.url,
                'schema_title': self.schema_title,
                'how_to_get': self.how_to_get,
            },
            'place_type': {
                'pk': self.place_type.id,
                'name': self.place_type.name,
            },
            'media': {
                'cover': self.cover.to_sized_image().dict(),
                'preview': self.preview.to_sized_image().dict(),
                'gallery': self.gallery,
                'gallery_webp': self.gallery_webp,
                'schema_url': self.schema_url,
                'schemas_urls': self.schemas_urls,
                'schema_webp': self.schema_webp,
                'schemas_webp': self.schemas_webp,
            }
        }
