"""Example helpers."""

from typing import List, Tuple
from datetime import timedelta

from service.ext import fn
from service.ext.testing import faker


TypeEventDateTime = Tuple[str, str, str, str]


def event_date_time(days: int = 1, future: bool = True) -> TypeEventDateTime:
    """Event date time."""

    if future:
        event_start = faker.any_dt_future_day(days=days)
    else:
        event_start = faker.any_dt_day_ago(days=days)

    event_finish = event_start + timedelta(hours=2)

    date_start, time_start = fn.dt_split(event_start)
    date_finish, time_finish = fn.dt_split(event_finish)

    return str(date_start), str(time_start), str(date_finish), str(time_finish)


def any_image_png(name: str = None) -> str:
    """Any image png."""

    img_name = name if name else 'image'
    return f'{faker.any_image_url()}/{img_name}.png'


def any_image_webp(name: str = None) -> str:
    """Any image webp."""

    img_name = name if name else 'image'
    return f'{faker.any_image_url()}/{img_name}.webp'


def any_list_image_png(alias: str = 'images') -> List[str]:
    """Any list image png."""

    return [
        any_image_png(name=f'{alias}_1'),
        any_image_png(name=f'{alias}_2'),
    ]


def any_list_image_webp(alias: str = 'images') -> List[str]:
    """Any list image webp"""

    return [
        any_image_webp(name=f'{alias}_1'),
        any_image_webp(name=f'{alias}_2'),
    ]
