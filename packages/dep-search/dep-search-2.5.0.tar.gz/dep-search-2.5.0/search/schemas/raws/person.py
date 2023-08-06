"""Raw person."""

from typing import List, Union

from ..common_types import (
    builtins,
    TypeSchema,
    TypeOptionalListImages,
    PersonType,
    SizedCloudImage,
)


class PersonMedia(TypeSchema):
    """Person media."""

    main: Union[SizedCloudImage, None]
    cover: Union[SizedCloudImage, None]

    gallery: TypeOptionalListImages
    gallery_webp: TypeOptionalListImages


class TypePerson(builtins.TypeRaw):
    """Type person."""

    slug: str
    name: str
    description: str

    parent_pk: Union[int, None]
    tags: Union[List[int], None]

    position: str
    person_type: PersonType

    media: PersonMedia
